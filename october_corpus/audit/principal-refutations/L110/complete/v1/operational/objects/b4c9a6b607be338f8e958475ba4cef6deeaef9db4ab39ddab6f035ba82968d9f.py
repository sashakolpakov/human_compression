from pathlib import Path
import ast,hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans');Y=S/'geometry/suzuki_incidence';F=S/'computation/f009'
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def put(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def pin(p):b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())

# Root-authored proof is submitted for distinct review, not self-accepted.
C=Y/'torus_extension_necessity';c=m.Closure()
for p in ['higher_families_root_review','normalizer_restrictions_root_review','preliminary_scope_root_review','higher_source_review01']:
 c.packet('geometry/suzuki_incidence/'+p)
c.add(S/'sources/catalogue_L110.txt');c.add(__file__)
put(C/'dependencies.json',list(c.files.values()))
put(C/'claims.json',dict(author='root',status='PENDING_DISTINCT_REVIEW',native_pages=5,claims=['Self-normalization and unique subfield overgroups for a cyclic torus subgroup with its full complement','Gcd intersections through a common full torus subgroup, with nonsplit rotation order above5','Residual primitivity forces a squarefree relative divisor lattice','Every rank-four extension of the specified R10/R11 residue has the displayed three-field and torus lattice','Every rank-four extension of the specified R13 residue has standard subfield intersections'],qualifications=['Classical subgroup structure and accepted compatible torus construction are premises','No general higher-rank classification claimed','L110 whole-source hold remains until the claim ledger incorporates distinctly reviewed arguments'],collaboration='j3_recovery checked the torus-normalizer crux, discussed divisor induction, and requested explicit coordinate alignment and the impossible equal-prime R11 case. The present manuscript and Ω proof were written by root; no independent discovery is claimed.',whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None))
exports=[]
for p in sorted(C.iterdir()):
 if p.is_file() and p.name!='manifest.json':r=pin(p);r['path']=p.name;exports.append(r)
assert not(C/'manifest.json').exists()
put(C/'manifest.json',dict(status='ROOT_AUTHOR_L110_TORUS_EXTENSION_NECESSITY_PENDING_DISTINCT_REVIEW',exports=exports));print(json.dumps(pin(C/'manifest.json')))

# Distinct mathematical review of the agent-authored split-extension argument.
assert pin(Y/'split_extension_necessity/manifest.json')['sha256']=='35de3b89fe8cbb9e234533e6a1feb0e252ad54f1f458d5d242a0a814751e8168'
c=m.Closure();c.packet('geometry/suzuki_incidence/split_extension_necessity');c.add(__file__)
for p in Path('/private/tmp/l110_split_necessity_root01').rglob('*'):
 if p.is_file():c.add(p)
status='ACCEPTED_L110_SPLIT_RESIDUE_EXTENSION_NECESSITY'
c.finish('geometry/suzuki_incidence/split_extension_necessity_root_review',status,dict(status=status,author='j3_recovery',reviewer='root',collaboration='The proof route, scalar irreducibility and intermediate affine overgroups were discussed collaboratively. This is a distinct check of the agent-authored complete manuscript, not a claim of independent discovery.',review=[
 'Read every line of the four-page proof and compared it with source R7/R9. Fresh TeX rebuild has four byte-identical native page streams; viewed every rebuilt page. All declared dependencies are reacquired.',
 'The affine containment lemma is valid: odd scalar order excludes nonsplit occurrence; the generating scalar field forces the degree; the Weyl involution or the central additive coordinate1 removes the diagonal transporter. Prime-index subfield arithmetic permits repeated primes in the base.',
 'Residual strictness and scalar generation force G2 into the split normalizer and G3 into the point stabilizer. The radical is exactly Z_q; the alternative Q_q contradicts the prescribed meet. In the affine quotient, commuting with a nonidentity scalar forces every translation component to vanish.',
 'At G3, all three candidate intersections have proper intermediate overgroups unless the full cyclic meet is H_d. The two cases of prime index in G2 then force d=M. The final panels force the two distinct additional primes and the full intersection lattice.',
 'The R7 G4/G3 typo and incorrect printed n-prime quotient condition are identified and corrected explicitly. The global classification is not used. This settles the conditional rank-four necessity for R7/R9; the whole L110 ledger remains held until the other conditional claims are incorporated.'
]))

