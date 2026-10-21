"""Extract unchanged legacy functions and construct only tiny control drivers."""
import hashlib, json, pathlib
if not __debug__: raise SystemExit('optimized execution forbidden')
HERE=pathlib.Path(__file__).resolve().parent
STUDY=HERE.parents[2]
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def main():
    src=STUDY/'phase7_sporadic_search.g'; b=src.read_bytes()
    if hashlib.sha256(b).hexdigest()!='9baf2767d5109251de3d95497fe6eb6926e49652d872c5501f122bf815381981':
        raise ValueError('legacy engine changed')
    begin=b.index(b'IsMaxPair:=function'); end=b.index(b'if not IsBound(BOREL_IDS)')
    body=b[begin:end]; (HERE/'legacy_functions.g').write_bytes(body)
    ib=b.index(b'maxorders:=rec();;'); ie=b.index(b'Print("INPUT')
    init=b[ib:ie];(HERE/'legacy_initialization.g').write_bytes(init)
    (HERE/'extraction.json').write_text(json.dumps(dict(source=pin(src),function_span=[begin,end],
        initialization_span=[ib,ie],functions=pin(HERE/'legacy_functions.g'),
        initialization=pin(HERE/'legacy_initialization.g'),
        changes='No function-body change; explicit group/reps input and REQUIRE_2T=false.'),indent=2)+'\n')
    out=HERE/'small_models01';out.mkdir(exist_ok=False)
    fixtures=['SymmetricGroup(3)','Group((1,2),(3,4))','Group((1,2,3,4),(2,4))',
              'AlternatingGroup(4)','Group((1,2,3))','Group((1,2,3),(4,5,6))']
    names=['S3','C2xC2','D8','A4','C3','C3xC3']
    lines=['SizeScreen([1000000,24]);;',
           'G:=Group(());;reps:=[];;maxorders:=rec();;maxinclusions:=[];;local2T:=[];;',
           'REQUIRE_2T:=false;;OUTPUT_DIR:="";;',
           'Read('+json.dumps(str(HERE/'legacy_functions.g'))+');;',
           'controlResults:=[];;']
    for k,(name,expr) in enumerate(zip(names,fixtures)):
        d=out/name;d.mkdir()
        lines += [f'G:={expr};;', 'reps:=List(ConjugacyClassesSubgroups(G),Representative);;',
                  'Read('+json.dumps(str(HERE/'legacy_initialization.g'))+');;',
                  'OUTPUT_DIR:='+json.dumps(str(d))+';;',
                  'controlElts:=Elements(G);;',
                  'controlMul:=List(controlElts,x->List(controlElts,y->Position(controlElts,x*y)-1));;',
                  'controlEncode:=H->Set(List(Elements(H),x->Position(controlElts,x)-1));;',
                  'controlRows:=[];;',
                  'for controlBid in [1..Length(reps)] do',
                  ' RunBorel(controlBid);',
                  ' controlB:=reps[controlBid];controlPanels:=OvergroupsFromInclusions(controlB,maxinclusions);',
                  ' controlLevels:=[];',
                  ' if Length(controlPanels)>0 then',
                  '  controlA:=Image(ActionHomomorphism(Normalizer(G,controlB),controlPanels,OnPoints));',
                  '  Add(controlLevels,List(Orbits(controlA,[1..Length(controlPanels)]),o->[o[1]-1]));',
                  '  for controlRank in [2..Length(FactorsInt(Index(G,controlB)))+1] do',
                  '   Read(Concatenation(OUTPUT_DIR,"/b",String(controlBid),"_r",String(controlRank),".g"));',
                  '   if borelCheckpoint.panels<>controlPanels then Error("panel ordering changed");fi;',
                  '   Add(controlLevels,List(borelCheckpoint.level,t->List(t,i->i-1)));',
                  '   if Length(borelCheckpoint.level)=0 then break;fi;',
                  '  od;',
                  ' fi;',
                  ' Read(Concatenation(OUTPUT_DIR,"/b",String(controlBid),"_done.g"));',
                  ' Add(controlRows,[controlEncode(controlB),List(controlPanels,controlEncode),controlLevels,',
                  '   List(borelResult.geometries,t->List(t,controlEncode))]);',
                  'od;',
                  'Add(controlResults,[Size(G),controlMul,List(reps,controlEncode),',
                  ' List(maxinclusions,p->List(p,controlEncode)),controlRows]);']
    lines += ['PrintTo('+json.dumps(str(out/'models.json'))+',controlResults,"\\n");',
              'Print("PASS_SMALL_MODELS_UNCHANGED_ENGINE_NO_L100_CENSUS\\n");','QUIT_GAP(0);']
    (HERE/'small_controls.g').write_text('\n'.join(lines)+'\n')
    (out/'fixtures.json').write_text(json.dumps(names,indent=2)+'\n')
    print(json.dumps(dict(driver=pin(HERE/'small_controls.g'),output=str(out)),indent=2))
if __name__=='__main__':main()
