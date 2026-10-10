# Exploratory exact subgroup presentation; no inferred finite-group claims.
SizeScreen([100000,24]);;
f34s:=FreeGroup("x","y","z");;
x34s:=f34s.1;; y34s:=f34s.2;; z34s:=f34s.3;;
rels34s:=[x34s^6,y34s^3,z34s^2,(z34s*x34s)^3,(z34s*y34s)^6,
 (x34s^-1*y34s)^2,(y34s^-1*x34s^-2)^3,(z34s*x34s^3)^2,
 (x34s^-1*z34s*(y34s^-1*z34s)^2)*(z34s*x34s*(z34s*y34s)^2)];;
t34s:=y34s*(z34s*y34s)^2;;
base34s:=f34s/Concatenation(rels34s,[t34s^2]);;
unfilled34s:=f34s/rels34s;;
table34s:=CosetTable(base34s,TrivialSubgroup(base34s));;
Print("INDEX ",Length(table34s[1]),"\n");

aug34s:=AugmentedCosetTableRrs(unfilled34s,table34s,2,"k");;
aug34s.subgroupRelators:=RewriteSubgroupRelators(aug34s,aug34s.groupRelators);;
pres34s:=PresentationAugmentedCosetTable(aug34s,"k");;
TzInitGeneratorImages(pres34s);;
DecodeTree(pres34s);; TzGoGo(pres34s);;
Print("FINAL ",pres34s,"\n");
Print("NAMES ",GeneratorsOfPresentation(pres34s),"\n");
f2_34s:=FreeGroup("u","v");;
u34s:=f2_34s.1;;v34s:=f2_34s.2;;
images34s:=[u34s^-1*v34s^-1,u34s^-1*v34s^-1,One(f2_34s),One(f2_34s),u34s,u34s,One(f2_34s),v34s,One(f2_34s)];;
newgens34s:=GeneratorsOfPresentation(pres34s);;
if Length(newgens34s)<>9 then Error("unexpected presentation");fi;
oldimages34s:=List(TzImagesOldGens(pres34s),w->MappedWord(w,newgens34s,images34s));;
# A BFS transversal in the literal finite action.
num34s:=Length(table34s[1]);;
reps34s:=List([1..num34s],i->fail);;reps34s[1]:=One(f34s);;
queue34s:=[1];;at34s:=1;;
while at34s<=Length(queue34s) do
 i34s:=queue34s[at34s];;at34s:=at34s+1;;
 for j34s in [1..3] do
  dest34s:=table34s[2*j34s-1][i34s];;
  if reps34s[dest34s]=fail then
   reps34s[dest34s]:=reps34s[i34s]*GeneratorsOfGroup(f34s)[j34s];;
   Add(queue34s,dest34s);
  fi;
 od;
od;
volts34s:=[];;witness34s:=[];;
for j34s in [1..3] do
 Add(volts34s,[]);
 for i34s in [1..num34s] do
  dest34s:=table34s[2*j34s-1][i34s];;
  loop34s:=reps34s[i34s]*GeneratorsOfGroup(f34s)[j34s]*reps34s[dest34s]^-1;;
  rw34s:=RewriteWord(aug34s,loop34s);;
  if rw34s=fail then Error("bad Schreier loop");fi;
  im34s:=One(f2_34s);;
  for k34s in rw34s do im34s:=im34s*DecodedTreeEntry(aug34s.tree,oldimages34s,AbsInt(k34s))^SignInt(k34s);od;
  Add(volts34s[j34s],LetterRepAssocWord(im34s));
  if im34s=u34s or im34s=v34s then Add(witness34s,[LetterRepAssocWord(loop34s),LetterRepAssocWord(im34s)]);fi;
 od;
od;
Print("VOLTAGE_LENGTHS ",Set(Concatenation(volts34s),Length)," WITNESSES ",Length(witness34s),"\n");
PrintTo("phase34_L003_free_voltage_data.json",[table34s{[1,3,5]},volts34s,witness34s],"\n");
QUIT;
