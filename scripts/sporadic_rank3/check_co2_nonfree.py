"""Replay only Co2 nonfree-orbit arithmetic on accepted normalized metadata.

Historical names are dictionary labels, never fallback filesystem paths.
No GAP, model, permutation parser, orbit algorithm or old reviewer is imported.
"""
import time
STARTED = time.monotonic()
import argparse
import ast
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import resource
import stat
import sys

ROOT = Path(__file__).resolve().parents[2]
DATA = 'data/sporadic_rank3/co2_nonfree/'
PROGRAM = 'scripts/sporadic_rank3/check_co2_nonfree.py'
PAPER = 'papers/sporadic_rank3/co2_nonfree.rst'
MAX_INPUT = 4*2**20
MAX_RESULT = 128*2**10
MAX_KEYS = 2*2**20
READS = set()


def need(ok, message):
    if not ok:
        raise ValueError(message)


def tick():
    need(time.monotonic()-STARTED < 100, 'shared observed100s refusal')
    high = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    high = high if sys.platform == 'darwin' else high*1024
    need(high < 128*2**20, 'observed128MiB refusal, not a hard memory quota')


def local(name):
    need(type(name) is str, 'relative public name')
    relative = PurePosixPath(name)
    need(not relative.is_absolute() and '..' not in relative.parts and str(relative) == name
         and (name.startswith(DATA) or name in (PROGRAM, PAPER)), 'component-relative input only')
    path = ROOT/name
    need(not any(p.is_symlink() for p in (path, *path.parents)), 'no input symlinks')
    need(path.resolve().is_relative_to(ROOT), 'public root containment')
    return path


def identity(info):
    return info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns


def exact_file(name, expected=None, keep=False):
    tick()
    path = local(name)
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and before.st_size <= MAX_INPUT,
         'bounded ordinary public input')
    digest, size, pieces = hashlib.sha256(), 0, ([] if keep else None)
    with path.open('rb', buffering=0) as stream:
        need(identity(os.fstat(stream.fileno())) == identity(before), 'stable opened file')
        if sys.platform == 'darwin':
            import fcntl
            fcntl.fcntl(stream.fileno(), 48, 1)  # Darwin F_NOCACHE; Linux does not import fcntl here.
        while True:
            block = stream.read(65536)
            if not block:
                break
            size += len(block)
            need(size <= MAX_INPUT and size <= before.st_size, 'bounded complete input')
            digest.update(block)
            if keep:
                pieces.append(block)
            tick()
        need(identity(os.fstat(stream.fileno())) == identity(before), 'stable final descriptor')
    need(size == before.st_size and identity(path.lstat()) == identity(before), 'stable complete file')
    ref = dict(path=name, bytes=size, sha256=digest.hexdigest())
    need(expected is None or ref == expected, 'externally manifested exact public bytes: '+name)
    READS.add(name)
    return ref, (b''.join(pieces) if keep else None)


def pairs(items):
    result = {}
    for key, value in items:
        need(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def number(text):
    result = float(text)
    need(math.isfinite(result), 'finite metadata number')
    return result


def json_document(raw):
    return json.loads(raw, object_pairs_hook=pairs, parse_float=number,
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))


def tree_spans(tree, function_name):
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == function_name]
    need(len(functions) == 1, 'one Source arithmetic function')
    body = functions[0].body
    loops = [n for n in body if isinstance(n, ast.For) and
             isinstance(n.target, ast.Tuple) and
             [x.id for x in n.target.elts if isinstance(x, ast.Name)] == ['scope_index', 'item']]
    need(len(loops) == 1, 'one complete accepted-scope loop')
    markers = (
        'complete global24690/3627/21063 domain and whole group mass',
        'independent total orbit lengths and row histogram')
    selected = [loops[0]]
    for marker in markers:
        rows = [n for n in body if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
                and any(isinstance(x, ast.Constant) and x.value == marker for x in n.value.args)]
        need(len(rows) == 1, 'one exact acquired global invariant')
        selected.append(rows[0])
    for target in ('ordered', 'digest'):
        rows = [n for n in body if isinstance(n, ast.Assign) and
                any(isinstance(x, ast.Name) and x.id == target for x in n.targets)]
        need(len(rows) == 1, 'one exact key-table calculation')
        selected.append(rows[0])
    return [ast.dump(n, include_attributes=False) for n in selected]


