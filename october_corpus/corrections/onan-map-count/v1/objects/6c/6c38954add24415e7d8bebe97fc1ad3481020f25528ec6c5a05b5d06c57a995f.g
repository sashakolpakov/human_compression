SizeScreen([4096,40]);;
LoadPackage("ctbllib");;
Need:=function(ok,msg)if not ok then Error(msg);fi;end;;
Run:=function(name)
 local t,orders,sizes,types,p,q,is,js,ks,i,j,k,answer,c;
 t:=CharacterTable(name);Need(t<>fail,"missing named table");
 orders:=OrdersClassRepresentatives(t);sizes:=SizesConjugacyClasses(t);types:=Filtered(Set(orders),n->n>2);
 ks:=Filtered([1..Length(orders)],n->orders[n]=2);
 for p in types do for q in Filtered(types,n->n>=p)do
  is:=Filtered([1..Length(orders)],n->orders[n]=p);
  js:=Filtered([1..Length(orders)],n->orders[n]=q);answer:=0;
  for i in is do for j in js do for k in ks do
   c:=ClassMultiplicationCoefficient(t,i,j,k);Need(IsInt(c)and c>=0,"bad class constant");
   answer:=answer+sizes[k]*c;
  od;od;od;
  Print("COUNT ",name," ",p," ",q," ",answer,"\n");
 od;od;
end;;
for name in Concatenation(["ON"],Set(Maxes(CharacterTable("ON"))))do Run(name);od;
Print("COMPLETE DISTINCT CLASS CONSTANT COUNTS\n");QUIT_GAP(0);
