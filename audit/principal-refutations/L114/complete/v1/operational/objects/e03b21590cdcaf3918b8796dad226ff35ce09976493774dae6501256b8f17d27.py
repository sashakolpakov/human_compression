from pathlib import Path
import hashlib,json,datetime
S=Path('/Users/sasha/medusa/research/leemans');B=S/'geometry/suzuki_subgroups';P=B/'preliminaries';R=B/'preliminaries_distinct_run01';W=B/'preliminaries_distinct_review';assert not W.exists();W.mkdir()
def pin(p):
 p=Path(p).absolute();b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
rows={}
def include(q):
 assert pin(q['path'])==q
 if q['path']in rows:assert rows[q['path']]==q
 rows[q['path']]=q
q=pin(P/'manifest.json');assert q['sha256']=='f8234485599a4af33c4e01b32c2a31e42105498fa9c18b04a8878c7ad47e53b4';include(q)
for x in json.loads((P/'manifest.json').read_text())['exports']:
 q=pin(P/x['path']);assert(q['bytes'],q['sha256'])==(x['bytes'],x['sha256']);include(q)
for q in json.loads((P/'dependencies.json').read_text()):include(q)
for p in R.iterdir():
 if p.is_file():include(pin(p))
for p in [Path('/private/tmp/review_l115_preliminaries.py'),Path(__file__)]:include(pin(p))
assert (P/'native03/preliminaries.tex').read_bytes()==(P/'preliminaries.tex').read_bytes()
checks=json.loads((R/'report.json').read_text());assert checks['status']=='PASS_FRESH_PRELIMINARY_CONTROLS';assert all(x['returncode']==0 and not x['timeout'] and x['stderr']['bytes']==0 for x in checks['processes'])
review=dict(status='ACCEPTED_L115_PRELIMINARY_RESULTS_WITH_DOMAIN_CORRECTION',author='root',reviewer='l070_publication',roles='Distinct source and proof review; reviewer did not author the manuscript or controls.',author_manifest=pin(P/'manifest.json'),fresh_controls=pin(R/'report.json'),source_statements=['Lemma3.1','Lemma3.2','Lemma3.3','Lemma3.4','Lemma3.5','Lemma3.6','Lemma3.7','Lemma5.1','Lemma5.2','Lemma5.3','Lemma6.1'],source_statement_count=11,scope='Surviving preliminary results only; Lemma3.2 carries the explicit domain correction.',source_pages_directly_viewed=[99,100,101,102,103,104,105],native_proof_pages_directly_viewed=[1,2,3,4,5],tex_native_source_bytes_identical=True,mathematical_findings=[
'The four residues modulo s^2+1 have nonzero absolute representatives below the modulus; coprimality and the product factorization yield the composite-factor assertions for proper subfields.',
'The printed Lemma3.2 omits r>1. At q=s=8 its literal assertion fails since q-1=7. The corrected claim needs s>2 and r>1; other arithmetic domains match the simple Suzuki convention.',
'The Frattini lifting lemma follows from P=(M intersect P)Z and the generating property. The square map exhausts Z because gcd(theta+1,q-1)=1; quotient hyperplanes give the reverse containment.',
'Affine averaging works with a nonfaithful action since |H| is prime to the characteristic. Irreducibility is explicitly over the prime field, which is necessary for the maximal-subgroup argument.',
'For a cyclic odd normal subgroup, an omitted normal factor gives a prime quotient; affine averaging conjugates its complement. This proves all maximal classes, including m=1 and nonfaithful complement actions.',
'The unique-overgroup obstruction uses a primitive constituent of the point residue. Firmness makes every type nontrivial, hence every parabolic proper. If G_i lies in B, the opposite-flag stabilizer equals the chamber stabilizer and its extension index is one. No truncation assertion is used.',
'The Suzuki application uses the stated maximal-subgroup classification: other types cannot contain the elementary abelian Z, by their Sylow two-subgroups; a nonidentity root-group element has exactly one fixed ovoid point.',
'The root-group scalar parameter is consistent with the source after t maps to t^theta. In particular gcd(theta+2,q-1)=1 follows from theta=-2 and theta^2=2 modulo a common odd divisor, so the displayed Z semidirect H has the expected full scalar action.'
],borrowed_premises=['Suzuki maximal-subgroup classification','Classical faithful root-group and ovoid realization','GAP operations are finite control premises only; the general results are proved in the manuscript'],finite_controls=dict(odd_exponents=50,subfield_parameters=240,point_stabilizer_q=8,cyclic_actions=34),preserved_failure='author01: FactorsInt(1)=[1] harness error; unchanged failed outputs are not evidence.',remaining=['All other Section6 statements','Corrected family list and Tables2–12','Global counts','Whole-original source review'],whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None,reviewed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
(W/'review.json').write_text(json.dumps(review,indent=2)+'\n')
(W/'review.rst').write_text('Distinct review of the Suzuki preliminary results\n================================================\n\nThe eleven stated preliminary source results are accepted with the explicit\nproper-subfield correction to Lemma 3.2. The frozen author manuscript and all\nfive final native pages were read, together with source pages 99--105. The\narithmetic reduction, two maximal-subgroup arguments, and all-rank geometric\nobstruction are mathematically sound under the listed classical premises.\n\nFresh ordinary-Python and bounded GAP controls passed. They supplement the\nproofs; they do not establish the arbitrary-parameter theorems by sampling.\nThe first failed FactorsInt(1) harness and its outputs remain unchanged.\nEvery acquired binding was freshly checked again while sealing this review.\n\nThe proof of the geometric obstruction also uses properness of every\nparabolic: firmness supplies at least two elements of every type. This\njustifies applying the unique-maximal-overgroup argument to G_i. The\nconclusion follows from the corank-one flag index, in every rank.\n\nNo complete L115 recovery, open-conjecture result, Lean theorem or compression\nmeasurement is admitted by this component. Attribution and the separate\nscalar-subspace correction are retained.\n')
(W/'dependencies.json').write_text(json.dumps(list(rows.values()),indent=2)+'\n')
exports=[]
for p in sorted(W.iterdir()):
 q=pin(p);exports.append(dict(path=p.name,bytes=q['bytes'],sha256=q['sha256']))
(W/'manifest.json').write_text(json.dumps(dict(status=review['status'],exports=exports,whole_original_credit=0),indent=2)+'\n');print(json.dumps(dict(manifest=pin(W/'manifest.json'),dependencies=len(rows),source_statements=11,whole_original_credit=0)))
