#!/usr/bin/env python3
"""Fresh exact GAP replay of the rewritten common theorem and its controls.
No Markdown, historical runner, sampled uniform theorem or Lean-completeness claim.
"""
import argparse,hashlib,json,re,shutil,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def need(ok,message):
    if not ok:raise ValueError('TOPIC_E_COMMON_REJECT '+message)
def sha(data):return hashlib.sha256(data).hexdigest()
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--gap',default=shutil.which('gap'));a=ap.parse_args()
    need(a.gap is not None,'GAP required');need(not a.out.exists() and not a.out.is_symlink(),'fresh output required')
    a.out.mkdir(parents=True);out=a.out.resolve();start=time.monotonic();report={}
    def run(label,source,positive,sentinel):
        target=out/(label+'.g');target.write_bytes(source);now=time.monotonic()
        p=subprocess.run([a.gap,'-q','-b',str(target)],cwd=out,text=True,capture_output=True,timeout=120)
        (out/(label+'.stdout')).write_text(p.stdout);(out/(label+'.stderr')).write_text(p.stderr)
        errors=bool(re.search(r'Error|Syntax error|Syntax warning|brk>',p.stdout+p.stderr))
        success=p.returncode==0 and sentinel in p.stdout and not errors
        need(success if positive else not success,label+' acceptance/rejection')
        row=dict(status='PASS' if positive else 'REJECTED_AS_REQUIRED',source_sha256=sha(source),exit_code=p.returncode,
          stdout_sha256=sha(p.stdout.encode()),stderr_sha256=sha(p.stderr.encode()),seconds=round(time.monotonic()-now,6))
        report[label]=row;return p.stdout
    required=(ROOT/'required_finite.g').read_bytes();validation=(ROOT/'validation.g').read_bytes()
    text=run('required',required,True,'TOPIC_E_REQUIRED_FINITE_PASS')
    need(re.findall(r'RANK3 (\d+) MARKINGS (\d+)',text)==[('24','72'),('60','360')],'complete 432 local markings')
    rows=re.findall(r'ROW (\d+) ORDER (\d+) IP (true|false)',text)
    need(rows==[(str(i),str(o),v) for i,o,v in [(1,1,'false'),(2,1,'false'),(3,3420,'true'),(4,60,'false'),(5,1,'false'),(6,96,'true'),(7,24,'false'),(8,660,'true'),(9,1,'false'),(10,120,'true')]],'all ten universal rows')
    for marker in ['SOURCE_L33_COUNTEREXAMPLE','OMITTED_S4 PSL23','SELFDUAL_CLASS1 PSL13']:
        need(text.count(marker)==1,'literal correction '+marker)
    sample=run('validation',validation,True,'TOPIC_E_VALIDATION_PASS')
    need(re.findall(r'CONSTANT_FAMILY (\d+)',sample)==['13','37','61'],'constant diagnostic fields')
    need(re.findall(r'PROPER_END_FAMILY (\d+)',sample)==['41','47','73'],'proper-end diagnostic fields')
    for control in ['ALLOW_IDENTITY','DIHEDRAL_NON_C_SGGI_CONTROL','NO_STRING']:
        need(control in sample,'false-weakening validation '+control)
    mutations=[('wrong_universal_order',required,b'[[5,3,5],[3,5,5],3420,true',b'[[5,3,5],[3,5,5],3421,true','TOPIC_E_REQUIRED_FINITE_PASS'),
       ('wrong_local_total',required,b'expected:=72;',b'expected:=71;','TOPIC_E_REQUIRED_FINITE_PASS'),
       ('wrong_outer_parity',required,b'Order(rr[1]*rr[2])=4 and Order(rr[3]*rr[4])=4',b'Order(rr[1]*rr[2])=3 and Order(rr[3]*rr[4])=3','TOPIC_E_REQUIRED_FINITE_PASS'),
       ('wrong_reversal',required,b'dual:=(1,3)(2,9)(4,7)(5,8)(6,12)(10,11)(13,14);',b'dual:=();','TOPIC_E_REQUIRED_FINITE_PASS'),
       ('allow_identity',validation,b'not ForAll(rr,x->Order(x)=2)',b'not ForAll(rr,x->x*x=())','TOPIC_E_VALIDATION_PASS')]
    for label,data,old,new,sentinel in mutations:
        need(data.count(old)==1,'unique semantic mutation '+label)
        run(label,data.replace(old,new),False,sentinel)
    result=dict(status='PASS',seconds=round(time.monotonic()-start,6),programs={'required_finite.g':sha(required),'validation.g':sha(validation)},
       checker_sha256=sha(Path(__file__).read_bytes()),runs=report,
       mathematical_scope='All432 string triples (IP is output), six local presentations, ten universal groups/markings including exact order96 parity, complete geometry, three literal source-correction witnesses.',
       validation_scope='Finite samples with exact source conjugacy and false-weakening controls. These do not prove any quantified prime family.',
       trust='GAP exact finite-group and finite-presentation algorithms; no complete Lean certificate.',
       scientific_claim_change='Reuses existing results and corrections; no source or question intake.')
    (out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','seconds':result['seconds'],'controls':len(mutations)},indent=2))
if __name__=='__main__':main()
