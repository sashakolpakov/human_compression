SizeScreen([4096,40]);;
LoadPackage("ctbllib");;
Need:=function(b,m)if not b then Error(m);fi;end;;
Emit:=function(name)
 local t,orders,types,sizes,chars,chi,v,rows,record;
 t:=CharacterTable(name);Need(t<>fail,"missing named table");
 orders:=OrdersClassRepresentatives(t);types:=Set(orders);sizes:=SizesConjugacyClasses(t);chars:=Irr(t);
 Print("TABLE ",name," ",Size(t)," ",Length(types)," ",Length(chars),"\n");
 Print("TYPES");for record in types do Print(" ",record);od;Print("\n");
 for chi in chars do
  v:=List(types,n->Sum(Filtered([1..Length(orders)],i->orders[i]=n),i->sizes[i]*chi[i]));
  Need(ForAll(v,IsInt),"order-class sum not integral");
  Print("VECTOR ",chi[1]);for record in v do Print(" ",record);od;Print("\n");
 od;
 Print("ENDTABLE ",name,"\n");
end;;
t:=CharacterTable("ON");;names:=Maxes(t);;
Emit("ON");;
for name in Set(names) do Emit(name);od;
Print("MAXCLASSES");for name in names do Print(" ",name);od;Print("\n");
Print("COMPLETE EXACT ORDER VECTORS\n");QUIT_GAP(0);
