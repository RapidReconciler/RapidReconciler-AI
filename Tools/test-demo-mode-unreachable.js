/* test-demo-mode-unreachable.js -- demo mode cannot be entered in V8 (2026-09-10).
 *
 *   ELECTRON_RUN_AS_NODE=1 "C:/Program Files/Azure Data Studio/azuredatastudio.exe" \
 *       Tools/test-demo-mode-unreachable.js
 *
 * WHY THIS EXISTS. Two hard rules say V8 is production-only with no demo mode
 * (feedback_no_demo, feedback_v8_agent_first). The code disagreed, in two ways
 * that were each reachable without any GSI involvement:
 *
 *   1. Every page resolved its mode as `?mode=` || RR_CONFIG.mode || 'demo'.
 *      So ANYONE WITH THE URL could append ?mode=demo in production.
 *   2. A deploy whose config.js omitted `mode` fell into demo SILENTLY. In
 *      sidebar.js that is not cosmetic: demo means `showSignOut = false` and
 *      an early return out of enforceSessionGuard(), so a misconfigured
 *      production deploy had no sign-out control and NO SESSION EXPIRY
 *      ENFORCEMENT at all.
 *
 * Both are now closed by routing every derivation through RRENV.mode()
 * (config.js), which reads RR_CONFIG.mode and bottoms out at 'staging'.
 *
 * WHAT THIS ASSERTS.
 *   A1  RRENV.mode() returns the configured value on the shipped config
 *   A2  RRENV.mode() cannot return 'demo' for ANY shape of RR_CONFIG,
 *       including absent, empty, null and blank-string
 *   A3  no file under RRV8/ reads the `mode` query parameter any more
 *   A4  no file under RRV8/ still carries a `|| 'demo'` fallback in code
 *   A5  sidebar.js resolves the mode in ONE place, not five
 *
 * A3 and A4 are source assertions rather than behaviour, deliberately: the
 * defect was that the rule existed in twenty-four copies, and the only way to
 * keep it dead is to assert that no copy came back.
 *
 * MUTATION CONTROL at the end, because a suite that has only run against fixed
 * code is untested (feedback_test_against_the_known_defect).
 */
'use strict';
const fs   = require('fs');
const path = require('path');
const vm   = require('vm');

const ROOT   = path.join(__dirname, '..');
const RRV8   = path.join(ROOT, 'RRV8');
const config = fs.readFileSync(path.join(RRV8, 'config.js'), 'utf8');

let failures = 0;
function check(name, got, want) {
  const ok = JSON.stringify(got) === JSON.stringify(want);
  if (!ok) failures++;
  console.log('  ' + (ok ? 'ok  ' : 'FAIL') + '  ' + name +
              (ok ? '' : '   got ' + JSON.stringify(got) + ' want ' + JSON.stringify(want)));
  return ok;
}

/** Load config.js in isolation and read RRENV.mode() back. */
function modeWith(rrConfigOverride, source) {
  const sandbox = { window: {}, console: { log: function () {}, warn: function () {} } };
  sandbox.window.window = sandbox.window;
  sandbox.globalThis = sandbox;
  vm.createContext(sandbox);
  vm.runInContext(source === undefined ? config : source, sandbox);
  // The page's own config object wins; simulate each deploy shape.
  if (rrConfigOverride === 'ABSENT') { delete sandbox.window.RR_CONFIG; }
  else { sandbox.window.RR_CONFIG = rrConfigOverride; }
  sandbox.RR_CONFIG = sandbox.window.RR_CONFIG;
  return sandbox.window.RRENV.mode.call(sandbox.window);
}

/** Every tracked file under RRV8/, as {name, text}. */
function rrv8Files() {
  return fs.readdirSync(RRV8)
    .filter(function (f) { return /\.(html|js)$/.test(f); })
    .map(function (f) {
      return { name: f, text: fs.readFileSync(path.join(RRV8, f), 'utf8') };
    });
}

/** Strip LINE comments only, and only ones that OPEN a line.
 *
 *  A source assertion must not be satisfied or broken by prose: the
 *  demo-removal commit left explanatory comments that QUOTE the old
 *  expressions, and counting those as violations would keep this gate
 *  permanently red for the right reason stated wrongly.
 *
 *  ⚠ THIS DELIBERATELY DOES NOT STRIP BLOCK COMMENTS, and the first version
 *  of this file did, with the obvious regex. Tools/test-comment-stripper-
 *  safety.js (UI-170) caught it in CI. That expression pairs a `/*` or `*` + `/`
 *  inside a STRING or REGEX LITERAL with the wrong delimiter: measured on
 *  sidebar.js it removed 48% of the file. A stripper that silently deletes
 *  half its subject makes every later assertion meaningless in both
 *  directions, and the dangerous direction is the quiet one — a false FAIL
 *  gets investigated, a false PASS does not. In THIS file that would have
 *  meant A3/A4 passing because the offending code had been deleted before
 *  they looked.
 *
 *  The form below is one of the two the repo sanctions: it matches only a
 *  comment that opens a line, so a `//` inside a URL in a string survives.
 *  It is sufficient here because every comment this gate must ignore is a
 *  line comment. If a future assertion genuinely needs block comments gone,
 *  port the quote-tracking scanner from Tools/check_txv_cards.py, which
 *  raises on an unterminated block rather than guessing. */
