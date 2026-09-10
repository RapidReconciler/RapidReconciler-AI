#!/usr/bin/env python3
"""Report class/id selectors that a page styles but never renders.

Answers one question: does any markup in this file carry the class or id
this stylesheet targets? A zero means the rule is dead weight -- or, more
usefully, that a design was written in CSS and never built in HTML.

WHAT IT DOES NOT ANSWER, stated because the distinction cost a session
elsewhere (see the VLC-66 worklist row): a usage count of 1+ does NOT mean
the selector is doing work, and a count of 0 on a PARENT does not mean its
descendant rules are dead. Read the descendants before deleting anything.

Usage:
    python Tools/orphan-selectors.py RRV8/inventory-transactions.html [...]
    python Tools/orphan-selectors.py --self-test

Exit 0 when every file was parsed. Exit 1 on a self-test failure or an
unreadable file. Finding orphans is not an error -- this is a reporter, not
a gate, because a shared stylesheet legitimately styles classes this page
does not use.
"""
import re
import sys

STYLE_BLOCK = re.compile(r"<style\b[^>]*>(.*?)</style>", re.S | re.I)
SCRIPT_BLOCK = re.compile(r"<script\b[^>]*>.*?</script>", re.S | re.I)
COMMENT = re.compile(r"/\*.*?\*/", re.S)
AT_RULE_HEAD = re.compile(r"@[a-z-]+[^{;]*[{;]", re.I)

# A selector token: .name or #name. Hyphens and digits allowed; a leading
# digit is not valid in CSS so it is not matched.
SELECTOR_TOKEN = re.compile(r"([.#])([A-Za-z_][A-Za-z0-9_-]*)")


# ⚠ SCRIPT BODIES ARE NOT STRIPPED, AND THAT IS THE WHOLE POINT.
# The first version of this tool removed them, reasoning that a class merely
# NAMED in JS is not markup. On the V8 pages that inverted the answer: these
# pages build most of their DOM from template strings inside one 7,000-line
# <script>, so `class="popover-row"` at inventory-transactions.html:9262 IS
# how that element gets its class. Stripping scripts reported 227 of 352
# selectors on that page as orphaned, including ten live ones. Caught by
# disagreeing with a hand grep, not by reading the code.
STYLE_ONLY = re.compile(r"<style\b[^>]*>.*?</style>", re.S | re.I)
CLASS_ATTR = re.compile(r"""class\s*=\s*(?:["']([^"']*)["']|\{?`([^`]*)`)""", re.I)
JS_STRING = re.compile(r"""['"]([A-Za-z_][A-Za-z0-9_ -]{1,120})['"]""")
CLASSLIST = re.compile(r"""classList\s*\.\s*(?:add|remove|toggle|contains)\s*\(([^)]*)\)""")


def selectors_in_styles(html):
    """Every class/id token appearing in a selector position, with its line."""
    found = {}
    for m in STYLE_BLOCK.finditer(html):
        body = m.group(1)
        base_line = html.count("\n", 0, m.start(1)) + 1
        body = COMMENT.sub(lambda c: "\n" * c.group(0).count("\n"), body)
        # Walk declaration blocks: text before a "{" is a selector list.
        pos = 0
        while True:
            brace = body.find("{", pos)
            if brace < 0:
                break
            head = body[pos:brace]
            close = body.find("}", brace)
            if close < 0:
                close = len(body)
            # An at-rule head (@media, @supports) carries no selectors of
            # its own, and its body is walked by the same loop afterwards.
            if not AT_RULE_HEAD.match(head.strip()):
                line = base_line + body.count("\n", 0, pos)
                for tok in SELECTOR_TOKEN.finditer(head):
                    kind, name = tok.group(1), tok.group(2)
                    key = ("id" if kind == "#" else "class", name)
                    found.setdefault(key, line + head[:tok.start()].count("\n"))
            pos = brace + 1
    return found


def markup_usage(html):
    """Count class/id usages across the file, static markup and JS alike.

    Returns (classes, ids, soft) where `soft` holds names seen only as a
    bare quoted JS string or a classList argument. Those are weaker
    evidence than a class attribute, so they are reported separately --
    but they still count as USED, because the safe direction for an
    orphan reporter is to under-report. Telling someone a live selector
    is dead is the expensive mistake.
    """
    body = STYLE_ONLY.sub(lambda m: "\n" * m.group(0).count("\n"), html)
    classes = {}
    for m in CLASS_ATTR.finditer(body):
        for tok in (m.group(1) or m.group(2) or "").split():
            # A template interpolation leaves fragments like ${x} or '+cls+'
            if tok.startswith("$") or "'" in tok or '"' in tok:
                continue
            classes[tok] = classes.get(tok, 0) + 1
    ids = {}
    for m in re.finditer(r"""id\s*=\s*["']([^"']*)["']""", body, re.I):
        val = m.group(1).strip()
        if val and not val.startswith("$"):
            ids[val] = ids.get(val, 0) + 1
    soft = {}
    for m in CLASSLIST.finditer(body):
        for s in JS_STRING.finditer(m.group(1)):
            for tok in s.group(1).split():
                soft[tok] = soft.get(tok, 0) + 1
    for m in re.finditer(r"""getElementById\s*\(\s*['"]([^'"]+)['"]""", body):
        soft[m.group(1)] = soft.get(m.group(1), 0) + 1
    for m in re.finditer(r"""querySelector(?:All)?\s*\(\s*['"]([^'"]+)['"]""", body):
        for tok in SELECTOR_TOKEN.finditer(m.group(1)):
            soft[tok.group(2)] = soft.get(tok.group(2), 0) + 1
    return classes, ids, soft


