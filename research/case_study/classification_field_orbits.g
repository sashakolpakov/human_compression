# Exact additive torsor/Frobenius orbit check for the all-odd-e formula.
RunFieldOrbitCheck:=function(e)
 local F,elts,full,cosets,neg,frb,op,seen,orbs,c,orbit,d,M,s,m,S,pred,nfixed;
 F:=GF(3^e);
 elts:=Elements(F);
 full:=Filtered(elts,t->DegreeFFE(t)=e);
 cosets:=Set(List(full,t->Set([t,t+One(F),t-One(F)])));
 seen:=[]; orbs:=[];
 for c in cosets do
  if not c in seen then
   orbit:=Set(Concatenation(List([0..e-1],i->[Set(List(c,t->t^(3^i))),Set(List(c,t->-t^(3^i)))])));
   Add(orbs,orbit); UniteSet(seen,orbit);
  fi;
 od;
 M:=Sum(DivisorsInt(e),d->MoebiusMu(e/d)*3^d);
 S:=0;
 if e mod 3=0 then
  s:=0;m:=e;
  while m mod 3=0 do s:=s+1;m:=m/3;od;
  S:=Sum(DivisorsInt(m),d->MoebiusMu(m/d)*3^(3^(s-1)*d));
 fi;
 pred:=(M+4*S)/(6*e);
 if Length(orbs)<>pred then Error("orbit formula failed");fi;
 Print("e=",e," q=",3^e," full_degree_elements=",Length(full)," oriented_cosets=",Length(cosets)," unordered_conjugacy=",Length(cosets)/2," semilinear_orbits=",Length(orbs)," predicted=",pred," orbit_sizes=",Collected(List(orbs,Length))," PASS\n");
end;
for e in [3,5,7,9] do RunFieldOrbitCheck(e); od;
QUIT;