# Concrete finite owner request. No scientific coverage is granted by release.
C=F/'sharing_session_resume01';P=F/'streaming_session_resume03'
assert pin(C/'manifest.json')['sha256']=='3724a713150ac64e2d3e6affdcf57ee861fe585cd1113720821a920ee1c494c9'
a=ast.parse((C/'owner.py').read_text());b=ast.parse((P/'owner.py').read_text())
fa={x.name:ast.dump(x) for x in a.body if isinstance(x,ast.FunctionDef)};fb={x.name:ast.dump(x) for x in b.body if isinstance(x,ast.FunctionDef)}
assert [k for k in fa if fa[k]!=fb[k]]==['validate','gate']
assert(C/'resource_guard.py').read_bytes()==(P/'resource_guard.py').read_bytes()
r=json.loads(Path('/private/tmp/f009_resume01_root_controls.json').read_text());assert r['status']=='PASS_INITIAL_SHARING_RESUME_CONTROLS' and len(r['checks'])==26
c=m.Closure();c.packet('computation/f009/sharing_session_resume01');c.packet('computation/f009/sharing_session1324_v2_root_review');c.add('/private/tmp/f009_resume01_root_controls.json');c.add(__file__)
status='ACCEPTED_F009_INITIAL_SHARING_TWO_INTERVAL_OWNER_REQUEST'
c.finish('computation/f009/sharing_session_resume01_root_review',status,dict(status=status,author='finite_recoveries',reviewer='root',release=dict(start=1324,end=14476,intervals=2,target_seconds_each=300,total_target_seconds=600,automatic_successor=False,rss_cap_bytes=4*1024**3,disk_reserve_bytes=4*1024**3,output_cap_bytes=2*1024**3,phase_wall_seconds=7200),review=['Read complete owner and validation delta; verified all execution/guard code unchanged and only validate/gate functions differ from the reviewed predecessor. Fresh actual26 controls passed. Exact1324 parent, complete dictionary, separate coverage/snapshot gates and predecessor bootstrap observation are bound. Both dictionaries must be independently acquired in the bounded batch before any writer; there is no second standalone full bootstrap. Release grants no coverage or source completion.']))

# Acquire the complete child union; no additional target execution.
F4=S/'computation/f004';H=F4/'q8_branch53_child22_union_handoff01'
assert pin(H/'manifest.json')['sha256']=='41756eb6e8fee2f7729dbf797e7a8b97593743496b43a869bafb02b161071773'
h=json.loads((H/'handoff01.json').read_text());p=Path('/private/tmp/f004_q8_child22_root_union01.json')
assert p.read_bytes()==Path(h['result']['path']).read_bytes()
c=m.Closure();c.packet('computation/f004/q8_branch53_child22_union_handoff01');c.packet('computation/f004/q8_branch53_child22_candidates_root_review');c.add(p);c.add(__file__)
status='ACCEPTED_F004_Q8_BRANCH53_CHILD22'
c.finish('computation/f004/q8_branch53_child22_root_adoption',status,dict(status=status,author='finite_recoveries',reviewer='root',review='Fresh independent union acquisition with the unchanged accepted collector read all2739 inputs and all511 candidates, obtained zero positive tuples, and produced a byte-identical result to the author. Exactly child22 is now complete; branch53 and the field remain incomplete.',candidate_count=511,tuple_count=0,child_index=22,child_credit=1,branch_credit=0,field_credit=0,source_credit=0))
