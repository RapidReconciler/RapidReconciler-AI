"""Test the decision logic of update-release-notes.yml's PR-and-merge step.

That step is shell nobody can run locally: it needs GitHub, a PAT and a real
PR. But its DECISIONS are testable -- when it merges, when it refuses, and
whether it can be fooled by the stale-read race that HK-8's family keeps
producing. So the step's `run:` block is EXTRACTED FROM THE WORKFLOW (not
retyped), `git` and `gh` are stubbed on PATH, and it is run under
`bash -e` to match GitHub's default shell exactly -- including the absence of
`-o pipefail`.

Five cases, and the two that matter are the ones where `gh pr checks` says
everything is fine and the step must refuse anyway.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WFDIR = os.path.join(REPO, ".github", "workflows")
STEP = "Open a PR and merge it once the checks pass"

# The three bot workflows that land their output through a PR. With no
# argument every one is checked, which is the form CI wants; naming one is for
# iterating on a single file.
ALL = ["update-release-notes", "refresh-indices", "update-doc-dates"]
_named = [a for a in sys.argv[1:] if not a.startswith("--")]
TARGETS = _named or ALL

if len(TARGETS) > 1:
    # Re-exec once per workflow so each gets its own extraction and report,
    # and the exit code is the worst of them.
    worst = 0
    for name in TARGETS:
        rc = subprocess.run([sys.executable, os.path.abspath(__file__), name]
                            + [a for a in sys.argv[1:] if a.startswith("--")]).returncode
        worst = max(worst, rc)
        print()
    print("all %d bot workflows checked; worst exit %d" % (len(TARGETS), worst))
    sys.exit(worst)

WF = os.path.join(WFDIR, TARGETS[0] + ".yml")
print("== %s" % os.path.basename(WF))


def extract_step_script(path, step_name):
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    i = text.index("- name: " + step_name)
    j = text.index("run: |", i) + len("run: |")
    body = text[j:]
    out = []
    for line in body.split("\n")[1:]:
        if line.strip() and not line.startswith(" " * 10):
            break
        out.append(line[10:] if len(line) > 10 else "")
    while out and out[-1].strip() == "":
        out.pop()
    return "\n".join(out)


SCRIPT = extract_step_script(WF, STEP)

# --mutate neuters the two sha-based guards, leaving only `gh pr checks`'s exit
# code -- i.e. the version that trusts --watch. The cases those guards exist
# for must then go red, or they were never testing anything.
if "--mutate" in sys.argv:
    before = SCRIPT
    SCRIPT = re.sub(r' \|\| echo ",\$state," \| grep -q [^;]*', "", SCRIPT)
    SCRIPT = SCRIPT.replace('if [ -z "$state" ]; then', "if false; then")
    if SCRIPT == before:
        print("ABORT: the mutation did not apply; the guards may have been reworded")
        sys.exit(1)
    print("MUTANT: both sha-based guards neutered")

if "gh pr merge" not in SCRIPT or "--watch --fail-fast" not in SCRIPT:
    print("ABORT: extraction looks wrong; got %d chars" % len(SCRIPT))
    print(SCRIPT[:400])
    sys.exit(1)
print("extracted %d lines of the step's shell" % len(SCRIPT.split("\n")))

GIT_STUB = r"""#!/usr/bin/env bash
echo "git $*" >> "$CALLS"
case "$1 $2" in
  "diff --staged")  exit ${GIT_DIFF_RC:-1} ;;   # 1 = there ARE staged changes
esac
exit 0
"""

# The step polls for a check run to REGISTER, sleeping 10s up to 30 times. A
# real sleep would make this suite take 5 minutes per case, so it is stubbed to
# return instantly. The stub still records the call, so a case can assert on
# how many times the poll went round.
SLEEP_STUB = r"""#!/usr/bin/env bash
echo "sleep $*" >> "$CALLS"
exit 0
"""

GH_STUB = r"""#!/usr/bin/env bash
echo "gh $*" >> "$CALLS"
if [ "$1" = "pr" ] && [ "$2" = "create" ]; then
  echo "https://github.com/o/r/pull/777"; exit 0
fi
if [ "$1" = "pr" ] && [ "$2" = "checks" ]; then
  echo "callsites  ${CHECKS_TEXT:-pass}  15s"
  exit ${CHECKS_RC:-0}
fi
if [ "$1" = "pr" ] && [ "$2" = "view" ]; then
  echo "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef"; exit 0
