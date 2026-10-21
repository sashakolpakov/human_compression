#!/usr/bin/env python3
"""Independent semantic and actual vector mutations; no author helper imports."""
import argparse,copy,json,tempfile,shutil
from pathlib import Path
import check as c

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);a=ap.parse_args()
    c.need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
    r=c.load(a.candidate/'results.json');old=c.load(a.candidate/'inputs/previous_results.json');f=c.load(a.candidate/'inputs/F_results.json');cat=c.load(a.candidate/'inputs/current_corpus.json')
    controls=[]
    def reject(name,fn):
        try:fn()
        except (RuntimeError,KeyError) as e:controls.append({'control':name,'rejected':True,'reason':str(e)});return
        raise RuntimeError('UNDETECTED MUTATION: '+name)
    def model(name,change):
        rr=copy.deepcopy(r);change(rr);reject(name,lambda:c.check_results(rr,old,f,cat))
    find=lambda x,k:next(t for t in x['topics'] if t['topic']==k)
    model('omit whole common from denominator',lambda x:find(x,'F').update(written_denominator=27398,written=c.ratio(69825,27398)))
    model('change complete source sum',lambda x:find(x,'F').update(source_sum=69826))
    model('stale selected L014 source coordinate',lambda x:find(x,'F')['pairs'][0].update(source_cost=25115,conditional=c.ratio(25115,11504)))
    model('conditional quietly includes common',lambda x:find(x,'F')['pairs'][1].update(conditional=c.ratio(44251,15894+15876)))
    model('count L014 twice instead of L007',lambda x:find(x,'F')['pairs'][1].update(source='L014'))
    model('asymmetric software factor restored',lambda x:find(x,'F').update(including_printed_programs=c.ratio(69825,43274+22466)))
    model('unknown source software set to zero',lambda x:find(x,'F').update(historical_software_cost=0))
    model('claim full Lean source formalization',lambda x:find(x,'F').update(full_source_formalized=True))
    model('misclassify F validation as proof premise',lambda x:find(x,'F').update(program_roles='Nine required proof programs.'))
    model('double F optional appendix in inventory',lambda x:find(x,'F').update(optional_validation_printed=44932))
    model('silently remove required old E program',lambda x:find(x,'E').update(printed_program_cost=0))
    model('discard N006 companion',lambda x:find(x,'Operations')['application_components']['DG2'].pop(next(iter(find(x,'Operations')['application_components']['DG2']))))
    model('invent program-free screening for old topics',lambda x:find(x,'A').update(embedded_validation_listings_screened=True))
    model('claim pooled comparison',lambda x:x.update(pooled_factor=c.ratio(2,1)))
    model('wrong active catalogue count',lambda x:x.update(active_originals=105))
    model('omit last source application',lambda x:x['topics'][-1]['pairs'].pop())
    specs=c.expected_specs(r);key='whole_topics';src=(a.candidate/(key+'.svg')).read_text()
    # Alter one actual source path while leaving metadata and labels unchanged.
    import re
    marker='id="bar-F-source"';pos=src.index(marker);pathpos=src.index('d="',src.index('<path',pos))+3;end=src.index('"',pathpos);nums=list(re.finditer(r'[-+]?(?:\d*\.\d+|\d+)(?:e[-+]?\d+)?',src[pathpos:end]))
    m=nums[2];start=pathpos+m.start();stop=pathpos+m.end();bad=src[:start]+str(float(m.group())+5)+src[stop:]
    p=a.out/'distorted.svg';p.write_text(bad);reject('distorted literal source SVG vertex',lambda:c.svg_geometry(p,specs[key]));p.unlink()
    # Change both right-hand vertices to preserve a rectangle but falsify its width.
    bad=src
    for m in reversed([nums[2],nums[4]]):
        start=pathpos+m.start();stop=pathpos+m.end();bad=bad[:start]+str(float(m.group())+5)+bad[stop:]
    p.write_text(bad);reject('rectangular SVG bar wrong numerical width',lambda:c.svg_geometry(p,specs[key]));p.unlink()
    # Delete the exact F stacked common path group.
    bad=re.sub(r'<g id="bar-F-common-whole_common">.*?</g>','',src,count=1,flags=re.S);c.need(bad!=src,'mutate actual common path');p.write_text(bad);reject('missing actual common-theory bar',lambda:c.svg_geometry(p,specs[key]));p.unlink()
    proto=c.load(a.candidate/'protocol.json');cats=[c.load(a.public_root/proto['external_catalogue_bindings'][k]['path'])for k in ['previous','current']]
    badcat=copy.deepcopy(cats[1]);target=next(e for e in badcat['entries']if e['original_id'] not in ['L014','L007']);target['unexpected_review_mutation']=True
    reject('unrelated accessible original changed',lambda:c.check_catalogues(cats[0],badcat))
    badcat=copy.deepcopy(cats[1]);badcat['entries'].pop();reject('active original silently dropped',lambda:c.check_catalogues(cats[0],badcat))
    rr=copy.deepcopy(r);find(rr,'F')['pairs'][1]['application_cost']+=1
    reject('reader fails a wrong application integer',lambda:c.check_reader(a.candidate/'summary.pdf',rr))
    fixture=a.out/'csv_fixture';fixture.mkdir()
    for name in ['topics.csv','applications.csv','program_inventory.csv']:shutil.copy2(a.candidate/name,fixture/name)
    p=fixture/'program_inventory.csv';original=p.read_text();p.write_text(original.replace('unknown','0',1));reject('CSV unknown software becomes zero',lambda:c.check_csv(fixture,r));p.write_text(original)
    p=fixture/'applications.csv';original=p.read_text();lines=original.splitlines();p.write_text('\n'.join(lines[:-1])+'\n');reject('CSV omits one complete application',lambda:c.check_csv(fixture,r));p.write_text(original)
    shutil.rmtree(fixture)
    result={'status':'PASS','controls':controls,'count':len(controls),'author_helpers_imported':False}
    (a.out/'controls.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
