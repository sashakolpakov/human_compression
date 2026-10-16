from pathlib import Path
import hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans')
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

F=S/'computation/f009';P=F/'validated_cache_work'
assert hashlib.sha256((P/'manifest.json').read_bytes()).hexdigest()=='04f3ee79f77fbaf4d72a9f0aa0483a6460955fe81790defa7404a5a530b1e897'
r=json.loads(Path('/private/tmp/f009_validated_cache_root01.json').read_text());assert r['status']=='PASS' and r['check_count']==408
c=m.Closure();c.packet('computation/f009/validated_cache_work');c.packet('computation/f009/sharing_startup_failure01');c.add('/private/tmp/f009_validated_cache_root01.json');c.add(__file__)
status='ACCEPTED_F009_COMPLETE_PARSER_JOURNAL_INITIALIZATION'
c.finish('computation/f009/validated_cache_root_review',status,dict(status=status,author='finite_recoveries',reviewer='root',review=[
 'Read the complete two-page equivalence proof and viewed both native pages. Read the whole helper, unchanged complete journal parser, entry validator and constructor, and the private tuple reader. The only omitted operations are repeated entry checks on the actual unexposed complete-parser result; immutable integer/tuple values cannot change between the two visits in the acquired execution.',
 'The public entry takes bytes rather than a purportedly trusted dictionary, invokes the actual complete reader, rejects unfinished tails, and constructs the original JournalCache class in a nested factory capturing that exact parsed dictionary. Initial and journal dictionaries remain distinct; ordered object identities, context, counter, header bytes and later class methods are unchanged. No default unchecked constructor or trust flag is exported.',
 'Fresh controls passed408 checks and20 prefix cases, including malformed JSON and journal domains, typed scalar damage, initial and later default rejection paths, exact ordered states, separate dictionaries and identical journal bytes. The19-entry fixture invokes the entry validator19 rather than38 times. This supports the proved initialization equivalence, not a measured runtime or memory bound.',
 'The failed interval is retained with no completed roots. Integration must retain both actual Q.context acquisitions, equality before request/search, the private reader lifetime, original input checks, and all search predicates. Moving the second context check just after header emission is an explicit caller change requiring review. A timeout without request.json must terminate with zero credit and no automatic successor.',
 'This accepts only the helper and its proof. No production profile, new interval, time cap, memory cap, conjecture answer, complete original or compression measurement is released by this gate.'
]))

B=S/'geometry/sporadic_polytopes';P=B/'ru_direct_key_cell8_v1'
assert hashlib.sha256((P/'manifest.json').read_bytes()).hexdigest()=='f05d28d5db9f511ce8ec435cfd1e31e541c2054bd56d0094f0ed706c2c141706'
assert hashlib.sha256((P/'request.json').read_bytes()).hexdigest()=='dc2b63f43bc297a5b26689595757fed87257437e49cb7e8a3c36c029d370d682'
r=json.loads(Path('/private/tmp/ru_direct_key_root_preflight01.json').read_text());assert r['inputs']==22874 and r['cells']==[[8,2]] and r['target_runs']==0
aliases=json.loads((P/'runtime_aliases.json').read_text())
for local,remote in aliases.items():assert(P/local).read_bytes()==Path(remote).read_bytes()
c=m.Closure();c.packet('geometry/sporadic_polytopes/ru_direct_key_cell8_v1');c.packet('geometry/sporadic_polytopes/endpoint_method_work/direct_conjugate_key_root_review');c.add(__file__)
for p in [Path('/private/tmp/ru_direct_key_root_preflight01.json'),Path('/private/tmp/ru_direct_key_root_request01.json')]:c.add(p)
for p in Path('/private/tmp/ru_direct_key_root_scope01').rglob('*'):
 if p.is_file():c.add(p)
