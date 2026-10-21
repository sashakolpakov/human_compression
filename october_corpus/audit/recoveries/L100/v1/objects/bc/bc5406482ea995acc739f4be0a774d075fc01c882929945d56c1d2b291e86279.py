"""Fresh seven-model replay of the unchanged engine and broad validator."""
import argparse,copy,hashlib,json,pathlib,subprocess,sys,time
if not __debug__:raise SystemExit('optimized execution forbidden')
sys.dont_write_bytecode=True
import literal_oracle as oracle
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=pathlib.Path);a=p.parse_args()
    here=pathlib.Path(__file__).resolve().parent;out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
    names=['S3','C2xC2','D8','A4','C3','C3xC3','C2xC2xC2']
    fixtures=['SymmetricGroup(3)','Group((1,2),(3,4))','Group((1,2,3,4),(2,4))','AlternatingGroup(4)',
              'Group((1,2,3))','Group((1,2,3),(4,5,6))','Group((1,2),(3,4),(5,6))']
    q=lambda p:json.dumps(str(p))
    lines=['SizeScreen([1000000,24]);;',
       'G:=Group(());;reps:=[];;maxorders:=rec();;maxinclusions:=[];;local2T:=[];;',
       'REQUIRE_2T:=false;;OUTPUT_DIR:="";;',
       'Read('+q(here/'legacy_functions.g')+');;', 'Read('+q(here/'accepted_verify.g')+');;',
       'controlResults:=[];;controlVerified:=0;;controlNonTwo:=0;;controlB:=G;;controlFam:=[];;']
    for name,expr in zip(names,fixtures):
        d=out/name;d.mkdir()
        lines += [f'G:={expr};;','reps:=List(ConjugacyClassesSubgroups(G),Representative);;',
           'Read('+q(here/'legacy_initialization.g')+');;', 'OUTPUT_DIR:='+q(d)+';;',
           'controlElts:=Elements(G);;',
           'controlMul:=List(controlElts,x->List(controlElts,y->Position(controlElts,x*y)-1));;',
           'controlEncode:=H->Set(List(Elements(H),x->Position(controlElts,x)-1));;',
           'controlRows:=[];;',
           'for controlBid in [1..Length(reps)] do',
           ' RunBorel(controlBid);',
           ' controlB:=reps[controlBid];controlPanels:=OvergroupsFromInclusions(controlB,maxinclusions);controlLevels:=[];',
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
           ' Add(controlRows,[controlEncode(controlB),List(controlPanels,controlEncode),controlLevels,List(borelResult.geometries,t->List(t,controlEncode))]);',
           ' for controlFam in borelResult.geometries do',
           '  if Length(controlFam)<2 then continue;fi;',
           '  controlPars:=List([1..Length(controlFam)],i->JoinPanels(controlB,controlFam{Difference([1..Length(controlFam)],[i])}));',
           '  controlR:=VerifyGeometry(G,controlPars);',
           '  if not (controlR.firm and controlR.ft and controlR.rc and controlR.rwpri and controlR.ip2 and controlR.join and controlR.borel=Size(controlB)) then Error("broad validation");fi;',
           '  controlVerified:=controlVerified+1;if not controlR.twot then controlNonTwo:=controlNonTwo+1;fi;',
           ' od;',
           'od;',
           'Add(controlResults,[Size(G),controlMul,List(reps,controlEncode),List(maxinclusions,p->List(p,controlEncode)),controlRows]);']
    lines += ['PrintTo('+q(out/'models.json')+',controlResults,"\\n");',
       'if controlVerified<>64 or controlNonTwo<>8 then Error("recognition control inventory");fi;',
       'INPUT_CATALOGUE:='+q(here/'input_catalogue01.g')+';;',
       'Read('+q(here/'catalogue_loader_v2.g')+');;',
       'if Length(reps)<>95 or Length(maxinclusions)<>367 or REQUIRE_2T<>false then Error("loader contract");fi;',
       'Print("PASS_FRESH_SEVEN_MODELS_AND_LOADER_NO_L100_EXTENSIONS\\n");','QUIT_GAP(0);']
    driver=out/'driver.g';driver.write_text('\n'.join(lines)+'\n')
    cmd=['/opt/homebrew/bin/gap','-q','-b',str(driver)];start=time.monotonic()
    receipt=dict(status='RUNNING',command=cmd,cap_seconds=30,target_census=False)
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    with (out/'stdout').open('wb') as so,(out/'stderr').open('wb') as se:
        try:
            r=subprocess.run(cmd,stdout=so,stderr=se,timeout=30);receipt.update(returncode=r.returncode,status='RETURNED')
        except subprocess.TimeoutExpired:receipt.update(returncode=None,status='DEADLINE')
    receipt['elapsed']=time.monotonic()-start
    receipt['semantic_pass']=receipt['returncode']==0 and not (out/'stderr').read_bytes() and b'PASS_FRESH_SEVEN_MODELS_AND_LOADER_NO_L100_EXTENSIONS' in (out/'stdout').read_bytes()
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    assert receipt['semantic_pass'],receipt
    models=json.loads((out/'models.json').read_text());assert len(models)==7
    reports=[oracle.check_model(n,m) for n,m in zip(names,models)]
    changes=[]
    def damage(name,fn):
        m=copy.deepcopy(models[-1]);fn(m)
        try:oracle.check_model('C2xC2xC2',m)
        except (AssertionError,ValueError,IndexError,KeyError,StopIteration):changes.append(name);return
        raise AssertionError('damage accepted: '+name)
    damage('missing subgroup',lambda m:m[2].pop())
    damage('missing inclusion',lambda m:m[3].pop())
    damage('missing Borel',lambda m:m[4].pop())
    damage('duplicate panel',lambda m:m[4][0][1].append(m[4][0][1][0]))
    damage('missing rank3',lambda m:m[4][0][2][2].pop())
    damage('duplicate family',lambda m:m[4][0][2][1].append(m[4][0][2][1][0]))
    damage('missing terminal',lambda m:m[4][0][2].pop())
    damage('missing full family',lambda m:m[4][0][3].pop())
    report=dict(status='PASS_FRESH_BROAD_APPLICABILITY_SMALL_CONTROLS',models=reports,damages=changes,
                target_runs=0,broad_recognition=64,non_two_transitive=8)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
