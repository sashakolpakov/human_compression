"""Reviewer-only exact GAP-record / literal-input / printed-table join."""
import sys
if sys.flags.optimize:
    raise SystemExit('optimized review unsupported')
import argparse, collections, hashlib, json, os, pathlib, subprocess

def need(value, message):
    if not value:
        raise ValueError(message)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--packet',type=pathlib.Path,required=True)
    ap.add_argument('--out',type=pathlib.Path,required=True)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=False)
    source=json.loads((a.packet/'source_map.json').read_text())
    driver=a.out/'export_records.g'
    output=a.out/'records.json'
    text=['hyperbolic_records:=[];;',
          's:=OutputTextFile('+json.dumps(str(output))+',false);;',
          'SetPrintFormattingStatus(s,false);;', 'PrintTo(s,"[\\n");;', 'first:=true;;']
    for typ in source['types']:
        text += ['Read('+json.dumps(str(a.packet/'censuses'/typ/'records.g'))+');;',
                 'for r in hyperbolic_records do',
                 'if not first then PrintTo(s,",\\n");fi;first:=false;',
                 'PrintTo(s,"[\\"'+typ+'\\",",r.node,",",r.order,",",r.permutations,"]");',
                 'od;']
    text += ['PrintTo(s,"\\n]\\n");;','CloseStream(s);;','QUIT;']
    driver.write_text('\n'.join(text)+'\n')
    r=subprocess.run(['/opt/homebrew/bin/gap','-q','-b','--quitonbreak',str(driver)],capture_output=True,text=True,timeout=30)
    (a.out/'stdout').write_text(r.stdout);(a.out/'stderr').write_text(r.stderr)
    need(r.returncode==0 and not r.stderr.strip() and not r.stdout.strip(),'unclean literal export')
    raw=json.loads(output.read_text())
    positives=json.loads((a.packet/'positives.json').read_text())
    key=lambda r: json.dumps(r,separators=(',',':'))
    need(collections.Counter(map(key,raw))==collections.Counter(key([r['type'],r['node'],r['order'],r['permutations']]) for r in positives),'literal inputs differ from actual positive census records')
    table=[]
    for typ,d in source['types'].items():
        rows=[r for r in positives if r['type']==typ]
        need(len(rows)==d['positive_kernels'],'positive multiplicity mismatch')
        need(min(r['order'] for r in rows)==d['broad_minimum'],'broad minimum mismatch')
        univ=[r['order'] for r in rows if r['local_orders']==d['universal_local_orders']]
        need((min(univ) if univ else None)==d['universal_minimum'],'universal minimum mismatch')
        table.append({'type':typ,'positive_count':len(rows),'broad_minimum':d['broad_minimum'],'universal_minimum':d['universal_minimum']})
    neg=json.loads((a.packet/'negatives.json').read_text())
    need(collections.Counter((r['type'],r['order']) for r in neg)=={('3434',336):3,('3534',360):1,('3534',2160):1},'negative inventory mismatch')
    report={'status':'PASS','literal_positive_joins':len(raw),'negative_inventory':len(neg),'table':table,'scope':'Input identity and table arithmetic only; no new algebra or census.'}
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__=='__main__':main()
