# Exhaustive rank-five string C-group search in PSL(4,q).
# Quotient by conjugacy of the ordered commuting triple (rho0,rho2,rho4),
# then by the triple's centralizer on rho1. All remaining rho3 are tested.
# No sampling. Proper adjacent commutation is excluded because G is simple.
if not IsBound(PSL4Q) then PSL4Q:=3; fi;
LogTo(Concatenation("research/leemans/psl4_search_q",String(PSL4Q),".log"));
Print("START GAP ",GAPInfo.Version," q=",PSL4Q," runtime=",Runtime(),"\n");

IsStringC := function(rr)
  local n, left, right, mid, gl, gr;
  n:=Length(rr);
  if n<=2 then return true; fi;
  left:=rr{[1..n-1]};
  right:=rr{[2..n]};
  if not IsStringC(left) or not IsStringC(right) then return false; fi;
  gl:=Group(left); gr:=Group(right); mid:=Group(rr{[2..n-1]});
  return Intersection(gl,gr)=mid;
end;

G:=PSL(4,PSL4Q);;
gsize:=Size(G);;
classes:=Filtered(ConjugacyClasses(G),c->Order(Representative(c))=2);;
stats:=rec(triples:=0,rho1orbits:=0,rho3candidates:=0,generating:=0,
  independent:=0,cgroups:=0);;
Print("GROUP ",gsize," degree ",LargestMovedPoint(G)," involutions ",
  List(classes,Size),"\n");

for c2 in classes do
  t2:=Representative(c2);;
  C2:=Centralizer(G,t2);;
  classes0:=Filtered(ConjugacyClasses(C2),c->Order(Representative(c))=2);;
  Print("CENTER classsize=",Size(c2)," centralizer=",Size(C2),
    " rho0classes=",Length(classes0),"\n");
  for c0 in classes0 do
    t0:=Representative(c0);;
    if t0=t2 then continue; fi;
    C02:=Centralizer(C2,t0);;
    classes4:=Filtered(ConjugacyClasses(C02),c->Order(Representative(c))=2);;
    pair:=Group(t0,t2);;
    for c4 in classes4 do
      t4:=Representative(c4);;
      if t4 in pair then continue; fi;
      stats.triples:=stats.triples+1;
      C024:=Centralizer(C02,t4);;
      C4:=Centralizer(G,t4);;
      invol1:=Filtered(Elements(C4),t->Order(t)=2 and
        t*t0<>t0*t and t*t2<>t2*t);;
      orbits1:=OrbitsDomain(C024,invol1,OnPoints);;
      Print("TRIPLE ",stats.triples," centralizer=",Size(C024),
        " rho1=",Length(invol1)," orbits=",Length(orbits1),"\n");
      for orb1 in orbits1 do
        t1:=orb1[1];;
        stats.rho1orbits:=stats.rho1orbits+1;
        C01:=Centralizer(Centralizer(G,t0),t1);;
        invol3:=Filtered(Elements(C01),t->Order(t)=2 and
          t*t2<>t2*t and t*t4<>t4*t);;
        for t3 in invol3 do
          stats.rho3candidates:=stats.rho3candidates+1;
          rr:=[t0,t1,t2,t3,t4];;
          if Size(Group(rr))<>gsize then continue; fi;
          stats.generating:=stats.generating+1;
          # Necessary independence before expensive IP intersections.
          if ForAny([1..5],j->Size(Group(rr{Difference([1..5],[j])}))=gsize) then
            continue;
          fi;
          stats.independent:=stats.independent+1;
          if stats.independent<=5 then
            Print("INDEPENDENT tuple=",rr,"\n");
          fi;
          if IsStringC(rr) then
            stats.cgroups:=stats.cgroups+1;
            Print("FOUND CGROUP ",rr," TYPE ",
              List([1..4],i->Order(rr[i]*rr[i+1])),"\n");
          fi;
        od;
      od;
      Print("STATUS ",stats," runtime=",Runtime(),"\n");
    od;
  od;
od;
Print("COMPLETE ",stats," runtime=",Runtime(),"\n");
LogTo();
QUIT;