status='ACCEPTED_L026_RU_DIRECT_KEY_CELL8_CALLER_V1'
c.finish('geometry/sporadic_polytopes/endpoint_method_work/ru_direct_key_cell8_root_review',status,dict(status=status,author='l070_publication',reviewer='root',review=[
 'Read the whole owner and exact owner/batch differences from the previously accepted finite caller. The only mathematical runtime substitution is the separately accepted direct conjugate-key kernel. The earlier-transversal upstep, cut2, middle classifier, compact sink and literal collector are retained. All frozen aliases match actual runtime files.',
 'Both actual GAP and Python selectors permit only pair8/middle2. The exact fifteen accepted prior cells and the failed300-second predecessor are acquired; no inventory or prefix from that failed computation is treated as a completed result. A complete disjoint orbit partition with full mass remains the acceptance condition.',
 'Fresh root preflight acquired22874 inputs without a target. Fresh request controls rejected twelve altered boundaries and passed the four resource cases. Fresh selector/literal controls passed three tiny cells with16 candidate records; transformed traces only check parser scope, not new Rudvalis mathematics. The author retained a fresh actual GAP-to-literal pipeline with21 damage controls.',
 'Release the one exact request dc2b63f43bc297a5b26689595757fed87257437e49cb7e8a3c36c029d370d682 to ru_direct_key_pair8_01, bounded by300seconds,1024MiB GAP workspace,512MiB sampled output,4GiB launch reserve and2GiB sampled floor. GAP workspace is not a whole-process RSS bound. No automatic successor or cap increase is authorized by this caller.',
 'A returned full cell still requires distinct literal acquisition. This gate adds no numerical source row, principal disposition, completed original, conjecture, Lean or measured compression credit. Seven other L026 numerical/rank obligations remain even after a complete Rudvalis rank-three row.'
]))

Y=S/'geometry/suzuki_incidence';P=Y/'higher_publication_work'
assert hashlib.sha256((P/'portable_handoff/manifest.json').read_bytes()).hexdigest()=='523517ad0d6c5baae321f488dd8b8a34bb18d8c7fecb8c741c08745c64532581'
r=json.loads((P/'root_portable02/report.json').read_text());assert r['status']=='PASS_PORTABLE_L110_SOURCE_COMPLETION' and r['root_closure']==3020 and r['native_pages']==105 and r['verified_payload_objects']==1240
c=m.Closure();c.packet('geometry/suzuki_incidence/higher_publication_work/portable_handoff');c.packet('geometry/suzuki_incidence/higher_source_root_review');c.add(__file__)
for p in(P/'root_portable02').rglob('*'):
 if p.is_file():c.add(p)
status='ACCEPTED_L110_PORTABLE_COMPLETE_SOURCE_TREATMENT'
c.finish('geometry/suzuki_incidence/higher_publication_operational_root_review',status,dict(status=status,author='j3_recovery',reviewer='root',review=[
 'Compared the complete portable checker with the accepted L114 portable implementation. L110 changes the exact source/gate identities,63-claim ledger,48 exact proof imports, source-boundary and split arithmetic applications, and105-page assembly. It preserves the codec, exact-content reader, explicit documentary/environment boundary and no-private-fallback condition.',
 'Fresh root portable replay passed66.84seconds:3020 closure paths,1240 payload objects,273 explicit premise objects, two reused tracked public files,11 finite markings and33 panels. The boundary and scalar arithmetic readers reproduce exact retained results; no new group census is performed.',
 'The overview, two necessity papers and entire volume rebuild; all105 native page rasters match the accepted root assembly. All24 exact retained proof pairs remain available, with imported drawing streams and embedded font programs checked. Stage02 corrects numeric page sorting beyond99 only; stage01 and scientific bytes remain unchanged.',
 'Five damaged claim/scope ledgers, codec controls and both optimization guards pass. The source original and specified environment remain documentary premises rather than redistributed source bytes. No new public Markdown paths are proposed. This accepts portable packaging of the existing complete mathematical disposition, pending a separately reviewed catalogue transition from the now committed96-original baseline.'
]))
