"""UNRUN synthetic metadata controls; no matrices, original jobs or science calls."""
from pathlib import Path
import ast,copy,hashlib,json,math,os,stat,sys

def main():
    assert sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize
    assert len(sys.argv)==3
    p=Path(sys.argv[1]);a=p.lstat();sig=lambda x:(x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns)
    assert p.is_absolute()and p.resolve()==p and stat.S_ISREG(a.st_mode)and a.st_nlink==1 and a.st_size<=65536
    with p.open('rb')as f:
        z=os.fstat(f.fileno());raw=f.read(a.st_size+1);t=os.fstat(f.fileno())
    assert sig(a)==sig(z)==sig(t)==sig(p.lstat())and len(raw)==a.st_size and hashlib.sha256(raw).hexdigest()==sys.argv[2]
    tree=ast.parse(raw);defs=[n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name in {'need','can','joined','decode','unique'}]
    assert len(defs)==5;ns=dict(hashlib=hashlib,json=json,math=math)
    exec(compile(ast.Module(body=defs,type_ignores=[]),'<synthetic-scope-metadata-only>','exec'),ns)
    def fixture(end):
        # Strings stand for opaque symbols. These are not matrix or tree certificates.
        binding=dict(schema='F004_FIXED_LINE_PORTABLE_CASE_V1',original_job=[24,4],position=66,
            representative_J_index=711,end=end,end_id='position0066_'+end)
        marks=['symbol-a','symbol-b','symbol-c','symbol-e'];triple=marks[:3]if end=='left'else marks[1:]
        acq=dict(schema='F004_FIXED_LINE_ORIGINAL_REPLAY_V1',original_job=[24,4],position=66,
            representative_J_index=711,status='ORIGINAL_QUARTET_RECONSTRUCTED_ONLY',marks=marks,
            marks_sha256=hashlib.sha256(ns['can'](marks)).hexdigest())
        cert=dict(word='opaque-word-token',seed='opaque-seed-token')
        wjob=dict(schema='F004_ORDER19_FIXED_SEED_CONSUMER_V1',end_marks=triple,end_id=binding['end_id'],certificate=cert)
        rjob=dict(schema='F004_ORDER19_REACHABILITY_CONSUMER_V1',end_marks=triple,end_id=binding['end_id'],
            word=cert['word'],seed=cert['seed'],certificate='opaque-parent-carrier')
        wp=dict(schema='F004_ORDER19_FIXED_SEED_CONSUMER_PROOF_V1',end_id=binding['end_id'],certificate=cert,supplier_or_solver_imported=False)
        rp=dict(schema='F004_ORDER19_REACHABILITY_CONSUMER_PROOF_V1',end_id=binding['end_id'],certificate=rjob['certificate'],supplier_discovery_or_solver_imported=False)
        wr=dict(schema='F004_ORDER19_FIXED_SEED_CONSUMER_RESULT_V1',answer=dict(status='VERIFIED_END_WORD_ORDER19_AND_FIXED_SEED_ONLY',fixed_dimension=1,exact_prime_order=19,word=cert['word'],selected_seed=cert['seed']))
        rr=dict(schema='F004_ORDER19_REACHABILITY_CONSUMER_RESULT_V1',answer=dict(status='VERIFIED_9241_REACHABLE_AND_ORDER19_STABILIZER_ONLY',reachable_distinct=9241,parent_images_verified=9240,concrete_end_order_lower_bound=175579))
        return [binding,acq,wjob,wp,wr,rjob,rp,rr]
    checks=[]
    for end,labels,omitted in [('right',[1,2,3],0),('left',[0,1,2],3)]:
        result=ns['joined'](*fixture(end));assert result['end']==end.upper()and result['end_labels']==labels and result['omitted_label']==omitted
        assert result['conditional_conclusion']==end.upper()+'_EQUALS_G2_11_AND_ORIGINAL_MARKING_FAILS_IP'
        checks.append(end+'_exact_conclusion_and_labels')
    def reject(name,change):
        values=fixture('right');change(values)
        try:ns['joined'](*values)
        except(ValueError,KeyError):checks.append(name);return
        raise AssertionError('accepted invalid '+name)
    reject('position_mixup',lambda v:v[0].__setitem__('position',68))
    reject('representative_mixup',lambda v:v[0].__setitem__('representative_J_index',712))
    reject('side_mixup',lambda v:v[0].update(end='left',end_id='position0066_left'))
    reject('Boolean_position',lambda v:v[0].__setitem__('position',True))
    reject('wrong_end_id',lambda v:v[0].__setitem__('end_id','position0068_right'))
    reject('seed_mismatch',lambda v:v[5].__setitem__('seed','different-opaque-token'))
    reject('word_mismatch',lambda v:v[5].__setitem__('word','different-opaque-word'))
    reject('reversed_end_triple',lambda v:v[2].__setitem__('end_marks',list(reversed(v[2]['end_marks']))))
    reject('different_end_triple',lambda v:v[5].__setitem__('end_marks',['other','opaque','symbols']))
    reject('missing_fixed_dimension',lambda v:v[4]['answer'].pop('fixed_dimension'))
    assert ns['decode'](b'{"counts":{"elapsed_seconds":0.25}}')['counts']['elapsed_seconds']==0.25
    checks.append('finite_elapsed_timing_metadata_allowed')
    assert ns['decode'](b'{"count":1}')=={'count':1}
    checks.append('optional_timing_not_a_mathematical_premise')
    for name,value in [('nonfinite_timing',b'{"counts":{"elapsed_seconds":1e999}}'),
                       ('scientific_float',b'{"seed":[0.25]}')]:
        try:ns['decode'](value)
        except ValueError:checks.append(name)
        else:raise AssertionError(name)
    print(json.dumps(dict(status='PASS',controls=len(checks),checks=checks,synthetic_metadata_only=True,
        original_scientific_or_matrix_tree_operations=0,Root_authority=False)))

if __name__=='__main__':main()
