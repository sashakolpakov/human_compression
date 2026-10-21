# Match all 66 literal active archive entries to the already exhausted M22 catalogue.
# No subgroup census is rerun.
Read("prior_representatives.g");;CatalogueG:=G;;
Read("archive_data/inputs.g");;SizeScreen([100000,100000]);;
SourceG:=Group(Concatenation(L096Inputs[1].parabolic_generators));;
iso:=IsomorphismGroups(SourceG,CatalogueG);;
if iso=fail then Error("source not prior M22 model");fi;
AutG:=AutomorphismGroup(CatalogueG);;
OnSub:=function(H,a)return Image(a,H);end;;
Equivalent:=function(p,q)
 local perm,order,cur,C,x,i;
 if SortedList(List(p,Size))<>SortedList(List(q,Size)) then return false;fi;
 for perm in SymmetricGroup(Length(p)) do
  order:=Permuted(q,perm);if List(p,Size)<>List(order,Size) then continue;fi;
  cur:=ShallowCopy(p);C:=AutG;x:=fail;
  for i in [1..Length(p)] do
   x:=RepresentativeAction(C,cur[i],order[i],OnSub);
   if x=fail then break;fi;
   cur:=List(cur,H->Image(x,H));C:=Stabilizer(C,order[i],OnSub);
  od;
  if x<>fail then return true;fi;
 od;return false;
end;;
seen:=[];;H:=[];;
for input in L096Inputs do
 SG:=Group(Concatenation(input.parabolic_generators));
 if SG<>SourceG then Error("literal common ambient changed");fi;
 H:=List(input.parabolic_generators,x->Image(iso,Group(x)));
 hits:=Filtered([1..Length(SporadicRepresentatives)],i->Length(SporadicRepresentatives[i].parabolics)=Length(H) and Equivalent(H,SporadicRepresentatives[i].parabolics));
 if Length(hits)>1 then Error("multiple previous classes");fi;
 if Length(hits)=1 then AddSet(seen,hits[1]);fi;
 Print("MATCH|",input.member,"|",input.active,"|",hits,"|",List(H,Size),"\n");
od;
expected:=Filtered([1..Length(SporadicRepresentatives)],i->Length(SporadicRepresentatives[i].parabolics)>=3);;
Print("COMPLETE_PRIOR_CLASSES|",seen,"|",expected,"\n");
Print("PASS_M22_PRIOR_MATCH\n");QUIT;
