ProbeAnchoredCentralizer:=function()
local n,G,T,pool,first,results,visited,IP,search,rank;
n:=8;rank:=5;G:=SymmetricGroup(n);T:=Stabilizer(G,1);
pool:=Filtered(Elements(T),x->Order(x)=2);
results:=[];visited:=0;
IP:=function(s)
 local m,u,v;
 m:=Length(s);if m<=2 then return true;fi;
 u:=Group(s{[1..m-1]});v:=Group(s{[2..m]});
 return Intersection(u,v)=Group(s{[2..m-1]}) and IP(s{[2..m]});
end;
search:=function(s,H,stabilizer)
 local choices,orbits,x,ss,HH,c;
 if Length(s)=rank then
  visited:=visited+1;
  if H=G then
   c:=Centralizer(T,Group(s{[2..rank]}));
   if Size(c)>1 then
    Add(results,[s,Size(c),GeneratorsOfGroup(c)]);
    Print("COUNTEREXAMPLE ",s," CENTRALIZER ",c,"\n");
   fi;
  fi;
  return;
 fi;
 choices:=Filtered(pool,x->not x in H and ForAll(s{[1..Length(s)-1]},y->x*y=y*x) and x*s[Length(s)]<>s[Length(s)]*x);
 orbits:=OrbitsDomain(stabilizer,choices,OnPoints);
 for x in List(orbits,o->o[1]) do
  ss:=Concatenation(s,[x]);
  if IP(ss) then
   HH:=Group(ss);search(ss,HH,Centralizer(stabilizer,x));
  fi;
 od;
end;
for first in [(1,2),(1,2)(3,4),(1,2)(3,4)(5,6),(1,2)(3,4)(5,6)(7,8)] do
 search([first],Group(first),Centralizer(T,first));Print("FINISHED_FIRST ",first," VISITED ",visited,"\n");
od;
Print("PROBE_FINISHED ",visited," ",Length(results),"\n");
end;
ProbeAnchoredCentralizer();QUIT_GAP(0);
