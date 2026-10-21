from pathlib import Path
import json,hashlib,shutil,datetime
S=Path('/Users/sasha/medusa/research/leemans');W=S/'reboot_20261013/N010_amalgamation_distinct';A=S/'corpus106_N010_universal_amalgamation_v1';D=S/'corpus106_N010_universal_amalgamation_independent_review'
def rec(p,base=S):return {'path':str(p.relative_to(base)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
if D.exists():raise ValueError('immutable target exists')
D.mkdir();shutil.copytree(W/'fresh01',D/'fresh01');shutil.copy2(W/'freeze_review.py',D/'freeze_review.py')
deps=[rec(p) for p in A.rglob('*') if p.is_file()]
for x in json.loads((A/'dependencies.json').read_text()):
 p=Path(x['path']);r=rec(p)
 if r['sha256']!=x['sha256']:raise ValueError('source pin')
 deps.append(r)
write(D/'dependencies.json',deps)
review={'status':'ACCEPTED_CONDITIONAL_UNIVERSAL_REGULAR_AMALGAMATION','author':'/root','reviewer':'/root/l044_resume','author_manifest':rec(A/'manifest.json'),'complete_proof_read':True,'fresh_session':80469,'fresh_report':json.loads((W/'fresh01/report.json').read_text()),'native_pages_directly_viewed':[1,2],'source_pages_directly_viewed':[3,4,7],'corrections_requested':[],'contributions':'No mathematical contribution to author proof. Prior source-contract audit is disclosed.','new_question_credit':0,'whole_original_credit':0,'new_measurements':0,'new_Lean_credit':0,'owned_live_handles':[],'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
write(D/'review.json',review)
(D/'review.rst').write_text('''Distinct review: conditional universal regular amalgamation
==========================================================

Accepted unchanged. I read the complete two-page proof, fixed survey Section4,
and exact string-group reconstruction/end-intersection input. Fresh edition
and native replay80469 passed; both native pages were directly viewed. The
checker is expressly not a mathematical proof certificate. No repeated finite
group search is needed for this general proof.

The W action is the flag adjacency right action, so it exists even when the
witness has no transitive automorphism group. A facet relation belongs to the
kernel on every local flag: a regular facet has a free transitive marked flag
action, and changing the starting flag conjugates the faithful local regular
action, preserving its normal kernel. Type-preserving local isomorphisms pay
the same assertion in each facet. The vertex-figure argument is identical.
Thus the normal closure N kills the whole flag action, not merely the base
flag, and the quotient G acts on all flags of the witness.

The exact local identifications are sound in both directions. N_A is killed
in G_A, yielding a surjection from Aut(K). Conversely any W_A word killed in
G fixes all witness flags, in particular the base facet flags, so it belongs
to N_A by the faithful local action. This proves equality of kernels, hence
G_A is the required marked C-group. The same proof pays G_B. It avoids the
invalid general inference that a quotient of a C-group preserves IP.

For g in both end groups the image base flag contains both prescribed end
faces. Strong flag connectivity of their section gives a C-word h with the
same image. Both words are in G_A, whose action on that facet is free, so the
actual group equality g=h holds. Therefore the full end intersection is G_C,
including rank n=2, and the retained end criterion applies. No quotient or
projected intersection property is assumed. The new regular group's local
polytopes have precisely the given marked types, not proper quotients.

For every other witness Q the same global kernel argument gives an equivariant
surjection from the flags of U. Connectivity gives surjectivity. Each face is
an orbit of all adjacency types except its own; its image therefore determines
one face of the same rank, independent of incident flag choice. Incidences and
adjacencies are preserved, so this is a polytope covering. This proves the
advertised universal property, with chosen base flags, for arbitrary witness
polytopes, in particular chiral witnesses with regular local types.

The proof uses regularity of K,L and existence of P essentially. It does not
settle compatibility, unconditional amalgamation, finiteness, or the oriented
chiral-local universal assertion. Those boundaries and the classical retained
reconstruction/end criteria are correctly attributed. No whole original or
new question is credited; no author byte or existing certificate was changed.
''')
write(D/'manifest.json',{'status':review['status'],'exports':[rec(p,D) for p in sorted(D.rglob('*')) if p.is_file() and p.name!='manifest.json']})
print(rec(D/'manifest.json'))
