# Diagnostic only: full rotation intersection tests in the fixed group Sz(8).
G:=SuzukiGroup(IsPermGroup,8);;
invols:=Filtered(Elements(G),x->Order(x)=2);;
w:=invols[1];; C:=Centralizer(G,w);;
uorbits:=Orbits(C,invols,OnPoints);;
Print("Sz8_order=",Size(G)," involutions=",Length(invols)," first_orbits=",Length(uorbits),"\n");
sets:=Combinations([1..4]);;
nontriv:=Filtered(sets,J->Length(J)>=2);;
count:=0;; generated:=0;; passed:=0;; failures:=[];; profiles:=[];;
for U in uorbits do
 u:=U[1];;
 if u=w then continue;fi;
 Cu:=Centralizer(C,u);;
 vorbits:=Orbits(Cu,invols,OnPoints);;
 for V in vorbits do
  v:=V[1];; count:=count+1;
  if v=w then continue;fi;
  H:=Group(u,v,w);; if Size(H)<>Size(G) then continue;fi;
  generated:=generated+1;
  a:=[One(G),w*v,u,w];;
  marked:=List(sets,J->Group(Concatenation([One(G)],List(Combinations(J,2),p->a[p[1]]^-1*a[p[2]]))));;
  F:=marked[Position(sets,[1,2,3])];; Vtx:=marked[Position(sets,[2,3,4])];;
  if Size(F)<Size(G) and Size(Vtx)<Size(G) then
   Add(profiles,[List([w*v,v*w*u,u*w],Order),Size(F),StructureDescription(F),Size(Vtx),StructureDescription(Vtx),Size(Intersection(F,Vtx)),Order(Comm(w*v,u*w))]);
  fi;
  bad:=fail;
  for J in nontriv do
   for K in nontriv do
    if IsSubset(J,K) or IsSubset(K,J) then continue;fi;
    expected:=marked[Position(sets,Intersection(J,K))];;
    if Intersection(marked[Position(sets,J)],marked[Position(sets,K)])<>expected then bad:=[J,K];break;fi;
   od;
   if bad<>fail then break;fi;
  od;
  if bad=fail then
   passed:=passed+1;
   Print("IP_PASS u=",u," v=",v," w=",w," rotations=",[w*v,v*w*u,u*w],"\n");
  else Add(failures,bad);fi;
 od;
 Print("progress=",count," generated=",generated," IP_passed=",passed,"\n");
od;
Print("COMPLETE_FIXED_SZ8_DIAGNOSTIC normalized_triples=",count," generated=",generated," IP_passed=",passed," failure_histogram=",Collected(failures),"\n");
Print("PROPER_FACET_AND_VERTEX_PROFILES=",Collected(profiles),"\n");
QUIT;
