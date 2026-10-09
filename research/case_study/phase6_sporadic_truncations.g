# Compare two truncation conventions without changing the exhaustive census.
# Required GROUP_NAME and WITNESS_FILE; no original geometry lists are read.
LoadPackage("tomlib");;SizeScreen([100000,24]);;
Read(WITNESS_FILE);;A:=AutomorphismGroup(G);;
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

RunTruncations:=function()
 local all,e,f,i,j,rank,restricted,broad,subs,J,hit,results;
 all:=SporadicRepresentatives;results:=[];
 for i in [1..Length(all)] do
  e:=all[i];rank:=Length(e.panels);
  if not e.twot then continue;fi;
  restricted:=[];broad:=[];
  for j in [1..Length(all)] do
   f:=all[j];
   if Length(f.panels)<=rank then continue;fi;
   for J in Combinations([1..Length(f.panels)],rank) do
    if EquivalentFamilies(A,e.parabolics,f.parabolics{J}) then
     Add(broad,[j,J]);
     if f.twot then Add(restricted,[j,J]);fi;
    fi;
   od;
  od;
  Add(results,rec(id:=i,rank:=rank,restricted:=restricted,broad:=broad));
  Print("TRUNCATION id=",i," rank=",rank," restricted=",restricted," broad=",broad,"\n");
 od;
 for rank in [2..Maximum(List(all,e->Length(e.panels)))+1] do
  Print("TRUNCATION_COUNTS rank=",rank," restricted_nontruncations=",Number(results,e->e.rank=rank and Length(e.restricted)=0)," broad_nontruncations=",Number(results,e->e.rank=rank and Length(e.broad)=0),"\n");
 od;
 Print("TRUNCATION_CONVENTIONS_COMPLETE\n");
end;
RunTruncations();
