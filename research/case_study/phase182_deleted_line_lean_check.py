#!/usr/bin/env python3
"""Fresh replay of the literal F4 residue certificate and two rejected changes."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

ROOT=Path(__file__).resolve().parent
SOURCE="formal/DeletedLineFourResidue.lean"
INPUTS=[SOURCE,"phase182_deleted_line_lean_bridge.md",
        "phase182_deleted_line_independent_theorem.md",
        "phase182_deleted_line_lean_check.py"]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--lean",default="/Users/sasha/.elan/bin/lean")
    p.add_argument("--packages",type=Path,
                   default=Path("/Users/sasha/bogachev/formal/.lake/packages"))
    args=p.parse_args()
    if args.out.exists():
        p.error("output already exists")
    args.out.mkdir(parents=True)
    out=args.out.resolve()
    for f in INPUTS:
        dest=out/f;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/f,dest)
    env=os.environ.copy();env["ELAN_TOOLCHAIN"]="leanprover/lean4:v4.32.2"
    env["LEAN_PATH"]=":".join(
        str(args.packages/package/".lake/build/lib/lean")
        for package in ["mathlib","plausible","proofwidgets","batteries",
                        "aesop","importGraph","LeanSearchClient","Qq"])
    rev=subprocess.run(["git","-C",str(args.packages/"mathlib"),
                        "rev-parse","HEAD"],capture_output=True,text=True,
                       check=True).stdout.strip()
    if rev!="905b95818eb32af7874a58b427f50c1711a5e96c":
        raise RuntimeError("unexpected mathlib revision")
    started=time.monotonic()
    result=subprocess.run([args.lean,"-o",str(out/"DeletedLineFourResidue.olean"),
                           SOURCE],cwd=out,env=env,text=True,
                          stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
    (out/"phase182_deleted_line_lean.log").write_text(result.stdout)
    if result.returncode or "sorryAx" in result.stdout or result.stdout.count("depends on axioms:")!=7:
        raise RuntimeError("certificate failed")
    controls=[]
    original=(out/SOURCE).read_text()
    mutations=[
        ("dropped_flag_center",
         "nonzero point.2 + nonzero flag.2","nonzero point.2"),
        ("wrong_cycle_modulus",
         "(i.val + 1) % 6 = j.val","(i.val + 1) % 5 = j.val"),
    ]
    for name,old,new in mutations:
        if old not in original:
            raise RuntimeError("missing mutation site")
        mutant=out/(name+".lean");mutant.write_text(original.replace(old,new,1))
        r=subprocess.run([args.lean,str(mutant)],cwd=out,env=env,text=True,
                         stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        logfile=out/(name+".log");logfile.write_text(r.stdout)
        if r.returncode==0 or "error:" not in r.stdout:
            raise RuntimeError("semantic mutation accepted: "+name)
        controls.append({"name":name,"returncode":r.returncode,"log_sha256":sha(logfile)})
    report={"status":"PASS","seconds":round(time.monotonic()-started,3),
            "inputs":{f:sha(out/f) for f in INPUTS},"mathlib_revision":rev,
            "source_pdf_sha256":sha(ROOT/"sources/older_L092_gwdg.pdf"),
            "lean_axiom_reports":7,"semantic_rejection_controls":controls,
            "scope":"Literal F4 equation; exact three-hexagon decomposition and disconnection; source object bridge written; uniform theorem not formalized",
            "log_sha256":sha(out/"phase182_deleted_line_lean.log")}
    (out/"phase182_deleted_line_lean_build.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":"PASS","seconds":report["seconds"],"out":str(out)}))


if __name__=="__main__":
    main()