def report(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        html = fh.read()
    styled = selectors_in_styles(html)
    classes, ids, soft = markup_usage(html)
    orphans, soft_only = [], []
    for (kind, name), line in sorted(styled.items(), key=lambda kv: kv[1]):
        hard = (ids if kind == "id" else classes).get(name, 0)
        if hard:
            continue
        if soft.get(name, 0):
            soft_only.append((line, kind, name, soft[name]))
        else:
            orphans.append((line, kind, name))
    print("%s -- %d styled selectors, %d class attrs, %d id attrs, "
          "%d orphaned, %d script-only" % (path, len(styled),
          sum(classes.values()), sum(ids.values()), len(orphans),
          len(soft_only)))
    for line, kind, name in orphans:
        print("  ORPHAN      line %-6d %s%s" % (line, "#" if kind == "id" else ".", name))
    for line, kind, name, n in soft_only:
        print("  script-only line %-6d %s%s  (%d JS reference%s, no class/id "
              "attribute)" % (line, "#" if kind == "id" else ".", name, n,
                              "" if n == 1 else "s"))
    return len(orphans)


SELF_TEST = """<html><head><style>
  .lives { color: red; }
  .orphan-class { color: blue; }
  #js-host.orphan-class { display: none; }
  #lives-id { margin: 0; }
  /* .commented-out { color: green; } */
  @media (max-width: 900px) {
    .orphan-in-media { flex: none; }
    .lives { color: pink; }
  }
  .parent > .orphan-child { gap: 2px; }
  .tpl-built { border: 0; }
  #js-soft-host { color: teal; }
</style></head><body>
  <div class="lives" id="lives-id">x</div>
  <div class="parent">y</div>
  <script>
    var s = 'orphan-class'; el.className = 'orphan-in-media';
    box.innerHTML = '<div class="tpl-built">built from a template string</div>';
    var h = document.getElementById('js-soft-host');
  </script>
</body></html>"""


def self_test():
    import tempfile
    import os
    checks = []
    styled = selectors_in_styles(SELF_TEST)
    names = {n for (_k, n) in styled}
    checks.append(("selector in a plain rule found", ("class", "lives") in styled))
    checks.append(("id selector found", ("id", "lives-id") in styled))
    checks.append(("compound #id.class -- both halves found",
                   ("id", "js-host") in styled and ("class", "orphan-class") in styled))
    checks.append(("selector inside @media found", ("class", "orphan-in-media") in styled))
    checks.append(("@media itself not read as a selector", "media" not in names))
    checks.append(("commented-out rule NOT found", ("class", "commented-out") not in styled))
    checks.append(("descendant selector -- both halves found",
                   ("class", "parent") in styled and ("class", "orphan-child") in styled))

    classes, ids, soft = markup_usage(SELF_TEST)
    checks.append(("markup class counted", classes.get("lives") == 1))
    checks.append(("markup id counted", ids.get("lives-id") == 1))
    checks.append(("a class named only as a bare JS string is NOT usage",
                   classes.get("orphan-class", 0) == 0 and
                   classes.get("orphan-in-media", 0) == 0))
    # THE REGRESSION GUARD for the defect this tool shipped with: the first
    # version stripped <script> bodies and so missed every class attribute
    # written inside a template string, which is how the V8 pages build
    # their DOM. It reported ten live selectors as orphaned.
    checks.append(("class attr inside a <script> template string IS usage",
                   classes.get("tpl-built") == 1))
    checks.append(("getElementById counts as SOFT evidence only",
                   soft.get("js-soft-host") == 1 and
                   "js-soft-host" not in ids))
    checks.append(("a class token containing $ is not counted",
                   not any(k.startswith("$") for k in classes)))

    fd, tmp = tempfile.mkstemp(suffix=".html")
    os.close(fd)
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(SELF_TEST)
    try:
        n = report(tmp)
    finally:
        os.unlink(tmp)
    # 9 styled selectors. Carried by markup: lives, lives-id, parent,
    # tpl-built. Soft-only: js-soft-host. Orphaned: orphan-class, js-host,
    # orphan-in-media, orphan-child = 4.
    # ⚠ This assertion first read 5 and the TOOL was right -- the fixture
    # expectation was the defect, the same slip HK-13's self-test made.
    # Count the fixture by hand before believing a red case.
    checks.append(("orphan count on the fixture is 4", n == 4))

    bad = [name for name, ok in checks if not ok]
    for name, ok in checks:
        print("  %-58s %s" % (name, "ok" if ok else "BROKEN"))
    print("self-test: %d cases, %d broken" % (len(checks), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "--self-test":
        sys.exit(self_test())
    rc = 0
    for path in args:
        try:
            report(path)
        except OSError as exc:
            print("could not read %s: %s" % (path, exc))
            rc = 1
    sys.exit(rc)