def authenticate(expected_sha256):
    manifest_name = DATA+'manifest.json'
    manifest_ref, raw = exact_file(manifest_name, keep=True)
    need(type(expected_sha256) is str and len(expected_sha256) == 64
         and manifest_ref['sha256'] == expected_sha256, 'external manifest SHA256 required')
    manifest = json_document(raw)
    need(manifest['schema'] == 'CO2_CONDITIONAL_NONFREE_ORBIT_PUBLIC_COMPONENT_V1'
         and manifest['scope'] == 'CONDITIONAL_NONFREE_METADATA_ARITHMETIC_ONLY'
         and manifest['mathematical_model_recomputed'] is False
         and manifest['whole_original_credit'] == 0, 'exact partial component boundary')
    rows = manifest['files']
    need(type(rows) is list and 1 <= len(rows) <= 64, 'bounded exact component roster')
    table = {}
    for row in rows:
        need(type(row) is dict and set(row) == {'path','bytes','sha256','role'}, 'manifest row fields')
        ref = {key:row[key] for key in ('path','bytes','sha256')}
        need(type(ref['bytes']) is int and ref['bytes'] >= 0 and ref['path'] not in table,
             'unique strict manifest row')
        exact_file(ref['path'], ref)
        table[ref['path']] = ref
    need(PROGRAM in table and PAPER in table and sum(r['bytes'] for r in table.values()) <= 8*2**20,
         'program/proof and whole8MiB component bound')
    def load(name):
        need(name in table, 'declared relative input')
        return json_document(exact_file(name, table[name], True)[1])
    mapping = load(DATA+'source_map.json')
    need(mapping['schema'] == 'CO2_PUBLIC_EXACT_LOGICAL_SOURCE_MAP_V1', 'source identity map')
    aliases = {}
    for row in mapping['files']:
        need(set(row) == {'original_path','public_path','bytes','sha256','role'}
             and type(row['original_path']) is str and row['original_path'].startswith('/')
             and row['original_path'] not in aliases, 'unique historical identity label')
        need(table[row['public_path']] == {key:row[key] for key in ('bytes','sha256')}|
             dict(path=row['public_path']), 'same exact original/public bytes')
        aliases[row['original_path']] = row
    def doc(ref):
        # Never Path(ref['path']): historical names are authenticated map keys.
        need(type(ref) is dict and set(ref) == {'path','bytes','sha256'}
             and ref['path'] in aliases, 'declared old identity, no private fallback')
        row = aliases[ref['path']]
        need((row['bytes'],row['sha256']) == (ref['bytes'],ref['sha256']), 'exact old/public identity join')
        return load(row['public_path'])
    reference = manifest['arithmetic_reference']
    need(reference == table[reference['path']], 'exact manifested reference identity')
    reference_raw = exact_file(reference['path'], table[reference['path']], True)[1]
    own_raw = exact_file(PROGRAM, table[PROGRAM], True)[1]
    old_spans = tree_spans(ast.parse(reference_raw), 'main')
    new_spans = tree_spans(ast.parse(own_raw), 'arithmetic')
    need(old_spans == new_spans, 'five whole mathematical AST spans unchanged from accepted reviewer')
    need([hashlib.sha256(x.encode()).hexdigest() for x in old_spans] == manifest['arithmetic_AST_sha256'],
         'manifested exact arithmetic ancestry')
    return manifest_ref, manifest, table, load, doc


