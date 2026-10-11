# Complete marked search; SmallGroups catalogue completeness is retained.
Check250:=function(ok,s) if not ok then Error(Concatenation("P250_REJECT ",s));fi;end;;
Search250:=function(G,k)
 local classes,cls,c,C,inv,b,orbit,a,pairs,triples,ip;
 pairs:=0;triples:=0;ip:=0;
 classes:=Filtered(ConjugacyClasses(G),cl->Order(Representative(cl))=2);
 for cls in classes do
  c:=Representative(cls);C:=Centralizer(G,c);
  inv:=Filtered(Elements(G),g->Order(g)=2 and Order(g*c)=k);
  while Length(inv)>0 do
   b:=inv[1];orbit:=Orbit(C,b);inv:=Difference(inv,orbit);pairs:=pairs+1;
   for a in Filtered(Elements(C),g->Order(g)=2 and Order(g*b)=6) do
    if Size(Group(a,b,c))=Size(G) then
     triples:=triples+1;
     if Size(Intersection(Group(a,b),Group(b,c)))=2 then ip:=ip+1;fi;
    fi;
   od;
  od;
 od;
 return [pairs,triples,ip];
end;;
Run250:=function()
 local N,eligible,pairs,triples,id,G,stats,positive;
 Check250(LoadPackage("smallgrp")=true,"SmallGroups package");
 N:=NumberSmallGroups(384);Check250(N=20169,"complete order384 count");
 eligible:=0;pairs:=0;triples:=0;
 Print("SMALLGRP_VERSION ",PackageInfo("smallgrp")[1].Version," GROUP_COUNT ",N,"\n");
 for id in [1..N] do
  G:=SmallGroup(384,id);
  if Exponent(G) mod 16=0 then
   eligible:=eligible+1;stats:=Search250(G,16);
   pairs:=pairs+stats[1];triples:=triples+stats[2];
   Check250(stats[3]=0,"unexpected Cgroup of type6,16");
  fi;
 od;
 Check250(eligible=1178 and pairs=4436 and triples=0,"bound exhaustive counts");
 Print("NO_CGROUP_6_16_ORDER384_PASS GROUPS ",N," ELIGIBLE ",eligible," PAIRS ",pairs," GENERATING ",triples,"\n");
 positive:=Search250(SmallGroup(384,18046),4);
 Check250(positive[3]>0,"same search detects the known6,4 seed");
 Print("POSITIVE_CGROUP_6_4_CONTROL ",positive,"\nPHASE250_CENSUS_PASS\n");
end;;
Run250();
QUIT_GAP(0);
