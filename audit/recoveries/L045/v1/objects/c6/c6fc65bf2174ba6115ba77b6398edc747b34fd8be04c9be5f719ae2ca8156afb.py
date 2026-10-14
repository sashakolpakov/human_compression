"""Fresh deterministic replay of all saved finite Lie witnesses; no search."""
import sys
if sys.flags.optimize:
    raise SystemExit("Run without Python optimization.")
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
from literal import need, roster, verify_literal

BASE=Path(__file__).resolve().parent


def save(path, value):
    path.write_text(json.dumps(value,indent=2)+"\n")


def pin(path):
    b=path.read_bytes()
    return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())


def check_pin(path,item):
    need(pin(path)=={k:item[k] for k in ["bytes","sha256"]},"Changed exact input: "+str(path))


def run(command,directory,seconds,negative=False):
    directory.mkdir()
    env=os.environ.copy();env.pop("PYTHONOPTIMIZE",None)
    start=time.monotonic()
    with (directory/"stdout").open("wb") as so,(directory/"stderr").open("wb") as se:
        try:
            result=subprocess.run([str(c) for c in command],stdout=so,stderr=se,env=env,timeout=seconds,cwd=directory.parent)
        except subprocess.TimeoutExpired:
            save(directory/"receipt.json",dict(status="TIMEOUT_NO_CERTIFICATE",command=[str(c) for c in command],elapsed_seconds=time.monotonic()-start))
            raise
    receipt=dict(status="REJECTED_CONTROL" if negative else "TERMINAL_PASS",command=[str(c) for c in command],returncode=result.returncode,elapsed_seconds=time.monotonic()-start,stdout=pin(directory/"stdout"),stderr=pin(directory/"stderr"))
    save(directory/"receipt.json",receipt)
    need(not (directory/"stderr").read_text().strip(),"Clean stderr: "+str(directory))
    need(result.returncode==(1 if negative else 0),"Expected terminal code: "+str(directory))
    return receipt


def gap_case(gap,row,out,control="none"):
    out.mkdir()
    driver=out/"driver.g"
    values=dict(ExpectedParameters=row["parameters"],ExpectedOrder=row["group_order"],ExpectedOrders=row["orders"],ExpectedDegree=row["degree"],CaseNumber=row["case_number"],PairPath=str(BASE/row["relative_pair"]),OutputPath=str(out/"result.json"),Control=control)
    driver.write_text("".join(k+":="+json.dumps(v)+";;\n" for k,v in values.items())+"Read("+json.dumps(str(BASE/"verify.g"))+");;\n")
    r=run([gap,"-q","-b",driver],out/"execution",45,control!="none")
    stdout=(out/"execution/stdout").read_text().strip()
    if control!="none":
        need(stdout.startswith("REJECT ") and not (out/"result.json").exists(),"Substantive negative rejection before result")
        return dict(control=control,message=stdout,receipt=r)
    need(stdout=="TERMINAL_PASS finite Lie certificate","Exact complete GAP terminal marker")
    result=json.loads((out/"result.json").read_text())
    need(result==dict(parameters=row["parameters"],degree=row["degree"],group_order=row["group_order"],orders=row["orders"],literal_constructor_generators=True,actual_membership=True,full_generation=True),"Exact fresh positive record")
    return result


