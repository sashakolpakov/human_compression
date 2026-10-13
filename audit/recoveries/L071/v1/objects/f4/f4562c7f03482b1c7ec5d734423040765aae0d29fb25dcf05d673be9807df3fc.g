Read("model.g");;Read("records.g");;Read("source.g");;
if Size(G)<>expectedOrder or not IsNormal(A,G) then Error("model");fi;
if Size(A)/Size(Centralizer(A,G))<>Size(AutomorphismGroup(G)) then
 Error("full automorphism action");fi;
root:=rec(marks:=[],children:=[],leaf:=fail);;
allCount:=0;;
for rank in [1..Length(recordedMarks)] do
 for index in [1..Length(recordedMarks[rank])] do
  t:=recordedMarks[rank][index];;node:=root;;
  for x in t do
   pos:=Position(node.marks,x);;
   if pos=fail then
    Add(node.marks,x);Add(node.children,rec(marks:=[],children:=[],leaf:=fail));
    pos:=Length(node.marks);
   fi;
   node:=node.children[pos];;
  od;
  if node.leaf<>fail then Error("duplicate literal recorded tuple");fi;
  node.leaf:=[rank,index];;allCount:=allCount+1;
 od;
od;
if Length(sourceTuples)<>allCount then Error("source cardinality");fi;
matched:=[];;
if Length(sourceTuples)>0 then
 H:=Group(sourceTuples[1]);;
 if Size(H)<>expectedOrder or not ForAll(sourceGens,x->x in H) then
  Error("source group consistency");fi;
 iso:=IsomorphismGroups(H,G);;
 if iso=fail or not IsBijective(iso) then Error("source model isomorphism");fi;
 Print("SOURCE_MODEL_GENERATORS ",GeneratorsOfGroup(H),"\n");
 Print("SOURCE_MODEL_IMAGES ",List(GeneratorsOfGroup(H),x->Image(iso,x)),"\n");
 sourceImages:=List(sourceGens,x->Image(iso,x));;
 Print("ALL_SOURCE_GENERATOR_IMAGES ",sourceImages,"\n");
 for sourceIndex in [1..Length(sourceTuples)] do
  original:=List(sourceTuples[sourceIndex],x->sourceImages[Position(sourceGens,x)]);;
  t:=ShallowCopy(original);;node:=root;;St:=A;;transporter:=One(A);;
  for i in [1..Length(t)] do
   found:=fail;;
   for j in [1..Length(node.marks)] do
    h:=RepresentativeAction(St,t[i],node.marks[j]);;
    if h<>fail then found:=[j,h];break;fi;
   od;
   if found=fail then Error("no matching orbit");fi;
   j:=found[1];;h:=found[2];;
   if not h in St or t[i]^h<>node.marks[j] then Error("transporter");fi;
   t:=List(t,x->x^h);;transporter:=transporter*h;;
   St:=Centralizer(St,node.marks[j]);;node:=node.children[j];;
  od;
  if node.leaf=fail or node.leaf in matched then Error("missing or repeated leaf");fi;
  if not transporter in A or List(original,x->x^transporter)<>
      recordedMarks[node.leaf[1]][node.leaf[2]] then Error("literal tuple match");fi;
  Add(matched,ShallowCopy(node.leaf));
  Print("SOURCE_MATCH ",sourceIndex," LEAF ",node.leaf," TRANSPORTER ",transporter,"\n");
 od;
fi;
if Length(matched)<>allCount then Error("not a bijection");fi;
Print("COMPLETE_SOURCE_ORBIT_BIJECTION ",modelName," CLASSES ",allCount,"\n");QUIT;
