# Independently authored bounded oracles. No author search program is imported.
SizeScreen([100000,100000]);;
RBNeed:=function(b,s) if not b then Error(s);fi;end;;
RBIP:=function(gs)
 local supports,groups,i,j,n;
 n:=Length(gs);supports:=List([0..2^n-1],m->Filtered([1..n],i->QuoInt(m,2^(i-1)) mod 2=1));
 groups:=List(supports,s->Group(Concatenation([()],gs{s})));
 for i in [1..Length(supports)]do for j in [1..Length(supports)]do
  if Intersection(groups[i],groups[j])<>Group(Concatenation([()],gs{Intersection(supports[i],supports[j])}))then return false;fi;
 od;od;return true;
end;;
RBInd:=function(gs)
 return ForAll([1..Length(gs)],i->not gs[i]in Group(Concatenation([()],gs{Difference([1..Length(gs)],[i])})));
end;;
RBCharacters:=function(H,gs)
 local el,ok,bits,values,todo,at,i,g,j,target,bad,hom;
 el:=Elements(H);ok:=[];
 for bits in [0..2^Length(gs)-1]do
  values:=List(el,g->-1);values[Position(el,())]:=0;todo:=[()];at:=1;bad:=false;
  while at<=Length(todo)and not bad do
   g:=todo[at];at:=at+1;
   for i in [1..Length(gs)]do
    j:=Position(el,g*gs[i]);target:=(values[Position(el,g)]+QuoInt(bits,2^(i-1)))mod 2;
    if values[j]=-1 then values[j]:=target;Add(todo,el[j]);elif values[j]<>target then bad:=true;break;fi;
   od;
  od;
  hom:=GroupHomomorphismByImages(H,Group((1,2)),gs,List([1..Length(gs)],i->(1,2)^(QuoInt(bits,2^(i-1))mod 2)));
  RBNeed((hom<>fail)=(not bad),"character BFS differs from exact homomorphism construction");
  if not bad then RBNeed(ForAll(values,x->x>=0),"marking did not generate");Add(ok,bits);fi;
 od;return ok;
end;;
RBMarkings:=function(H,k,rank,label,expected)
 local inv,tuples,visit,gs,x,orbs,N,charcounts;
 inv:=Filtered(Elements(H),x->Order(x)=2);tuples:=[];
 # No normalizer pruning and no index bound; enumerate every eligible ordered tuple.
 visit:=function(gs)
  local x;
  if Length(gs)=rank then
   if Group(gs)=H and RBIP(gs)then Add(tuples,gs);fi;return;
  fi;
  for x in inv do
   if x in Group(Concatenation([()],gs))then continue;fi;
   if ForAll([1..Maximum(Length(gs)-1,0)],i->x*gs[i]=gs[i]*x)then visit(Concatenation(gs,[x]));fi;
  od;
 end;
 visit([]);N:=Normalizer(SymmetricGroup(k),H);orbs:=OrbitsDomain(N,tuples,OnTuples);
 RBNeed(Length(orbs)=expected,"unnormalized marking orbit count");
 charcounts:=Set(List(orbs,o->Length(RBCharacters(H,o[1]))));RBNeed(charcounts=[4],"four literal characters");
 Print("ORACLE_MARKINGS|",label,"|",Length(tuples),"|",Length(orbs),"|",Size(N),"|",charcounts,"\n");
 return List(orbs,o->o[1]);
end;;
RBMarkings(Group((1,2),(3,4),(4,5)),5,3,"S2xS3",4);;
RBMarkings(Group((1,2),(2,3),(4,5),(5,6)),6,4,"S3xS3",1);;
RBNeed(Size(TransitiveGroup(6,9))=36 and Size(TransitiveGroup(6,11))=48,"specified catalogue orders");;
RBMarkings(TransitiveGroup(6,9),6,4,"T6_9",1);;
RBMarkings(TransitiveGroup(6,11),6,4,"T6_11",12);;
# Enumerate the complete degree-six wreath product and all neighbors literally.
k:=3;;r:=(1,4)(2,5)(3,6);;W:=Group((1,2),(2,3),(4,5),(5,6),r);;
RBNeed(Size(W)=72,"literal wreath order");;
el:=Elements(W);;inv:=Filtered(el,g->Order(g)=2);;
xs:=Filtered(inv,x->x*r<>r*x and 1^x<=k);;ys:=xs;;
stab:=Filtered(el,g->g*r=r*g);;
RBNeed(Set(stab)=Set(Elements(Centralizer(W,r))),"literal centralizer oracle");;
RBNeed(ForAll(stab,g->Set(List(xs,x->x^g))=Set(xs)and Set(List(ys,y->y^g))=Set(ys)),"simultaneous centralizer preserves candidates");;
orb:=OrbitsDomain(Group(stab),xs,OnPoints);;rawpairs:=[];;prunedpairs:=[];;
for x in xs do for y in ys do
 if x*y=y*x and IsTransitive(Group(x,r,y),[1..6])and RBInd([x,r,y])then
  RBNeed(RBIP([x,r,y]),"positive family full IP");Add(rawpairs,[x,y]);
 fi;
od;od;
for o in orb do
 x:=o[1];
 for y in ys do if x*y=y*x and IsTransitive(Group(x,r,y),[1..6])and RBInd([x,r,y])then Add(prunedpairs,[x,y]);fi;od;
od;
RBNeed(Length(prunedpairs)=6,"six true positive completions");;
RBNeed(ForAll(rawpairs,p->ForAny(prunedpairs,q->ForAny(stab,g->p[1]^g=q[1]and p[2]^g=q[2]))),"pruned pairs cover raw pairs");;
RBNeed(RBIP([(5,6),r,(1,2)]),"printed positive marking");;
RBNeed(not RBIP([(1,2),(2,3),(1,3)])and not RBInd([(1,2),(2,3),(1,3)]),"redundancy and IP controls");;
# Nearest-end formulas are exact for all possible split positions and generator types.
positions:=0;;ties:=0;;
for rank in [0..6]do for l in [0..rank]do
 size:=rank+3;ri:=l+2;dist:=Minimum(ri-1,size-ri);
 RBNeed(dist=Minimum(l+1,rank+1-l),"r distance formula");
 RBNeed(Minimum(l,rank+2-l)=Minimum((ri-1)-1,size-(ri-1)),"x distance formula");
 RBNeed(Minimum(l+2,rank-l)=Minimum((ri+1)-1,size-(ri+1)),"y distance formula");
 for i in [1..size]do
  positions:=positions+1;
  if Minimum(i-1,size-i)=dist then ties:=ties+1;fi;
 od;
od;od;
Print("ORACLE_NEIGHBORS|",Length(xs),"|",Length(rawpairs),"|",Length(prunedpairs),"|",positions,"|",ties,"\n");
Print("PASS_L047_INDEPENDENT_ORACLES\n");
QUIT;
