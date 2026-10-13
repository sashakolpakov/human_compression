F001Need:=function(b,s) if not b then Error(s); fi; end;;
F001Normalize:=function(v)
  local p; p:=PositionProperty(v,x->not IsZero(x));
  return v/v[p];
end;;
F001Points:=function(q,d)
  local ff,oo,zz,els,pts,p,tail;
  ff:=GF(q); oo:=One(ff); zz:=Zero(ff); els:=Elements(ff); pts:=[];
  for p in [1..d] do
    for tail in Tuples(els,d-p) do
      Add(pts,Concatenation(List([1..p-1],i->zz),[oo],tail));
    od;
  od;
  Sort(pts); return pts;
end;;
F001Form:=function(q,cs)
  local m,i; m:=IdentityMat(5,GF(q));
  for i in [1..4] do m[i][i+1]:=cs[i]/2; m[i+1][i]:=cs[i]/2; od;
  return m;
end;;
F001Reflections:=function(q,cs)
  local m,pts,i,j,r,rs,gs,imgs,v,u,pos;
  m:=F001Form(q,cs);
  pts:=Filtered(F001Points(q,5),v->v*m*v=Zero(GF(q)));
  rs:=[]; gs:=[];
  for i in [1..5] do
    r:=IdentityMat(5,GF(q));
    for j in [1..5] do r[j][i]:=r[j][i]-2*m[j][i]; od;
    F001Need(r*m*TransposedMat(r)=m,"reflection preserves form");
    F001Need(DeterminantMat(-r)=One(GF(q)),"negative reflection determinant");
    Add(rs,-r); imgs:=[];
    for v in pts do
      u:=F001Normalize(v*r); pos:=PositionSorted(pts,u);
      F001Need(pos<=Length(pts) and pts[pos]=u,"isotropic action membership");
      Add(imgs,pos);
    od;
    Add(gs,PermList(imgs));
  od;
  return rec(form:=m,points:=pts,matrices:=rs,generators:=gs);
end;;
F001ProjectiveFaithfulness:=function(pts,q)
  local basis,v,coords,graph,i,j,k,changed;
  basis:=[];
  for v in pts do
    if RankMat(Concatenation(basis,[v]))>Length(basis) then Add(basis,v); fi;
    if Length(basis)=5 then break; fi;
  od;
  F001Need(Length(basis)=5,"isotropic points span");
  graph:=List([1..5],i->[i]);
  for v in pts do
    coords:=v*basis^-1;
    for i in [1..5] do for j in [1..5] do
      if coords[i]<>Zero(GF(q)) and coords[j]<>Zero(GF(q)) then AddSet(graph[i],j); fi;
    od; od;
  od;
  changed:=true;
  while changed do
    changed:=false;
    for i in [1..5] do for j in ShallowCopy(graph[i]) do for k in graph[j] do
      if not k in graph[i] then AddSet(graph[i],k); changed:=true; fi;
    od; od; od;
  od;
  F001Need(ForAll(graph,x->Length(x)=5),"projective diagonal constraints connected");
  return basis;
end;;
F001AllIP:=function(gs)
  local sets,groups,i,j,k,checks,n;
  n:=Length(gs); sets:=Combinations([1..n]);
  groups:=List(sets,s->Group(Concatenation([()],gs{s}))); checks:=0;
  for i in [1..Length(sets)] do for j in [i+1..Length(sets)] do
    if IsSubset(sets[i],sets[j]) or IsSubset(sets[j],sets[i]) then continue; fi;
    k:=Position(sets,Union(sets[i],sets[j]));
    F001Need(Size(Intersection(groups[i],groups[j]))=Size(groups[k]),"full subset intersection");
    checks:=checks+1;
  od; od;
  return rec(logical_pairs:=Length(sets)^2,actual_intersections:=checks);
end;;
F001StringC:=function(gs)
  local n,left,right,middle;
  n:=Length(gs); if n<=2 then return true; fi;
  if not F001StringC(gs{[1..n-1]}) or not F001StringC(gs{[2..n]}) then return false; fi;
  left:=Group(gs{[1..n-1]}); right:=Group(gs{[2..n]}); middle:=Group(gs{[2..n-1]});
  return Size(Intersection(left,right))=Size(middle);
end;;
F001Q3Group:=function()
  local ff,oo,zz,j,pts,v,imgs,w,u,p,gs;
  ff:=GF(3); oo:=One(ff); zz:=Zero(ff);
  j:=[[zz,oo,zz,zz],[-oo,zz,zz,zz],[zz,zz,zz,oo],[zz,zz,-oo,zz]];
  pts:=F001Points(3,4); gs:=[];
  for v in pts do
    imgs:=[];
    for w in pts do
      u:=F001Normalize(w+(w*j*v)*v); p:=PositionSorted(pts,u);
      F001Need(p<=Length(pts) and pts[p]=u,"symplectic projective membership");
      Add(imgs,p);
    od;
    Add(gs,PermList(imgs));
  od;
  F001Need(Length(pts)=40 and ForAll(gs,x->Order(x)=3),"symplectic transvections");
  return Group(gs);
end;;
F001Q3Exhaust:=function()
  local g,classes,invs,nodes,rejected,leaves,full,Explore,cl,x;
  g:=F001Q3Group(); F001Need(Size(g)=25920,"PSp4(3) full order");
  F001Need(IsSimpleGroup(g),"PSp4(3) simplicity");
  classes:=Filtered(ConjugacyClasses(g),c->Order(Representative(c))=2);
  invs:=Concatenation(List(classes,Elements)); Sort(invs);
  F001Need(Length(invs)=315 and Set(List(classes,Size))=[45,270],"all involutions");
  nodes:=List([1..14],i->0); rejected:=List([1..14],i->0); leaves:=0; full:=[];
  Explore:=function(seq,h,previous,central)
    local r,cands,orbs,orb,y,hh,next;
    r:=Length(seq); F001Need(r<=14,"irredundancy length bound"); nodes[r]:=nodes[r]+1;
    if Size(h)=Size(g) then Add(full,seq); return; fi;
    cands:=Filtered(invs,y->y in previous and not y in h and y*seq[r]<>seq[r]*y);
    orbs:=Orbits(central,cands,OnPoints);
    F001Need(Sum(List(orbs,Length))=Length(cands),"extension orbit coverage");
    if IsEmpty(orbs) then leaves:=leaves+1; fi;
    for orb in orbs do
      y:=Minimum(orb); next:=Concatenation(seq,[y]);
      if not F001StringC(next) then rejected[r+1]:=rejected[r+1]+1; continue; fi;
      hh:=Group(next); F001Need(Size(hh)>=2*Size(h),"strict extension order");
      Explore(next,hh,central,Centralizer(central,y));
    od;
  end;
  for cl in classes do x:=Representative(cl); Explore([x],Group(x),g,Centralizer(g,x)); od;
  F001Need(nodes=[2,13,121,20,2,0,0,0,0,0,0,0,0,0],"complete q3 prefix counts");
  F001Need(rejected=[0,0,20,25,0,0,0,0,0,0,0,0,0,0] and leaves=108,"q3 rejection counts");
  F001Need(IsEmpty(full),"no complete q3 marking");
  return rec(nodes:=nodes,rejected:=rejected,leaves:=leaves,full:=Length(full));
end;;
