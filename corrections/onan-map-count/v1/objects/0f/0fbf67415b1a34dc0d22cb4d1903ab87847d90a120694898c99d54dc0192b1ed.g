LoadPackage("ctbllib");;
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
t:=CharacterTable("ON");; names:=Maxes(t);; Print("MAXES ",names,"\n");;
for name in names do
 m:=CharacterTable(name);; Need(m<>fail,"maximal character table missing");;
 Print("MAX ",name," ORDER ",Size(m)," TYPES ",Set(OrdersClassRepresentatives(m)),"\n");
 for row in AllCounts(m) do Print("MCOUNT ",name," ",row[1]," ",row[2]," ",row[3],"\n");od;
od;
Print("COMPLETE MAXIMAL CHARACTER PROBE\n");QUIT_GAP(0);
