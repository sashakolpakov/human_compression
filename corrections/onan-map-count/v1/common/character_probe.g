LoadPackage("ctbllib");;
LoadPackage("tomlib");;
Need:=function(b,m)if not b then Error(m);fi;end;;
AllCounts:=function(t)
 local orders,types,sizes,chars,v,chi,n,i,rows,p,q,z;
 orders:=OrdersClassRepresentatives(t);types:=Set(orders);sizes:=SizesConjugacyClasses(t);chars:=Irr(t);rows:=[];
 v:=List(chars,chi->List(types,n->Sum(Filtered([1..Length(orders)],i->orders[i]=n),i->sizes[i]*chi[i])));
 if not 2 in types then return [];fi;
 for p in [1..Length(types)] do for q in [p..Length(types)] do
  if types[p]>1 then
   z:=Sum([1..Length(chars)],i->v[i][Position(types,2)]*v[i][p]*v[i][q]/chars[i][1])/Size(t);
   Need(IsInt(z)and z>=0,"nonnegative integral Frobenius count");Add(rows,[types[p],types[q],z]);
  fi;
 od;od;return rows;
end;;
row:=[];;elts:=[];;
for g in [SymmetricGroup(3),AlternatingGroup(4),AlternatingGroup(5),SymmetricGroup(4)] do
 t:=CharacterTable(g);rows:=AllCounts(t);elts:=Elements(g);
 for row in rows do
  direct:=Sum(Filtered(elts,a->Order(a)=row[1]),a->Number(elts,b->Order(b)=row[2]and Order(a*b)=2));
  Need(direct=row[3],"small exact all-pair character control");
 od;
 Print("CONTROL ",Size(g)," ",Length(rows)," PASS\n");
od;
t:=CharacterTable("ON");u:=CharacterTable("ON.2");;
Need(Size(t)=460815505920 and Size(u)=2*Size(t),"named tables/orders");;
orders:=OrdersClassRepresentatives(t);inv:=PowerMap(t,-1);fusion:=GetFusionMap(t,u);;
Need(fusion<>fail,"stored exact subgroup fusion");;
Print("TABLE_PROVENANCE ",InfoText(t),"\n");
Print("EXTENSION_PROVENANCE ",InfoText(u),"\n");
Print("ORDERS ",orders,"\nINVERSE ",inv,"\nFUSION ",fusion,"\n");
for n in Set(orders) do
 inds:=Filtered([1..Length(orders)],i->orders[i]=n);;
 inner:=Filtered(inds,i->inv[i]=i);;
 outer:=Filtered(inds,i->(inv[i]<>i and fusion[inv[i]]=fusion[i])or(inv[i]=i and Number(fusion,j->j=fusion[i])=1));;
 Print("INVERSION ",n," ",Length(inds)," ",Length(inner)," ",Length(outer),"\n");
od;
for row in AllCounts(t) do Print("COUNT ",row[1]," ",row[2]," ",row[3],"\n");od;
Print("TOM_ON_AVAILABLE ",TableOfMarks("ON")<>fail,"\n");
Print("COMPLETE ON CHARACTER AND INVERSION PROBE\n");
QUIT_GAP(0);
