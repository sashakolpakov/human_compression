# Independent source-witness matching, after exhaustive classification.
LoadPackage("tomlib");;SizeScreen([100000,24]);;
Read(WITNESS_FILE);;
Read("phase4_geometry_checks.g");;
Read(ARCHIVE_PARSED_FILE);;
if G<>UnderlyingGroup(TableOfMarks(GROUP_NAME)) then Error("witness group differs from named group");fi;
A:=AutomorphismGroup(G);;
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

CompareArchive:=function()
 local dataset,geo,H,iso,raw,pars,r,hits,seen,selectedSeen,expected,e;
 for dataset in archiveData do
  H:=Group(Concatenation(List(dataset.geos[1],GeneratorsOfGroup)));
  iso:=IsomorphismGroups(H,G);
  if iso=fail then Error("Source ambient group is not the named group");fi;
  Print("SOURCE_GROUP file=",dataset.name," order=",Size(H)," identified_with_named_group=true\n");
  seen:=[];selectedSeen:=[];
  for raw in [1..Length(dataset.geos)] do
   geo:=dataset.geos[raw];
   if not ForAll(geo,P->IsSubgroup(H,P)) then Error("source ambient mismatch");fi;
   pars:=List(geo,P->Image(iso,P));r:=VerifyGeometry(G,pars);
   if not (r.firm and r.rc and r.ft and r.rwpri and r.ip2 and r.join) then Error("source geometry fails requested axioms");fi;
   if not r.twot then
    Print("SOURCE_EXCLUDED file=",dataset.name," raw_id=",raw," selected=",raw in dataset.selected," reason=not_locally_2T\n");
    continue;
   fi;
   hits:=Filtered([1..Length(SporadicRepresentatives)],i->EquivalentFamilies(A,pars,SporadicRepresentatives[i].parabolics));
   if Length(hits)<>1 then Error("source geometry has no unique census class");fi;
   AddSet(seen,hits[1]);if raw in dataset.selected then AddSet(selectedSeen,hits[1]);fi;
   Print("SOURCE_MATCH file=",dataset.name," raw_id=",raw," census_id=",hits[1]," selected=",raw in dataset.selected," twot=",r.twot," rank=",Length(pars)," parabolic_orders=",r.orders," truncation_from=",SporadicRepresentatives[hits[1]].truncation_from,"\n");
  od;
  expected:=Filtered([1..Length(SporadicRepresentatives)],i->Length(SporadicRepresentatives[i].panels)=Length(dataset.geos[1]));
  Print("SOURCE_COVERAGE file=",dataset.name," matched_classes=",seen," selected_classes=",selectedSeen," expected_classes=",expected," matches_complete_census=",seen=expected,"\n");
 od;
 Print("ARCHIVE_COMPARISON_COMPLETE\n");
end;
CompareArchive();
