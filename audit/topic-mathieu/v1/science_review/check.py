#!/usr/bin/env python3
"""Independent complete source-row/signature audit and actual orbit-set check."""
import argparse, collections, hashlib, itertools, json, re, subprocess
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
PIN = 'e70770940fe3db852b77a3e400bf913263eec6f1114e89d311f6d4e07b0dad57'

def need(v,m):
    if not v: raise ValueError(m)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text())
def norm(s): return ''.join(s.split())

def signatures(data,n):
    out = {}
    need(len(data['triples']) == n, 'full coordinate classes')
    for row in data['triples']:
        need(row['signatures'], 'nonempty coordinates')
        for sig in row['signatures']:
            key = tuple(sig)
            need(key not in out or out[key] == row['witness'], 'distinct classes share a signature')
            out[key] = row['witness']
    need(set(out.values()) == set(range(1,n+1)), 'all classes represented')
    return out

def complete_codes(h):
    seeds=read(h/'data/phase180_source_notation.json')['octad_seeds']
    masks=[sum(1<<j for j in s['support']) for s in seeds]
    basis={}
    for x in masks:
        while x:
            bit=x.bit_length()-1
            if bit in basis: x^=basis[bit]
            else: basis[bit]=x;break
    need(len(masks)==20 and len(basis)==10,'literal seed rank')
    need(all((u&v).bit_count()%2==0 for u in basis.values() for v in basis.values()),'self-orthogonal seed')
    def span(gens):
        s={0}
        for g in gens:s|={x^g for x in s}
        return s
    seed=span(basis.values());need((1<<24)-1 in seed,'all-one seed word')
    null=[]
    for free in set(range(24))-set(basis):
        v=1<<free
        for bit in sorted(basis):
            if (v&basis[bit]).bit_count()%2:v^=1<<bit
        need(all((v&r).bit_count()%2==0 for r in masks),'orthogonal basis vector')
        null.append(v)
    orthogonal=span(null);need(len(orthogonal)==16384 and seed<=orthogonal,'complete orthogonal space')
    remaining=set(orthogonal);cosets=[];which={};representatives=[]
    while remaining:
        v=min(remaining);c={v^x for x in seed};idx=len(cosets)
        need(c<=remaining,'coset partition');remaining-=c
        cosets.append(c);representatives.append(v);which.update({x:idx for x in c})
    need(len(cosets)==16 and representatives[0]==0,'four-dimensional quotient')
    planes={tuple(sorted({0,i,j,which[representatives[i]^representatives[j]]}))
            for i,j in itertools.combinations(range(1,16),2)}
    need(len(planes)==35 and all(len(p)==4 for p in planes),'all35 quotient planes')
    actual=[]
    for plane in planes:
        code=set().union(*(cosets[i] for i in plane))
        distribution=collections.Counter(x.bit_count() for x in code)
        if not set(distribution)<={0,8,12,16,24}:continue
        need(distribution=={0:1,8:759,12:2576,16:759,24:1},'exact code weights')
        blocks=frozenset(tuple(i for i in range(24) if x>>i&1) for x in code if x.bit_count()==8)
        fives=collections.Counter(t for b in blocks for t in itertools.combinations(b,5))
        need(len(fives)==42504 and set(fives.values())=={1},'actual Steiner design')
        actual.append(blocks)
    saved=read(h/'evidence/code_completions.json')['completions']
    expected={frozenset(map(tuple,c['blocks'])) for c in saved}
    need(len(actual)==4 and set(actual)==expected,'all four exact compatible labelled completions')
    return dict(seed_rank=10,orthogonal_rank=14,quotient_planes=35,compatible_codes=4,
                actual_Steiner_five_subsets_per_code=42504)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);ap.add_argument('--primary',type=Path)
    ap.add_argument('--gap',default='/opt/homebrew/bin/gap');a=ap.parse_args();h=a.packet
    need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
    need(sha(h/'manifest.json')==PIN,'correct author edition')
    exports=read(h/'manifest.json')['exports']
    for r in exports:
        name=Path(r['path']);need(not name.is_absolute() and '..' not in name.parts,'safe export')
        f=h/name;need(sha(f)==r['sha256'] and f.stat().st_size==r['bytes'],'unchanged whole export')
    literal=read(h/'data/phase164_L073_table_contract.json')['rows']
    source_checked=False
    if a.primary:
        need(sha(a.primary)=='595809bceeb03e663fa3c7b15219d6141d9fcbfce207fb5d4eab514e90f77341','exact source PDF')
        found=[]
        for page,p in enumerate(PdfReader(a.primary).pages,1):
            if page<3: continue
            for line in p.extract_text().splitlines():
                for m in re.finditer(r'(M\d{3}\([^)]*\))\s+(\d+)\s+(.+?)(?=\s+M\d{3}\(|$)',line):
                    found.append((page,norm(m[1]),int(m[2]),norm(m[3])))
        wanted=[(r['page'],norm(r['label_text']),r['source_number'],norm(r['Borel_text'])) for r in literal]
        need(found==wanted and len(found)==431,'all431 physical primary rows independently extracted')
        source_checked=True
    broad=read(h/'evidence/source_triples.json');canonical=read(h/'evidence/canonical_triples.json')
    bi=signatures(broad,431);ci=signatures(canonical,431)
    bp=signatures(read(h/'evidence/source_pairs.json'),81);cp=signatures(read(h/'evidence/canonical_pairs.json'),81)
    need((len(bi),len(ci),len(bp),len(cp))==(976,801,115,104),'exact complete signature counts')
    sizes={1:1,2:6,3:7,4:7,5:8,6:2,7:12,8:11};pairs=[(0,1),(0,2),(1,2)]
    for b,c in zip(broad['triples'],canonical['triples']):
        expanded=set()
        for s in c['signatures']:
            for flips in itertools.product([False,True],repeat=3):
                if any(flips[i] and s[i]!=8 for i in range(3)): continue
                t=list(s)
                for k,(i,j) in enumerate(pairs):
                    if flips[i] and flips[j]: t[3+k]=22-sizes[s[i]]-sizes[s[j]]+s[3+k]
                    elif flips[i]: t[3+k]=sizes[s[j]]-s[3+k]
                    elif flips[j]: t[3+k]=sizes[s[i]]-s[3+k]
                expanded.add(tuple(t))
        need(expanded==set(map(tuple,b['signatures'])) and b['borel_id']==c['borel_id'],'all independent complements')
    rec=read(h/'evidence/reconciliation.json');rows=rec['source_rows']
    need(len(rows)==431 and [r['row'] for r in rows]==list(range(1,432)),'whole row dispositions')
    for r,old in zip(rows,literal):
        need(all(r[k]==v for k,v in old.items()),'literal source fields retained')
        m=re.fullmatch(r'M(\d{3})\((.*)\)',r['label_text']);need(m,'literal label syntax')
        types=list(map(int,m[1]));terms=m[2].split(':')[0].split(',')
        values=[int(s.strip()[0]) for s in terms]
        for mode,index,orders in [('source_pair_order',bi,r['pair_orders_p112']),
                                  ('canonical_pair_order',ci,r['pair_orders_p112']),
                                  ('explicit_pair_objects',bi,r['literal_pair_orders_p114'])]:
            candidates=sorted({w for s,w in index.items() if list(s[:6])==types+values and
                               all(x is None or s[6+k]==x for k,x in enumerate(orders))})
            # Explicit configurations after a colon require actual transporter
            # evidence, while invalid literal pairs cannot supply a class.
            if ':' in r['label_text']:
                candidates=sorted({w for q in read(h/'evidence/mog_check.json')['completion_cases']
                                   if norm(q['label']).replace('_','')==norm(r['label_text']).replace('_','')
                                   for w in q['census_witnesses']})
            if mode=='explicit_pair_objects' and r['undefined_literal_pair_labels']:
                candidates=None
            need(candidates==r['candidates'][mode],'complete row candidate set '+str((r['row'],mode,candidates,r['candidates'][mode])))
    shape={(x['source_row'],x['witness']):x['shape_compatible'] for x in read(h/'evidence/Borel_check.json')['rows']}
    summary={}
    for mode in ['source_pair_order','canonical_pair_order','explicit_pair_objects']:
        accepted=[];used=set()
        for row in rows:
            expected=None if row['candidates'][mode] is None else [w for w in row['candidates'][mode] if shape[(row['row'],w)]]
            need(expected==row['shape_compatible'].get(mode),'exact Borel compatibility retained')
            if expected: accepted.append(row['row']);used.update(expected)
        summary[mode]={'compatible_rows':len(accepted),'distinct_classes':len(used)}
        need(all(summary[mode][k]==rec['summaries'][mode][k] for k in summary[mode]),'whole row summary')
    need(not rec['historical_geo_numbering_recovered'] and not rec['unconditional_all_source_labels_matched'],'unproved historical identification')
    codes=complete_codes(h)
    g='Read('+json.dumps(str((h/'evidence/phase164_m22_witnesses.g').resolve()))+');;\n'+(ROOT/'distinct.g').read_text()
    run=subprocess.run([a.gap,'-q','-b','--quitonbreak'],input=g,capture_output=True,text=True,timeout=120)
    (a.out/'gap.stdout').write_text(run.stdout);(a.out/'gap.stderr').write_text(run.stderr)
    need(run.returncode==0 and not run.stderr,'distinct actual geometry computation')
    need(norm(run.stdout)=='PASS_L073_DISTINCT_WITNESSES:pairs=81;triples=431;residues=1293;actual-completion-orbits=1293;panels=1293','complete actual orbit output')
    report=dict(status='PASS_DISTINCT_ROOT_L073',author_program_imports=False,frozen_exports=len(exports),
                primary_rows_reextracted=431 if source_checked else None,source_rows=431,
                pair_classes=81,triple_classes=431,canonical_triple_signatures=801,broad_triple_signatures=976,
                canonical_pair_signatures=104,broad_pair_signatures=115,independent_complement_closures=431,
                exact_completion_orbit_sets=1293,residue_generation_tests=1293,panel_tests=1293,
                independent_binary_code_enumeration=codes,
                row_summaries=summary,exhaustive_traversal_replayed_by_author_runner=True,
                new_independent_exhaustive_traversal=False,retained_catalogue_and_group_algorithms=True,
                historical_geo_numbering_recovered=False,formal_declarations=0,new_source_credit=0,compression_factor=None)
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

if __name__=='__main__':main()