def arithmetic(inventory, m, doc, tick):
    expected_inputs = []
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
    ordered=sorted(nonfree,key=lambda r:(r['top_index'],r['top_row']))
    digest=hashlib.sha256(json.dumps(ordered,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return dict(whole_rows=len(all_keys),whole_mass=full_mass,nonfree_rows=len(nonfree),
        full_size_rows=histogram[1280],normalized_metadata_bytes=normal_bytes,
        orbit_size_histogram={str(k):histogram[k]for k in sorted(histogram)},
        block_totals=sorted(block_summary,key=lambda row:row['top_index']),
        ordered_nonfree_keys=ordered,key_table_sha256=digest)


def write_once(path, value, cap, encoded=False):
    raw = value if encoded else (json.dumps(value,sort_keys=True,indent=2)+'\n').encode()
    need(type(raw) is bytes and len(raw) <= cap, 'whole bounded output, no truncation')
    with path.open('xb') as stream:
        stream.write(raw)
    return dict(path=path.name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def main():
    need(sys.platform in ('darwin','linux') and not sys.flags.optimize,
         'ordinary Python3.11+ on macOS/Linux, no optimization')
    sys.dont_write_bytecode = True
    parser = argparse.ArgumentParser(description=__doc__,allow_abbrev=False)
    parser.add_argument('--manifest-sha256',required=True)
    parser.add_argument('--metadata-only',action='store_true')
    parser.add_argument('--out',type=Path)
    args = parser.parse_args()
    manifest_ref, manifest, table, load, doc = authenticate(args.manifest_sha256)
    if args.metadata_only:
        need(args.out is None, 'metadata-only writes no output')
        print(json.dumps(dict(status='PASS_CO2_NONFREE_COMPONENT_METADATA',files=len(table),
            arithmetic_replayed=False,model_or_group_calls=0,whole_original_credit=0)))
        return
    need(args.out is not None and args.out.is_absolute() and not os.path.lexists(args.out)
         and args.out.parent.is_dir(), 'fresh absolute external output')
    out = args.out.resolve()
    need(not out.is_relative_to(ROOT) and not ROOT.is_relative_to(out)
         and not any(p.is_symlink() for p in (args.out,*args.out.parents)), 'outputs outside canonical checkout')
    out.mkdir()
    write_once(out/'started.json',dict(status='STARTED_CONDITIONAL_CO2_NONFREE_ARITHMETIC',
        manifest_sha256=args.manifest_sha256,model_recomputed=False),4096)
    try:
        premises = load(DATA+'premises.json')
        expected = load(DATA+'expected.json')
        inventory = doc(manifest['inventory_original_identity'])
        m = doc(manifest['shared_manifest_original_identity'])
        need(premises['kind'] == 'IMPORTED_NAMED_GROUP_AND_ORBIT_PARTITION_PREMISES'
             and premises['centerless_named_group'] == 'Co2'
             and premises['pointwise_S_definition'] == 'C_G(a,c)'
             and premises['pointwise_S_order'] == 1280 and premises['U_order'] == 1474560
             and premises['full_size_does_not_imply_generation'] is True
             and premises['positive_orbit_bijection_checked'] is False, 'honest imported mathematical premises')
        need(inventory['pair'] == 12 and inventory['middle_class'] == 1
             and inventory['top_blocks'] == 178 and inventory['domain_rows'] == 24690
             and len(inventory['scopes']) == 12 and inventory['borrowed_partition_and_named_model_premises'] is True,
             'complete acquired normalized domain remains a premise')
        need(m['configuration']['centralizer_order'] == 1474560
             and m['configuration']['pointwise_order'] == 1280
             and m['configuration']['group_order'] == m['configuration']['ambient_order'] == 42305421312000,
             'exact borrowed scalar application, not order-only model identification')
        outcome = arithmetic(inventory,m,doc,tick)
        need(outcome['key_table_sha256'] == expected['key_table_sha256']
             and outcome['orbit_size_histogram'] == expected['orbit_size_histogram']
             and outcome['whole_rows'] == expected['whole_rows']
             and outcome['nonfree_rows'] == expected['nonfree_rows']
             and outcome['full_size_rows'] == expected['full_size_rows']
             and outcome['whole_mass'] == expected['whole_mass'], 'whole independently derived expected arithmetic')
        keys = outcome.pop('ordered_nonfree_keys')
        raw = json.dumps(keys,sort_keys=True,separators=(',',':')).encode()
        need(hashlib.sha256(raw).hexdigest() == expected['key_table_sha256'], 'entire unchanged canonical key table')
        for name, ref in table.items():
            exact_file(name,ref)
        need(exact_file(DATA+'manifest.json')[0] == manifest_ref, 'manifest stable after complete replay')
        tick()
        keys_pin = write_once(out/'nonfree_keys.json',raw,MAX_KEYS,encoded=True)
        report = dict(status='PASS_CONDITIONAL_CO2_NONFREE_ORBIT_ARITHMETIC',
            manifest_sha256=args.manifest_sha256,**outcome,nonfree_key_table=keys_pin,
            imported_premises=DATA+'premises.json',all_component_bytes_unchanged=True,
            exact_arithmetic_AST_ancestry_checked=True,mathematical_model_recomputed=False,
            group_or_permutation_or_orbit_algorithm_calls=0,full_size_rows_remain_undecided=True,
            generating_or_self_dual_orbit_counts_not_derived=True,new_cells=0,census_credit=0,
            whole_original_credit=0,conjecture_or_Lean_or_measurement_credit=0,
            seconds=time.monotonic()-STARTED,
            observed_peak_self_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
            fit_claim=False)
        tick()
        result_pin = write_once(out/'result.json',report,MAX_RESULT)
        print(json.dumps(dict(status=report['status'],nonfree_rows=report['nonfree_rows'],
            full_size_rows=report['full_size_rows'],result=result_pin,whole_original_credit=0)))
    except BaseException as error:
        write_once(out/'failure.json',dict(status='FAILED_CONDITIONAL_CO2_NONFREE_REPLAY',
            error=dict(type=type(error).__name__,message=str(error)[:2048]),
            no_success_claim=True,seconds=time.monotonic()-STARTED),65536)
        raise


if __name__ == '__main__':
    main()
