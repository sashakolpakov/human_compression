"""Procedural exact D images, fresh full b; no complete cache or ledger writes."""
import struct
import common as C
import budget,point_kernel as K,family,subset_kernel as N,supplier,positive,checks
DUTIES=('accepted_procedural_D_same_original_bridge_frame_membership_owned',
 'actual_a_c_and_D_products_belong_to_named_original_simple_Fi22_owned',
 'inner_G_target_not_mere_Aut_properness_and_exact_coset_scope_owned',
 'complete_corrected_simple_Fi22_maximal_11_13_avoidance_theorem_owned',
 'faithful_original_degree3510_G_transitivity_minimal_index_and_even_subgroup_argument_owned',
 'same_exact_original_witness_rows_partner_triangles_current_unpaid_H_and_two_fibre_scope_owned',
 'generation_and_properness_only_no_IP_or_Aut_reversal_or_class_credit_owned')
PROVIDER_DUTIES=('same_original_d0_ordered_A_and_full_signed_tree_owned',
 'accepted_equal_stabilizer_bridge_defines_all3510_equivariant_D_images_owned',
 'known_G_seed_and_G_normal_in_A_give_all_queried_D_membership_owned',
 'no_uncomputed_native_bytes_or_complete_native_cache_authority_claimed')
def main():
    b,q,g,pins,out=C.start('worker.py',(C,budget,K,family,N,supplier,positive,checks));C.admission(b,g,pins)
    C.need(set(q)=={'schema','Root_authority','python_executable','Root_import','procedural_D_import','scope','operands','witness_bank','current_snapshot','cases','search','saved','mode'}and q['schema']=='L026_PROCEDURAL_MIDDLE_REQUEST_V1'and q['mode']in('produce','check')and type(q['cases'])is list and 1<=len(q['cases'])<=8,'one bounded current procedural GEN/NG bank')
    C.need(q['Root_import']['bytes']<=32768 and q['procedural_D_import']['bytes']<=32768,'bounded exact fresh imports')
    imp=b.doc(q['Root_import']);provider=b.doc(q['procedural_D_import'])
    C.need(imp['root']=='/root'and imp['Root_authority']is imp['adopted']is True and imp['manifest']==pins['manifest']and all(imp[k]is True for k in DUTIES),'fresh inner-simpleG/member/coset/fibre/transitivity Root scope')
    for k in('scope','operands','witness_bank','current_snapshot','cases','procedural_D_import'):C.need(imp[k]==q[k],'exact inherited and fresh Root scope '+k)
    C.need(provider['schema']=='ROOT_L026_PROCEDURAL_D_PROVIDER_IMPORT_V1'and provider['root']=='/root'and provider['Root_authority']is provider['adopted']is True and provider['operands']==q['operands']and all(provider[k]is True for k in PROVIDER_DUTIES),'explicit procedural bridge authority, not partial-cache adoption')
    C.need(provider['old_family_premise_import']['bytes']<=32768,'bounded old bridge-premise metadata')
    old=b.doc(provider['old_family_premise_import'])
    C.need(old['schema']=='ROOT_L026_D_FAMILY_EXACT_ORIGINAL_IMPORT_V1'and old['root']=='/root'and old['Root_authority']is old['adopted']is True and old['operands']==q['operands']and old['original_point_to_involution_bridge_full_equivariance_and_G_membership_owned']is old['same_original_d0_and_ordered_A_and_full_bridge_frame_owned']is True,'exact accepted Original bridge/frame premises')
    C.need(provider['global_scope']==old['same_global_family_scope']and provider['global_scope']['degree']==3510 and provider['global_scope']['root']==2961,'same globally keyed point frame')
    authority_refs=provider['global_scope']['accepted_inputs']+[provider['bridge_argument'],provider['bridge_Source']]
    C.need(len(authority_refs)==6 and sum(C.ref(r)['bytes']for r in authority_refs)<=900000,'finite full imported bridge context')
    baseheader=dict(schema='L026_PROCEDURAL_GEN_NEG_CARRIER_V1',Source_manifest=pins['manifest'],Root_import=q['Root_import'],procedural_D_import=q['procedural_D_import'],scope=q['scope'],family_key=provider['family_key'],operands=q['operands'],witness_bank=q['witness_bank'],current_snapshot=q['current_snapshot'])
    C.need(len(C.can(baseheader))<=24576 and len(C.can(dict(pins=pins,Root_import=q['Root_import'],procedural_D_import=q['procedural_D_import'],current_snapshot=q['current_snapshot'],cases=q['cases'])))<=8192,'prepaid complete framing')
    refs=q['scope']['context'];C.need(type(refs)is list and len(refs)<=12 and sum(C.ref(r)['bytes']for r in refs)<=32768,'bounded exact old theorem/member/fibre context')
    snap=q['current_snapshot'];C.need(type(snap)is dict and set(snap)=={'CURRENT','receipt','bank'}and sum(C.ref(r)['bytes']for r in snap.values())<=65536,'whole fresh current typed status snapshot')
    C.need(q['scope']['degree']==3510 and q['scope']['rows']==28908,'same entire Original row domain')
    future=refs+authority_refs+[q['operands'],q['witness_bank']]+list(snap.values())
    if q['mode']=='check':C.need(q['saved']is not None and C.ref(q['saved'])['bytes']<=65536,'whole strict hint bank');future.append(q['saved'])
    operations=1500000+513000*len(q['cases'])
    if not checks.fit(b,future,operations):
        for r in future:b.read(r)
        b.close();v=dict(status='INCONCLUSIVE_PRE_NUMERICAL_CASE_BANK_FIT',selected_cases=q['cases'],all_unpaid_unchanged=True,no_numerical_case_predicates_called=True,pins=pins)
        files=b.emit(out,{'certificate.json':C.can(v),'proof.json':C.can(dict(v,physical_reads=b.bytes,point_units=b.work.units))});print(C.can(dict(status=v['status'],outputs=files,new_IP_or_case_credit=0)).decode(),end='');return
    b.work.charge(65536,'complete framing/index/sorted-subset bookkeeping')
    for r in refs+authority_refs:b.read(r)
    C.need(q['operands']['bytes']==52658,'same five-vector/tree format');ctx,nodes,key=family.frame(K,b.read(q['operands']),b.work);C.need(key==provider['family_key'],'whole d0/orderedA/tree key and every parent-point edge')
    count=q['scope']['rows'];C.need(q['witness_bank']['bytes']==16*count,'whole exact16B row bank');witness=b.read(q['witness_bank'])
    for r in snap.values():b.read(r)
    status=b.read(snap['bank']);C.need(len(status)==count,'whole typed current status domain')
    triangles=[checks.binding(witness,row,count,b.work)for row in q['cases']];indices=[r['free_index']for r in q['cases']];C.need(indices==sorted(set(indices))and all(status[i]==0 for i in indices),'all and only fresh unpaid rows')
    verified=[];probe=dict(attempts=0,point_letters=0);remaining=4096
    if q['mode']=='produce':
        C.need(q['saved']is None,'fresh untrusted discovery');records=[]
        for identity,triangle in zip(q['cases'],triangles):
            K.prepare_triangle(ctx,triangle,b.work)
            pair=positive.search(K,ctx,triangle,q['search'],probe,b.work);record=dict(identity=identity,outcome='INCONCLUSIVE',prime11=None,prime13=None,points=None)
            if pair is not None:record.update(outcome='GEN_HINT',**pair)
            elif remaining:
                cap=min(3509,remaining);seed=q['search']['negative_seed'];C.need(type(seed)is int and 0<=seed<3510,'literal negative start');note=supplier.cursor(None,identity['free_index'],identity['owner'],identity['witness_row_sha256'],3510,cap,seed,b.work)
                supplier.explore(checks.PROVIDER,ctx,K.prepare_triangle(ctx,triangle,b.work),note,b.work,cap);remaining-=len(note['points'])
                if note['outcome']=='closed_hint':record.update(outcome='PROPER_HINT',points=sorted(note['points']))
            records.append(record)
        carrier=dict(baseheader,records=records)
    else:
        saved=b.read(q['saved']);carrier=C.strict(saved);C.need(saved==C.can(carrier)and {k:v for k,v in carrier.items()if k!='records'}==baseheader,'same canonical untrusted bank/subject/Source')
        records=carrier['records'];C.need(type(records)is list and len(records)==len(q['cases'])and sum(len(r['points'])for r in records if type(r.get('points'))is list)<=4096,'whole saved bank and total proper4096point cap')
        for identity,triangle,record in zip(q['cases'],triangles,records):
            C.need(record['identity']==identity,'exact once Original row order');K.prepare_triangle(ctx,triangle,b.work);verified.append(dict(identity=identity,verdict=checks.kernel_verify(ctx,triangle,record,b.work)))
    body=C.can(carrier);C.need(len(body)<=65536,'bounded complete certificate');b.close()
    proof=dict(schema='L026_PROCEDURAL_GEN_NEG_PROOF_V1',status='VERIFIED_PROCEDURAL_SUPPLIED_GEN_OR_PROPER_CERTIFICATES'if q['mode']=='check'else'UNTRUSTED_BOUNDED_PROCEDURAL_DISCOVERY_FINISHED',pins=pins,Root_import=q['Root_import'],procedural_D_import=q['procedural_D_import'],global_family_key=key,current_snapshot=snap,selected_cases=q['cases'],verified_records=verified,probe=probe,remaining_negative_point_bank=remaining,fresh_full_b_from_exact_procedural_D_images=True,all_Original_innerG_coset_H_two_fibre_and_theorem_meanings_imported=True,complete_native_D_family_claim=False,native_D_carrier_bytes_trusted=0,new_IP_or_Aut_reversal_or_class_or_case_credit=0,all_misses_unpaid=True,physical_reads=b.bytes,point_units=b.work.units)
    proofbody=C.can(proof);C.need(len(proofbody)<=16384,'bounded proof');files=b.emit(out,{'certificate.json':body,'proof.json':proofbody});print(C.can(dict(status=proof['status'],outputs=files,new_IP_or_case_credit=0,Root_adoption_owed=True)).decode(),end='')
if __name__=='__main__':main()
