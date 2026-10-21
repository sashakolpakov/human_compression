# Standalone original arbitrary-rank checks; no supplementary archive required.
IsMaximalPair:=function(K,H)
 local d,A,m;
 d:=Index(K,H);
 if d=1 then return false;fi;
 if IsPrimeInt(d) then return true;fi;
 if Size(K)>1000 then
  return ForAny(ConjugacyClassesMaximalSubgroups(K),m->Size(Representative(m))=Size(H) and RepresentativeAction(K,H,Representative(m),OnPoints)<>fail);
 fi;
 A:=Action(K,RightCosets(K,H),OnRight);
 return IsPrimitive(A,[1..d]);
end;
VerifyGeometry:=function(G,pars)
 local I,ss,sub,J,K,remaining,rr,i,j,panel,firm,rc,rwpri,twot,ip2,ft,rows,common,expected,T,A,B,C,x,left,right,digon,dis,joins,pans,joinok,failures;
 I:=[1..Length(pars)];ss:=Combinations(I);
 if not ForAll(pars,H->IsSubgroup(G,H) and H<>G) then Error("input subgroup membership");fi;
 sub:=List(ss,J->Intersection(Concatenation([G],pars{J})));
 firm:=true;rc:=true;rwpri:=true;twot:=true;ip2:=true;ft:=true;joinok:=true;failures:=[];
 for rr in [1..Length(ss)] do
  J:=ss[rr];K:=sub[rr];remaining:=Difference(I,J);
  if Length(remaining)>0 then
   if not ForAny(remaining,i->IsMaximalPair(K,Intersection(K,pars[i]))) then rwpri:=false;fi;
  fi;
  if Length(remaining)>=2 then
   joins:=Group(Concatenation(List(remaining,i->GeneratorsOfGroup(Intersection(K,pars[i])))));
   if joins<>K then rc:=false;fi;
  fi;
  if Length(remaining)=1 then
   B:=Intersection(K,pars[remaining[1]]);
   if Index(K,B)<2 then firm:=false;fi;
   if Length(DoubleCosets(K,B,B))<>2 then twot:=false;fi;
  fi;
  if Length(remaining)=2 then
   A:=Intersection(K,pars[remaining[1]]);B:=Intersection(K,pars[remaining[2]]);C:=Intersection(A,B);
   digon:=Size(A)*Size(B)=Size(K)*Size(C);
   if not digon then
    left:=Set(List(RightTransversal(A,C),h->RightCoset(B,h)));
    for dis in DoubleCosets(B,C,C) do
     x:=Representative(dis);
     if not x in C then
      right:=Set(List(RightTransversal(A,C),h->RightCoset(B,h*x)));
      if Length(Intersection(left,right))<>1 then ip2:=false;fi;
     fi;
    od;
   fi;
  fi;
 od;
 # Typed Helly: every partial base flag has precisely the expected common orbit.
 for i in I do
  remaining:=Difference(I,[i]);rows:=[];
  for j in remaining do
   T:=Intersection(pars[i],pars[j]);
   rows[j]:=Set(List(RightTransversal(pars[j],T),x->RightCoset(pars[i],x)));
  od;
  for J in Combinations(remaining) do
   if Length(J)>=2 then
    common:=Length(Intersection(List(J,j->rows[j])));
    T:=sub[Position(ss,J)];expected:=Index(T,Intersection(T,pars[i]));
    if common<>expected then ft:=false;Add(failures,[i,J,common,expected]);fi;
   fi;
  od;
 od;
 # Panels reconstruct every parabolic by joins in the common torsor.
 B:=Intersection(pars);pans:=List(I,i->Intersection(Concatenation([G],pars{Difference(I,[i])})));
 for J in ss do
  joins:=ClosureGroup(B,Group(Concatenation([()],Concatenation(List(Difference(I,J),i->GeneratorsOfGroup(pans[i]))))));
  if joins<>sub[Position(ss,J)] then joinok:=false;fi;
 od;
 return rec(orders:=List(pars,Size),borel:=Size(B),panels:=List(pans,Size),firm:=firm,rc:=rc,rwpri:=rwpri,twot:=twot,ip2:=ip2,ft:=ft,join:=joinok,failures:=failures);
end;
