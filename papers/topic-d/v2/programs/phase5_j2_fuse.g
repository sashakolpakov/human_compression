# Fuse independently enumerated J2 geometries; no published geometry list read.
LoadPackage("tomlib");;
SizeScreen([100000,24]);;
G:=UnderlyingGroup(TableOfMarks("J2"));;A:=AutomorphismGroup(G);;
all:=[];;
for bid in [1..146] do
 Read(Concatenation("research/leemans/phase5_j2_checkpoints/b",String(bid),"_done.g"));
 if borelResult.id<>bid then Error("checkpoint id mismatch");fi;
 for t in borelResult.J2 do
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
allFinal:=[];;counts:=[];;
for rank in [2..14] do
 candidates:=Filtered(all,e->Length(e.panels)=rank);classes:=[];orbits:=[];
 for i in [1..Length(candidates)] do
  hit:=First([1..Length(classes)],j->EquivalentFamilies(A,candidates[classes[j]].parabolics,candidates[i].parabolics));
  if hit=fail then Add(classes,i);Add(orbits,[i]);else Add(orbits[hit],i);fi;
 od;
 counts[rank]:=Length(classes);Append(allFinal,candidates{classes});
 Print("FUSION rank=",rank," inner_classes=",Length(candidates)," aut_type_classes=",Length(classes)," orbits=",orbits,"\n");
 Print("BOREL_CLASSES rank=",rank," orders=",List(candidates{classes},e->e.borel_order),"\n");
od;
PrintTo("research/leemans/phase5_j2_representatives.g","# Independently enumerated J2 geometry witnesses.\nG:=",G,";\nJ2Representatives:=",allFinal,";\n");
if counts{[2..4]}<>[8,19,3] or not ForAll([5..14],r->counts[r]=0) then Error("published principal census differs from independent result");fi;
Print("FULL_CENSUS_PASS counts=",counts{[2..14]}," aut_order=",Size(A),"\n");
QUIT;