def native(out):
    out.mkdir();shutil.copy2(BASE/"finite_lie.tex",out/"finite_lie.tex")
    shutil.copy2(BASE/"table.tex",out/"table.tex")
    for i in range(2):
        run(["pdflatex","-halt-on-error","-interaction=nonstopmode","-output-directory="+str(out),str(out/"finite_lie.tex")],out/f"pass{i}",60)
    log=(out/"finite_lie.log").read_text()
    need("Overfull" not in log and "LaTeX Warning" not in log,"Native overflow/reference guard")
    from pypdf import PdfReader
    pdf=PdfReader(out/"finite_lie.pdf");text="\n".join(p.extract_text() or "" for p in pdf.pages)
    (out/"text.txt").write_text(text)
    need(text==(BASE/"native/text.txt").read_text(),"Exact frozen native text")
    run(["gs","-q","-dNOPAUSE","-dBATCH","-sDEVICE=png16m","-r110","-sOutputFile="+str(out/"page-%02d.png"),out/"finite_lie.pdf"],out/"render",60)
    return dict(pages=len(pdf.pages),text_matches=True,underfull_paragraph="Underfull" in log)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--study",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    ap.add_argument("--gap",type=Path,default=Path(shutil.which("gap") or "/missing/gap"))
    ap.add_argument("--gap-root",type=Path)
    ap.add_argument("--render",action="store_true")
    args=ap.parse_args()
    need(args.out.is_absolute() and not args.out.exists() and not args.out.is_symlink(),"Fresh absolute output required")
    gap=args.gap.resolve();roots=dict(study=args.study.resolve(),gap=(args.gap_root or gap.parent.parent).resolve())
    manifest=json.loads((BASE/"manifest.json").read_text())
    for p in manifest["exports"]: check_pin(BASE/p["path"],p)
    dependencies=json.loads((BASE/"dependencies.json").read_text())["files"]
    for p in dependencies: check_pin(roots[p["namespace"]]/p["path"],p)
    provenance=json.loads((BASE/"input_provenance.json").read_text())
    for p in provenance["files"]: check_pin(BASE/p["local_path"],p)
    rows=json.loads((BASE/"cases.json").read_text());scope=roster(rows)
    for row in rows:
        driver=(BASE/row["relative_pair"]).with_name("driver.g").read_text()
        need("CaseNumber:="+str(row["case_number"])+";;" in driver,"Exact original constructor seed")
    args.out.mkdir()
    literal=verify_literal(BASE,rows);save(args.out/"literal_report.json",literal)
    expected=json.loads((BASE/"expected.json").read_text())
    need(literal==expected["literal"],"All independent cycle oracle results")
    results=[]
    for row in rows:
        results.append(gap_case(gap,row,args.out/row["id"]))
    need(results==expected["gap"],"All exact named finite certificates")
    negatives=args.out/"negative_controls";negatives.mkdir()
    controls=[gap_case(gap,rows[0],negatives/c,c) for c in ["parameters","ambient","identity","outside","generation","orders","equal_words"]]
    save(negatives/"report.json",controls)
    malformed=[]
    for name in ["missing","duplicate","nonsimple","wrong_route","wrong_path"]:
        changed=copy.deepcopy(rows)
        if name=="missing": changed.pop()
        elif name=="duplicate": changed[-1]=copy.deepcopy(changed[0])
        elif name=="nonsimple": changed[0]["parameters"]=["S",4,2]
        elif name=="wrong_route": changed[0]["source_clause"]="physical page 8"
        else: changed[0]["relative_pair"]="elsewhere/pair.g"
        try: roster(changed)
        except ValueError as e: malformed.append(dict(control=name,message=str(e)))
        else: raise ValueError("Malformed source roster accepted")
    save(negatives/"source_controls.json",malformed)
    guards=[]
    for script in ["check.py","literal.py"]:
        for mode in ["argument","environment"]:
            dest=negatives/(script+"_"+mode)
            env=os.environ.copy();env.pop("PYTHONOPTIMIZE",None)
            cmd=[sys.executable]
            if mode=="argument": cmd.append("-O")
            else: env["PYTHONOPTIMIZE"]="1"
            cmd += [str(BASE/script),"--study",str(args.study),"--out",str(dest)]
            p=subprocess.run(cmd,capture_output=True,env=env,timeout=15)
            need(p.returncode!=0 and p.stderr.decode().strip()=="Run without Python optimization." and not dest.exists(),"Explicit pre-output optimization guard")
            guards.append(dict(script=script,mode=mode,returncode=p.returncode,stderr=p.stderr.decode().strip(),no_output=True))
    save(negatives/"optimization.json",guards)
    rendering=native(args.out/"native") if args.render else None
    summary=dict(status="PASS_FINITE_LIE_WITNESSES",scope=scope,exports=len(manifest["exports"]),bindings=len(dependencies),literal_cases=len(literal),fresh_GAP_cases=len(results),negative_GAP_controls=len(controls),source_controls=len(malformed),optimization_guards=len(guards),native=rendering,whole_original_credit=0,measurement=None)
    save(args.out/"report.json",summary);print(json.dumps(summary))


if __name__=="__main__": main()
