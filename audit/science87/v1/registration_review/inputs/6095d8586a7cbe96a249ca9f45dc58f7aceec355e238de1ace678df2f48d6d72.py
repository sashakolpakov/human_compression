"""Generate explicit registration parameters from accepted immutable handoffs."""
import sys
if sys.flags.optimize:raise RuntimeError('Ordinary Python required')
from pathlib import Path
import argparse,hashlib,json,subprocess
W=Path(__file__).resolve().parent;R=Path('/Users/sasha/medusa/math_compression');D=W/'registration_drafts_v2';AUD='audit/science87/v1'
def load(p):return json.loads(p.read_text())
def pin(p,root):return dict(path=str(p.relative_to(root)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def dump(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
NOTES={
 'L076':'Complete corrected q>=4 principal classification with a Borel or full torus-normalizer parabolic; measurement deferred. Preserve the ordered/unordered q11/q13 correction, q2/q3 boundaries, retained Dickson/maximal-subgroup inputs, and explicit exclusion of unused numerical subgroup multiplicities and other source Table4 actions. No higher-rank Boolean theorem, new question, Lean or compression credit.',
 'L027':'Complete corrected principal Theorems1.1-1.3 with56 source clauses, all15 numbered statements and21 table cells; measurement deferred. Preserve12 retained-input records, the three positive PSU3(17) pairs without exhaustion, source-attributed unreproduced earlier censuses, and inherited correction of the q81 negative claim. No new question, census-completeness, Lean or compression credit.',
 'L036':'Principal refutation of the fixed Table1 Ru total1511: a proved lower bound50669 suffices. The corrected exact Ru total, the other11 table classifications, orbit-length/design data and external census remain unpaid. Preserve the primary Atlas group/maximality inputs and unordered Aut(G) convention. No ordinary recovery, new question, measurement or Lean credit.',
 'L046':'Principal refutation of fixed Theorem1.1(2), applying the later disposition convention to the unchanged published correction. The lower798370 contradicts796772; exact cell(20,31)=9118 corrects7246. All116 other exact cells, the exact total, zero-type and chirality/nonorientable/outer-reflexible claims and Section7 inversion census remain unpaid. All old pending/no-credit records stay historical; no new mathematics, ordinary recovery or measurement.',
 'L063':'Principal refutation of Theorem1.1/Table4 and Lemma5.11/Proposition5.12 in the fixed2013 source. The actual PSL2(512) scalar-plane geometry has parabolic orders504/448, intersection56 and local degrees9/8. This is the same omission as L064, with retained prime-extension subfield maximality; nine planes are not nine geometry classes. Other source claims and any corrected full classification remain unpaid.',
 'L064':'Principal refutation of the m=2 restriction in the proof of Proposition22,p12,general case,subcase2 of the fixed21-page appendix. Lemma21 is not the target. The same PSL2(512) scalar-plane example as L063 pays the contradiction; no second independent mathematical defect, geometry-class count or corrected complete classification is claimed. Other source claims remain unpaid.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--bundle',type=Path,required=True);a=ap.parse_args();B=a.bundle.resolve();ST=B/'stage';bundle=load(B/'accepted_bundle.json');assert bundle['baseline']=='ade9feeb7f8feaffa8f773932d57a50e60cb64c2'
 def resolve(name):p=ST/name;return p if p.exists()else R/name
 def public_pin(r):
  name=r if isinstance(r,str)else r.get('public_path',r.get('path'));return pin(resolve(name),ST)if(ST/name).exists()else pin(R/name,R)
 packages=[];specs={}
 for c in bundle['packages']:
  candidates=[r for r in load(B/'stage_manifest.json')['files']if r['sha256']==c['proposal_pin']['sha256']and r['bytes']==c['proposal_pin']['bytes']];assert len(candidates)==1
  pp=candidates[0];p=load(ST/pp['path']);op=next(r for r in bundle['operational_reviews']if f"/{c['id']}/"in r['path'])
  packages.append(dict(id=c['id'],source_ids=c['source_ids'],kind=c['kind'],proposal=pp,operational_review=op,operational_manifest_sha256=c['operational_review']['sha256'],operational_status=c['operational_review']['status'],transport=c.get('transport')))
  scope_route=p['scope_routes'];scope_path=scope_route if isinstance(scope_route,str)else scope_route['path'];scope=load(resolve(scope_path))
  raw_manuscripts=p.get('complete_manuscripts',p.get('manuscripts',p.get('proof_manuscripts')));manuscripts=[]
  for i,m in enumerate(raw_manuscripts):
   ident=m.get('id')or(c['id']+'-'+Path(m['tex']).stem)
   if c['id']=='L027'and not ident.startswith('L027-'):ident='L027-'+ident
   manuscripts.append(dict(id=ident,title=m.get('title',m.get('role','Complete proof')),source_ids=m.get('source_ids',c['source_ids']),tex=public_pin(m['tex']),pdf=public_pin(m['pdf']),tex_inputs=[public_pin(x)for x in m.get('tex_inputs',[])],physical_pages=m.get('physical_pages',m.get('pages')),topic=p.get('title',c['id'])))
  for sid in c['source_ids']:
   source_contract=scope
   if c['id']=='planes':
    exact_source=next(x for x in p['source_routes']if x['source_id']==sid);source_contract=dict(source=exact_source,shared_construction_scope=scope,mathematical_defects=1);edition=exact_source['edition']
   elif c['id']=='L046':edition=scope['source']['edition']
   else:edition=p.get('source_edition',scope.get('edition'))
   specs[sid]=dict(package_id=c['id'],proposal=pp,operational_review=op,edition=edition,source_contract=source_contract,manuscripts=manuscripts,scope_note=NOTES[sid])
 # Explicit literal current-position edits, with the predecessor text bound.
 delta=[];texts={n:(R/n).read_text()for n in ['README.rst','audit/completion.rst','audit/protocol.tex']}
 def edit(name,before,after,expected=1):
  assert texts[name].count(before)==expected,(name,before,texts[name].count(before));delta.append(dict(path=name,before=before,after=after,occurrences=expected));texts[name]=texts[name].replace(before,after)
 edit('README.rst','**85 accessible originals','**87 accessible originals')
 edit('README.rst','53 are measured and thirty-two (','53 are measured and thirty-four (')
 edit('README.rst','L045, L052, N010 and L041) await measurement.','L045, L052, N010, L041, L027 and L076) await measurement.')
 edit('README.rst','Five further originals, F003, L029, L110, L114 and L115, have reviewed principal refutations;','Nine further originals, F003, L029, L110, L114, L115, L036, L046, L063 and L064,\nhave reviewed principal refutations;')
 edit('README.rst','15 await a complete mathematical disposition.','9 await a complete mathematical disposition.')
 edit('README.rst','Thus 90 of 105 mathematical originals are\nhandled: 85 recoveries and five refutations.','Thus 96 of 105 mathematical originals have reviewed principal\ndispositions: 87 recoveries and nine refutations.')
 edit('README.rst','**L046 remains among the 15 pending originals:** 116 exact table counts,\nthe exact total and remaining chirality claims still require recovery.\nThis correction adds no completed original, compression factor or\nopen-conjecture credit.','**L046 now has a principal-refutation disposition**, applying the same convention\nas the later refutations to the unchanged published correction. All 116 exact\ntable counts, the exact total and the remaining chirality, nonorientable,\nouter-reflexible and inversion claims remain unpaid. The\n`disposition layer <audit/principal-refutations/L046/v1/PUBLICATION.rst>`_\npreserves the earlier pending/no-credit decision as history. This adds no\nordinary recovery, new mathematics, measurement or open-question credit.')
 refute="""The `Rudvalis correction <corrections/rudvalis-rank-two/v1/PUBLICATION.rst>`_
proves at least 50,669 unordered Aut(G) classes, contradicting L036's printed
total 1,511. It does not give the corrected exact total or recover the other
eleven table rows. The `scalar-plane correction
<corrections/projective-subfield-planes/v1/PUBLICATION.rst>`_ supplies one
omission in the two separate fixed sources L063 and L064. Its PSL2(512)
geometry has local degrees 9 and 8; nine exhibited planes are not a count
of geometry classes. The L064 target is the proof of Proposition 22, not
Lemma 21. Retained classical inputs and all unpaid results remain explicit.

"""
 edit('README.rst','A corrected count with remaining work',refute+'A corrected count with remaining work')
 ordinary="""The `L076 guide <papers/projective-line-rank-two/v1/PUBLICATION.rst>`_
gives the complete six-page corrected projective-line rank-two classification,
including the ordered/unordered corrections at q=11 and q=13. The
`L027 guide <papers/recoveries/L027/v1/PUBLICATION.rst>`_ supplies the complete
34-page proof collection for the three principal dimension-three theorems.
Its twelve retained-input records and earlier source-attributed censuses remain
explicit. The three PSU3(17) pairs are positive examples, not an exhaustion;
the printed q=81 negative claim is corrected by an already acquired theorem.
Neither recovery adds a measurement, new question answer or Lean claim.

"""
 edit('README.rst','All thirty-two source editions',ordinary+'All thirty-four source editions')
 edit('README.rst','None of these thirty-two recoveries','None of these thirty-four recoveries')
 edit('README.rst','audit/science85/v1/new_original_registration.json','audit/science87/v1/new_original_registration.json')
 edit('audit/completion.rst','**85 reviewed corrected principal recoveries**','**87 reviewed corrected principal recoveries**')
 edit('audit/completion.rst','53 are measured and thirty-two (','53 are measured and thirty-four (')
 edit('audit/completion.rst','L045, L052, N010 and L041','L045, L052, N010, L041, L027 and L076',2)
 edit('audit/completion.rst','F003, L029, L110, L114 and L115 have separate reviewed principal refutations; 15 originals','F003, L029, L110, L114, L115, L036, L046, L063 and L064 have separate reviewed principal refutations; 9 originals')
 edit('audit/completion.rst','Thus 90 of the 105 mathematical originals\nare handled.','Thus 96 of the 105 mathematical originals\nhave reviewed principal dispositions.')
 edit('audit/completion.rst','(20,31) entry 9,118 versus 7,246. L046 remains pending: 116 exact entries,\nthe exact total and the remaining chirality claims are unpaid. The common\nand application proofs and independent computations are public; this\nbounded correction changes none of the programme totals.','(20,31) entry 9,118 versus 7,246. L046 receives a principal-refutation\ndisposition under the later convention; the old pending/no-credit layer remains\nimmutable history. All 116 exact entries, the exact total and remaining\nchirality/nonorientable/outer-reflexible and inversion claims are unpaid.\nThe `new disposition <principal-refutations/L046/v1/PUBLICATION.rst>`_ adds\nno ordinary recovery, new mathematics, measurement or question credit.')
 edit('audit/completion.rst','The `L046 count correction',refute.replace('<corrections/','<../corrections/')+'The `L046 count correction')
 edit('audit/completion.rst','science85/v1/new_original_registration.json','science87/v1/new_original_registration.json')
 edit('audit/completion.rst','F008 is an auxiliary original',ordinary.replace('<papers/','<../papers/').replace('<audit/','<')+'F008 is an auxiliary original')
 edit('audit/protocol.tex','106={}&85\\ \\text{reviewed corrected recoveries}+5\\ \\text{principal refutations}','106={}&87\\ \\text{reviewed corrected recoveries}+9\\ \\text{principal refutations}')
 edit('audit/protocol.tex','&+15\\ \\text{mathematical targets}','&+9\\ \\text{mathematical targets}')
 edit('audit/protocol.tex','Of the 85 corrected recoveries','Of the 87 corrected recoveries')
 edit('audit/protocol.tex','L045, L052, N010 and L041','L045, L052, N010, L041, L027 and L076')
 addition=r'''L027 and L076 add two corrected principal recoveries, with complete
proof collections of 34 and six pages. Their exact source conventions,
retained classifications and unreproduced historical census boundaries
remain explicit. The three PSU$_3(17)$ pairs are positive examples, not a
classification; the $q=81$ source correction acquires an earlier theorem.
Measurement remains deferred.

L036, L046, L063 and L064 add four separately scoped principal refutations.
For L036 the lower bound $50669>1511$ refutes the fixed Ru total without
claiming a corrected exact total or recovering the other eleven rows.
L046 applies the later disposition convention to its unchanged published
correction: $798370>796772$, with type $(20,31)$ exactly $9118$.
All 116 other exact cells, the exact total, chirality and finer inversion
obligations remain unpaid; the old pending/no-credit decisions remain
immutable historical records. L063 and L064 share one scalar-plane omission,
with separately pinned source clauses; the latter target is the proof of
Proposition 22, not Lemma 21. Nine planes are not nine geometry classes.
None of these refutations is an ordinary recovery or a claim that all valid
source assertions have been recovered. There is no new measurement,
question-answer or Lean credit.

'''
 edit('audit/protocol.tex','F008 is an auxiliary original',addition+'F008 is an auxiliary original')
 # Bind the entire actual Git tree, including symlinks and executable modes.
 raw=subprocess.check_output(['git','ls-tree','-rz','--full-tree',bundle['baseline']],cwd=R);files=[]
 for line in raw.split(b'\0'):
  if not line:continue
  prefix,name=line.split(b'\t',1);mode,kind,oid=prefix.decode().split();name=name.decode();p=R/name
  if mode=='120000':files.append(dict(path=name,mode=mode,git_oid=oid,link=str(p.readlink())))
  else:files.append(dict(pin(p,R),mode=mode,git_oid=oid))
 dump(D/'predecessor_tree.json',dict(commit=bundle['baseline'],files=files))
 params=dict(baseline=bundle['baseline'],source_ids=sorted(specs),packages=packages,source_specs=specs,bundle_manifest=pin(B/'stage_manifest.json',B),bundle_record=pin(B/'accepted_bundle.json',B),narrative_delta=delta,L046_remaining_claims=load(resolve('audit/principal-refutations/L046/v1/remaining_claims.json')))
 assert not(D/'registration_parameters.json').exists();dump(D/'registration_parameters.json',params)
 dump(W/'parameter_summary_v2.json',dict(source_ids=params['source_ids'],packages=len(packages),ordinary_recoveries=2,principal_refutations=4,source_manuscript_entries=sum(len(s['manuscripts'])for s in specs.values()),predecessor_paths=len(files),public_writes=False))
 print(json.dumps(load(W/'parameter_summary_v2.json')))
if __name__=='__main__':main()
