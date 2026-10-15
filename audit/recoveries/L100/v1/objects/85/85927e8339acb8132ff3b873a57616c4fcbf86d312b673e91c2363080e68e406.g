# Complete tiny-model equality; every saved level is compared literally.
G:=Group(());;reps:=[];;maxinclusions:=[];;maxorders:=rec();;local2T:=[];;REQUIRE_2T:=false;;OUTPUT_DIR:="";;borelCheckpoint:=rec();;borelResult:=rec();;
TestLevelResume:=function(models,root)
 local mi,subgroups,K,H,bid,full,counts,cps,cut,i,c,state,resumed,original,rr,damage,z,checks,r;
 checks:=0;
 for mi in [1..Length(models)] do
  G:=models[mi];reps:=Concatenation(List(ConjugacyClassesSubgroups(G),Elements));maxinclusions:=[];maxorders:=rec();
  for K in reps do
   maxorders.(String(Size(K))):=[];
  od;
  for K in reps do
   for H in MaximalSubgroups(K) do
    Add(maxinclusions,[K,H]);AddSet(maxorders.(String(Size(K))),Size(H));
   od;
  od;
  bid:=Position(reps,TrivialSubgroup(G));OUTPUT_DIR:=Concatenation(root,"/m",String(mi),"full");RunBorel(bid);
  Read(Concatenation(OUTPUT_DIR,"/b",String(bid),"_done.g"));full:=borelResult;
  for cut in [2..Length(full.levels)-1] do
   cps:=[];
   for r in [2..cut] do Read(Concatenation(OUTPUT_DIR,"/b",String(bid),"_r",String(r),".g"));Add(cps,borelCheckpoint);od;
   counts:=full.levels{[1..cut]};state:=ValidateLevelResume(bid,cps,counts);
   if state=fail then Error("valid saved level rejected");fi;
   for damage in [1..5] do
    z:=ShallowCopy(cps);z[Length(z)]:=ShallowCopy(z[Length(z)]);c:=z[Length(z)];
    if damage=1 then c.id:=bid+1;
    elif damage=2 then c.rank:=c.rank+1;
    elif damage=3 then c.order:=c.order+1;
    elif damage=4 then c.geometries:=Concatenation(c.geometries,[[G]]);
    else c.level:=ShallowCopy(c.level);c.level[1]:=List([1..cut],x->1);fi;
    if ValidateLevelResume(bid,z,counts)<>fail then Error("damaged saved level accepted");fi;
   od;
   original:=OUTPUT_DIR;OUTPUT_DIR:=Concatenation(root,"/m",String(mi),"resume",String(cut));RunBorelFromLevel(bid,state);
   Read(Concatenation(OUTPUT_DIR,"/b",String(bid),"_done.g"));resumed:=borelResult;
   if resumed<>full then Error("complete resumed result differs");fi;
   for r in [cut+1..Length(full.levels)] do
    Read(Concatenation(OUTPUT_DIR,"/b",String(bid),"_r",String(r),".g"));rr:=borelCheckpoint;
    Read(Concatenation(original,"/b",String(bid),"_r",String(r),".g"));
    if rr<>borelCheckpoint then Error("literal resumed checkpoint differs");fi;
   od;
   OUTPUT_DIR:=original;checks:=checks+1;
  od;
 od;
 Print("PASS_COMPLETE_LEVEL_RESUME models=",Length(models)," resumptions=",checks," damages=",5*checks,"\n");
end;
