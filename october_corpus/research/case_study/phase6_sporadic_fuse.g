# Fuse independently enumerated geometries under full group automorphisms and types.
# Required: GROUP_NAME, CHECKPOINT_DIR, OUTPUT_FILE.
LoadPackage("tomlib");;
SizeScreen([100000,24]);;
tom:=TableOfMarks(GROUP_NAME);;G:=UnderlyingGroup(tom);;A:=AutomorphismGroup(G);;
all:=[];;
for bid in [1..Length(OrdersTom(tom))] do
 Read(Concatenation(CHECKPOINT_DIR,"/b",String(bid),"_done.g"));
 if borelResult.id<>bid then Error("checkpoint id mismatch");fi;
 for t in borelResult.geometries do
  if Length(t)<2 then continue;fi;
  Add(all,rec(borel_id:=bid,borel_order:=borelResult.order,panels:=t,parabolics:=List([1..Length(t)],i->Group(Concatenation(List(t{Difference([1..Length(t)],[i])},GeneratorsOfGroup))))));
 od;
od;
AutoSub:=function(H,a) return Image(a,H);end;
Signature:=function(p)
 return [SortedList(List(p,Size)),SortedList(List(Combinations([1..Length(p)],2),ij->Size(Intersection(p[ij[1]],p[ij[2]])))),Size(Intersection(p))];
end;
EquivalentFamilies:=function(A,p,q)
 local perm,ord,cur,C,x,i;
 if Signature(p)<>Signature(q) then return false;fi;
 for perm in SymmetricGroup(Length(p)) do
  ord:=Permuted(q,perm);
  if List(p,Size)<>List(ord,Size) then continue;fi;
  cur:=ShallowCopy(p);C:=A;x:=fail;
  for i in [1..Length(p)] do
   x:=RepresentativeAction(C,cur[i],ord[i],AutoSub);
   if x=fail then break;fi;
   cur:=List(cur,H->Image(x,H));C:=Stabilizer(C,ord[i],AutoSub);
  od;
  if x<>fail then return true;fi;
 od;
 return false;
end;
allFinal:=[];;counts:=[];;candidates:=[];;classes:=[];;
for rank in [2..Length(FactorsInt(Size(G)))+1] do
 candidates:=Filtered(all,e->Length(e.panels)=rank);classes:=[];orbits:=[];
 for i in [1..Length(candidates)] do
  hit:=First([1..Length(classes)],j->EquivalentFamilies(A,candidates[classes[j]].parabolics,candidates[i].parabolics));
  if hit=fail then Add(classes,i);Add(orbits,[i]);else Add(orbits[hit],i);fi;
 od;
 counts[rank]:=Length(classes);Append(allFinal,candidates{classes});
 Print("FUSION rank=",rank," inner_classes=",Length(candidates)," aut_type_classes=",Length(classes)," orbits=",orbits,"\n");
 Print("BOREL_CLASSES rank=",rank," orders=",List(candidates{classes},e->e.borel_order),"\n");
od;
# Exact post-processing: the later 2T tables suppress truncations.
# These checks do not affect the exhaustive search or automorphism fusion.
for e in allFinal do
 B:=Intersection(e.parabolics);
 e.twot:=ForAll(e.panels,P->Length(DoubleCosets(P,B,B))=2);
 e.truncation_from:=[];
od;
for i in [1..Length(allFinal)] do
 e:=allFinal[i];rank:=Length(e.panels);
 if not e.twot then continue;fi;
 for j in [1..Length(allFinal)] do
  f:=allFinal[j];
  if not f.twot or Length(f.panels)<=rank then continue;fi;
  if ForAny(Combinations([1..Length(f.panels)],rank),J->EquivalentFamilies(A,e.parabolics,f.parabolics{J})) then
   Add(e.truncation_from,j);
  fi;
 od;
od;
for rank in [2..Length(counts)] do
 Print("LOCAL_2T rank=",rank," total=",Number(allFinal,e->Length(e.panels)=rank and e.twot)," nontruncations=",Number(allFinal,e->Length(e.panels)=rank and e.twot and Length(e.truncation_from)=0),"\n");
od;
PrintTo(OUTPUT_FILE,"# Independently enumerated geometry witnesses.\nG:=",G,";\nSporadicRepresentatives:=",allFinal,";\n");
Print("FULL_CENSUS_PASS counts=",List([2..Length(counts)],r->counts[r])," aut_order=",Size(A),"\n");