fi
if [ "$1" = "api" ]; then
  # Two different calls hit this endpoint and they must not be conflated:
  # the registration poll asks for .total_count (a number), the verdict asks
  # for the joined conclusions (a string). Returning the string to the poll
  # would make `[ "$n" -gt 0 ]` an integer-expression error under bash -e.
  case "$*" in
    *total_count*) printf '%s\n' "${COUNT-2}"; exit 0 ;;
  esac
  printf '%s\n' "${CONCLUSIONS-success,success}"; exit 0
fi
if [ "$1" = "pr" ] && [ "$2" = "merge" ]; then exit 0; fi
exit 0
"""


def run_case(name, env, expect_rc, expect_merge):
    d = tempfile.mkdtemp()
    bin_dir = os.path.join(d, "bin")
    os.makedirs(bin_dir)
    for fname, body in (("git", GIT_STUB), ("gh", GH_STUB), ("sleep", SLEEP_STUB)):
        p = os.path.join(bin_dir, fname)
        with open(p, "w", newline="\n", encoding="utf-8") as fh:
            fh.write(body)
        os.chmod(p, 0o755)
    calls = os.path.join(d, "calls.txt")
    open(calls, "w").close()
    script = os.path.join(d, "step.sh")
    with open(script, "w", newline="\n", encoding="utf-8") as fh:
        fh.write(SCRIPT)

    e = dict(os.environ)
    e.update({"PATH": bin_dir + ":" + os.environ.get("PATH", ""),
              "CALLS": calls, "GITHUB_RUN_ID": "12345",
              "GITHUB_REPOSITORY": "o/r", "RUNNER_TEMP": d})
    e.update(env)
    # bash -e with NO -o pipefail: GitHub's documented default shell.
    proc = subprocess.run(["bash", "-e", script], capture_output=True,
                          text=True, env=e, cwd=d)
    with open(calls, encoding="utf-8") as fh:
        made = fh.read()
    merged = "pr merge" in made
    created = "pr create" in made
    ok_rc = proc.returncode == expect_rc
    ok_merge = merged == expect_merge
    verdict = "ok  " if (ok_rc and ok_merge) else "FAIL"
    print("  %s %-46s exit=%-2d (want %-2d)  merged=%-5s (want %s)"
          % (verdict, name, proc.returncode, expect_rc, merged, expect_merge))
    if not (ok_rc and ok_merge):
        print("       stdout: %s" % proc.stdout.strip().replace("\n", " | ")[:300])
        print("       calls : %s" % made.strip().replace("\n", " | ")[:300])
    shutil.rmtree(d, ignore_errors=True)
    return ok_rc and ok_merge, created


results = []

# 1. nothing changed -> exit 0 without opening anything
ok, created = run_case("no staged changes: exits clean, opens no PR",
                       {"GIT_DIFF_RC": "0"}, 0, False)
results.append(ok and not created)

# 2. the happy path
results.append(run_case("checks green: merges",
                        {"CHECKS_RC": "0", "CONCLUSIONS": "success,success"}, 0, True)[0])

# 3. gh pr checks itself reports failure
results.append(run_case("gh pr checks exit 1: refuses to merge",
                        {"CHECKS_RC": "1", "CONCLUSIONS": "failure,success"}, 1, False)[0])

# 4. THE STALE-READ CASE. gh says 0, the sha says failure. Measured on UI #539:
#    --watch returned 0 quoting the previous head's run.
results.append(run_case("gh exit 0 but sha says failure: refuses",
                        {"CHECKS_RC": "0", "CONCLUSIONS": "failure,success"}, 1, False)[0])

# 5. no check runs at all -- the GITHUB_TOKEN-equivalent symptom
results.append(run_case("no check runs reported: refuses",
                        {"CHECKS_RC": "0", "CONCLUSIONS": ""}, 1, False)[0])

# 5b. THE DEFECT THE FIRST LIVE RUN EXPOSED. A check that has not REGISTERED
#     yet is not a verdict. Before the fix the step read `gh pr checks`'s
#     instant "no checks reported" and refused, while callsites was created 19
#     seconds later and passed. COUNT=0 makes the registration poll never
#     succeed, which must end in a refusal that names registration rather than
#     a merge.
ok, _created = run_case("check never registers: refuses, does not merge",
                        {"COUNT": "0", "CHECKS_RC": "0",
                         "CONCLUSIONS": "success"}, 1, False)
results.append(ok)

# 6. a cancelled check must not read as a pass
results.append(run_case("cancelled check: refuses",
                        {"CHECKS_RC": "0", "CONCLUSIONS": "success,cancelled"}, 1, False)[0])

print()
bad = len([r for r in results if not r])
print("%d cases, %d failed" % (len(results), bad))
sys.exit(1 if bad else 0)
