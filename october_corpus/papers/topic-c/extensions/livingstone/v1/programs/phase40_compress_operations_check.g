# Entire finite certificate for Compress_C. No geometry census is read.
LoadPackage("tomlib");;
SizeScreen([100000,24]);;
CheckC:=function(test,msg) if not test then Error(msg);fi;end;;
G:=UnderlyingGroup(TableOfMarks("J1"));;
CheckC(Size(G)=175560,"ambient J1 order");;
FindSeedC:=function(K)
 local a,b,c,d,iv,bs;
 a:=GeneratorsOfGroup(K)[1];
 CheckC(Order(a)=2,"ambient first generator");
 iv:=Filtered(Elements(Centralizer(K,a)),x->Order(x)=2);
 for d in iv do
  if d=a then continue;fi;
  bs:=Filtered(Elements(Centralizer(K,d)),x->Order(x)=2 and Order(a*x)=5);
  for c in iv do
   if Order(c*d)<>5 then continue;fi;
   for b in bs do
    if Order(b*c)=3 and (a*b*c)^5=One(K)
      and ((d*c*b)^5*a)^3=One(K) and Group(a,b,c,d)=K then
     return [a,b,c,d];
    fi;
   od;
  od;
 od;
 Error("no source seed");
end;;
s:=FindSeedC(G);;
pairs:=Combinations([1..4],2);;
CheckC(List(pairs,p->Order(s[p[1]]*s[p[2]]))=[5,2,2,3,2,5],"seed pairs");;
CheckC(Normalizer(G,Group(s{[1,2,3]}))=Group(s{[1,2,3]}),"seed facet normalizer");;
# Exact upper bound for the literal source presentation.
F:=FreeGroup("a","b","c","d");; u:=GeneratorsOfGroup(F);;
rels:=Concatenation(List(u,x->x^2),List([1..6],i->
 (u[pairs[i][1]]*u[pairs[i][2]])^[5,2,2,3,2,5][i]),
 [(u[1]*u[2]*u[3])^5,((u[4]*u[3]*u[2])^5*u[1])^3]);;
Q:=F/rels;; q:=GeneratorsOfGroup(Q);;
ct:=CosetTable(Q,Subgroup(Q,q{[2,3,4]}));;
CheckC(Length(ct[1])=1463,"presentation coset index");;
CheckC(Size(Group(List([1,3,5,7],i->PermList(ct[i]))))=175560,"presentation image");;
w:=(s[2]*s[3]*s[4])^5;;
CheckC(Order(w)=2 and ForAll(s{[2,3,4]},x->Comm(w,x)=()),"twist center");;
marks:=[s,[s[1],w*s[2],s[3],s[4]],
 [s[1],s[2],s[3],s[3]^s[4]],
 [s[2]^s[1],s[2],s[3],s[4]],
 [s[2]^s[1],s[2],s[3],s[3]^s[4]],
 [(w*s[2])^s[1],w*s[2],s[3],s[4]]];;
CheckC(Intersection(Group(s{[2,3,4]}),Group(s{[2,3,4]})^s[1])
 =Group(s{[3,4]}),"left overlap");;
CheckC(Intersection(Group(s{[1,2,3]}),Group(s{[1,2,3]})^s[4])
 =Group(s{[1,2]}),"right overlap");;
VerifyC:=function(t)
 local ss,subs,a,b,ip,pars,i,j,J,rows,T,common,expected,h,pan;
 ss:=Combinations([1..4]);
 subs:=List(ss,J->Group(Concatenation([()],t{J})));
 ip:=0;
 for a in [1..16] do for b in [1..16] do
  if Intersection(subs[a],subs[b])<>subs[Position(ss,Intersection(ss[a],ss[b]))]
   then ip:=ip+1;fi;
 od;od;
 pars:=List([1..4],i->Group(t{Difference([1..4],[i])}));
 h:=[];
 for i in [1..4] do
  rows:=[];
  for j in Difference([1..4],[i]) do
   T:=Intersection(pars[i],pars[j]);
   rows[j]:=Set(List(RightTransversal(pars[j],T),x->RightCoset(pars[i],x)));
  od;
  for J in Combinations(Difference([1..4],[i])) do
   if Length(J)<2 then continue;fi;
   common:=Length(Intersection(rows{J})); T:=Intersection(pars{J});
   expected:=Index(T,Intersection(T,pars[i]));
   Add(h,[i,J,common,expected]);
  od;
 od;
 pan:=List([1..4],i->Size(Intersection(pars{Difference([1..4],[i])})));
 return rec(order:=Size(Group(t)),pairs:=List(pairs,p->Order(t[p[1]]*t[p[2]])),
  parabolics:=List(pars,Size),types:=List(pars,StructureDescription),
  ip_failures:=ip,helly:=h,borel:=Size(Intersection(pars)),panels:=pan);
end;;
expectedP:=[[120,20,20,60],[120,20,20,660],[120,20,60,60],
 [120,120,20,60],[120,120,60,60],[120,120,20,660]];;
expectedPairs:=[[5,2,2,3,2,5],[5,2,2,6,2,5],[5,2,2,3,3,5],
 [5,3,2,3,2,5],[5,3,3,3,3,5],[5,6,2,6,2,5]];;
for i in [1..6] do
 CheckC(ForAll(marks[i],x->Order(x)=2),"marker orders");
 r:=VerifyC(marks[i]);
 CheckC(r.order=175560 and r.ip_failures=0,"generation and IP");
 CheckC(r.parabolics=expectedP[i] and r.pairs=expectedPairs[i],"source tables");
 CheckC(r.types=List(r.parabolics,o->["C2 x A5","D20","A5","PSL(2,11)"]
  [Position([120,20,60,660],o)]),"parabolic isomorphism types");
 CheckC(r.borel=1 and r.panels=[2,2,2,2],"thinness");
 CheckC(ForAll(r.helly,z->z[3]=z[4]),"typed Helly");
 Print("GEOMETRY ",i," PAIRS ",r.pairs," PARABOLICS ",r.parabolics,
  " TYPES ",r.types," IP_MEETS 256 HELLY_ROWS ",Length(r.helly)," PASS\n");
od;
CheckC(Length(Set(List(expectedP,SortedList)))=6,"pairwise nonisomorphism");;
bad:=[[s[1],w*s[2],s[3],s[3]^s[4]],[s[1],s[2],s[3],w*s[4]]];;
for i in [1..2] do
 r:=VerifyC(bad[i]);
 CheckC(r.order=175560 and r.ip_failures=8 and r.borel=1,"negative scope");
 CheckC(r.panels=[[2,4,2,2],[2,2,2,4]][i],"negative panel");
 CheckC(ForAll(r.helly,z->z[3]=z[4]),"negative Helly");
 Print("NEGATIVE ",i," IP_FAILURES ",r.ip_failures," PANELS ",r.panels," PASS\n");
od;
Print("COMPRESS_C_J1_PASS\n");
QUIT;
