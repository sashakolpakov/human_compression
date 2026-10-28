"""UNRUN corpus-relative supplied Fi22 invariant-subset replay.
New author /root/middle_dictionary_author. Retained6538 context/transitivity
and unchanged60ee/70ab providers;74b-derived explicit relative IO boundary.
Historical Root records are data, never new gate/caller or paid authority.
"""
import time
START=time.monotonic()
import argparse,hashlib,json,math,os,resource,signal,stat,struct,sys
from pathlib import Path,PurePosixPath
ENV4=('COVERAGE_PROCESS_START','COVERAGE_PROCESS_CONFIG','OPENSSL_CONF','OPENSSL_MODULES')
SCOPE='7795d9d9d4bbf392cb5a943053372149950eef15d4bd468a63e0cc41f5fcce3a'
SELECTOR=dict(first_block_index=2,endpoint_position=18,local_class_position=164,middle_block_index=2,first_ambient_class_position=13,middle_ambient_class_position=13)
WORKER_SHA='6538cdb65314e9c275dc72fdf88c130f8887567257784c77901ea2a563d5022d'
POINT_SHA='60eedb3ce207831ec66cdcc18c689c7c5e334205772cabf888f950503cc267ee'
SUBSET_SHA='70ab578386e5829b81b59e35657a9eef8af81793043e48237b8d88acb0d284da'


def need(ok,message):
    if not ok:raise ValueError(message)

