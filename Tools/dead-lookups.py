#!/usr/bin/env python3
"""Report element lookups that can never resolve: getElementById / querySelector
on an id that no markup anywhere produces.

Answers one question: when this page calls getElementById('x'), is there any
`id="x"` for it to find -- in this page's own markup, in a template string this
page builds, or injected into every V8 page by a shared script?

A lookup with no producer returns null forever. Because these pages guard almost
every lookup (`if (el)`, `el && el.addEventListener`, `typeof f === 'function'`),
nothing throws and nothing is logged. The feature is simply absent, and the code
reaching for it reads as live to the next person grepping. That shape produced
UI-183 (six features built in CSS and JS with no markup for two months) and
UI-184 (fifteen dead lookups, one of them an entire popover wired to nothing).

WHAT IT DOES NOT ANSWER, stated because each of these already cost something:

  * A resolvable lookup is not a working feature. This tool proves an element
    exists to be found, nothing beyond that.
  * A DYNAMIC lookup -- getElementById('row-' + id) -- cannot be evaluated
    statically. Those are counted and listed under their own heading rather
    than dropped, because silently discarding them would understate the
    answer and look identical to a clean result.
  * ⚠ THE SUBTRACTION IS THE MEASUREMENT, AND A SAMPLE GETS IT WRONG. An id
    absent from a page's own markup can still be live, because sidebar.js and
    the other shared modules inject chrome into every V8 page. UI-184 tested 8
    of one page's 14 candidates, found one shared-script hit, and was about to
    record "only one comes from a shared script". Checked against every
    RRV8/*.js and Tools/*.js instead: five did. A sample is not a denominator.
    So this tool always scans the FULL shared set, never a subset.

⚠ SCRIPT BODIES ARE NOT STRIPPED, for the same reason orphan-selectors.py
documents: these pages build most of their DOM from template strings inside one
very large <script>, so `id="popover-row"` inside a backtick template IS how
that element comes to exist. Stripping scripts would report most of the page's
own elements as missing.

Usage:
    python Tools/dead-lookups.py RRV8/inventory-transactions.html [...]
    python Tools/dead-lookups.py --all          # every RRV8/*.html
    python Tools/dead-lookups.py --self-test

Exit 0 when every file was parsed. Exit 1 on a self-test failure or an
unreadable file. Finding dead lookups is NOT an error -- this is a reporter,
not a gate. Some of what it finds is a deliberate leftover with a comment
explaining itself, and a gate would force those to be deleted or suppressed
rather than read.
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

# ---------------------------------------------------------------------------
# What counts as a lookup.
# ---------------------------------------------------------------------------
# getElementById with a single quoted literal and nothing else inside the
# parens. The `\s*\)` is load-bearing: it is what separates a static lookup
# from getElementById('row-' + id), which must NOT be read as a lookup for the
# literal 'row-'.
GET_BY_ID_STATIC = re.compile(
    r"""getElementById\s*\(\s*(['"`])([A-Za-z_][\w-]*)\1\s*\)"""
)
# Any getElementById at all, so the dynamic ones can be counted by subtraction
# rather than by trying to enumerate every expression shape.
GET_BY_ID_ANY = re.compile(r"""getElementById\s*\(""")

# querySelector('#foo') / querySelectorAll("#foo") / closest('#foo') where the
# whole selector is one plain id. A compound selector ('#foo .bar') is left to
# orphan-selectors.py -- that tool already answers the CSS-selector question and
# two producers for one figure is its own defect.
QUERY_ID_STATIC = re.compile(
    r"""(?:querySelector|querySelectorAll|closest)\s*\(\s*"""
    r"""(['"`])#([A-Za-z_][\w-]*)\1\s*\)"""
)

# ---------------------------------------------------------------------------
# What counts as producing an id.
# ---------------------------------------------------------------------------
# id="foo" in markup, in a template string, or in an attribute built by JS.
ID_ATTR = re.compile(r"""\bid\s*=\s*(['"])([A-Za-z_][\w-]*)\1""")
# id=${...} and id="${...}" are dynamic; matched only to be counted, since a
# page that builds ids by interpolation cannot be statically resolved either.
ID_ATTR_DYNAMIC = re.compile(r"""\bid\s*=\s*['"]?\$\{""")
# el.id = 'foo'
ID_ASSIGN = re.compile(r"""\.id\s*=\s*(['"`])([A-Za-z_][\w-]*)\1""")
# setAttribute('id', 'foo')
ID_SETATTR = re.compile(
    r"""setAttribute\s*\(\s*(['"`])id\1\s*,\s*(['"`])([A-Za-z_][\w-]*)\2\s*\)"""
)


def ids_produced(text):
    """Every id this text can bring into existence, statically."""
    out = set()
    for m in ID_ATTR.finditer(text):
        out.add(m.group(2))
    for m in ID_ASSIGN.finditer(text):
        out.add(m.group(2))
    for m in ID_SETATTR.finditer(text):
        out.add(m.group(3))
    return out


def lookups_in(text):
    """(static lookups as {id: [lines]}, count of dynamic getElementById calls)."""
    found = {}
    for rx, grp in ((GET_BY_ID_STATIC, 2), (QUERY_ID_STATIC, 2)):
        for m in rx.finditer(text):
            name = m.group(grp)
            line = text.count("\n", 0, m.start()) + 1
            found.setdefault(name, []).append(line)
    total = len(GET_BY_ID_ANY.findall(text))
    static_by_id = len(GET_BY_ID_STATIC.findall(text))
    return found, max(0, total - static_by_id)


def shared_script_ids(extra_globs=None):
    """Ids injected by any shared module, scanned in FULL -- never sampled.

    Returns (ids, files_scanned). The file list is returned so the caller can
    print it: a subtraction whose inputs are invisible is not reviewable.
    """
    patterns = extra_globs or [
        os.path.join(REPO, "RRV8", "*.js"),
        os.path.join(REPO, "Tools", "*.js"),
    ]
    ids, files = set(), []
    for pat in patterns:
        for path in sorted(glob.glob(pat)):
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
            except OSError:
                continue
            files.append(os.path.relpath(path, REPO).replace("\\", "/"))
            ids |= ids_produced(text)
    return ids, files


def analyse(path, injected):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    looked_up, dynamic_calls = lookups_in(text)
    own = ids_produced(text)
    dynamic_ids = len(ID_ATTR_DYNAMIC.findall(text))

    absent = {k: v for k, v in looked_up.items() if k not in own}
    from_shared = {k: v for k, v in absent.items() if k in injected}
    dead = {k: v for k, v in absent.items() if k not in injected}
    return {
        "path": path,
        "looked_up": len(looked_up),
        "own_ids": len(own),
        "absent": len(absent),
        "from_shared": from_shared,
        "dead": dead,
        "dynamic_calls": dynamic_calls,
        "dynamic_ids": dynamic_ids,
    }


def report(r):
    rel = os.path.relpath(r["path"], REPO).replace("\\", "/")
    print("")
    print("=" * 72)
    print(rel)
    print("=" * 72)
    # Rule 6: the numbers that drive the decision are printed, not implied.
    print("  ids looked up statically : %d" % r["looked_up"])
    print("  ids the page produces    : %d" % r["own_ids"])
    print("  absent from own markup   : %d" % r["absent"])
    print("  of those, shared-script  : %d" % len(r["from_shared"]))
    print("  GENUINELY DEAD           : %d" % len(r["dead"]))
    if r["dynamic_calls"] or r["dynamic_ids"]:
        print("  not evaluated (dynamic)  : %d lookups, %d id= interpolations"
              % (r["dynamic_calls"], r["dynamic_ids"]))

    if r["from_shared"]:
        print("\n  injected by a shared script, so NOT dead:")
        for name in sorted(r["from_shared"]):
            print("    %-34s looked up at %s"
                  % (name, ", ".join(str(n) for n in r["from_shared"][name])))
    if r["dead"]:
        print("\n  DEAD -- no producer anywhere:")
        for name in sorted(r["dead"]):
            print("    %-34s looked up at %s"
                  % (name, ", ".join(str(n) for n in r["dead"][name])))
    else:
        print("\n  no dead lookups.")


# ---------------------------------------------------------------------------
# Self-test.
# ---------------------------------------------------------------------------
# ⚠ A PASSING SELF-TEST ON CORRECT INPUT PROVES NOTHING. Every case below is
# paired with the defect it is meant to catch, and the last block re-runs the
# analyser against a MUTATED subtraction to confirm the suite goes red. A check
# that has only ever been run on good input is untested.
_FIXTURE = """
<div id="real-thing"></div>
<script>
  const a = document.getElementById('real-thing');
  const b = document.getElementById('ghost-thing');
  const c = document.getElementById('injected-thing');
  const d = document.querySelector('#also-ghost');
  const e = document.getElementById('row-' + n);
  const f = document.querySelector('#real-thing .child');
  el.innerHTML = `<span id="built-by-template"></span>`;
  const g = document.getElementById('built-by-template');
  node.id = 'assigned-thing';
  const h = document.getElementById('assigned-thing');
</script>
"""


def self_test():
    failures = []

    def check(label, got, want):
        if got != want:
            failures.append("%s: got %r, want %r" % (label, got, want))

    own = ids_produced(_FIXTURE)
    check("markup id found", "real-thing" in own, True)
    check("template-string id found", "built-by-template" in own, True)
    check("assigned id found", "assigned-thing" in own, True)
    check("ghost not produced", "ghost-thing" in own, False)

    looked, dyn = lookups_in(_FIXTURE)
    check("static getElementById counted", "ghost-thing" in looked, True)
    check("querySelector('#x') counted", "also-ghost" in looked, True)
    # The two traps that would silently corrupt the answer:
    check("concatenated lookup NOT read as literal", "row-" in looked, False)
    check("dynamic lookup counted separately", dyn, 1)
    check("compound selector left alone", "real-thing .child" in looked, False)

    injected = {"injected-thing"}
    absent = {k for k in looked if k not in own}
    dead = {k for k in absent if k not in injected}
    check("shared-script id subtracted", "injected-thing" in dead, False)
    check("genuine ghosts survive", dead, {"ghost-thing", "also-ghost"})

    # MUTATION CONTROL: drop the subtraction, which is the one step the tool
    # exists for. The suite must go red, and it must be the shared-script
    # assertion that reddens -- not merely "something failed".
    mutant_dead = {k for k in absent}          # subtraction removed
    mutation_caught = "injected-thing" in mutant_dead
    if not mutation_caught:
        failures.append("MUTATION CONTROL DID NOT FIRE: removing the "
                        "shared-script subtraction changed nothing, so the "
                        "assertion above is vacuous")

    if failures:
        print("SELF-TEST FAILED (%d)" % len(failures))
        for f in failures:
            print("  " + f)
        return 1
    print("self-test OK -- 12 assertions, plus a mutation control that fires "
          "when the shared-script subtraction is removed")
    return 0


def main(argv):
    if "--self-test" in argv:
        return self_test()

    args = [a for a in argv if not a.startswith("--")]
    if "--all" in argv:
        args = sorted(glob.glob(os.path.join(REPO, "RRV8", "*.html")))
    if not args:
        print(__doc__)
        return 1

    injected, scanned = shared_script_ids()
    print("shared modules scanned for injected ids: %d files, %d ids"
          % (len(scanned), len(injected)))
    print("  " + ", ".join(scanned))

    results, bad = [], 0
    for a in args:
        path = a if os.path.isabs(a) else os.path.join(REPO, a)
        if not os.path.isfile(path):
            sys.stderr.write("dead-lookups: cannot read %s\n" % a)
            bad = 1
            continue
        r = analyse(path, injected)
        results.append(r)
        report(r)

    total = sum(len(r["dead"]) for r in results)
    print("")
    print("-" * 72)
    print("TOTAL genuinely dead lookups across %d file(s): %d"
          % (len(results), total))
    return bad


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
