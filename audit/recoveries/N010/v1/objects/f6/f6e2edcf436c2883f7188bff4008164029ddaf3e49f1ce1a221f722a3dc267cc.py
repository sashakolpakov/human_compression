from pathlib import Path
import json,hashlib,shutil,datetime
S=Path('/Users/sasha/medusa/research/leemans');W=S/'reboot_20261013/N010_chamber_distinct';A=S/'corpus106_N010_chamber_words_v1';D=S/'corpus106_N010_chamber_words_independent_review'
def rec(p,base=S):return {'path':str(p.relative_to(base)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
if D.exists():raise ValueError('immutable target exists')
D.mkdir();shutil.copytree(W/'fresh01',D/'fresh01')
for x in ['independent_controls.py','independent_controls.json','freeze_review.py']:shutil.copy2(W/x,D/x)
deps=[rec(p) for p in A.rglob('*') if p.is_file()]
for x in json.loads((A/'dependencies.json').read_text()):
 p=Path(x['path']);r=rec(p);assert r['sha256']==x['sha256'];deps.append(r)
write(D/'dependencies.json',deps)
review={'status':'ACCEPTED_ROTATION_AND_FLAG_WORD_COMPONENT','author':'/root','reviewer':'/root/l044_resume','author_manifest':rec(A/'manifest.json'),'complete_proof_read':True,'fresh_session':45239,'fresh_report':json.loads((W/'fresh01/report.json').read_text()),'native_pages_directly_viewed':[1,2,3],'source_pages_directly_viewed':[3,4,5,6],'independent_controls':json.loads((W/'independent_controls.json').read_text()),'corrections_requested':[],'contributions':'No mathematical contribution to author proof. Prior fixed-source contract audit and independent supplementary controls disclosed.','new_question_credit':0,'whole_original_credit':0,'new_measurements':0,'new_Lean_credit':0,'owned_live_handles':[],'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
write(D/'review.json',review)
(D/'review.rst').write_text('''Distinct review: rotations and closed flag walks
================================================

Accepted unchanged in the exact stated scope. I read the complete proof and
fixed source Sections 2--3, including the actual reconstruction qualification,
then rebuilt and directly viewed all three native pages. The checker certifies
edition and native identity only; acceptance rests on the following proof read.

The change of generators is literal: alpha_i is an involution for i>=2, so
inverting all based rotations fixes those alpha_i. The formulas for sigma_2
and all later consecutive rotations follow without an intersection assumption.
Conversely those formulas fix the involutory alpha_i. Squaring the automorphism
fixes the generating set. This permits the identity automorphism; a separate
chamber-exchanging involution is not silently identified with it.

The action conventions are consistent. Automorphisms act on the left and
commute with adjacency applied in written order. Thus rho_0 rho_1 Phi equals
rho_0(Phi^{r_1})=(rho_0 Phi)^{r_1}=Phi^{r_0 r_1}. The same induction justifies
all word evaluations at the base flag. A flag stabilizer is trivial by flag
connectivity, which pays exact return times, not only divisibility of them.

The explicit local edge changes give h_j and z_j=h_j r_2. The selected incident
face is part of the traversal state: no first-repeat-vertex interpretation is
asserted. Even words preserve a chiral flag orbit; odd words exchange the two.
The displayed cancellation for r_0 s_2 r_0 is correct, and conjugation respects
powers. Therefore z_j squared is exactly the displayed commutator, and its
return time is twice the commutator order; an odd return is excluded by the
two distinct flag orbits. The alternative commutator is conjugate by sigma_2^j.
The regular and chiral formulas coincide with the source, including j=1.

Supplementary controls independently check 3,120 literal identities on all
commuting-end involution triples in Sym(4), and actual 48-flag actions of the
cube and octahedron, including q=4,j=2. The index-two rotation actions verify
the parity return calculation; these regular models are not represented as
examples of genuinely chiral polytopes. They supplement, not replace, the
uniform proof. Both infinite orders and finite periods are covered by the
written freeness argument.

The retained reconstruction theorem still requires the exact intersection
hypotheses. This component does not classify holes or zigzags, prove a finite
universal quotient, or resolve Problem 7. No whole-original, question, Lean,
or numerical-compression credit is granted. No author bytes were changed.
''')
write(D/'manifest.json',{'status':review['status'],'exports':[rec(p,D) for p in sorted(D.rglob('*')) if p.is_file() and p.name!='manifest.json']})
print(rec(D/'manifest.json'))