function stripComments(text) {
  return text.replace(/^[ \t]*\/\/.*$/gm, '');
}

console.log('demo mode cannot be entered in V8\n');

// ---------------------------------------------------------------------------
// A1 / A2 -- the producer
// ---------------------------------------------------------------------------
check('A1 shipped dev config resolves to its configured mode',
      modeWith({ mode: 'staging' }), 'staging');
check('A1 a prod deploy resolves to prod',
      modeWith({ mode: 'prod' }), 'prod');

// The four shapes a broken deploy actually takes.
check('A2 RR_CONFIG absent      -> not demo', modeWith('ABSENT'), 'staging');
check('A2 RR_CONFIG empty {}    -> not demo', modeWith({}), 'staging');
check('A2 mode null             -> not demo', modeWith({ mode: null }), 'staging');
check('A2 mode blank string     -> not demo', modeWith({ mode: '' }), 'staging');
// ⭐ The one that makes "IS_DEMO is provably false" a true statement rather
// than an observation about today's config. Removing the fallbacks stops a
// page DRIFTING into demo; only this stops a deploy CHOOSING it, and a
// config.js setting mode:'demo' would otherwise switch all ~94 IS_DEMO
// branches back on — including sidebar.js hiding sign-out and skipping
// enforceSessionGuard().
check("A2 mode explicitly 'demo' -> COERCED, not honoured",
      modeWith({ mode: 'demo' }), 'staging');
check('A2 control: a legitimate mode is never coerced',
      modeWith({ mode: 'prod' }), 'prod');

// ---------------------------------------------------------------------------
// A3 / A4 / A5 -- no copy of the old rule came back
// ---------------------------------------------------------------------------
const files = rrv8Files();
console.log('  (scanning ' + files.length + ' files under RRV8/)');

const readsQueryMode = [];
const hasDemoDefault = [];
files.forEach(function (f) {
  const code = stripComments(f.text);
  if (/get\(\s*['"]mode['"]\s*\)/.test(code)) readsQueryMode.push(f.name);
  if (/\|\|\s*['"]demo['"]/.test(code))       hasDemoDefault.push(f.name);
});
check('A3 no RRV8 file reads the mode query parameter', readsQueryMode, []);
check("A4 no RRV8 file carries a || 'demo' fallback in code", hasDemoDefault, []);

const sidebar = stripComments(
  files.filter(function (f) { return f.name === 'sidebar.js'; })[0].text);
const modeProducers = (sidebar.match(/function _rrMode\s*\(/g) || []).length;
check('A5 sidebar.js declares exactly one mode producer', modeProducers, 1);

// ---------------------------------------------------------------------------
// MUTATION CONTROL
// ---------------------------------------------------------------------------
console.log('\nmutation control -- demo default re-injected into RRENV.mode():');
const MUTANT = config.replace(
  "return m === 'demo' ? 'staging' : m;",
  "return m;");
if (MUTANT === config) {
  console.log('  FAIL  mutation did not apply -- the control is vacuous');
  failures++;
} else {
  const mutantDemo = modeWith({ mode: 'demo' }, MUTANT);
  const caught = (mutantDemo === 'demo');
  console.log('  ' + (caught ? 'ok  ' : 'FAIL') +
              '  A2 fails on the mutant (mode:"demo" -> "' + mutantDemo + '")');
  if (!caught) {
    failures++;
    console.log('  the control did not discriminate: A2 would have passed against '
                + 'the known defect');
  }
  // Must SURVIVE the mutation, or the suite is just failing everything: a
  // deploy that sets its mode was never affected by this defect.
  const stillFine = modeWith({ mode: 'prod' }, MUTANT);
  const survives = (stillFine === 'prod');
  console.log('  ' + (survives ? 'ok  ' : 'FAIL') +
              '  a configured deploy is unaffected by the mutant (still "' + stillFine + '")');
  if (!survives) failures++;
}

console.log('\n' + (failures ? failures + ' FAILURE(S)' : 'all assertions passed'));
process.exit(failures ? 1 : 0);
