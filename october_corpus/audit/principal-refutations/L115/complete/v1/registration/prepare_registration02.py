"""Prepare L115 completion against the exact L110 baseline; no public writes."""
from pathlib import Path
import copy,difflib,hashlib,json,re,shutil,subprocess,sys
if not __debug__:raise RuntimeError('ordinary Python required')
P=Path(__file__).resolve().parent;F=P.parent;R=Path('/Users/sasha/medusa/math_compression')
STAGE=P/'stage02';AUD='audit/principal-refutations/L115/complete/v1';PAPER='papers/corrections/L115/v1';C=P/'registration_candidate02'
BASELINE='de093380caee98006f8175ef7f8b4d760ca18b2e'
OP_SHA='4ed33f290c04e0fe9ee06926a12b0b65469adf85be7f12da3bb7974cc8f878ae'
def need(v,s):
    if not v:raise ValueError(s)
def load(p):return json.loads(p.read_text())
def pin(p,base=None):
    p=Path(p);h=hashlib.sha256()
    with p.open('rb')as f:
        for b in iter(lambda:f.read(2**20),b''):h.update(b)
    return dict(path=str(p.relative_to(base)if base else p),bytes=p.stat().st_size,sha256=h.hexdigest())
def write(n,x):
    p=C/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n');return p
