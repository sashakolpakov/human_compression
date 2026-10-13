#!/usr/bin/env python3
"""Required small, complete centralizer-template check; no marking census."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,tempfile,time,ast
ROOT=Path(__file__).resolve().parent
def need(x,message):
    if not x:raise ValueError(message)
def parse(log):
    yes=[];no=[];end=None
    for line in log.splitlines():
        if line.startswith('TEMPLATE|'):
            s=line.split('|');yes.append({'row':int(s[1]),'dual':s[2]=='true','degree':int(s[3]),'endpoint':int(s[4]),'attachment_vertices':ast.literal_eval(s[5]),'auxiliary_vertices':ast.literal_eval(s[6]),'centralizer_order':int(s[7]),'centralizer_on_attachment':int(s[8]),'auxiliary_group_order':int(s[9]),'last_two_group_order':int(s[10]),'centralizer_elements':ast.literal_eval(s[11])})
        elif line.startswith('NO_ENDPOINT|'):
            s=line.split('|');no.append({'row':int(s[1]),'dual':s[2]=='true'})
        elif line.startswith('COMPLETE_TEMPLATES|'):end=[int(x)for x in line.split('|')[1:]]
    need(end==[12,14] and len(yes)==12 and len(no)==14,'complete template boundary')
    need({(r['row'],r['dual'])for r in yes+no}=={(i,d)for i in range(4,17)for d in (False,True)},'all orientations')
    for r in yes:
        need(r['last_two_group_order']<60,'A5 obstruction')
        need(r['centralizer_on_attachment']<=2 and (r['degree']!=11 or r['centralizer_on_attachment']==1),'normal-orbit range')
        need(r['auxiliary_group_order']<=2,'central decoration')
    return {'templates':yes,'no_endpoint':no}
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');p.add_argument('--gap',default='/opt/homebrew/bin/gap');a=p.parse_args();a.out.mkdir(exist_ok=False,parents=True)
    if (ROOT/'manifest.json').exists():
        for r in json.loads((ROOT/'manifest.json').read_text())['exports']:
            b=(ROOT/r['path']).read_bytes();need(len(b)==r['bytes']and hashlib.sha256(b).hexdigest()==r['sha256'],'export '+r['path'])
    rows=json.loads((ROOT/'source_table2.json').read_text())['rows'];need([r['source_row']for r in rows]==list(range(1,17)),'literal row set')
    t=time.monotonic()
    with tempfile.TemporaryDirectory(prefix='L044_templates_')as w:
        w=Path(w);shutil.copyfile(ROOT/'templates.g',w/'templates.g')
        (w/'literal_rows.g').write_text('L044SourceRows:=[\n'+',\n'.join('rec(id:=%d,n:=%d,gens:=%s)'%(r['source_row'],r['degree'],str(r['generators']))for r in rows)+'\n];;\n')
        r=subprocess.run([a.gap,'-q','-b','templates.g'],cwd=w,capture_output=True,timeout=20)
    log=(r.stdout+r.stderr).decode();(a.out/'templates.log').write_text(log);need(r.returncode==0 and 'Error,'not in log and 'Syntax error'not in log,'GAP failure')
    data=parse(log);(a.out/'templates.json').write_text(json.dumps(data,indent=2)+'\n')
    controls=[]
    for label,bad in [('missing_end',log.replace('COMPLETE_TEMPLATES|','WRONG|')),('missing_orientation','\n'.join(x for x in log.splitlines()if not x.startswith('NO_ENDPOINT|8|true')))]:
        try:parse(bad)
        except ValueError:controls.append(label)
        else:raise ValueError('control '+label)
    render=None
    if a.render:
        from pypdf import PdfReader
        w=a.out/'render';w.mkdir();shutil.copyfile(ROOT/'small_attachments.tex',w/'small_attachments.tex')
        for k in range(2):
            r=subprocess.run(['/opt/homebrew/bin/xelatex','-interaction=nonstopmode','-halt-on-error','small_attachments.tex'],cwd=w,capture_output=True,timeout=45);(a.out/f'render{k}.log').write_bytes(r.stdout+r.stderr);need(r.returncode==0,'render')
        old=[p.extract_text()for p in PdfReader(ROOT/'small_attachments.pdf').pages];new=[p.extract_text()for p in PdfReader(w/'small_attachments.pdf').pages];need(old==new,'page texts');render={'pages':len(new),'page_texts_equal':True}
    report={'status':'PASS','full_template_orientations':26,'positive_templates':12,'no_endpoint':14,'controls':controls,'elapsed_seconds':time.monotonic()-t,'render':render,'no_marking_census_or_formal_rerun':True};(a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
