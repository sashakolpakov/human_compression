#!/usr/bin/env python3
"""Replay a private exact documentation stage; never modify the public checkout."""
from pathlib import Path
import argparse,ast,copy,hashlib,importlib.util,io,json,re,shutil,subprocess,sys
from docutils.core import publish_parts
from pypdf import PdfReader
H=Path(__file__).resolve().parent

def need(x,m):
    if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def bound(p,r):
    b=p.read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'exact '+str(p));return b
def imp(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');a=ap.parse_args()
    repo=a.repo.resolve();out=a.out.resolve();need(not out.exists() and not out.is_relative_to(repo),'fresh private output, not public');out.mkdir(parents=True)
    if (H/'manifest.json').exists():
        for r in load(H/'manifest.json')['exports']:bound(H/r['path'],r)
    base=load(H/'baseline.json');need(base['commit']=='f0633645938bea9861d07500d86f70f7696a8e22','confirmed committed baseline')
    for r in base['files']:bound(H/'baseline'/r['path'],r)
    plan=load(H/'copy_plan.json')['files'];need(len(plan)==10,'exact ten mapped files')
    routes={r['public_path']:H/r['proposal_path'] for r in plan};need(len(routes)==10,'unique map')
    for r in plan:bound(H/r['proposal_path'],r)
    for r in load(H/'admission_template.json')['accepted_programme']:bound(repo/r['path'],r)
    # Temporary overlay: exact new docs plus separately saved old bytes. All other files are read-only links.
    stage=out/'stage';stage.mkdir();special=set(routes)|{'scripts/verify_snapshot.py','audit/documentation/v1/admission.json'}
    def populate(src,dst,prefix=''):
        dst.mkdir(exist_ok=True)
        for child in src.iterdir():
            rel=prefix+child.name;target=dst/child.name
            if rel in special:continue
            if any(k.startswith(rel+'/')for k in special):populate(child,target,rel+'/')
            else:target.symlink_to(child,target_is_directory=child.is_dir())
    populate(repo,stage)
    for name,source in routes.items():
        target=stage/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
    source=(H/'baseline/scripts/verify_snapshot.py').read_text();old_ast={n.name:sha(ast.dump(n,include_attributes=False).encode())for n in ast.parse(source).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name!='main'}
    need(old_ast==base['nonmain_verifier_functions'],'exact128 starting functions')
    live_ast={n.name:sha(ast.dump(n,include_attributes=False).encode())for n in ast.parse((repo/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name!='main'}
    need(all(live_ast.get(k)==v for k,v in old_ast.items()),'all128 public historical ASTs unchanged')
    fragment=(H/'proposed/integration/new_guard_functions.py').read_text()
    need(source.count('    programme51 = check_programme51()')==1,'exact main call')
    migrated=source.replace('    programme51 = check_programme51()','    programme51 = check_programme51_documentation_history()\n    documentation51 = check_current_documentation()')
    need(migrated.count('\ndef main():')==1,'one main')
    migrated=migrated.replace('\ndef main():','\n'+fragment+'\n\ndef main():',1)
    actual={n.name:sha(ast.dump(n,include_attributes=False).encode())for n in ast.parse(migrated).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name!='main'}
    need(all(actual.get(k)==v for k,v in old_ast.items())and len(actual)==130,'old128 ASTs exact; two new functions')
    (stage/'scripts/verify_snapshot.py').write_text(migrated)
    admission=load(H/'admission_template.json');admission['status']='PRIVATE_TEST_DOCUMENTATION_STAGE';(stage/'audit/documentation/v1/admission.json').write_text(json.dumps(admission,indent=2)+'\n')
    guard=imp(stage/'scripts/check_current_documentation.py','documentation_candidate_guard');result=guard.verify(stage,allow_proposal=True)
    # Historical guard invoked through only the new read-only three-document overlay.
    verifier=imp(stage/'scripts/verify_snapshot.py','documentation_candidate_snapshot')
    historical=verifier.check_programme51_documentation_history();need(historical['recovered']==51,'prior programme51 replay')
    # RST syntax and table output, without adding HTML as a public document.
    warnings=io.StringIO();parts=publish_parts(source=(H/'replacements/README.rst').read_text(),writer_name='html5',settings_overrides={'warning_stream':warnings,'halt_level':2,'report_level':2})
    need(not warnings.getvalue(),'RST diagnostics: '+warnings.getvalue());need(parts['html_body'].count('<tr>')==20,'header plus19 current topic rows')
    (out/'README.html').write_text(parts['whole'])
    render=None
    if a.render:
        build=out/'render_source';(build/'scripts').mkdir(parents=True);(build/'papers').mkdir();(build/'audit').mkdir()
        for rel,src in [('scripts/build_papers.py',H/'baseline/scripts/build_papers.py'),('papers/catalogue.json',H/'baseline/papers/catalogue.json'),('audit/protocol.tex',H/'replacements/audit/protocol.tex')]:shutil.copyfile(src,build/rel)
        proc=subprocess.run([sys.executable,'-B',build/'scripts/build_papers.py','--paper','audit/protocol','--output-dir',out/'render'],capture_output=True,text=True)
        (out/'render.stdout').write_text(proc.stdout);(out/'render.stderr').write_text(proc.stderr);need(proc.returncode==0,'canonical protocol render')
        render=load(out/'render/report.json');need(not render['papers'][0]['diagnostics'],'empty TeX diagnostics')
        old=[p.extract_text()or''for p in PdfReader(H/'replacements/audit/protocol.pdf').pages];new=[p.extract_text()or''for p in PdfReader(out/'render/audit/protocol/paper.pdf').pages];need(old==new and len(new)==4,'four exact protocol pages')
    readme=(H/'replacements/README.rst').read_text();tex=(H/'replacements/audit/protocol.tex').read_text();table=load(H/'topic_table.json')['topics'];controls=[]
    def reject(label,rt=readme,tx=tex,tab=None):
        try:guard.validate_text(rt,tx,table if tab is None else tab)
        except ValueError:controls.append(label);return
        raise ValueError('accepted documentation mutation '+label)
    reject('stale_measured_count',rt=readme.replace('51 accessible originals','50 accessible originals'))
    reject('lost_pending_status',rt=readme.replace('54 await mathematical recovery','55 await mathematical recovery'))
    reject('old_overview_route',rt=readme.replace('audit/overview/v17/packet/reader.pdf','audit/overview/v16/packet/reader.pdf'))
    reject('asymmetric_program_statement',rt=readme.replace('Executable software is excluded symmetrically','Only replacement software is excluded'))
    reject('lost_software_unknown',rt=readme.replace('there is no software-inclusive factor','a software-inclusive factor is reported'))
    reject('pooled_factor',rt=readme.replace('there is no pooled factor','there is a pooled factor'))
    reject('lost_expansion_label',rt=readme.replace('expansion','saving'))
    bad=copy.deepcopy(table);bad[0]['display']='1.999999';reject('changed_primary_factor',tab=bad)
    reject('dropped_topic',tab=table[:-1])
    bad=copy.deepcopy(table);bad[1]['original_ids'][0]=bad[0]['original_ids'][0];reject('original_counted_twice',tab=bad)
    reject('old_one_sided_formula',tx=tex+'\nR_A^{\\rm required}\n')
    reject('old_current_version',tx=tex+'\nThe current report: audit/overview/v3/\n')
    reject('complete_formalization',tx=tex.replace('Successful compilation and declaration counts do not establish complete source','Successful compilation establishes complete source'))
    need(sha((stage/'README.rst').read_bytes())!=sha((stage/'audit/documentation/v1/previous/README.rst').read_bytes()),'history overlay is necessary')
    report=dict(status='PASS_PRIVATE_CURRENT_DOCUMENTATION_PROPOSAL',base_commit=base['commit'],guard=result,
                historical_programme_guard=historical,unchanged_old_functions=128,new_functions=2,
                current_document_files=3,historical_document_files=3,topic_rows=19,comparison_values_reused=70,
                readme_bytes=(H/'replacements/README.rst').stat().st_size,previous_readme_bytes=(H/'baseline/README.rst').stat().st_size,
                protocol_pages=4,protocol_rendered=bool(a.render),RST_diagnostics=[],negative_controls=controls,
                full_snapshot_run=False,new_source_or_mathematical_or_numerical_work=False,public_writes=False)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
