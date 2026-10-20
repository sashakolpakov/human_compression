"""Independent ordinary metadata arithmetic, never Root planner/Reader replay."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import resource
import runpy
import time

START=time.monotonic()
F=Path(__file__).absolute().parent
S=F.parents[4]
UTIL=F/'review_interval_actual.py'
UTIL_SHA='65fd035735c75713823ea1ebb319009706a9d5e0eca0cda1f169fee4c7ca4551'
ACTOR='/root/resource_cleanup_audit'


def main():
    ap=argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--plan-sha256',required=True)
    ap.add_argument('--interval-acceptance',type=Path,required=True)
    ap.add_argument('--interval-acceptance-sha256',required=True)
    args=ap.parse_args()
    # Exact acquired own stdlib-only metadata utilities; no proposed subject,
    # Root planner, binding, Reader or scientific module is imported/called.
    raw=UTIL.read_bytes()
    if len(raw)!=39216 or hashlib.sha256(raw).hexdigest()!=UTIL_SHA:
        raise ValueError('exact acquired metadata utility Source')
    io=runpy.run_path(str(UTIL),run_name='row_mass_review_acquired_metadata_utilities')
    pin,doc,merge,scope,need=[io[k]for k in ('pin','document','merge','scope','need')]
    def tick():
        need(time.monotonic()-START<100 and resource.getrusage(resource.RUSAGE_SELF).ru_maxrss<128*2**20,
             'complete ordinary metadata100s/observed128MiB')
    need(not(F/'row_mass_distinct_review.json').exists()and not(F/'row_mass_distinct_execution.json').exists(),
         'fresh metadata review only')
    plan_ref=pin(F/'row_mass_plan.json');need(plan_ref['sha256']==args.plan_sha256,'explicit Root plan SHA')
    plan=doc(plan_ref);manifest_ref=pin(F/'shared_manifest.json');m=doc(manifest_ref)
    inventory=doc(m['inventory']);lemma_ref=pin(F.parent/'generation_reduction/root_lemma_acceptance.json')
    need(lemma_ref['sha256']=='54bb04dae1868fe3c155adb7170441e4a563b252fa40a0f9c157a24115d44b1e','exact accepted lemma')
    lemma=doc(lemma_ref)
    need(lemma['root']=='/root'and lemma['status']=='ROOT_ACCEPTED_CONDITIONAL_CO2_GENERATION_BY_TRANSITIVITY_LEMMA'
         and lemma['all_source_rows_fresh']is True,'borrowed genuine conditional mathematical authority')
    _,proof=pin(lemma['proof']['path'],True)
    need(hashlib.sha256(proof).hexdigest()==lemma['proof']['sha256']and
         b'generating => l=|S|'in proof and b'Its\nstabilizer is C_S(b)=C_A(a,b,c)'in proof,
         'acquired proof explicitly contains free-action implication and centralizer identity')
    need(inventory['pair']==12 and inventory['middle_class']==1 and inventory['top_blocks']==178
         and inventory['domain_rows']==24690 and len(inventory['scopes'])==12,'whole accepted row domain metadata')
    need(m['configuration']['centralizer_order']==1474560 and m['configuration']['pointwise_order']==1280
         and m['configuration']['group_order']==m['configuration']['ambient_order']==42305421312000,
         'exact borrowed named-group/centralizer scalars')
    planner=pin(S/'maintenance/intake/inspect_row_masses.py')
    binding=pin(S/'computation/co2/cells/pair12_markings/reversal_certificates/pointwise_word_tree_source/operational_error_capture_source/binding.py')
    expected_inputs=[manifest_ref,m['inventory'],lemma_ref,planner,binding]
    all_keys=set();nonfree=[];block_summary=[];full_mass=0;normal_bytes=0;scope_mass=0
    histogram={};domain_by_top={}
    for scope_index,item in enumerate(inventory['scopes']):
        tick()
        gate=doc(item['acceptance']);ranges=doc(item['block_ranges']);rows=doc(item['literal_rows_metadata'])
        expected_inputs += [item[k]for k in ('acceptance','block_ranges','literal_rows_metadata')]
        normal_bytes+=item['literal_rows_metadata']['bytes']
        need(gate['adopted']is True and gate['pair']==12 and gate['middle']==1 and gate['pointwise_order']==1280
             and gate['literal_rows']==item['literal_rows_metadata']and gate['block_ranges']==item['block_ranges']
             and gate['first_top']==item['first_top']and gate['last_top']==item['last_top']
             and gate['completed_top_indices']==[b['top_index']for b in ranges]
             ==list(range(item['first_top'],item['last_top']+1)),'each actual accepted scope/range/normalized-file join')
        need(len(rows)==item['rows']==gate['lower_rows']and [r['index']for r in rows]==list(range(1,len(rows)+1)),
             'entire accepted normalized list, exact coordinate domain')
        cursor=1;accepted_scope_mass=0
        for block in ranges:
            tick();top=block['top_index']
            need(top not in domain_by_top and all(type(block[k])is int and block[k]>0
                 for k in ('top_index','first_row','last_row','lower_rows','mass'))and
                 block['first_row']==cursor and block['last_row']==cursor+block['lower_rows']-1,
                 'disjoint whole contiguous top-local ranges')
            need(next(b for b in inventory['blocks']if b['top_index']==top)==dict(block,scope=scope_index),
                 'literal full-inventory top/range/mass linkage')
            domain_by_top[top]=block['lower_rows'];subtotal=0;count=0
            for local in range(1,block['lower_rows']+1):
                row=rows[cursor+local-2];key=(top,local)
                need(key not in all_keys and set(row)=={'index','representative_sha256','middle_sha256',
                     'double_coset_mass','middle_S_orbit_size'}and type(row['index'])is int,
                     'one complete normalized row per exact top-local key')
                all_keys.add(key)
                mass,orbit=row['double_coset_mass'],row['middle_S_orbit_size']
                need(type(mass)is int and type(orbit)is int and mass==1474560*orbit and
                     1<=orbit<=1280 and 1280%orbit==0 and row['index']==cursor+local-1,
                     'exact integer orbit-stabilizer mass, divisor and slice coordinate')
                need(all(type(row[k])is str and len(row[k])==64 and all(c in '0123456789abcdef'for c in row[k])
                     for k in ('representative_sha256','middle_sha256')),'retained normalized digest shapes, no permutation rehash')
                subtotal+=mass;histogram[orbit]=histogram.get(orbit,0)+1
                if orbit<1280:
                    count+=1;nonfree.append(dict(top_index=top,top_row=local,slice_row=row['index'],
                        orbit_size=orbit,double_coset_mass=mass))
            need(subtotal==block['mass'],'every individual top mass exactly sums its acquired rows')
            full_mass+=subtotal;accepted_scope_mass+=subtotal
            block_summary.append(dict(top_index=top,rows=block['lower_rows'],nonfree=count,full_size=block['lower_rows']-count))
            cursor=block['last_row']+1
        need(cursor==len(rows)+1 and accepted_scope_mass==gate['selected_double_coset_mass'],
             'whole accepted scope mass and row ranges, no trailing omission')
        del rows
    need(sorted(domain_by_top)==list(range(1,179))and len(all_keys)==24690 and normal_bytes==6969559
         and full_mass==42305421312000 and len(nonfree)==3627 and histogram[1280]==21063,
         'complete global24690/3627/21063 domain and whole group mass')
    need(sum(orbit*count for orbit,count in histogram.items())==28690200 and sum(histogram.values())==24690,
         'independent total orbit lengths and row histogram')
    need(plan['root']=='/root'and plan['status']=='ROOT_PROVISIONAL_ROW_MASS_PLAN_NOT_COVERAGE'
         and plan['potential_nonfree_keys']==nonfree and plan['blocks']==sorted(block_summary,key=lambda r:r['top_index'])
         and plan['domain_rows']==24690 and plan['nonfree_rows']==3627 and plan['full_size_rows']==21063
         and plan['mass']==full_mass and plan['inputs']==merge(expected_inputs)
         and plan['input_scope']==scope(plan['inputs'])and plan['all_metadata_inputs_fresh_before_after']is True
         and plan['new_accepted_rows']==plan['new_cells']==plan['whole_original_credit']==plan['scientific_module_calls']==0,
         'entire Root provisional plan distribution, exact3627 identities and41-input scope')
    family=doc(F/'root_family_acceptance.json');initial=doc(family['initial95_projection'])
    initial_keys=set()
    need(initial['covered_rows']==95 and len(initial['top_outcomes'])==178,'actual initial95 projection')
    for top,row in enumerate(initial['top_outcomes'],1):
        need(row['top_index']==top and len(row['outcomes'])==domain_by_top[top]and set(row['outcomes'])<=set('.M'),
             'all initial95 metadata coordinates')
        initial_keys.update((top,i)for i,symbol in enumerate(row['outcomes'],1)if symbol=='M')
    accepted_ref=pin(args.interval_acceptance.absolute())
    need(accepted_ref['sha256']==args.interval_acceptance_sha256,'exact newly adopted interval authority SHA')
    accepted=doc(accepted_ref);case=doc(accepted['case'])
    need(accepted['root']=='/root'and accepted['status']=='ROOT_ACCEPTED_CONDITIONAL_PAIR12_CLASS1_ROW_INTERVAL'
         and accepted['pair']==12 and accepted['middle_class']==1 and accepted['family_manifest']==manifest_ref
         and accepted['closed_source_keys']==case['selected_rows']==len(accepted['records'])==53
         and accepted['generating_S_orbits']==accepted['fixed_S_orbits']==0,'actual accepted53 zero-outcome authority')
    new_keys={(r['source_key']['top_index'],r['source_key']['top_row'])for r in accepted['records']}
    need([(r['source_key']['top_index'],r['source_key']['top_row'])for r in accepted['records']]==
         [(r['top_index'],r['top_row'])for r in case['expected_source_keys']]and
         all(r['proof_kind']=='NONGENERATING_KIND3_MASS'and r['generates_ambient']is False and
             r['self_dual']is False for r in accepted['records']),'all-and-only accepted53 source keys/outcomes')
    nonfree_keys={(r['top_index'],r['top_row'])for r in nonfree}
    need(len(initial_keys)==95 and len(new_keys)==53 and not initial_keys&new_keys and
         initial_keys<=nonfree_keys and new_keys<=nonfree_keys and len(nonfree_keys-(initial_keys|new_keys))==3479,
         'exact overlaps95 and53, no new double counting')
    for ref in merge(plan['inputs'],[lemma[k]for k in ('proof','source_review','source_checks','source_execution')],
        [m['borrowed_ROOT_authority'][0],pin(UTIL),pin(__file__),plan_ref,accepted_ref,
         accepted['distinct_actual_review'],accepted['distinct_actual_execution']]):
        need(pin(ref['path'])==ref,'fresh exact small proof/metadata input')
    fresh=merge(list(io['FRESH'].values()))
    for ref in fresh:need(pin(ref['path'])==ref,'all Source/metadata arithmetic inputs stable afterward')
    tick()
    ordered=sorted(nonfree,key=lambda r:(r['top_index'],r['top_row']))
    digest=hashlib.sha256(json.dumps(ordered,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    review=dict(status='PASS_DISTINCT_CONDITIONAL_CO2_PAIR12_ROW_MASS_METADATA_AUDIT',reviewer=ACTOR,
        source_author='/root',blockers=[],program=planner,metadata_utility=pin(UTIL),method=pin(__file__),
        root_plan=plan_ref,inventory=m['inventory'],family_manifest=manifest_ref,accepted_generation_lemma=lemma_ref,
        generation_argument=lemma['proof'],generation_source_review=lemma['source_review'],
        complete_S12_authority=m['borrowed_ROOT_authority'][0],accepted_new53=accepted_ref,
        initial95_projection=family['initial95_projection'],accepted_scopes=12,normalized_metadata_bytes=normal_bytes,
        whole_rows=24690,whole_mass=full_mass,full_size_rows=21063,nonfree_rows=3627,
        nonfree_key_table=dict(record=plan_ref,field='potential_nonfree_keys',count=3627,
            ordered_by_top_row_canonical_sha256=digest,exact_complete_equality_independently_checked=True),
        orbit_size_histogram={str(k):histogram[k]for k in sorted(histogram)},
        overlap=dict(initial95=95,newly_accepted53=53,initial_vs_new53=0,accepted_union=148,
            nonfree_additional_after_current_acceptances=3479,nonfree_union_with_accepted=3627,
            not_excluded_by_this_rule=21063),
        independent_fresh_inputs=fresh,independent_fresh_scope=scope(fresh),
        conditional_proof='For a genuine adopted S-orbit row with m=|U|*l and S=C_A(a,c), its stabilizer is C_A(a,b,c). If the three marks generate the acquired centerless Co2=A, this stabilizer is Z(A)=1, hence l=|S|=1280. Every acquired l<1280 row is therefore nongenerating. This accepted contrapositive gives no subgroup order or conclusion for l=1280.',
        required_new_authority='ROOT must separately accept the exact per-row nonfree metadata/proof union in its own named exclusion gate and explicitly compose that authority into typed checkpoint/source consumers. This provisional plan/audit is not3627 native candidate-validation returns and must not be relabeled as such. Existing95+53 overlap must be counted once.',
        qualifications=[
            'No Root planner, binding/Reader, scientific literal/permutation parser, group, generation/reversal, snapshot, controls or native candidate function was imported/called. Only the exact65fd own stdlib metadata utility namespace was loaded; its main was not invoked or globals patched.',
            'Independent review covers every accepted normalized JSON row/key/range/mass/divisor and exact plan equality. Actual normalized permutation correctness, full orbit/double-coset partition, named faithful centerless Co2, complete S12 and their historical acquisition are borrowed exact accepted premises, not independently recomputed from scientific payloads.',
            'The identified nonfree count is not inferred from aggregate bounds: actual3627 literal source keys are checked against all24690 normalized entries. Neither free size1280 nor remaining21063 implies generation.',
            'No CURRENT/SNAP, prior accepted record, Source, row flag or ledger is changed. No new candidate certificate, exact nongenerating subgroup order, cell, duality, parity, census, manuscript or whole-original credit is supplied.'
        ],planner_reexecutions=0,scientific_module_calls=0,new_accepted_rows=0,new_cells=0,whole_original_credit=0,
        observed_seconds=time.monotonic()-START,observed_peak_self_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    output=F/'row_mass_distinct_review.json';encoded=(json.dumps(review,sort_keys=True,indent=2)+'\n').encode()
    need(len(encoded)<128*2**10,'small whole metadata review; keys retained by exact plan pointer')
    with output.open('xb')as stream:stream.write(encoded)
    print(json.dumps(dict(review=pin(output),method=pin(__file__),nonfree_rows=3627,full_size_rows=21063,
        overlaps=review['overlap'],fresh_scope=scope(fresh),seconds=review['observed_seconds'],peak_self_bytes=review['observed_peak_self_bytes'])))


if __name__=='__main__':main()
