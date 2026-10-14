LoadPackage("ctbllib");;
Need:=function(b,m)if not b then Error(m);fi;end;;
PiVector:=function(h,types)
 local t,orders,sizes,chars,v,chi,n,rows,p,q,z,i;
 t:=CharacterTable(h);orders:=OrdersClassRepresentatives(t);sizes:=SizesConjugacyClasses(t);chars:=Irr(t);
 v:=List(chars,chi->List(types,n->Sum(Filtered([1..Length(orders)],i->orders[i]=n),i->sizes[i]*chi[i])));
 rows:=[];
 for p in [1..Length(types)] do for q in [p..Length(types)] do
  z:=Sum([1..Length(chars)],i->v[i][Position(types,2)]*v[i][p]*v[i][q]/chars[i][1])/Size(t);
  Need(IsInt(z)and z>=0,"exact count");Add(rows,z);
 od;od;return rows;
end;;
CheckIncidence:=function(g)
 local cls,h,conj,M,types,pairs,p,q,i,j,v,eps,actual,pi,x,y,k,elts,checked,autn;
 cls:=ConjugacyClassesSubgroups(g);h:=List(cls,Representative);Sort(h,function(a,b)return Size(a)<Size(b);end);
 conj:=List(h,x->Elements(ConjugacyClassSubgroups(g,x)));
 M:=List(h,x->List(conj,y->Number(y,z->IsSubgroup(x,z))));
 for i in [1..Length(h)] do Need(M[i][i]=1 and ForAll([i+1..Length(h)],j->M[i][j]=0),"unit triangular incidence");od;
 types:=Filtered(Set(List(Elements(g),Order)),n->n>1);Need(2 in types,"control contains involutions");pairs:=[];
 for p in [1..Length(types)] do for q in [p..Length(types)] do Add(pairs,[types[p],types[q]]);od;od;
 eps:=[];checked:=0;
 for i in [1..Length(h)] do
  v:=PiVector(h[i],types);pi:=ShallowCopy(v);
  for j in [1..i-1] do v:=v-M[i][j]*eps[j];od;
  Need(ForAll(v,x->IsInt(x)and x>=0),"nonnegative inverted counts");Add(eps,v);
  actual:=List(pairs,x->0);elts:=Elements(h[i]);
  for x in elts do for y in elts do
   if Order(x*y)=2 and Order(x)>1 and Order(y)>1 and Order(x)<=Order(y) then
    k:=Position(pairs,[Order(x),Order(y)]);pi[k]:=pi[k]-1;
    if Subgroup(h[i],[x,y])=h[i] then actual[k]:=actual[k]+1;fi;
   fi;
  od;od;
  Need(ForAll(pi,x->x=0),"all pair counts agree");Need(actual=v,"all generated-subgroup counts agree");
  autn:=Size(AutomorphismGroup(h[i]));Need(ForAll(v,x->x mod autn=0),"free orbit divisibility");
  checked:=checked+Length(elts)^2;
 od;
 Print("CONTROL ",Size(g)," SUBGROUP_CLASSES ",Length(h)," TYPES ",Length(pairs)," DIRECT_PAIRS ",checked," GENERATED ",eps[Length(eps)]," PASS\n");
end;;
for group in [SymmetricGroup(3),DihedralGroup(IsPermGroup,8),AlternatingGroup(4),SymmetricGroup(4),AlternatingGroup(5)] do CheckIncidence(group);od;
Print("COMPLETE ALL SUBGROUP INCIDENCE CONTROLS\n");
QUIT_GAP(0);
