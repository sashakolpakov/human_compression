"""Freeze subfield exhaustion and the general orbit formula, without numerical-table credit."""
from pathlib import Path
import hashlib,json,sys
from pypdf import PdfReader
W=Path(__file__).resolve().parent;Z=W.parent;S=W.parents[2]
def need(ok,message):
 if not ok:raise ValueError(message)
def pin(p):
 p=Path(p).absolute();h=hashlib.sha256()
 with p.open('rb')as f:
  for b in iter(lambda:f.read(2**20),b''):h.update(b)
 return dict(path=str(p),bytes=p.stat().st_size,sha256=h.hexdigest())
def main():
 need(not(W/'manifest.json').exists(),'fresh proof component');rows={}
 def include(q):
  need(pin(q['path'])==q,'exact acquired binding');need(q['path']not in rows or rows[q['path']]==q,'consistent duplicate');rows[q['path']]=q
 for packet,sha in [(Z/'rank_two_families_root_review','c594e7a8595eb488277d50690091a8929a5ce62fd4ede3b28bfc5e997f84fdb7'),(S/'corpus106_L115_scalar_subspaces_root_adoption','33fb6d9c4cb1aa2808dfd93ac78e5bd67327be13c3c4b38c739ac3fa2278015e')]:
  q=pin(packet/'manifest.json');need(q['sha256']==sha,'exact prior independent acceptance');include(q)
  for e in json.loads((packet/'manifest.json').read_text())['exports']:
   q=pin(packet/e['path']);need((q['bytes'],q['sha256'])==(e['bytes'],e['sha256']),'accepted export');include(q)
  for q in json.loads((packet/'dependencies.json').read_text()):include(q)
 for p in [Path(sys.executable),Path('/opt/homebrew/bin/pdflatex').resolve(),Path('/opt/homebrew/bin/gs').resolve(),Z/'rank_two_families/quotient_controls.py',S/'sources/older_L115_emis.pdf']:
  include(pin(p))
 need(len(PdfReader(W/'native01/subfields.pdf').pages)==6,'six proof pages')
 log=(W/'native01/subfields.log').read_text();need('undefined'not in log.lower()and'Overfull'not in log,'complete native layout')
 (W/'native01/subfields.tex').write_bytes((W/'subfields.tex').read_bytes())
 c=json.loads((W/'orbit_controls01.json').read_text());need(c['status']=='PASS_LITERAL_PROJECTIVE_FROBENIUS_CONTROLS','literal controls pass')
 need([(x['n'],x['d'],x['orbits'])for x in c['rows']]==[(9,3,1),(15,3,41),(15,5,3),(21,3,1791)],'exact complete finite actions')
 (W/'source_pages').mkdir()
 for k in range(1,5):(W/'source_pages'/f'page-{111+k}.png').write_bytes(Path(f'/private/tmp/l115-global-{k:02}.png').read_bytes())
 contract=dict(status='AUTHOR_SOURCE_JOIN_PENDING_DISTINCT_REVIEW',source=pin(S/'sources/older_L115_emis.pdf'),
  source_statements=[dict(label='Lemma6.9/Table8',printed_pages=[111,112,113],disposition='Corrected complete exhaustion: central covers plus torus prime extensions and distinct maximal subfield pairs.'),
  dict(label='Theorem7.1/Tables9–11',printed_pages=[113,114],disposition='Corrected full family list with explicit duplicate-family removal and general total formulas.'),
  dict(label='Local double transitivity column',printed_pages=[114],disposition='Central covers are locally doubly transitive; other families recovered, including q8 exceptions.'),
  dict(label='Section9 unique surviving family claim',printed_pages=[118,119],disposition='Corrected: all central-cover classes also survive for composite absolute field degree.')],
  remaining=[dict(label='Table12',printed_pages=[115],obligation='60 rows: prime-divisor counts, corrected exact totals or source lower bounds, explicit literal source transcription.'),
             dict(label='Section8 diagrams1–29',printed_pages=[116,117,118],obligation='Every numerical diagram label/invariant and multiplicity must be matched, reconstructed or explicitly corrected.')],
  cited_premises=['Previously accepted Suzuki structural list and root coordinates','Accepted preliminary and normalizer proofs','Accepted scalar-subspace correction and orbit equivalence'],
  new_conjecture_credit=0,whole_original_credit=0,Lean_certificate=False,measurement=None)
 (W/'source_contract.json').write_text(json.dumps(contract,indent=2)+'\n')
 (W/'audit.rst').write_text('Subfield parabolics and their Frobenius orbits\n============================================\n\n'
  'The six-page manuscript gives exhaustive subfield families and a general corrected classification.\n'
  'This does not complete the source: its sixty numerical rows and twenty-nine diagrams still have explicit obligations.\n'
  'The scalar-subspace correction and preceding normalizer proof are acquired through exact independent reviews.\n'
  'The new normalizer-condition argument proves every B_s-cover is central.\n'
  'The Frobenius count treats both gcd cases and permits the relative prime r to divide d.\n'
  'The simple-subfield intersection argument explicitly requires field order at least eight; Sz(2) is handled as C5:C4.\n\n'
  'Literal controls enumerate four full projective actions, with 9,585,33 and37449 points.\n'
  'The Kummer model for the last action uses X^7-a over F8; a has order7 and ord_49(8)=7, proving degree7.\n'
  'All Frobenius fixed counts, cycle lengths and orbit totals agree with the formula. No ambient subgroup census occurs.\n'
  'Replay orbit_controls.py --out FRESH_PATH. Author time was3.43seconds.\n'
  'All six final native proof pages and source printed pages111–115 were directly viewed.\n'
  'Source pages118–119 were also read for the final-observation correction.\n'
  'No whole-original, conjecture, Lean or compression credit is claimed by this component.\n')
 (W/'dependencies.json').write_text(json.dumps(list(rows.values()),indent=2)+'\n')
 exports=[]
 for p in sorted(W.rglob('*')):
  if p.is_file():q=pin(p);exports.append(dict(path=str(p.relative_to(W)),bytes=q['bytes'],sha256=q['sha256']))
 (W/'manifest.json').write_text(json.dumps(dict(status='AUTHOR_COMPLETE_L115_SUBFIELD_CLASSIFICATION_AWAITING_DISTINCT_REVIEW',exports=exports,author='l070_publication',proof_pages=6,whole_original_credit=0,new_conjecture_credit=0,Lean_certificate=False),indent=2)+'\n')
 print(json.dumps(dict(manifest=pin(W/'manifest.json'),exports=len(exports),dependencies=len(rows),whole_original_credit=0)))
if __name__=='__main__':main()
