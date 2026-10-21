# Fuse marked parabolic families under Aut(G) and arbitrary type permutations.
Read("research/leemans/phase4_j2_parsed.g");;
AutoSub:=function(H,a) return Image(a,H);end;
FamilySignature:=function(p)
 return [SortedList(List(p,Size)),SortedList(List(Combinations([1..Length(p)],2),ij->Size(Intersection(p[ij[1]],p[ij[2]])))),Size(Intersection(p))];
end;
EquivalentFamilies:=function(A,p,q)
 local perm,ord,cur,C,x,i;
 if FamilySignature(p)<>FamilySignature(q) then return false;fi;
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
Fuse:=function(G,pars,name)
 local A,classes,orb,i,j,hit;
 A:=AutomorphismGroup(G);classes:=[];orb:=[];
 for i in [1..Length(pars)] do
  hit:=First([1..Length(classes)],j->EquivalentFamilies(A,pars[classes[j]],pars[i]));
  if hit=fail then Add(classes,i);Add(orb,[i]);else Add(orb[hit],i);fi;
 od;
 Print("FUSION name=",name," input=",Length(pars)," classes=",Length(classes)," aut_order=",Size(A)," orbits=",orb,"\n");
 return rec(classes:=classes,orbits:=orb,representatives:=pars{classes});
end;
for src in sourceData do
 result:=Fuse(src.G,src.geos{src.selected},src.name);
 Print("SOURCE_INDICES ",src.name," ",List(result.orbits,o->src.selected{o}),"\n");
od;
LoadPackage("tomlib");;
G:=UnderlyingGroup(TableOfMarks("J2"));;
Read("research/leemans/phase4_thin_rank4.g");;
thin:=Filtered(thinLevel,t->Size(Group(t))=Size(G));;
pars:=List(thin,t->List([1..4],i->Group(t{Difference([1..4],[i])})));;
result:=Fuse(G,pars,"independent_thin_rank4");;
Print("THIN_CLASS_ORDERS ",List(result.representatives,p->List(p,Size)),"\n");
PrintTo("research/leemans/phase4_thin_j2_witnesses.g","# Independently generated witnesses.\nG:=",G,";\nthinWitnesses:=",thin{result.classes},";\n");
if Length(result.classes)<>2 then Error("thin census mismatch");fi;
Print("FUSION_COMPLETE\n");
QUIT;
