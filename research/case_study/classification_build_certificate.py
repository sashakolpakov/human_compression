"""Bind recorded classification results and available inputs by hash.

The public checkout excludes third-party source PDFs and some operational
sidecars. Their original hashes remain explicitly labeled historical metadata.
This script does not rerun the GAP census or the independent witness checker.
"""
from pathlib import Path
import argparse,hashlib,json,os,re,shutil,subprocess
BASE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--gap',default=os.environ.get('GAP') or shutil.which('gap'),
                    help='GAP executable; defaults to GAP environment variable or PATH')
parser.add_argument('--tomlib-data',type=Path,
                    help='TomLib data directory containing tmjank.tom.gz and tmtw.tom.gz; otherwise ask GAP')
parser.add_argument('--sources-dir',type=Path,default=BASE/'sources',
                    help='Optional directory containing the original source PDFs')
args=parser.parse_args()
if args.tomlib_data:
    DATA=args.tomlib_data.expanduser().resolve()
    INFO=DATA.parent/'PackageInfo.g'
else:
    if not args.gap:
        parser.error('GAP was not found; install it on PATH, set GAP, or supply --tomlib-data')
    query='''
SizeScreen([100000,24]);;
if LoadPackage("tomlib")=fail then Error("TomLib is not installed"); fi;
Print("TOMLIB_DATA_FILE=",Filename(DirectoriesPackageLibrary("tomlib","data"),"tmjank.tom.gz"),"\\n");
Print("TOMLIB_INFO_FILE=",Filename(DirectoriesPackageLibrary("tomlib",""),"PackageInfo.g"),"\\n");
QUIT;
'''
    run=subprocess.run([args.gap,'--quitonbreak','-q'],input=query,text=True,
                       capture_output=True,timeout=30)
    data_match=re.search(r'TOMLIB_DATA_FILE=([^\r\n]+)',run.stdout)
    info_match=re.search(r'TOMLIB_INFO_FILE=([^\r\n]+)',run.stdout)
    if run.returncode or not data_match or not info_match:
        parser.error('GAP could not locate TomLib; install TomLib or supply --tomlib-data')
    DATA=Path(data_match.group(1)).parent
    INFO=Path(info_match.group(1))
for required in [DATA/'tmjank.tom.gz',DATA/'tmtw.tom.gz']:
    if not required.is_file():
        parser.error(f'TomLib data file is missing: {required.name}')

prior_path=BASE/'classification_compression_certificate.json'
prior=json.loads(prior_path.read_text()) if prior_path.exists() else {}
historical={Path(row['file']).name:row for key in ['artifacts','primary_sources','imported_subgroup_data']
            for row in prior.get(key,[])}
