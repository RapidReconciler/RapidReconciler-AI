#!/usr/bin/env python3
"""Prove the tokenizer Tools/v8-callsites.py depends on actually works.

    python Tools/_persona/check-tokenizer.py

Run BEFORE the gate, in CI and locally. v8-callsites.py exits 2 when esprima is
missing, which is neither a pass nor a verdict -- and an exit 2 three steps into
a job reads as "the gate failed" rather than "the gate never ran".

It exercises what the gate actually uses rather than checking that an import
succeeded:

  * tokenize() with options={"loc": True}, because line numbers are how every
    finding is addressed. An esprima whose loc shape changed would import
    cleanly and then report every call site at the wrong line.
  * a string literal survives tokenization with its quotes attached. The gate
    strips them; a first version of it did not, and A3 failed on all 54 api/v1
    literals because a quoted literal never matched an unquoted one. If a future
    esprima strips them itself, that stripping becomes a silent no-op and this
    catches it here instead.
  * optional chaining TOKENIZES even though esprima 4 cannot PARSE it. That
    property is the whole reason the gate tokenizes instead of parsing, and it
    is a fact about this implementation, not a promise of the API.
"""
import sys

try:
    import esprima
except ImportError:
    sys.stderr.write("check-tokenizer: esprima is not installed\n")
    raise SystemExit(2)

try:
    import importlib.metadata as _md
    VERSION = _md.version("esprima")
except Exception:                                     # pragma: no cover
    VERSION = "unknown"


def main():
    failures = []

    toks = esprima.tokenize("var a = f('api/v1/tenant/x');", options={"loc": True})
    if not toks:
        failures.append("tokenize() returned nothing")
    else:
        if getattr(toks[0], "loc", None) is None:
            failures.append("tokens carry no .loc -- every reported line would be wrong")
        elif toks[0].loc.start.line != 1:
            failures.append("first token reports line %r, expected 1" % toks[0].loc.start.line)

        strings = [str(t.value) for t in toks if t.type == "String"]
        if strings != ["'api/v1/tenant/x'"]:
            failures.append(
                "string token value is %r; the gate strips surrounding quotes and "
                "would now strip nothing, so its literal matching breaks" % (strings,))

    # esprima 4 is ES2017 and CANNOT parse `?.`. It must still tokenize it.
    try:
        esprima.tokenize("var b = a?.c;")
    except Exception as exc:
        failures.append("cannot tokenize optional chaining (%s) -- the gate would "
                        "fail on most RRV8 pages for a reason unrelated to the code"
                        % str(exc)[:80])

    # And the control: the thing esprima genuinely cannot do, so a run where
    # tokenize() had silently become a no-op returning [] for everything does
    # not read as three passes.
    try:
        esprima.parseScript("var b = a?.c;")
        failures.append("parseScript accepted optional chaining -- this is not "
                        "esprima 4, and the gate's engine assumptions no longer hold")
    except Exception:
        pass

    if failures:
        print("check-tokenizer: FAILED (esprima %s)" % VERSION)
        for f in failures:
            print("  %s" % f)
        return 1
    print("check-tokenizer: esprima %s -- tokenize+loc, quoted literals, optional "
          "chaining, and the parse control all behave as the gate assumes" % VERSION)
    return 0


if __name__ == "__main__":
    sys.exit(main())