def pp(n):return pin(C/'proposed'/n,C/'proposed')
def sp(n):return pin(STAGE/n,STAGE)
def main():
    need(len(sys.argv)==1 and not C.exists(),'fresh no-argument preparation')
    need(subprocess.check_output(['git','-C',str(R),'rev-parse','HEAD'],text=True).strip()==BASELINE,'exact L110 predecessor')
    need(not subprocess.check_output(['git','-C',str(R),'status','--porcelain']).strip(),'clean predecessor')
    need(shutil.disk_usage(P).free>=4*2**30+64*2**20,'4GiB reserve plus bounded metadata allowance')
    op=F/'publication_operational_root_review';root=pin(op/'manifest.json');need(root['sha256']==OP_SHA,'exact portable acceptance')
    need(load(op/'manifest.json')['status']=='ACCEPTED_L115_PORTABLE_COMPLETE_SOURCE_TREATMENT','accepted portable status')
    old=load(R/'audit/corpus/latest.json')
    need([old[k]for k in ['admitted_principal_originals','refuted_principal_originals','handled_mathematical_originals','currently_measured_originals','fully_treated_originals','surviving_claim_obligation_originals','completion_obligation_originals']]==[92,9,101,53,97,4,8],'exact predecessor counts')
    need('L115'in old['surviving_claim_obligation_original_ids']and 'L115'not in old['fully_treated_original_ids'],'unpaid L115 only')
    C.mkdir();transport=load(STAGE/AUD/'transport.json');science=pin(F/'principal_root_review/manifest.json');need(transport['root_acceptance']==science,'same complete scientific treatment')
    stage_records=load(STAGE/AUD/'manifest.json')['exports']+[sp(AUD+'/manifest.json')];stage_by_hash={r['sha256']:r for r in stage_records}
    objects=transport['objects'];premises=transport['premises'];premise_by_hash={r['sha256']:r for r in premises};need(len(premises)==len(premise_by_hash)==2583,'exact documentary/environment boundary')
    premise_occurrences={(r['original_path'],r['sha256'],r['bytes'])for r in transport['logical_files']if r['sha256']in premise_by_hash}
    raw=load(op/'dependencies.json')+[dict(r,path=str(op/r['path']))for r in load(op/'manifest.json')['exports']]+[root]
    need(science in raw,'operational review acquired exact scientific acceptance')
    unique={}
    for r in raw:need(r['path']not in unique or unique[r['path']]==r,'consistent repeated bindings');unique[r['path']]=r
    routes=[];copied={};accepted_transport=sp(AUD+'/transport.json')
    for row in unique.values():
        source=Path(row['path']);need(pin(source)==row,'unchanged operational input');h=row['sha256']
        if (row['path'],h,row['bytes'])in premise_occurrences:
            routes.append(dict(original=row,premise=premise_by_hash[h]));continue
        need(h not in premise_by_hash or row['bytes']==0,'only empty operational logs may share documentary content')
        if h in stage_by_hash:target=stage_by_hash[h]
        elif row['path']not in [science['path'],root['path']] and h in objects and objects[h]['kind']in ['NEW_PACKED_EXACT_CONTENT','EXISTING_PUBLIC']:
            obj=objects[h];need(obj['kind']in ['NEW_PACKED_EXACT_CONTENT','EXISTING_PUBLIC']and obj['bytes']==row['bytes'],'scientific transport object')
            routes.append(dict(original=row,transport_object=dict(transport=accepted_transport,sha256=h,bytes=row['bytes'])));continue
        elif source.is_relative_to(R)and str(source.relative_to(R)).startswith(('audit/','papers/','corrections/')):
            target=pin(source,R)
        else:
            suffix='.bin'if source.suffix.lower()=='.md'else source.suffix
            name=AUD+'/operational/objects/'+h+suffix;target=dict(row,path=name)
            if name not in copied:
                dest=C/'proposed'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest);copied[name]=target
        routes.append(dict(original=row,public=target))
    mapping=dict(status='EXACT_L115_PORTABLE_REVIEW_TRANSPORT',original_manifest=root,original_status=load(op/'manifest.json')['status'],routes=routes,premises=premises,accepted_content_transport=accepted_transport)
    write('proposed/'+AUD+'/operational/mapping.json',mapping)
    physical={r['original']['path']:r['public']for r in routes if 'public'in r}
    need(science['path']in physical and root['path']in physical,'readable acceptance records')
    claims=load(F/'principal_v2/source_claims.json');native=load(R/'papers/catalogue_principal_refutations.json');native_entry=next(e for e in native['entries']if e['source_ids']==['L115'])
    titles=dict(principal='A corrected classification of rank-two Suzuki geometries',arithmetic='Integer certificates for the Suzuki geometry counts',preliminaries='Maximal subgroups and elementary reductions for Suzuki geometries',scalar_subspaces='Scalar subspaces in rank-two Suzuki geometries',normalizer_families='Normalizer fibres in rank-two Suzuki geometries',subfield_families='Subfield parabolics and the corrected Suzuki classification',diagram_labels='Corrections to the Suzuki diagram labels',diagrams='The twenty-nine rank-two Suzuki geometries over the field of eight elements')
    manuscripts=[]
    for item in load(STAGE/PAPER/'manuscripts.json')['manuscripts']:
        reused=item['name']=='scalar_subspaces'
        row=dict(id='L115-'+item['name'],title=titles[item['name']],physical_pages=item['pages'],tex=sp(PAPER+'/'+item['tex']),pdf=sp(PAPER+'/'+item['pdf']),tex_inputs=[],compiler='pdflatex',existing_principal_manuscript_reused=reused)
        if reused:
            for k in ['tex','pdf']:need(row[k]['sha256']==pin(R/native_entry[k])['sha256'],'existing principal manuscript is byte-identical')
        manuscripts.append(row)
    collection=dict(manifest=sp(PAPER+'/manuscripts.json'),physical_pages=36,manuscripts=8,already_counted_principal_pages=4,additional_manuscript_pages=32,merged_volume_claimed=False)
    admission=dict(status='REVIEWED_L115_SOURCE_COMPLETION_REQUIRING_ROOT_PUBLICATION_GATE',source_ids=['L115'],disposition_kind='principal_refutation_with_complete_corrected_source_disposition',source_identity=claims['source'],source_edition='Beitraege zur Algebra und Geometrie 39(1) (1998), 97–120',principal_refutation_admission=pin(R/native_entry['admission']['path'],R),mathematical_acceptance=physical[science['path']],portable_acceptance=physical[root['path']],operational_mapping=pp(AUD+'/operational/mapping.json'),stage_manifest=sp(AUD+'/manifest.json'),transport=accepted_transport,portable_checker=sp(AUD+'/portable_check.py'),source_claim_ledger=sp(PAPER+'/source_claims.json'),source_claim_rows=70,complete_proof_collection=collection,manuscripts=manuscripts,unresolved_asserted_claims=claims['unresolved_asserted_claims'],classical_premises=['Tits Suzuki construction and Bruhat decomposition','Classical subgroup, torus and automorphism facts expressly cited in the manuscripts'],ordinary_recovery_credit=0,principal_refutation_credit=0,new_original_credit=0,proposed_source_completion_credit=1,new_measurements=0,new_question_credit=0,new_Lean_credit=0,whole_source_formalized=False,compression_factor=None,source_retrieval_performed=False,public_gate=AUD+'/root_integration.json')
    write('proposed/'+AUD+'/admission.json',admission);ap=pp(AUD+'/admission.json');updated=copy.deepcopy(old)
    for ids,count,addition in [('source_complete_refutation_original_ids','source_complete_refutation_originals',True),('fully_treated_original_ids','fully_treated_originals',True),('surviving_claim_obligation_original_ids','surviving_claim_obligation_originals',False),('completion_obligation_original_ids','completion_obligation_originals',False)]:
        updated[ids]=sorted(old[ids]+['L115'])if addition else[x for x in old[ids]if x!='L115'];updated[count]=len(updated[ids])
    updated['handled_count_meaning']='Principal dispositions only: 92 corrected recoveries and nine principal refutations. F003, L029, L036, L110, L114 and L115 have complete surviving-source dispositions; three other refutations retain surviving-claim obligations.'
    delta={k:v for k,v in updated.items()if old.get(k)!=v};write('machine_delta.json',delta)
    registration=dict(status='REVIEWED_L115_SOURCE_COMPLETION_REQUIRING_ROOT_GATES',source_ids=['L115'],admission=ap,predecessor_commit=BASELINE,previous_principal_disposition=old['current_principal_disposition_registration'],previous_science_registration=old['current_science_registration'],previous_source_completion_registration=old['current_source_completion_registration'],ordinary_recoveries_added=0,principal_refutations_added=0,principal_dispositions_added=0,fully_treated_originals_added=1,surviving_claim_obligations_closed=['L115'],new_measurements=0,new_question_credit=0,new_Lean_credit=0,compression_factor=None,public_gate=AUD+'/root_integration.json')
    write('proposed/'+AUD+'/source_completion_registration.json',registration);rp=pp(AUD+'/source_completion_registration.json')
    catalogue=load(R/old['active_catalogue']['path']);entry=next(e for e in catalogue['entries']if e['original_id']=='L115');before_entry=copy.deepcopy(entry)
    entry['current_source_completion']=dict(status='REVIEWED_COMPLETE_CORRECTED_SOURCE_DISPOSITION_AFTER_PRINCIPAL_REFUTATION',admission=ap,principal_refutation_preserved=True,ordinary_recovery_credit=0,source_claim_rows=70,source_contract='Fixed 24-page article, 97–120: all 70 source dispositions, the corrected all-q classification and counts, all 60 numerical rows, and all 29 Sz(8) diagrams, with 75 inner classes and explicit classical premises.',qualification='The original principal refutation is preserved. Lemma 6.1 has rank greater than one; source domain, classification, counting and diagram corrections remain explicit. Equivalence uses automorphisms of the specified group and type interchange. No new conjecture, Lean or compression measurement is claimed.',whole_source_formalized=False,measured=False,compression_factor=None)
    entry['next_obligation']='No surviving mathematical source-disposition obligation remains for the fixed 24-page article. Preserve the prior principal refutation, complete corrected classification and counts, all numerical and diagram corrections, and attributed classical premises. No ordinary recovery, new principal refutation or measurement is assigned.'
    catalogue.update(previous_catalogue=old['active_catalogue'],review_revision='L115 receives complete corrected treatment after its already registered principal refutation. Ordinary recoveries, principal dispositions and measurements do not change.')
    for k in ['source_complete_refutation_original_ids','source_complete_refutation_originals','fully_treated_original_ids','fully_treated_originals']:catalogue[k]=updated[k]
    catalogue['current_recovery_counts'].update(surviving_claim_obligations=3,completion_obligations=7,fully_treated=98,completed_refutation_sources=6)
    catname='audit/corpus/accessible106/updates/completion-L115-catalogue.json';write('proposed/'+catname,catalogue)
    updated.pop('snapshot');updated.update(previous_snapshot=dict(pin(R/'audit/corpus/latest.json',R),path=AUD+'/previous/audit/corpus/latest.json'),active_catalogue=pp(catname),current_source_completion_registration=rp)
    snapname='audit/corpus/updates/accessible106-completion-L115.json';write('proposed/'+snapname,updated);updated['snapshot']=pp(snapname);write('proposed/audit/corpus/latest.json',updated)
    native_entry['source_completion']=dict(admission=ap,complete_proof_collection=collection,additional_manuscripts=[m for m in manuscripts if not m['existing_principal_manuscript_reused']],principal_manuscript_counted_again=False,measured=False,compression_factor=None)
    native.update(source_complete_original_ids=updated['source_complete_refutation_original_ids'],source_completion_credit=6);write('proposed/papers/catalogue_principal_refutations.json',native)
    paper=load(R/'papers/latest_catalogue.json');paper.update(active_source_catalogue=pp(catname),principal_refutation_catalogue=pp('papers/catalogue_principal_refutations.json'));write('proposed/papers/latest_catalogue.json',paper)
    paragraph='F003, L029, L036, L110, L114 and L115 now have complete reviewed treatments\nof their surviving source claims. Thus 98 originals are fully treated:\n92 ordinary recoveries and six complete source treatments after principal\nrefutations. Three other refuted originals and four without a principal\ndisposition retain completion obligations: 7 originals remain. There are\n101 principal dispositions and 92 ordinary recoveries; the stopping\ncondition is unchanged.'
    note='The `complete L115 proof collection <{prefix}papers/corrections/L115/v1/README.rst>`_\ntreats all 70 source dispositions in the 24-page article on rank-two Suzuki\ngeometries. It gives the corrected general classification and counts,\ncertifies all 180 torus integers and 60 numerical rows, and verifies the\n29 diagrams representing 75 inner classes. Eight complete manuscripts\ncontain 36 proof pages, including the existing four-page principal\nrefutation. Domain, counting and diagram corrections remain explicit,\nand classical structure results are attributed. This closes one source\nobligation without adding an ordinary recovery, principal refutation,\nquestion, Lean claim or compression measurement.\n\n'
    changes=[]
    for name,prefix in [('README.rst',''),('audit/completion.rst','../')]:
        before=(R/name).read_text();pat=r'(?m)^F003, L029[^\n]*now have complete[\s\S]*?stopping\s+condition\s+is unchanged\.';matches=list(re.finditer(pat,before));need(len(matches)==1,'unique completion narrative paragraph')
        match=matches[0];after=before[:match.start()]+paragraph+before[match.end():];anchor='The `complete L114 volume';need(after.count(anchor)==1,'stable preceding completion note');after=after.replace(anchor,note.format(prefix=prefix)+anchor)
        dest=C/'proposed'/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(after);changes.append(dict(path=name,before=pin(R/name,R),after=pp(name)))
        (C/(name.replace('/','_')+'.diff')).write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='before/'+name,tofile='after/'+name)))
    name='audit/protocol.tex';before=(R/name).read_text();pat=r'statement is handled separately from a recovery\. F003, L029[\s\S]*?stopping condition is unchanged\.';matches=list(re.finditer(pat,before));need(len(matches)==1,'unique protocol completion paragraph')
    match=matches[0];scope='statement is handled separately from a recovery. '+paragraph.replace('stopping\ncondition','stopping condition');after=before[:match.start()]+scope+before[match.end():]
    anchor="L114's complete source treatment";need(after.count(anchor)==1,'stable protocol insertion anchor')
    text="L115's complete corrected treatment covers all 70 source dispositions in the\n24-page article. It supplies the general classification and counting formulas,\n180 certified torus integers and 60 numerical rows, and all 29 diagrams with\n75 inner classes. Eight complete manuscripts retain 36 proof pages, including\nthe existing four-page principal correction. Domain and diagram corrections\nand classical premises remain explicit. No ordinary recovery, new principal\nrefutation, conjecture, Lean declaration or compression factor is added.\n\n"
    after=after.replace(anchor,text+anchor);(C/'proposed'/name).write_text(after);changes.append(dict(path=name,before=pin(R/name,R),after=pp(name)));(C/'audit_protocol.tex.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='before/'+name,tofile='after/'+name)))
    write('narrative_changes.json',changes);write('source_entry_delta.json',dict(original_id='L115',before=before_entry,added_current_source_completion=entry['current_source_completion'],next_obligation=entry['next_obligation'],principal_disposition_unchanged=True,all_other_originals_unchanged=True))
    write('baseline.json',dict(commit=BASELINE,current_corpus=pin(R/'audit/corpus/latest.json',R),active_catalogue=old['active_catalogue'],preserved_measured_ids=old['measured_original_ids'],preserved_recovery_ids=old['admitted_original_ids'],preserved_refutation_ids=old['refuted_principal_original_ids'],history_paths=['README.rst','audit/completion.rst','audit/protocol.tex','audit/protocol.pdf','audit/corpus/latest.json','papers/latest_catalogue.json','papers/catalogue_principal_refutations.json','scripts/verify_snapshot.py']))
    write('proposal.json',dict(status='PRIVATE_L115_SOURCE_COMPLETION_REGISTRATION_PROPOSAL',baseline=BASELINE,source_ids=['L115'],stage=pin(STAGE/AUD/'manifest.json'),mathematical_acceptance=science,operational_acceptance=root,admission=ap,source_completion_registration=rp,machine_delta=delta,public_files_written=False,root_final_gate_required=AUD+'/root_integration.json',proposed_paths=[str(p.relative_to(C/'proposed'))for p in sorted((C/'proposed').rglob('*'))if p.is_file()],installation_and_snapshot_checker='Root supplies after review of this exact proposal.'))
    print(json.dumps(dict(status='PREPARED_L115_REGISTRATION_CANDIDATE',proposal=pin(C/'proposal.json'),fully_treated=98,remaining=7,ordinary_recovery_delta=0,public_mutations=0,operational_routes=len(routes),operational_objects=len(copied))))
if __name__=='__main__':main()
