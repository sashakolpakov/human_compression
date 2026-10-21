from pathlib import Path
import hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans');Y=S/'geometry/suzuki_incidence';P=Y/'publication_work'
assert hashlib.sha256((P/'portable_handoff/manifest.json').read_bytes()).hexdigest()=='50e6e0d0670c315469ec06b3d6bc731021467314d63816de4c296bbb653f7c7d'
r=json.loads((P/'root_portable02/report.json').read_text());assert r['status']=='PASS_PORTABLE_L114_SOURCE_COMPLETION' and r['root_closure']==1639 and r['native_pages']==68 and r['finite_markings']==11 and r['finite_panels']==33
assert r['stage_manifest']['sha256']=='8d4971228fd389c5892676926a87cb320362a2be1a06ec5d5bc07204e5cd7c88' and r['transport']['sha256']=='2bcc4a2007c14b5d5b50f800f14aec83839fa8c9c85768d299745c63d9e06a95'
prefix=Path('audit/principal-refutations/L114/complete/v1')
a=(P/'stage01'/prefix/'portable_check.py').read_text();b=(P/'stage02'/prefix/'portable_check.py').read_text()
for x,y in [('prime_patterns_author01','prime_patterns_root01'),('remaining_markings_application_author01','remaining_markings_root01'),('nonthin_application02_author01','nonthin_root01'),('nonthin32_application_author01','nonthin32_root01')]:assert a.count(x)==1;a=a.replace(x,y)
assert a==b
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.Closure();c.packet('geometry/suzuki_incidence/publication_work/portable_handoff');c.packet('geometry/suzuki_incidence/source_synthesis_root_review');c.add(__file__)
for p in (P/'root_portable02').rglob('*'):
 if p.is_file():c.add(p)
status='ACCEPTED_L114_PORTABLE_COMPLETE_SOURCE_TREATMENT'
c.finish('geometry/suzuki_incidence/publication_operational_root_review',status,dict(status=status,author='j3_recovery',reviewer='root',review=[
 'Read the complete portable reader and its reused archive interface. Verified the stage01-to02 delta consists solely of four report locators corrected to their accepted root reports. All scientific content and the original stage are retained.',
 'Fresh root portable replay passed59.05seconds, acquiring the exact1639-path accepted closure and780 scientific payload objects. The263 premise objects are explicitly documentary originals or installed software/environment; mathematical selected inputs cannot fall back to unavailable premise bytes or private paths.',
 'The packed transport covers exactly the declared spans, reuses one tracked public file, and makes every accepted proof available as readable native TeX/PDF. Twenty-eight proof imports are exact; the16 papers contain67 mathematical pages plus a volume cover.',
 'All17 TeX entrypoints rebuilt, page streams/font programs matched and all68 rendered native pages matched the accepted science. The unchanged literal readers verify11 markings and33 actual panels with their damage controls. The only two reader adapters change one literal path apiece; original bytes remain in the archive.',
 'Four damaged source-credit/scope ledgers and both optimization guards reject. No new group acquisition or principal-refutation credit is claimed. This accepts the portable artifact for registration as completion of the existing L114 refutation; public counts remain unchanged until the separately checked catalogue transition.'
]))
