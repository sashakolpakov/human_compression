"""Prepare, but do not execute, one exact broad-mode L100 anchor traversal."""
import argparse,hashlib,json,pathlib
if not __debug__:raise SystemExit('optimized execution forbidden')
HERE=pathlib.Path(__file__).resolve().parent
STUDY=HERE.parents[2]
INPUT_SHA='cc42a4c765b85a628b272d1ad1105a713f0a9f6635c2ed59ae8f736030d5dfc6'
ENGINE_SHA='9baf2767d5109251de3d95497fe6eb6926e49652d872c5501f122bf815381981'
def pin(p):
    b=p.read_bytes();return dict(path=str(p.resolve()),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def validate(input_path,source_path,function_path):
    assert pin(input_path)['sha256']==INPUT_SHA,'changed retained catalogue'
    assert pin(source_path)['sha256']==ENGINE_SHA,'changed legacy engine'
    source=source_path.read_bytes()
    assert function_path.read_bytes()==source[source.index(b'IsMaxPair:=function'):source.index(b'if not IsBound(BOREL_IDS)')],'function delta'
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=pathlib.Path,required=True)
    p.add_argument('--borels',default=','.join(map(str,range(95,0,-1))))
    a=p.parse_args();bids=[int(x) for x in a.borels.split(',')]
    if not bids or len(set(bids))!=len(bids) or not all(1<=b<=95 for b in bids):raise SystemExit('invalid anchor inventory')
    if not a.out.is_absolute():raise SystemExit('absolute output path required')
    inp=HERE/'input_catalogue01.g';src=STUDY/'phase7_sporadic_search.g';functions=HERE/'legacy_functions.g'
    validate(inp,src,functions)
    a.out.mkdir(parents=True,exist_ok=False);(a.out/'checkpoints').mkdir()
    s=['SizeScreen([100000,24]);;', 'INPUT_CATALOGUE:='+json.dumps(str(inp))+';;',
       'OUTPUT_DIR:='+json.dumps(str(a.out/'checkpoints'))+';;',
       'Read('+json.dumps(str(HERE/'catalogue_loader_v2.g'))+');;',
       'Read('+json.dumps(str(functions))+');;',
       'if REQUIRE_2T<>false then Error("broad mode changed");fi;',
       'BOREL_IDS:='+str(bids)+';;',
       'Print("L100_BROAD_BEGIN anchors=",BOREL_IDS,"\\n");',
       'for bid in BOREL_IDS do RunBorel(bid);od;',
       'Print("L100_REQUESTED_ANCHORS_COMPLETE\\n");','QUIT_GAP(0);']
    driver=a.out/'driver.g';driver.write_text('\n'.join(s)+'\n')
    req=dict(status='PREPARED_NOT_EXECUTED_NO_CENSUS_CREDIT',borels=bids,
             proposed_external_cap_seconds=60,require_2T=False,
             equivalence='inner conjugacy and type permutations only',
             inputs=[pin(x) for x in [inp,src,functions,HERE/'catalogue_loader_v2.g',pathlib.Path(__file__)]],
             driver=pin(driver),output=str(a.out/'checkpoints'),
             completion='Every requested Borel must have its exact done file and certified empty final level; partial request is not a complete census.')
    (a.out/'request.json').write_text(json.dumps(req,indent=2)+'\n');print(json.dumps(req,indent=2))
if __name__=='__main__':main()