def can(value):return(json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()

def decode(raw):
 def pairs(items):
  out={}
  for k,v in items:need(k not in out,'unique JSON keys');out[k]=v
  return out
 def floating(text):
  value=float(text);need(math.isfinite(value),'finite JSON float');return value
 return json.loads(raw,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda x:(_ for _ in()).throw(ValueError(x)))

def relative(text):
 need(type(text)is str and text and text.isascii(),'literal relative path')
 path=PurePosixPath(text)
 need(not path.is_absolute()and str(path)==text and not set(path.parts)&{'.','..','.git','__pycache__','.lake'},
      'relative corpus artifact only, no private fallback')
 return Path(*path.parts)

def reference_key(reference):
 need(type(reference)is dict and set(reference)=={'path','bytes','sha256'}
      and type(reference['path'])is str and type(reference['bytes'])is int
      and 0<=reference['bytes']<=2**21 and type(reference['sha256'])is str
      and len(reference['sha256'])==64 and set(reference['sha256'])<=set('0123456789abcdef'),
      'complete bounded original identity')
 return(reference['path'],reference['bytes'],reference['sha256'])

class Budget:
 def __init__(self,root):
  need(type(root)is Path or isinstance(root,Path),'explicit Path root')
  need(root.is_absolute()and root.resolve(strict=True)==root,'canonical explicit corpus root')
  self.root=root;self.maps={};self.refs={};self.raw={};self.bytes=0
  self.peak=0;self.work=None
 def tick(self):
  rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
  self.peak=max(self.peak,rss)
  need(rss<128*2**20 and time.monotonic()-START<140,'128MiB140s portable point replay envelope')
 def physical(self,reference,again=False):
  self.tick();reference_key(reference);name=str(relative(reference['path']))
  need(self.refs.get(name,reference)==reference,'one exact physical identity')
  if name in self.raw and not again:return self.raw[name]
  need(self.bytes+reference['bytes']<=8*2**20 and(name in self.refs or len(self.refs)<32),
       '8MiB32paths includes every physical reread')
  if self.work is not None:self.work.charge(reference['bytes'],'every_actual_relative_physical_input_byte')
  path=self.root/relative(name);before=path.lstat()
  need(path.resolve(strict=True)==path and path.is_relative_to(self.root)
       and stat.S_ISREG(before.st_mode)and before.st_nlink==1 and before.st_size==reference['bytes'],
       'canonical single-link relative ordinary input')
  with path.open('rb')as stream:
   opened=os.fstat(stream.fileno());raw=stream.read(reference['bytes']+1);after=os.fstat(stream.fileno())
  signature=lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
  need(signature(before)==signature(opened)==signature(after)==signature(path.lstat())
       and len(raw)==reference['bytes']and hashlib.sha256(raw).hexdigest()==reference['sha256'],
       'fresh whole relative content, never an original-machine path read')
  self.refs[name]=dict(reference);self.raw[name]=raw;self.bytes+=len(raw);return raw
 def bind(self,rows):
  need(type(rows)is list and 1<=len(rows)<=90,'finite explicit original-to-relative map')
  maps={}
  for row in rows:
   need(type(row)is dict and set(row)=={'original','relative'},'explicit complete mapping row')
   key=reference_key(row['original']);name=str(relative(row['relative']))
   need(key not in maps,'one original complete identity mapping')
   maps[key]=dict(path=name,bytes=key[1],sha256=key[2])
  self.maps=maps
 def read(self,reference,again=False):
  key=reference_key(reference);need(key in self.maps,'all original reads require explicit included mapping')
  return self.physical(self.maps[key],again)
 def doc(self,reference):return decode(self.read(reference))
 def recheck(self):
  for reference in list(self.refs.values()):self.physical(reference,True)


class Work:
    def __init__(self,check,cap=10000000,seconds=20):
        need(type(cap)is int and 0<cap<=10000000 and type(seconds)in(int,float)and 0<seconds<=20,'unchanged finite shared work cap')
        self.units=0;self.cap=cap;self.seconds=seconds;self.start=time.monotonic();self.check=check;self.labels={}
    def charge(self,amount,label):
        need(type(amount)is int and amount>=0,'typed nonnegative complete work charge');self.check()
        need(amount<=self.cap-self.units and time.monotonic()-self.start<self.seconds,'shared10M/20s point/field/framing budget')
        self.units+=amount;self.labels[label]=self.labels.get(label,0)+amount

def document(budget,ref,work):
    work.charge(2*ref['bytes'],'complete_config_or_retained_JSON_byte_admission')
    return budget.doc(ref)

def imported_context(plan,budget,work):
    need(plan['scope_digest']==SCOPE and plan['original_selector']==SELECTOR,'same currently acquired original endpoint/middle subject')
    R=plan['roles']
    def document(name):
        work.charge(2*R[name]['bytes'],'complete_retained_premise_JSON_byte_admission')
        return budget.doc(R[name])
    a=document('operand_adoption');f=document('free_adoption')
    need(a['schema']=='ROOT_ACCEPTED_L026_PRIME_CYCLE_OPERAND_DATA_V1'and a['root']=='/root'and a['adopted']is True
        and f['schema']=='ROOT_L026_ACCEPTED_FREE_PRODUCT_WITNESS_PROJECTION_V1'and f['root']=='/root'and f['adopted']is True
        and a['operand_bytes']==52658 and f['free_rows']==28908
        and a['all28908_generation_questions_unresolved']is f['all28908_generation_questions_unresolved']is True,
        'actual metadata operand/witness adoptions, not a transferred scientific verdict')
    need(a['outputs']['operands.bin']==R['operands']and a['outputs']['premises.json']==R['operand_premises']
        and a['outputs']['byte_inverse.json']==R['operand_inverse']and a['outputs']['projection.json']==R['operand_projection']
        and f['outputs']['free_witnesses.bin']==R['witnesses']and f['outputs']['projection.json']==R['free_projection'],
        'exact whole adopted byte/framing/premise outputs')
    premises=document('operand_premises');inverse=document('operand_inverse');projection=document('operand_projection');free=document('free_projection')
    need(premises['schema']=='L026_PRIME_CYCLE_OPERAND_RETAINED_PREMISES_V1'
        and premises['exact_original_scope']==projection['scope_digest']==free['scope_digest']==SCOPE
        and premises['path_max']==10 and premises['d_image_elementary_map_bound']==21
        and premises['b_image_elementary_map_bound']==63 and premises['rotation_image_elementary_map_bound']==64
        and premises['seed_equals_first_Q_vector_proved_by_same_accepted_compact_identity']is True
        and projection['qualified_original_a_c_d0_A_and_tree']is True
        and inverse['schema']=='L026_PRIME_CYCLE_OPERAND_EXACT_BYTE_INVERSE_V1'
        and free['free_projected']==28908 and free['exact_literal_record_bytes']is True,
        'actual complete operand/witness identity with retained exact inverse, scope and path bounds')
    imports=premises['inherited_member_and_Reader_imports']
    need(imports['original_G_normal_in_A']is True and imports['GAP_IsNormal_A_G_means_G_normal_in_A']is True
        and imports['same_accepted_original_degree3510_action']is True
        and imports['original_exact_orders_and_full_class_predicates_borrowed']is True
        and premises['named_group_or_class_or_GAP_classification_reproved']is False
        and 'GLOBAL block2 class'in premises['qualification']and 'H=B'in premises['qualification'],
        'explicit imported known-G seed/normality/faithful Reader/class/graph/two-fibre/qualified H=B meanings')
    theorem=document('maximal_orders');review=document('theorem_review');note=document('theorem_source_note');handoff=document('theorem_handoff')
    work.charge(2*R['theorem_argument']['bytes'],'whole_written_theorem_byte_admission')
    budget.read(R['theorem_argument'])
    need(theorem['schema']=='FI22_COMPLETE_SIMPLE_MAXIMAL_ORDER_PREMISE_V1'and theorem['named_group']=='Fi22'
        and theorem['classification_is_borrowed']is True and theorem['completeness_independently_reproved_here']is False
        and theorem['Aut_Fi22_substitution_permitted']is False and theorem['conjugacy_classes']==14,
        'borrowed complete simple Fi22 classification with1988 correction; not Aut substitution')
    rows=theorem['rows'];need(type(rows)is list and len(rows)==12,'all twelve types/fourteen conjugacy classes')
    total=0
    for row in rows:
        work.charge(64,'whole_imported_maximal_order_divisibility_row')
        n,k=row['order'],row['conjugacy_classes']
        need(type(n)is type(k)is int and n>0 and k>0 and not(n%11==n%13==0)
            and row['divisible_by_11']==(n%11==0)and row['divisible_by_13']==(n%13==0),
            'every imported proper maximal omits one prime')
        total+=k
    need(total==14 and review['schema']=='DISTINCT_FI22_PRIME_CYCLE_WRITTEN_THEOREM_REVIEW_V1'
        and review['status']=='PASS_DISTINCT_FI22_PRIME_CYCLE_WRITTEN_THEOREM'and review['reviewer']==review['actor']=='/root'
        and review['blockers']==[]and review['all14_maximal_classes_accounted_for']is True
        and review['exact_G_membership_required']is True and review['Aut_G_substitution_forbidden']is True
        and review['maximal_avoidance_and_point_cycle_proof_accepted']is True
        and review['source_handoff']==R['theorem_handoff'],'same actual written-theorem review only, not a current checker verdict')
    need(handoff['artifacts']['ARGUMENT.rst']==R['theorem_argument']and handoff['artifacts']['maximal_orders.json']==R['maximal_orders']
        and handoff['artifacts']['source_note.json']==R['theorem_source_note']
        and note['actual_input_gate_and_point_action_premises']['original_input_acceptance']==premises['original_input']
        and note['actual_input_gate_and_point_action_premises']['point_bridge_acceptance']==premises['whole_old_proof_roles']['bridge_root'],
        'exact same original G/Reader/bridge membership and classified theorem source lineage')
    return dict(premises=premises,adopted_operand=a,adopted_witness=f,qualification=premises['qualification'])

def transitivity(plan,budget,work,imports):
    R=plan['roles'];premises=imports['premises']
    root=document(budget,R['original_input'],work)
    bridge_root=document(budget,R['bridge_adoption'],work)
    bridge=document(budget,R['bridge_certificate'],work)
    table=document(budget,R['maximal_orders'],work)
    need(R['original_input']==premises['original_input']==premises['whole_old_proof_roles']['input_root']
         and R['bridge_adoption']==premises['whole_old_proof_roles']['bridge_root']
         and R['bridge_certificate']==premises['whole_old_proof_roles']['bridge_carrier'],
         'exact same accepted original normal-G and whole point bridge')
    need(root['schema']=='ROOT_L026_FI22_NORMAL_AMBIENT_INPUT_ACCEPTANCE_V1'
         and root['root']=='/root'and root['status']=='ROOT_ACCEPTED_CONDITIONAL_FI22_NORMAL_AMBIENT_INPUTS'
         and root['full_Aut_conditional_on_named_Fi22_and_Out2']is True,
         'retained original named-simple-Fi22/full-Aut conditional scope')
    summary=root['summary'];need(summary['degree']==3510
         and summary['group_order']==64561751654400 and summary['ambient_order']==2*summary['group_order'],
         'actual original degree and normal index-two orders')
    need(bridge_root['schema']=='ROOT_ACCEPTED_FI22_ORIGINAL_POINT_ACTION_BRIDGE_V1'
         and bridge_root['root']=='/root'and bridge_root['adopted']is True
         and bridge_root['strict_Saved_status']=='VERIFIED'
         and bridge_root['input_gate']==R['original_input']
         and bridge_root['saved_certificate']==R['bridge_certificate'],
         'actual adopted complete original A point-action bridge')
    need(bridge['schema']=='FI22_ORIGINAL_3TRANSPOSITION_ACTION_BRIDGE_V1'
         and bridge['status']=='VERIFIED'and bridge['input_gate']==R['original_input']
         and bridge['premises']['original_G_normal_in_A']is True
         and bridge['premises']['same_accepted_original_degree3510_action']is True,
         'retained actual bridge normality and equivariant faithful action meaning')
    action=bridge['point_action'];vertices=action['vertices'];parents=action['parents'];labels=action['labels']
    work.charge(32*3510,'entire accepted ambient spanning-tree field and coverage checks')
    need(len(vertices)==len(parents)==len(labels)==3510 and set(vertices)==set(range(3510))
         and all(type(x)is int for x in vertices)and vertices[0]==action['root']==2961
         and parents[0]is None and labels[0]==0,'whole original rooted spanning point-tree')
    for i in range(1,3510):
        need(type(parents[i])is int and 0<=parents[i]<i and type(labels[i])is int
             and labels[i]in(-2,-1,1,2),'accepted original signed ambient spanning edges')
    for row in table['rows']:
        work.charge(64,'each_retained_complete_maximal_order_index_bound')
        need(summary['group_order']%row['order']==0 and summary['group_order']//row['order']>=3510,
             'every proper maximal in the imported complete simple-G list has index at least3510')
    # A is transitive by the accepted tree. Normal index-two G would otherwise
    # have two orbits of size1755, contradicting the complete minimal-index bound.
    # No actual G orbit, new primitive action or image is being inferred from A alone.
    return dict(original_input=R['original_input'],point_bridge=R['bridge_adoption'],
                complete_simple_maximal_table=R['maximal_orders'],G_transitivity_derived=True,
                degree=3510,minimal_proper_G_index=3510,
                qualification=imports['qualification'])

def bound_row(raw,index,work):
    work.charge(96,'whole_exact_free_owner_record_and_digest')
    record=raw[16*index:16*index+16];owner,partner,mass,x,y,z=struct.unpack('<IIHHHH',record)
    need(owner<500178 and partner<500178 and mass==1024,'actual adopted free product witness')
    return owner,hashlib.sha256(record).hexdigest(),(x,y,z)

def supplied(raw,plan,work):
    work.charge(2*len(raw),'complete_supplied_positive_subset_JSON')
    value=decode(raw)
    need(raw==can(value)and type(value)is dict and set(value)=={'schema','scope_digest','original_selector',
         'operand_adoption','free_witness_adoption','records'}
         and value['schema']=='L026_SUPPLIED_ROTATION_PROPER_SUBSETS_V1'and value['scope_digest']==SCOPE
         and value['original_selector']==SELECTOR and value['operand_adoption']==plan['roles']['operand_adoption']
         and value['free_witness_adoption']==plan['roles']['free_adoption'],'whole canonical supplied subset subject')
    rows=value['records'];need(type(rows)is list and len(rows)<=16,'bounded supplied positive records')
    indices=[]
    for r in rows:
        need(type(r)is dict and set(r)=={'free_index','owner','witness_row_sha256','points'}
             and type(r['free_index'])is int and r['free_index']in plan['selected_free_indices'],
             'exact actual selected positive subset record')
        indices.append(r['free_index'])
    expected=plan['expected_positive_free_indices']
    need(type(expected)is list and all(type(i)is int for i in expected)
         and expected==sorted(set(expected))and indices==expected,'all and only announced supplied positives')
    return rows

def mapped_same(budget,left,right):
    a,b=reference_key(left),reference_key(right)
    need(a in budget.maps and b in budget.maps and budget.maps[a]==budget.maps[b],
         'both complete historical aliases map to the same entire corpus object')

def load_provider(reference,budget,work,names):
    raw=budget.read(reference);work.charge(2*len(raw),'whole_actual_kernel_Source_declaration')
    physical=budget.maps[reference_key(reference)];filename=str(budget.root/relative(physical['path']))
    ns={'__name__':'fi22_corpus_subset_provider','__file__':filename}
    exec(compile(raw,filename,'exec'),ns)
    for name in names:
        need(ns[name].__globals__ is ns and ns[name].__code__.co_filename==filename,
             'unchanged authenticated kernel under its actual corpus filename, never old host namespace')
    return ns

def historical_subject(plan,budget,work,carrier):
    adoption=document(budget,plan['adoption'],work);result=document(budget,plan['historical_result'],work)
    prior=document(budget,plan['historical_plan'],work);gate=document(budget,plan['historical_gate'],work)
    review=document(budget,plan['historical_review'],work);controls=document(budget,plan['historical_controls'],work)
    peer=document(budget,plan['historical_peer'],work)
    need(adoption['schema']=='ROOT_ACCEPTED_L026_ROTATION_INVARIANT_SUBSET_NONGENERATION_V1'
         and adoption['root']=='/root'and adoption['adopted']is True
         and adoption['scope_digest']==SCOPE and adoption['proof_category']=='ROTATION_INVARIANT_SUBSET'
         and adoption['new_subset_count']==12 and adoption['new_subset_mass']==12288
         and adoption['new_generation_IP_reversal_census_Original_conjecture_Lean_or_measurement_credit']==0,
         'actual historical0129 twelve-negative category only; no new adoption')
    need(result['schema']=='L026_BOUNDED_ROTATION_SUBSET_RESULT_V1'and result['mode']=='check'
         and result['status']=='SUPPLIED_CHECK_COMPLETE'and result['scope_digest']==SCOPE
         and result['program']['sha256']==WORKER_SHA and result['supplier_activated']is False
         and result['strict_check_activates_supplier']is False
         and result['marking_nongeneration_uses_additional_imported_original_middle_involution_and_simpleG']is True
         and result['generation_IP_reversal_census_Original_conjecture_Lean_or_measurement_credit']==0,
         'exact original6538 supplied-only proof identity and explicit qualifications')
    need(prior['schema']=='L026_ROTATION_INVARIANT_SUBSET_PLAN_V1'and prior['mode']=='check'
         and prior['program']==result['program']and prior['roles']==plan['roles']
         and prior['scope_digest']==plan['scope_digest']==SCOPE
         and prior['original_selector']==plan['original_selector']==SELECTOR
         and prior['selected_free_indices']==plan['selected_free_indices']==list(range(16))
         and prior['maximum_subset_points']==plan['maximum_subset_points']==512,
         'whole original historical mathematical context and selected sixteen-owner window')
    for left,right in[(adoption['actual_strict_result'],plan['historical_result']),
                      (adoption['actual_supplied_carrier'],plan['carrier']),(prior['records'],plan['carrier']),
                      (result['plan'],plan['historical_plan']),(result['program'],plan['mathematical_parent']),
                      (prior['point_kernel'],plan['point_kernel']),(prior['subset_kernel'],plan['subset_kernel'])]:
        mapped_same(budget,left,right)
    need(gate['schema']=='ROOT_AUTHORIZED_L026_ROTATION_INVARIANT_SUBSETS_V1'and gate['root']=='/root'
         and gate['adopted']is True and gate['program']==result['program']and gate['plan']==plan['historical_plan'],
         'old gate retained as exact historical data, never this replay authority')
    mapped_same(budget,gate['Root_code_math_review'],plan['historical_review'])
    mapped_same(budget,gate['control_report'],plan['historical_controls'])
    need(review['root']=='/root'and review['status']=='SUPPORTED'and review['blockers']==[]
         and review['program']==result['program']and review['plan']==plan['historical_plan']
         and review['point_kernel']==prior['point_kernel']and review['subset_kernel']==prior['subset_kernel']
         and review['G_transitivity_and_even_subgroup_proof_reviewed']is True,
         'same retained original context/transitivity/involution-simpleG written review')
    need(controls['schema']=='L026_INVARIANT_SUBSET_GENERIC_CONTROLS_V1'and controls['status']=='PASS'
         and controls['worker']==result['program']and controls['point_kernel']==prior['point_kernel']
         and controls['subset_kernel']==prior['subset_kernel']and controls['program']==prior['control_program']
         and controls['controls']==14 and controls['original_case_calls']==0,
         'old fourteen controls are historical subjects, not new-control PASS transfer')
    need(peer['schema']=='INDEPENDENT_L026_INVARIANT_SUBSET_METHOD_REVIEW_V1'
         and peer['status']=='SUPPORTED_STATIC_METHOD_AND_CONTROL_BOUNDARY'and peer['blockers']==[]
         and peer['subjects']['program']==result['program']and peer['subjects']['point_kernel']==prior['point_kernel']
         and peer['subjects']['subset_kernel']==prior['subset_kernel'],
         'exact retained scientific-source peer, with original model/action imports retained')
    expected=[0,2,4,6,7,8,9,11,12,13,14,15]
    need(plan['expected_positive_free_indices']==prior['expected_positive_free_indices']==expected
         and [r['free_index']for r in result['verified_nongeneration_records']]==expected
         and [r['free_index']for r in adoption['new_facts']]==expected,
         'every and only the twelve adopted positive records; no current-unpaid query')
    need(carrier['operand_adoption']==plan['roles']['operand_adoption']
         and carrier['free_witness_adoption']==plan['roles']['free_adoption'],
         'same actual adopted operand and original free-middle witness context')
    return adoption,result

def main():
    need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize and all(k not in os.environ for k in ENV4),'minimal EBS/ENV4 replay interpreter')
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in()).throw(TimeoutError('140s relative Fi22 subset replay')))
    signal.setitimer(signal.ITIMER_REAL,max(.001,140-(time.monotonic()-START)))
    ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--corpus-root',required=True)
    ap.add_argument('--self-sha256',required=True);ap.add_argument('--plan',required=True);ap.add_argument('--plan-sha256',required=True)
    args=ap.parse_args();budget=Budget(Path(args.corpus_root));work=Work(budget.tick);work.start=START;budget.work=work
    own=Path(__file__).resolve(strict=True);need(own.is_relative_to(budget.root),'actual replay Source inside corpus')
    ownref=dict(path=str(own.relative_to(budget.root)),bytes=own.stat().st_size,sha256=args.self_sha256)
    need(ownref['bytes']<=65536,'whole bounded new Source')
    budget.bytes+=ownref['bytes']+4;work.charge(3*ownref['bytes']+4,'interpreter_bootstrap_and_current_Source_declaration')
    budget.physical(ownref)
    pp=budget.root/relative(args.plan);pref=dict(path=args.plan,bytes=pp.stat().st_size,sha256=args.plan_sha256)
    need(pref['bytes']<=65536,'bounded entire actual replay plan')
    praw=budget.physical(pref);work.charge(2*len(praw),'complete_actual_replay_config_JSON');plan=decode(praw)
    need(plan['schema']=='L026_CORPUS_RELATIVE_ADOPTED_SUBSET_PLAN_V1'and plan['program']==ownref
         and plan['Root_execution_authority_granted']is False,'new independent optional arithmetic replay, no old caller/gate identity')
    budget.bind(plan['reference_map'])
    expected={str(relative(r['relative'])):dict(path=str(relative(r['relative'])),bytes=r['original']['bytes'],sha256=r['original']['sha256'])for r in plan['reference_map']}
    for r in plan['reference_map']:
        need(expected[str(relative(r['relative']))]['bytes']==r['original']['bytes']
             and expected[str(relative(r['relative']))]['sha256']==r['original']['sha256'],'one entire version per physical corpus artifact')
    for r in(ownref,pref):need(expected.get(r['path'],r)==r,'consistent current Source/plan physical identity');expected[r['path']]=r
    need(len(expected)<=32 and ownref['bytes']+4+2*sum(r['bytes']for r in expected.values())<=8*2**20,
         'complete first/final8MiB32path input scope including interpreter reserve')
    for r in plan['reference_map']:budget.read(r['original'])
    need(plan['mathematical_parent']['sha256']==WORKER_SHA and plan['point_kernel']['sha256']==POINT_SHA
         and plan['subset_kernel']['sha256']==SUBSET_SHA
         and plan['relative_parent']['sha256']=='74b61864324a90577f1c7aede1ec0b0729c25ba2145dc9ba855932e3cefac2e5',
         'exact unchanged point/subset kernels and explicit reviewed source ancestry')
    imports=imported_context(plan,budget,work);authority=transitivity(plan,budget,work,imports)
    rawcarrier=budget.read(plan['carrier']);rows=supplied(rawcarrier,plan,work)
    work.charge(2*len(rawcarrier),'complete_second_historical_carrier_JSON_read');carrier=decode(rawcarrier)
    adoption,historical=historical_subject(plan,budget,work,carrier)
    need(ownref['bytes']+plan['point_kernel']['bytes']+plan['subset_kernel']['bytes']<=50000,'whole current mathematical Source namespace50k')
    K=load_provider(plan['point_kernel'],budget,work,['decode_operands','prepare_triangle','rotation_word'])
    C=load_provider(plan['subset_kernel'],budget,work,['check_subset'])
    ctx=K['decode_operands'](budget.read(plan['roles']['operands']),work)
    witnesses=budget.read(plan['roles']['witnesses']);need(len(witnesses)==462528,'whole exact adopted28908 witness carrier')
    checked=[]
    for row,prior,fact in zip(rows,historical['verified_nongeneration_records'],adoption['new_facts']):
        owner,sha,triangle=bound_row(witnesses,row['free_index'],work)
        need(type(row['owner'])is int and row['owner']==prior['owner']==fact['owner']==owner
             and row['witness_row_sha256']==prior['witness_row_sha256']==fact['witness_row_sha256']==sha
             and fact['middle_mass']==1024,'every exact original free-index/owner/witnessSHA/mass identity')
        result=C['check_subset'](K,ctx,triangle,row['points'],work,512)
        need(result['points']==prior['points']==fact['invariant_points']
             and result['checked_positive_rotation_edges']==prior['checked_positive_rotation_edges']==fact['strict_positive_rotation_edges'],
             'fresh full closure agrees with retained positive cardinalities only')
        checked.append(dict(free_index=row['free_index'],owner=owner,witness_row_sha256=sha,**result))
    need(len(checked)==12 and sum(r['points']for r in checked)==3009
         and sum(r['checked_positive_rotation_edges']for r in checked)==6018,'complete actual adopted twelve-set replay')
    work.charge(32768,'whole_bounded_scalar_and_stdout_serialization_reserve')
    need(budget.refs==expected,'every actual read in the declared relative physical closure')
    budget.recheck();work.charge(0,'complete_shared10M20s_and_final_relative_hash_guard');budget.tick()
    print(json.dumps(dict(schema='L026_CORPUS_RELATIVE_SUBSET_REPLAY_RESULT_V1',status='VERIFIED_ADOPTED_ORIGINAL_ROTATION_SUBSETS',
        program=ownref,plan=pref,existing_adoption=plan['adoption'],historical_result=plan['historical_result'],actual_carrier=plan['carrier'],
        verified_nongeneration_records=checked,verified_count=12,actual_checked_points=3009,actual_positive_rotation_edges=6018,
        imported_original_transitivity=authority,original_model_member_action_bridge_global_class_two_fibre_and_simpleG_imports=True,
        actual_original_machine_path_reads=0,untrusted_supplier_or_search_or_SGS_or_full_virtual_middle_vectors=0,
        prior_Source_caller_or_control_PASS_identity_transferred=False,new_Root_adoption_or_current_ledger_change=False,
        generation_IP_reversal_census_Original_conjecture_Lean_or_measurement_credit=0,
        resources=dict(work_units=work.units,work_labels=work.labels,physical_read_bytes=budget.bytes,physical_paths=len(budget.refs),peak_RSS=budget.peak),
        qualification='Fresh point actions prove the twelve supplied sets invariant under actual ab/bc. Proper rotations and marking nongeneration use the exact retained transitivity and original involution/simpleG premises. All model/Reader/member/action/bridge/graph/GLOBAL-class/two-fibre/qualifiedH=B meanings remain imports. No new paid fact, positive generation,IP,reversal,other endpoint or whole Original claim.'),sort_keys=True))

if __name__=='__main__':main()
