"""Check the L036 assembly, accepted imports, scope and native documents.

This checker does not repeat any GAP/graph acquisition. The general proof
and its whole-source scope require a distinct mathematical review.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import shutil
import subprocess
import sys
import time

if not __debug__:
    raise SystemExit('optimization is not an admitted execution mode')

C=Path(__file__).resolve().parent
P=C.parent
R=Path('/Users/sasha/medusa/math_compression')
COUNTS={'M11':37,'M12':166,'M22':81,'M23':170,'M24':5074,'J1':669,
        'J2':334,'J3':546,'HS':339,'McL':443,'He':4074,'Ru':556287}
GATES={
 'character_application_root_review':'ACCEPTED_L036_FIVE_CHARACTER_TOTALS_AND_L073_IMPORT',
 'table_application_root_review':'ACCEPTED_L036_SIX_OUTER_TOTALS_AND_SUBORBIT_TABLES',
 'algorithm_scope_review_adoption':'ADOPTED_L036_COSET_ACTION_SCOPE_DISTINCT_REVIEW',
 'm11_application_root_review':'ACCEPTED_L036_M11_TABLES_WITH_FOUR_ORIENTATION_CORRECTIONS',
}
PARTS=[('completion.pdf',4),('proofs/principal.pdf',2),('proofs/theory.pdf',3),
       ('proofs/characters.pdf',2),('proofs/marks.pdf',4),
       ('proofs/algorithm.pdf',2),('proofs/m11.pdf',6)]

def need(test,message):
    if not test: raise ValueError(message)

def load(path): return json.loads(path.read_text())

def binding(path,base=None):
    b=path.read_bytes()
    return dict(path=str(path.relative_to(base) if base else path),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())

def verify(row,base=None):
    path=Path(row['path']) if base is None else base/row['path']
    need(binding(path,base)==row,'binding changed: '+str(path))

def ledger_check(d):
    need(d['source_id']=='L036' and d['source_edition']=='Art Discrete Appl Math 2 (2019), P1.08, fixed twelve-page journal PDF','source edition')
    rows=d['claims']
    need(len(rows)==35 and len({r['label'] for r in rows})==35,'missing or repeated source claim')
    counts={r['label'][9:] for r in rows if r['label'].startswith('Table 1: ')}
    need(counts==set(COUNTS),'missing group count')
    for r in rows:
        need(r['physical_pages'] and all(1<=p<=12 for p in r['physical_pages']),'source page')
        need(all(r[k] for k in ['status','proof','qualification','attribution']),'incomplete claim scope')
    by={r['label']:r for r in rows}
    need(by['Table 1: Ru']['status']=='CORRECTED_EXACT_COUNT','Ru correction hidden')
    need(by['Electronic geometry files linked on page 2']['status']=='EXTERNAL_ARTIFACTS_UNVERIFIED','external files promoted')
    need(by['Section 3: unrestricted faithfulness of a maximal coset action']['status']=='REFUTED_AND_HYPOTHESIS_IDENTIFIED','core correction hidden')
    need(by['Algorithm 3.1: unrestricted inverse-image output']['status']=='REFUTED_AND_REPAIRED','algorithm correction hidden')
    need(by['Table 3: all 37 M11 geometries and named intersections']['status']=='RECOVERED_WITH_FOUR_ORIENTATION_CORRECTIONS','orientation corrections hidden')
    need(by['Table 7: the two index-253 M23 subgroup labels']['status']=='CORRECTED_TWO_LABELS','label correction hidden')
    need(d['principal_disposition']=='principal_statement_refuted','principal disposition')
    for k in ['ordinary_recovery_credit','new_principal_refutation_credit','new_original_credit','new_named_open_questions_solved','new_Lean_declarations','new_measurements']:
        need(d[k]==0,'unearned credit: '+k)
    for k in ['public_registration_performed','principal_acquisition_repeated','external_representative_files_verified','external_dataset_obligation_promoted']:
        need(d[k] is False,'scope promoted: '+k)
    need(d['remaining_fixed_paper_mathematical_claims']==[],'remaining fixed-paper assertion')
    need(len(d['borrowed_premises'])==4 and len(d['uncertified_extensions'])==4,'premises or limits hidden')

def group_check(d):
    need(len(d['groups'])==12,'group map length')
    need({g['name']:g['count'] for g in d['groups']}==COUNTS,'group totals changed')
    need(d['sum_of_counts']==sum(COUNTS.values())==568220,'aggregate arithmetic')
    need(d['external_representative_files_verified'] is False and d['characters_identify_embeddings'] is False,'data scope promoted')
    chars={g['name']:g for g in load(P/'character_application/arithmetic01.json')['groups']}
    marks={g['name']:g for g in load(P/'table_application/results.json')['counts']}
    for g in d['groups']:
        verify(g['input'])
        if g['name'] in chars:
            src=chars[g['name']]
            need(g['automorphism_group']==g['name'] and g['normalizer_is_maximal'] is True,'Out=1 route')
            for k in ['maximal_classes','maximal_table_names','indices']:
                need(g[k]==src[k],'character input map changed: '+k)
            need(g['count']==src['unordered_pair_orbits'],'character total')
        elif g['name']!='M22':
            need(g['automorphism_group']==g['name']+'.2','full automorphism action missing')
            src=marks[g['automorphism_group']]
            for k in ['socle_class','maximal_classes','maximal_orders','normalizer_classes','normalizer_orders']:
                need(g[k]==src[k],'mark input map changed: '+k)
            need(g['count']==src['unordered_pair_orbits'],'outer total')
        else:
            need(g['source_import']==load(P/'character_application/imports.json'),'M22 import changed')
            need(g['automorphism_group']=='Aut(M22)' and g['count']==81,'M22 scope')

def edition_check(d,override=None):
    need(d['frozen_application_unchanged'] is True and len(d['changes'])==3,'edition scope')
    for row in d['changes']:
        verify(row['source'])
        actual=Path(row['source']['path']).read_text()
        for change in row['replacements']:
            need(actual.count(change['before'])==change['count'],'edition occurrence count')
            actual=actual.replace(change['before'],change['after'])
        dest=C/row['destination']['path']
        text=override if override is not None and dest.name=='m11.tex' else dest.read_text()
        need(text==actual,'unrecorded publication delta')
        need(row['mathematics_changed'] is False,'math change disguised as edition')
        if override is None: verify(row['destination'],C)
    tex=(C/'proofs/m11.tex').read_text()
    need('Section 2 (physical page 3) of the source defines' in tex,'citation not corrected')
    need('\\section{Identifying $\\mathrm{GL}_2(3)$}' in tex,'heading not corrected')
    old=load(P/'m11_application/source_join_corrected.json')
    new=load(C/'proofs/m11_source_join_corrected.json')
    def replace(x):
        if isinstance(x,str): return x.replace('Section3 defines','Section2 (physical page3) defines')
        if isinstance(x,list): return [replace(y) for y in x]
        if isinstance(x,dict): return {k:replace(v) for k,v in x.items()}
        return x
    need(new==replace(old),'M11 numerical comparison changed')

def normalized(page): return ''.join(page.extract_text().split())

def compare_pdfs(first,second):
    from pypdf import PdfReader
    a,b=PdfReader(first),PdfReader(second)
    need(len(a.pages)==len(b.pages),'native page count changed')
    for i,(x,y) in enumerate(zip(a.pages,b.pages)):
        need(normalized(x)==normalized(y),'native text changed: '+str(first)+' page '+str(i+1))

def embedded_page_check(source,container):
    forms=[x.get_object() for x in container['/Resources']['/XObject'].values()]
    need(len(forms)==1,'one imported form required')
    form=forms[0]
    need(form.get_data()==source.get_contents().get_data(),'imported drawing stream changed')
    a,b=source['/Resources']['/Font'],form['/Resources']['/Font']
    need(set(a)==set(b),'page font resources changed')
    for name in a:
        x,y=a[name].get_object(),b[name].get_object()
        need(x['/Subtype']==y['/Subtype'],'font type changed')
        dx,dy=x['/FontDescriptor'].get_object(),y['/FontDescriptor'].get_object()
        for key in ['/FontFile','/FontFile2','/FontFile3']:
            need((key in dx)==(key in dy),'font program presence changed')
            if key in dx: need(dx[key].get_data()==dy[key].get_data(),'glyph program changed')

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--out',required=True);parser.add_argument('--render',action='store_true');args=parser.parse_args()
    out=Path(args.out).resolve()
    need(not out.exists() and not out.is_relative_to(C),'fresh separate output required')
    need(shutil.disk_usage(C).free>=4*1024**3,'hold below4GiB reserve')
    deps=load(C/'dependencies.json')
    for row in deps: verify(row)
    if (C/'manifest.json').exists():
        for row in load(C/'manifest.json')['exports']: verify(row,C)
    for gate,status in GATES.items(): need(load(P/gate/'manifest.json')['status']==status,'accepted component gate missing')
    old=load(R/'audit/principal-refutations/L036/v1/admission.json')
    need(old['principal_refutation_credit']==1 and old['ordinary_recovery_credit']==0,'principal import')
    ledger=load(C/'claims.json');ledger_check(ledger)
    groups=load(C/'group_inputs.json');group_check(groups)
    for row in load(C/'imports.json'):
        verify(row['source']);verify(row['destination'],C)
        need(Path(row['source']['path']).read_bytes()==(C/row['destination']['path']).read_bytes(),'accepted proof changed')
    editions=load(C/'edition_deltas.json');edition_check(editions)
    controls=[]
    trials=[
      ('missing_claim',ledger,lambda x:x['claims'].pop(),ledger_check),
      ('ordinary_credit',ledger,lambda x:x.update(ordinary_recovery_credit=1),ledger_check),
      ('external_files_promoted',ledger,lambda x:x.update(external_representative_files_verified=True),ledger_check),
      ('wrong_Ru_total',groups,lambda x:x['groups'][-1].update(count=1511),group_check),
      ('inner_action_substituted',groups,lambda x:x['groups'][1].update(automorphism_group='M12'),group_check),
      ('missing_normalizer_class',groups,lambda x:x['groups'][1]['normalizer_classes'].pop(),group_check),
    ]
    for name,data,mutate,check in trials:
        bad=copy.deepcopy(data);mutate(bad)
        try: check(bad)
        except ValueError: controls.append(name)
        else: raise ValueError('damaged data accepted: '+name)
    try: edition_check(editions,override=(C/'proofs/m11.tex').read_text().replace('47586','47585'))
    except ValueError: controls.append('unrecorded_mathematical_edition_rejected')
    else: raise ValueError('unrecorded math edit accepted')
    from pypdf import PdfReader
    whole=PdfReader(C/'complete.pdf')
    need(len(whole.pages)==24,'full volume length')
    offset=1
    for rel,count in PARTS:
        part=PdfReader(C/rel);need(len(part.pages)==count,'part length')
        for i,page in enumerate(part.pages):embedded_page_check(page,whole.pages[offset+i])
        offset+=count
    for flag in ['-O','-OO']:
        r=subprocess.run([sys.executable,flag,str(C/'check.py')],capture_output=True,timeout=10)
        need(r.returncode!=0 and b'optimization is not an admitted execution mode' in r.stderr,'optimization guard')
        controls.append(flag+'_rejected')
    out.mkdir(parents=True)
    runs=[]
    if args.render:
        work=out/'native';(work/'proofs').mkdir(parents=True)
        for path in sorted(C.glob('*.tex'))+sorted((C/'proofs').glob('*.tex')):
            shutil.copyfile(path,work/path.relative_to(C))
        for rel in ['proofs/principal','proofs/theory','proofs/characters','proofs/marks','proofs/algorithm','proofs/m11','completion','complete']:
            stem=work/rel
            for n in [1,2]:
                command=['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error',stem.name+'.tex']
                start=time.monotonic();r=subprocess.run(command,cwd=stem.parent,capture_output=True,timeout=30)
                stem.with_name(stem.name+'-pass'+str(n)+'.stdout').write_bytes(r.stdout)
                stem.with_name(stem.name+'-pass'+str(n)+'.stderr').write_bytes(r.stderr)
                need(r.returncode==0,'native TeX failed: '+rel)
                runs.append(dict(command=command,cwd=str(stem.parent),seconds=time.monotonic()-start,returncode=r.returncode))
            log=stem.with_suffix('.log').read_text()
            need('Overfull' not in log and 'undefined' not in log,'native document warning: '+rel)
            compare_pdfs(C/(rel+'.pdf'),stem.with_suffix('.pdf'))
        command=['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r105','-sOutputFile='+str(out/'complete-%02d.png'),str(work/'complete.pdf')]
        start=time.monotonic();r=subprocess.run(command,capture_output=True,timeout=30)
        (out/'render.stdout').write_bytes(r.stdout);(out/'render.stderr').write_bytes(r.stderr)
        need(r.returncode==0 and len(list(out.glob('complete-*.png')))==24,'native rasters')
        runs.append(dict(command=command,seconds=time.monotonic()-start,returncode=r.returncode))
    for row in deps: verify(row)
    report=dict(status='PASS_L036_COMPLETE_SOURCE_ASSEMBLY',dependencies=len(deps),source_claims=35,groups=12,exact_total=568220,suborbit_cells=308,M11_geometry_rows=37,M11_design_entries=70,volume_pages=24,embedded_page_streams_and_glyph_programs_match=True,controls=controls,runs=runs,new_acquisitions=0,public_mutations=0,general_proofs='REQUIRE_DISTINCT_MATHEMATICAL_REVIEW',external_representative_files_verified=False,new_Lean=0,measurements=None,outputs=[binding(f,out) for f in sorted(out.rglob('*')) if f.is_file()])
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','dependencies','source_claims','volume_pages','controls']}))

if __name__=='__main__':main()
