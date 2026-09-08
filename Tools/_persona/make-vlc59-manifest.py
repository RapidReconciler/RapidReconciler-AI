#!/usr/bin/env python3
"""Build a manifest carrying the VLC-59 defect, so persona-probe.py can be
proven able to FAIL.

    python Tools/v8-callsites.py --json Tools/_out/v8-callsites.json
    python Tools/_persona/make-vlc59-manifest.py
    python Tools/persona-probe.py --manifest Tools/_out/v8-callsites-vlc59.json

Expected: a wall of FAILs and a non-zero exit. persona-probe.py's own C1
control proves the operator GATE refuses, which is one link; this proves the
whole prober -- enumeration, personas, verdict table, reporting -- turns that
refusal into a named failure. A run that only ever sees fixed code is not a
test of anything, and every green line above it would be indistinguishable
from a harness that had quietly stopped asserting.

This writes a SEPARATE file. It never touches the real manifest.
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "_out")
SRC = os.path.join(OUT, "v8-callsites.json")
DST = os.path.join(OUT, "v8-callsites-vlc59.json")


def main():
    if not os.path.exists(SRC):
        print("no manifest at %s -- run Tools/v8-callsites.py --json first" % SRC)
        return 2
    m = json.load(io.open(SRC, encoding="utf-8"))
    n = 0
    for s in m["sites"]:
        p = s.get("path")
        if p and p.startswith("api/v1/tenant/"):
            # Exactly what shipped in Valc #241: the customer half of the
            # surface pointed at the operator prefix.
            s["path"] = "api/v1/admin/" + p[len("api/v1/tenant/"):]
            n += 1
    if not n:
        print("nothing to mutate: no api/v1/tenant/ path in the manifest. The "
              "control cannot be built, so the prober is UNTESTED.")
        return 1
    io.open(DST, "w", encoding="utf-8").write(json.dumps(m, indent=1, sort_keys=True))
    print("re-pointed %d tenant path(s) at the operator prefix" % n)
    print("wrote %s" % DST)
    print()
    print("now run:  python Tools/persona-probe.py --manifest %s" % DST)
    print("expect:   FAILURES, exit 1. A pass means the prober is not asserting.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
