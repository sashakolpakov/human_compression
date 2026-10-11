#!/usr/bin/env python3
"""Fresh finite/formal/render replay for the complete matching-extension edition."""
import argparse,hashlib,json,os,pathlib,re,subprocess,time,sys
ROOT=pathlib.Path(__file__).resolve().parent

def need(b,s):
    if not b:raise RuntimeError("MATCHING_REJECT "+s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for key in ['out','gap','lean','packages']:ap.add_argument('--'+key,type=pathlib.Path,required=True)
    ap.add_argument('--study-root',type=pathlib.Path)
    ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='xelatex')
    a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh raw output')
    out=a.out.resolve();need(not out.exists(),'fresh resolved output');out.mkdir(parents=True)
    start=time.monotonic();m=ROOT/'manifest.json';bindings=[]
    if m.exists():bindings=json.loads(m.read_text())['exports']
    def verify():
        for row in bindings:
            rel=pathlib.PurePosixPath(row['path']);need(not rel.is_absolute() and '..' not in rel.parts,'safe bound path')
            q=ROOT/rel;need(q.is_file() and q.stat().st_size==row['bytes'] and sha(q)==row['sha256'],'frozen file '+str(rel))
    verify();contract=json.loads((ROOT/'contract.json').read_text())
    if a.study_root:
        row=contract['primary'];q=a.study_root/row['path'];need(q.stat().st_size==row['bytes'] and sha(q)==row['sha256'],'primary binding')
    ledger=json.loads((ROOT/'source_clause_map.json').read_text())
    need(len(ledger['rows'])==32 and len({r['id'] for r in ledger['rows']})==32,'exact32source clauses')
    need(contract['source_id']=='F015' and contract['question_delta']==0 and contract['principal_credit_delta']==0,'candidate scope')
    for key,row in ledger['proof_spans'].items():
        raw=b''.join((ROOT/row['path']).read_bytes().splitlines(keepends=True)[row['start_line']-1:row['end_line']])
        need(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'complete proof span '+key)
    scope=json.loads((ROOT/'formal/scope.json').read_text());need(scope['declarations']==7 and scope['new_declarations']==0 and scope['all_reused'] is True,'formal boundary')
    runs = []
    def run(label, cmd, env=None):
        before = time.monotonic()
        p = subprocess.run([str(v) for v in cmd], cwd=out, env=env, text=True,
                           capture_output=True, timeout=180)
        o, e = out / (label + ".stdout"), out / (label + ".stderr")
        o.write_text(p.stdout); e.write_text(p.stderr)
        runs.append(dict(label=label, returncode=p.returncode, seconds=round(time.monotonic()-before, 4),
                         stdout_sha256=sha(o), stderr_sha256=sha(e)))
        return p
    p = run("gap_version", [a.gap, "-q", "-T", "-c", 'Print(GAPInfo.Version,"\\n");QUIT;'])
    need(p.returncode == 0 and p.stdout.strip() == "4.15.1", "GAP version")
    p = run("orbit_census", [a.gap, "-q", "-T", ROOT / "programs/exceptional_orbits.g"])
    need(p.returncode == 0 and not re.search("Error|warning", p.stdout+p.stderr, re.I), "clean full orbit census")
    output = p.stdout.replace("\\\n", "")
    need("PHASE278_EXCEPTIONAL_CENSUS_PASS five_actions all_pairs exact35_with20_missing" in output, "exact census completion")
    rows = [json.loads(line.split("PHASE278_ROW ", 1)[1]) for line in output.splitlines() if "PHASE278_ROW " in line]
    need(len(rows) == 5 and [len(x["unordered_orbit_sizes"]) for x in rows] == [3,5,4,8,35], "five full orbit counts")
    need(rows[-1]["missing_orbits"] == 20 and rows[-1]["burnside_numerator"] == 504000, "actual120-cell discrepancy")
    missing = [json.loads(line.split("PHASE278_MISSING_WORDS ", 1)[1]) for line in output.splitlines() if "PHASE278_MISSING_WORDS " in line]
    need(len(missing) == 1 and len(missing[0]) == 20, "twenty explicit short representatives")
    (out / "census.json").write_text(json.dumps(dict(rows=rows, missing_words=missing[0]), indent=2)+"\n")
    text = (ROOT / "programs/exceptional_orbits.g").read_text()
    for label, old, new, rejection in [
        ("false_fifteen", "Length(orbs)=35", "Length(orbs)=15", "120-cell full census is35"),
        ("missing_word_mutation", "[-3,3,-1,3600]", "[0,0,0,3600]", "missing orbit new and distinct")]:
        need(text.count(old) == 1, "unique finite mutation location " + label)
        bad = out / (label + ".g"); bad.write_text(text.replace(old, new))
        p = run(label, [a.gap, "-q", "-T", bad])
        need("PHASE278_REJECT " + rejection in p.stdout+p.stderr and "PHASE278_EXCEPTIONAL_CENSUS_PASS" not in p.stdout,
             "finite false claim rejected " + label)

    deps = json.loads((ROOT / "formal/dependency_manifest.json").read_bytes()); checked = []
    for row in deps["packages"]:
        folder = a.packages / row["name"]
        rev = subprocess.check_output(["git", "-C", folder, "rev-parse", "HEAD"], text=True).strip()
        need(rev == row["rev"], "dependency revision " + row["name"])
        need(subprocess.run(["git", "-C", folder, "diff", "--quiet", "HEAD", "--"]).returncode == 0, "clean dependency")
        checked.append(dict(name=row["name"], rev=rev))
    version = subprocess.check_output([a.lean, "--version"], text=True).strip()
    need("version 4.32.2," in version, "Lean version")
    env = dict(os.environ)
    env["LEAN_PATH"] = os.pathsep.join(str(p / ".lake/build/lib/lean") for p in a.packages.iterdir()
                                       if (p / ".lake/build/lib/lean").is_dir())
    text = (ROOT / "formal/OrbitPresentationWords.lean").read_text()
    need(not re.search(r"\b(sorry|admit|native_decide)\b|^\s*axiom\s", text, re.M), "formal proof-hole scan")
    target = out / "OrbitPresentationWords.lean"; target.write_text(text)
    p = run("formal", [a.lean, "-o", out / "OrbitPresentationWords.olean", target], env)
    need(p.returncode == 0 and not re.search("error:|warning:|sorryAx", p.stdout+p.stderr), "clean formal compilation")
    need(p.stdout.count("depends on axioms: [propext]") == 5 and p.stdout.count("depends on axioms: [propext, Classical.choice, Quot.sound]") == 2,
         "seven exact axiom reports")
    for label, old, new in [
        ("false_conjugate", "= (a * w⁻¹ * a * w)⁻¹ := by", "= (a * w⁻¹ * a * w) := by"),
        ("false_power", "omittedBlock ^ n ≠ 1 := by", "omittedBlock ^ n = 1 := by")]:
        need(text.count(old) == 1, "unique formal mutation location " + label)
        bad = out / (label + ".lean"); bad.write_text(text.replace(old, new))
        p = run(label, [a.lean, bad], env)
        need(p.returncode != 0 and "error:" in p.stdout+p.stderr, "false formal conclusion rejected " + label)
    render_report=None
    if a.render:
        p=run('render',[sys.executable,ROOT/'build.py','--out',out/'render','--xelatex',a.xelatex])
        need(p.returncode==0,'complete current render')
        render_report=json.loads((out/'render/report.json').read_text())
    verify()
    report=dict(status='PASS',seconds=round(time.monotonic()-start,4),executions=runs,
        primary_checked=bool(a.study_root),bound_files_checked=len(bindings),source_clauses=32,proof_spans=len(ledger['proof_spans']),
        formal_declarations=7,new_formal_declarations=0,dependencies=checked,
        finite_census=dict(groups=5,unordered_orbits=[3,5,4,8,35],missing120cell=20),
        finite_controls=2,formal_controls=2,render=render_report,
        status_scope='Author candidate; distinct mathematical/source review required',new_source_credit=0,new_question_credit=0,ratio=None)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','seconds':report['seconds'],'report':str(out/'report.json')}))
if __name__=='__main__':main()