def file_record(path,label=None,allow_historical=False):
    path=Path(path)
    if label is not None: name=label
    else:
        try: name=str(path.relative_to(BASE))
        except ValueError: name=path.name
    if not path.is_file():
        if not allow_historical or path.name not in historical:
            raise FileNotFoundError(f'Required artifact is unavailable: {name}')
        record={k:v for k,v in historical[path.name].items() if k in ['bytes','sha256']}
        return dict(record,file=name,verification='historical_metadata_only_not_reverified')
    return {'file':name,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
outputs=['classification_compression.md','classification_rank2_census.g','classification_rank2_census.log','classification_rank2_census.time','classification_J2_representatives.json','classification_Sz8_representatives.json','classification_normalizer_check.g','classification_normalizer_check.log','classification_normalizer_check.stderr','classification_a4_torsor_check.g','classification_a4_torsor_check.log','classification_field_orbits.g','classification_field_orbits.log','classification_verify_witnesses.py','classification_witness_check.json']
log=(BASE/'classification_rank2_census.log').read_text().replace('\r','')
assert 'REPRODUCTION_PASS J2' in log and 'REPRODUCTION_PASS Sz(8)' in log
field=(BASE/'classification_field_orbits.log').read_text()
assert field.count(' PASS')==4
witness=json.loads((BASE/'classification_witness_check.json').read_text())
assert witness['pass'], 'Independent witness check has not passed'
groups=[]
for name,expected in [('J2',8),('Sz8',29)]:
    data=json.loads((BASE/f'classification_{name}_representatives.json').read_text())
    assert len(data['representatives'])==expected
    groups.append({'group':data['group'],'order':data['order'],'subgroup_conjugacy_classes_imported':data['tom_subgroup_classes'],'accepted_local_inclusion_classes':data['local_inclusion_classes'],'representatives_verified':expected,'require_2transitive':data['require_2transitive'],'require_IP2':data['require_IP2']})
source_records=[]
for filename,url,locator in [
('catalogue_L063.pdf','https://amc-journal.eu/index.php/amc/article/download/181/241','2013 paper: §2 equivalence definition; §4.1 Lemma 4.1; Tables 2 and 5'),
('catalogue_L064.pdf','https://amc-journal.eu/index.php/amc/article/download/181/1862','Publisher-hosted appendix, proof of Proposition 26'),
('catalogue_L104.pdf','https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v21n1p77/585','2002 paper §3: 8 rank-two, 19 rank-three, 3 rank-four; only rank-two reproduced'),
('older_L115_emis.pdf','https://emis.de/ft/11479','1998 paper Corollary 8.1: 29 rank-two Sz(8) geometries'),
('psl2_chiral2017.pdf','https://arxiv.org/pdf/1606.08017','§2.2 Proposition 2.3, preprint page 5: maximal subgroup theorem')]:
    r=file_record(args.sources_dir/filename,label='sources/'+filename,allow_historical=True)
    r.update(url=url,locator=locator);source_records.append(r)
imported=[file_record(DATA/'tmjank.tom.gz',label='TomLib/data/tmjank.tom.gz'),
          file_record(DATA/'tmtw.tom.gz',label='TomLib/data/tmtw.tom.gz'),
          file_record(INFO,label='TomLib/PackageInfo.g',allow_historical=True)]
for record in imported[:2]:
    expected=historical.get(Path(record['file']).name)
    if expected and record['sha256']!=expected['sha256']:
        raise SystemExit('Installed TomLib data differ from the recorded census input. Rerun the census and review the input change before rebuilding this certificate.')
timing=BASE/'classification_rank2_census.time'
run_time=timing.read_text().strip() if timing.exists() else prior.get('rank2_census_run_time','not recorded')
result={
 'as_of':'2026-10-09','status':'passed',
 'scope':'Exact finite computational reproductions conditional on complete imported subgroup-class datasets; independent witness validity checks; finite-field orbit checks of a written all-odd-degree theorem. No Lean certification of these computations or subgroup catalogues is claimed.',
 'software':{'GAP':'4.15.1','TomLib':'1.2.11'},
 'software_scope':'Versions recorded for the original computations; this rebuild checks dataset hashes but does not rerun those computations.',
 'rebuild_scope':'Available artifacts are hashed now. Excluded source PDFs and operational sidecars retain explicitly marked historical hashes and are not reverified. No GAP census or witness verification is rerun by this builder.',
 'counts':groups,
 'finite_field_degrees_verified':[3,5,7,9],
 'finite_field_aut_orbit_counts':[2,8,52,366],
 'rank2_census_run_time':run_time,
 'rank2_census_run_time_scope':'Current timing sidecar' if timing.exists() else 'Historical metadata; timing sidecar not redistributed',
 'imported_subgroup_data':imported,
 'imported_data_documentation':'https://gap-packages.github.io/tomlib/doc/chap1.html',
 'imported_data_limitation':'Completeness of the 146 J2 and 22 Sz(8) subgroup conjugacy classes is assumed from TomLib. The enumerator recomputes incidence conditions, normalizer orbits, reversal and automorphism fusion. The separate witness checker checks validity but not completeness or pairwise inequivalence.',
 'artifacts':[file_record(BASE/f,allow_historical=f.endswith(('.time','.stderr'))) for f in outputs],
 'primary_sources':source_records,
 'automorphism_theorem_source':{'url':'https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/finite-groups-the-centralizers-of-whose-involutions-have-normal-2complements/6FBC01E6154FF052A081196345F335E9','locator':'Gorenstein, Canadian Journal of Mathematics 21 (1969), p.335, opening paragraph; publisher extract checked'},
 'table_correction_scope':'In the checked 2013 version, the conjugacy definition permits swapping parabolics, while some Table 2/Table 5 values count ordered pairs. Isomorphism counts match. No general claim of publication novelty.',
 'reproduction_commands':['gap --quitonbreak -q research/leemans/classification_rank2_census.g','gap --quitonbreak -q research/leemans/classification_normalizer_check.g','gap --quitonbreak -q research/leemans/classification_a4_torsor_check.g','gap --quitonbreak -q research/leemans/classification_field_orbits.g','python3 research/leemans/classification_verify_witnesses.py']
}
(BASE/'classification_compression_certificate.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':result['status'],'groups':groups,'run_time':result['rank2_census_run_time']},indent=2))
