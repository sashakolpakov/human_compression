"""Root accepts the independently verified230; the remaining266 stay unpaid.

This is a metadata-only successor of the preserved thirty-nine adopter.
It never changes CURRENT/SNAP or calls a mathematical/scientific function.
"""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import runpy
import sys
import time

S = Path(__file__).absolute().parents[2]
M = S/'maintenance/intake'
W = S/'computation/f004/small_inventory_work/cayley_centralizer_certificate'
C = W/'cases/prefix8_saved230_independent_verification'
PACKET = M/'f004_saved230_acceptance_source_packet.json'
PREPARATION = M/'f004_saved230_acceptance_source_preparation_execution.json'
START = time.monotonic()


def refs(value):
    if type(value) is dict:
        if set(value) == {'path', 'bytes', 'sha256'}:
            return [value]
        return [row for item in value.values() for row in refs(item)]
    if type(value) is list:
        return [row for item in value for row in refs(item)]
    return []


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('--review-sha256', required=True)
    parser.add_argument('--execution-sha256', required=True)
    parser.add_argument('--source-review', type=Path, required=True)
    parser.add_argument('--source-review-sha256', required=True)
    parser.add_argument('--source-execution', type=Path, required=True)
    parser.add_argument('--source-execution-sha256', required=True)
    parser.add_argument('--source-preparation-sha256', required=True)
    args = parser.parse_args()
    assert sys.flags.ignore_environment and sys.dont_write_bytecode and not sys.flags.optimize
    mp = S/'computation/f009/rooted_census_split/order32_continuation/from4369/root_metadata.py'
    hp = M/'acquire_f004_prefix8_export.py'
    assert hashlib.sha256(mp.read_bytes()).hexdigest() == 'a45c7863eeeece0e5218e3179a0ad3863d0bbea6eef55e6b9f1564849cf999c2'
    assert hashlib.sha256(hp.read_bytes()).hexdigest() == 'd00a74cb52959a298f4e6e236594f4c6e7606b4c7661419ab9e5d095695e10fe'
    m = runpy.run_path(str(mp), run_name='root_saved230_adoption_metadata')
    h = runpy.run_path(str(hp), run_name='root_saved230_adoption_helpers')
    h['authenticate'].__globals__['M'] = m
    pin, read, union = h['plain_pin'], h['read'], h['union']

    def put(path, value):
        raw = (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()
        assert len(raw) <= 2*2**20
        with path.open('xb') as stream:
            assert stream.write(raw) == len(raw)
            stream.flush()
            os.fsync(stream.fileno())
        return pin(path)

    def bounded():
        assert time.monotonic()-START < 140
        assert m['psutil'].Process().memory_info().rss <= 128*2**20

    def tool_return(execution, peer_ref, checks_ref):
        h['canonical_tool'](execution['actual_tool'])
        tool = execution['actual_tool']
        raw = execution['full_tool_return']
        assert type(tool['exit_code']) is int and tool['exit_code'] == raw['exit_code'] == 0
        assert raw['chunk_id'] == tool['terminal_chunk']
        printed = json.loads(raw['output'])
        assert printed['review'] == peer_ref and printed['checks'] == checks_ref
        first = execution['initial_tool_return']
        assert first['chunk_id'] == tool['initial_chunk']
        if tool['synchronous']:
            assert first == raw and 'session_id' not in raw
        else:
            assert first['session_id'] == tool['handle']

    with (S/'maintenance/runtime/active.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        current, snapshot = h['states']([[]])
        assert current['current_handle'] is None
        names = [C/'root_saved230_acceptance_source_authentication.json', C/'root_saved230_acceptance.json']
        assert all(not os.path.lexists(path) for path in names)
        self_ref, packet_ref = pin(__file__), pin(PACKET)
        packet = read(PACKET)
        assert packet['schema'] == 'ROOT_F004_SAVED230_ACCEPTANCE_SOURCE_V1'
        assert packet['program'] == self_ref and packet['source_author'] == '/root/c5_terminal_audit'
        assert packet['case_root'] == str(C) and packet['metadata_only'] is True
        source_peer_ref, source_ex_ref = pin(args.source_review), pin(args.source_execution)
        assert source_peer_ref['sha256'] == args.source_review_sha256 and source_ex_ref['sha256'] == args.source_execution_sha256
        source_peer, source_ex = read(source_peer_ref['path']), read(source_ex_ref['path'])
        assert source_peer['status'] == 'PASS_DISTINCT_ROOT_F004_SAVED230_ACCEPTANCE_SOURCE'
        assert source_peer['source_author'] == packet['source_author'] and source_peer['reviewer'] != source_peer['source_author']
        assert source_peer['program'] == source_ex['program'] == self_ref
        assert source_peer['source_packet'] == source_ex['source_packet'] == packet_ref
        assert source_peer['blockers'] == [] and source_ex['review'] == source_peer_ref
        assert source_ex['actor'] == source_peer['reviewer']
        h['canonical_tool'](source_ex['actual_tool'])
        assert source_ex['actual_tool']['exit_code'] == 0
        preparation_ref = pin(PREPARATION)
        assert preparation_ref['sha256'] == args.source_preparation_sha256
        preparation = read(PREPARATION)
        assert preparation['program'] == self_ref and preparation['source_packet'] == packet_ref
        assert preparation['represented_calls'] == preparation['scientific_calls'] == 0

        pr, er = pin(C/'distinct_actual_review.json'), pin(C/'distinct_actual_execution.json')
        assert pr['sha256'] == args.review_sha256 and er['sha256'] == args.execution_sha256
        assert pr == packet['actual_review'] and er == packet['actual_execution']
        peer, execution = read(pr['path']), read(er['path'])
        assert peer['status'] == 'PASS_DISTINCT_F004_PREFIX8_SAVED230_ACTUAL_METADATA'
        assert execution['status'] == 'COMPLETED_GENUINE_DISTINCT_F004_SAVED230_ACTUAL_METADATA_REVIEW'
        assert peer['reviewer'] == execution['actor'] == '/root/c5_terminal_audit'
        assert peer['source_author'] == peer['method_author'] == '/root/unit_actual_review' and peer['blockers'] == []
        assert execution['review'] == pr and execution['checks'] == peer['checks']
        assert peer['method'] == execution['method'] == packet['actual_method']
        assert peer['method_source_review'] == execution['method_source_review'] == packet['actual_method_source_review']
        assert peer['method_source_execution'] == execution['method_source_execution'] == packet['actual_method_source_execution']
        assert execution['metadata_only'] is peer['metadata_only'] is True
        assert execution['scientific_or_control_replay'] == peer['scientific_or_control_replay'] == 0
        tool_return(execution, pr, peer['checks'])

        tr, cr = pin(C/'root_terminal.json'), pin(C/'root_handle_clearance.json')
        terminal, clearance = read(tr['path']), read(cr['path'])
        assert tr == packet['terminal'] == peer['root_terminal'] == execution['root_terminal']
        assert cr == packet['clearance'] == peer['root_handle_clearance'] == execution['root_handle_clearance']
        assert terminal['passed'] is True and terminal['purpose'] == 'saved230' and terminal['errors'] == []
        assert clearance['terminal'] == tr and clearance['known_scope_drained'] is True
        h['canonical_tool'](terminal['actual_tool'])
        assert terminal['actual_tool'] == clearance['actual_tool'] == peer['actual_tool'] == execution['scientific_actual_tool']
        assert terminal['actual_tool']['exit_code'] == 0
        release_ref = terminal['release']; release = read(release_ref['path'])
        rr = terminal['result']; result = read(rr['path'])
        assert rr == packet['result'] == peer['result'] == execution['result']
        assert result['status'] == 'VERIFIED_ALL230_ACTUAL_PROPER_END_INTERSECTIONS'
        assert result['program'] == peer['program'] == execution['program'] == release['program'] == packet['scientific_program']
        assert peer['source_packet'] == execution['source_packet'] == release['source_packet'] == packet['scientific_source_packet']
        assert result['source_worker'] == peer['subject'] == execution['subject'] == packet['subject']
        assert result['original_job'] == [8, 4] and result['original_prefix_index'] == 8
        assert result['journal'] == peer['journal'] == execution['journal'] == packet['journal']
        assert result['candidate_credit'] == result['census_credit'] == result['whole_original_credit'] == 0
        assert result['prefix_complete'] is peer['prefix_complete'] is False and result['root_adoption'] is None
        assert peer['root_adoption'] is execution['Root_adoption'] is None
        assert result['word_search_executed'] is result['full_end_or_order4_certificate_verified'] is False
        assert result['prior_acceptance_and_weights_borrowed'] is True
        assert len(result['scientific_direct_inputs']) == 47

        prior_ref = result['prior_gate']
        assert prior_ref == packet['prior_acceptance'] and prior_ref['sha256'] == 'cc7bedda717a6bb757185fdf22f73c4efaa0871e540e21f5ba890ef253ae9b94'
        prior = read(prior_ref['path'])
        assert prior['root'] == '/root' and prior['status'] == 'ROOT_ACCEPTED_PREFIX8_DOUBLE_PROPER_END_REJECTIONS'
        assert prior['original_job'] == [8, 4] and prior['original_prefix_index'] == 8
        assert prior['total_rejected_orbits'] == result['prior_accepted_orbits_preserved'] == peer['prior_accepted_orbits_borrowed'] == 3283
        assert prior['old_rejected_orbits'] == 3244 and prior['new_rejected_orbits'] == 39
        assert prior['domain'] == result['domain'] and prior['prefix_complete'] is False and prior['unvisited_orbits'] == []
        prior_auth_ref = prior['source_authentication']; prior_auth = read(prior_auth_ref['path'])
        assert prior_auth['root'] == '/root' and prior_auth['all_inputs_freshly_hashed'] is True
        old_ref = prior['prior_partial_acceptance']; old = read(old_ref['path'])
        assert old_ref['sha256'] == 'bb7fab3d15834fac1ab12e8c41a966a48e16e5f1f6d24283315e4ab6d4479440'
        assert old['status'] == 'ROOT_ACCEPTED_QUALIFIED_PARTIAL_PREFIX8_MATRIX_REJECTIONS'
        assert old['domain'] == prior['domain'] and old['completed_orbits'] == 3779 and old['rejected_orbits'] == 3244
        old_auth_ref = old['source_authentication']; old_auth = read(old_auth_ref['path'])
        attachment_ref = old['generation_source_attachment']; attachment = read(attachment_ref['path'])
        assert old_auth['root'] == '/root' and old_auth['all_inputs_freshly_hashed'] is True
        assert attachment_ref['sha256'] == '3eb33961c12933b016e950b16c58175032b0f4b2c4e2b9bc3813de160a44bbf1'
        assert attachment['original_root_rosters_unchanged'] is True and attachment['retroactive_root_roster_freshness_claimed'] is False
        old_unpaid, thirty_nine = old['unpaid_orbits'], prior['newly_rejected_orbits']
        assert old_unpaid == sorted(set(old_unpaid)) and len(old_unpaid) == 535
        assert thirty_nine == sorted(set(thirty_nine)) and len(thirty_nine) == 39 and set(thirty_nine) <= set(old_unpaid)
        unpaid = prior['unpaid_orbits']
        assert unpaid == [rep for rep in old_unpaid if rep not in set(thirty_nine)] and len(unpaid) == 496
        new = result['newly_verified_representatives']
        assert all(type(rep) is int and rep >= 0 for rep in old_unpaid + thirty_nine + unpaid + new)
        assert new == sorted(set(new)) and len(new) == result['new_rejected_orbits'] == peer['verified230'] == 230
        assert new == peer['verified_representatives'] and set(new) <= set(unpaid)
        remaining = [rep for rep in unpaid if rep not in set(new)]
        assert remaining == result['remaining_unpaid_orbits'] == peer['remaining_unpaid_representatives']
        assert len(remaining) == result['remaining_unpaid_count'] == peer['remaining_unpaid_count'] == 266
        assert result['unvisited_orbits'] == [] and len(new) + len(remaining) == len(unpaid)
        counts = dict(SPLIT_SPLIT=223, SPLIT_UNITARY=7)
        assert result['rejection_type_counts'] == peer['rejection_type_counts'] == execution['rejection_type_counts'] == counts
        assert 3244 + 39 + 230 + 266 == 3779
        assert result['proper_end_theorem'] == packet['proper_end_theorem'] and result['theorem_reviews'] == packet['theorem_reviews']

        after_ref = terminal['source_after']; after = read(after_ref['path'])
        inventory_ref = terminal['output_inventory']; inventory = read(inventory_ref['path'])
        assert inventory['count'] == len(inventory['files']) == 6
        assert inventory['bytes'] == sum(row['bytes'] for row in inventory['files'])
        assert rr in inventory['files'] and result['journal'] in inventory['files']
        workflow_ref = pin(C/'root_workflow_execution.json')
        assert workflow_ref == packet['root_workflow'] == peer['root_workflow_execution'] == execution['root_workflow_execution']
        assert peer['required_root_adoption_scope_rosters'] == execution['required_root_adoption_scope_rosters'] == [dict(role='Root_full_after', document=after_ref, field='inputs')]
        recipe_path = S/'computation/f004/small_inventory_work/original_prefix8_matrix_export/authentication_input_recipe.json'
        recipe_ref = pin(recipe_path)
        assert recipe_ref['sha256'] == '2e5c000afd81a3c39482e54bbca4b69848244ce9ec7dbf70afd3a45a13d504bb'
        recipe = read(recipe_path)
        rows = union(after['inputs'], peer['required_root_adoption_inputs'], execution['required_root_adoption_inputs'],
                     prior_auth['inputs'], old_auth['inputs'], attachment['inputs'],
                     packet['required_source_inputs'], refs(peer), refs(execution), refs(source_peer), refs(source_ex),
                     refs(terminal), refs(clearance), refs(prior), refs(old), inventory['files'], result['scientific_direct_inputs'],
                     [pr, er, tr, cr, rr, prior_ref, prior_auth_ref, old_ref, old_auth_ref, attachment_ref,
                      after_ref, inventory_ref, release_ref, workflow_ref,
                      self_ref, packet_ref, preparation_ref, source_peer_ref, source_ex_ref, pin(mp), pin(hp), recipe_ref])
        assert len(rows) <= 4096 and sum(row['bytes'] for row in rows) <= 2*2**30
        assert union(after['inputs']) == after['inputs'] and after['input_scope']['all_freshly_hashed'] is True
        forbidden = {str(S/'reboot_20261013/CURRENT.json'), str(S/'maintenance/intake/current_status.json')}
        assert not forbidden.intersection(row['path'] for row in rows)
        bounded()
        resources_before = h['resources']()
        assert resources_before['available_ram_bytes'] >= 4*2**30 and resources_before['free_disk_bytes'] >= 10*2**30
        aliases = h['chains'](recipe)
        assert aliases == after['alias_evidence']
        fresh = h['authenticate'](rows, recipe)
        assert fresh['all_freshly_hashed'] is True and h['chains'](recipe) == aliases
        resources_after = h['resources']()
        assert resources_after['available_ram_bytes'] >= 4*2**30 and resources_after['free_disk_bytes'] >= 10*2**30
        bounded()
        current, snapshot = h['states']([[]])
        assert current['current_handle'] is None
        auth = put(names[0], dict(
            root='/root', inputs=rows, input_scope=fresh, alias_evidence=aliases,
            all_inputs_freshly_hashed=True, resources_before=resources_before, resources_after=resources_after,
            scientific_replays=0, method=self_ref, source_packet=packet_ref,
            source_review=source_peer_ref, source_execution=source_ex_ref, source_preparation=preparation_ref,
            late_root_workflow=workflow_ref, late_workflow_retroactively_injected_into_before=False))
        gate = put(names[1], dict(
            schema='ROOT_F004_PREFIX8_SAVED230_ACCEPTANCE_V1', root='/root',
            status='ROOT_ACCEPTED_PREFIX8_SAVED230_INDEPENDENT_CERTIFICATES', case_root=str(C),
            original_job=[8, 4], original_prefix_index=8, program=result['program'], subject=result['source_worker'],
            source_packet=release['source_packet'], result=rr, journal=result['journal'], domain=result['domain'],
            terminal=tr, clearance=cr, scientific_actual_tool=terminal['actual_tool'],
            independent_actual_review=pr, independent_actual_execution=er, metadata_actual_tool=execution['actual_tool'],
            prior_acceptance=prior_ref, prior_partial_acceptance=old_ref,
            source_authentication=auth, method=self_ref, adoption_source_packet=packet_ref,
            adoption_source_review=source_peer_ref, adoption_source_execution=source_ex_ref,
            old_rejected_orbits=3283, new_rejected_orbits=230, total_rejected_orbits=3513,
            newly_rejected_orbits=new, rejection_type_counts=counts, unpaid_orbits=remaining,
            remaining_unpaid_count=266, unvisited_orbits=[], prefix_complete=False,
            proper_end_theorem=result['proper_end_theorem'], theorem_reviews=result['theorem_reviews'],
            prior_acceptance_and_weights_borrowed=True, original_weights_reproved=False,
            full_end_or_order4_certificate_verified=False, original_permutation_lifts_executed=False,
            original_root_roster_omission_preserved=True, retroactive_root_roster_freshness_claimed=False,
            late_root_workflow=workflow_ref, late_workflow_retroactively_injected_into_before=False,
            candidate_credit=0, census_credit=0, whole_original_credit=0, CURRENT_or_SNAP_modified=False,
            qualification='Root accepts the independent verifier and distinct actual metadata audit for exactly230 '
                'proper-end certificates (223 split/split and7 split/unitary), disjoint from the accepted3283. '
                'All266 remaining representatives stay unpaid. The earlier3244 qualified proof and its genuine '
                'postreturn generation-Source attachment, plus39 unitary rejections, remain borrowed unchanged. '
                'The whole literal adoption union is freshly streamed with acquired aliases and48 inert identities. '
                'No search/order4/FULL certificate, weight recomputation, permutation lift, complete prefix/original, '
                'census, manuscript or conjecture completion is asserted. This immutable gate does not publish a ledger pointer.'))
        print(json.dumps(dict(acceptance=gate, source_authentication=auth, input_scope=fresh,
                              new_rejected_orbits=230, total_rejected_orbits=3513,
                              unpaid_orbits=266, CURRENT_or_SNAP_modified=False, census_credit=0)))


if __name__ == '__main__':
    main()
