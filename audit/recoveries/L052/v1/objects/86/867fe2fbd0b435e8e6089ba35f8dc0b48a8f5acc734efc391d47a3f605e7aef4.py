"""Check the literal links between presentation receipts and model scripts."""
import sys
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')
import argparse, ast, json, re
from pathlib import Path

def need(ok,msg):
    if not ok: raise ValueError(msg)

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    base=Path(__file__).resolve().parent
    data=json.loads((base/'literal_inputs.json').read_text());rows=data['tables']
    # The full model scripts are generated from these precise groups.
    model=(base/'structures.g').read_text()
    arrays=re.findall(r'^G:=Group\(List\((\[.*?\]),PermList\)\);;',model,re.M)
    need(len(arrays)==23,'exact named-model roster')
    for row,raw in zip(rows,arrays):
        need(ast.literal_eval(raw)==row['full'],'named-model literal group '+row['id'])
    rel=(base/'relationships.g').read_text()
    for row in rows:
        key=row['id'].replace('.','_')
        for label,field in [('Rotations','rotation'),('FullMarks','full')]:
            found=re.findall(re.escape(label+'.'+key)+r':=List\((\[.*?\]),PermList\)',rel)
            need(len(found)==1 and ast.literal_eval(found[0])==row[field],'halving literal input '+label+key)
        folder=base/('table1_author' if row['id'].startswith('T1.') else 'table2_author')/row['id']
        old=(folder/'stdout.log').read_text()
        for label,field in [('ROTATION_GENERATORS','rotation'),('FULL_GENERATORS','full')]:
            need(old.count('\n'+label+' ')==1,'unique original array '+label)
            raw=old.split('\n'+label+' ',1)[1];start=raw.index('[');depth=0;end=None
            for i,c in enumerate(raw[start:],start):
                if c=='[':depth+=1
                elif c==']':
                    depth-=1
                    if depth==0:end=i+1;break
            need(end is not None and ast.literal_eval(raw[start:end])==row[field],'original exact-presentation receipt '+row['id'])
        need(old.splitlines()[-1]=='PASS_L052_ROW '+row['id'],'complete original presentation receipt')
    result={'status':'PASS_LITERAL_INPUT_LINKS','named_models':23,'halving_arrays':46,'presentation_arrays':46}
    a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

if __name__=='__main__':main()
