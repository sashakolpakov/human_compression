# Exact Todd-Coxeter orders of primary Atlas presentations and their amalgams.
# Finite source rows are hypotheses to compare, not quotient candidate filters.
SizeScreen([240,40]);;
Read("phase22_N009_atlas4_library.g");;Read("phase22_N009_universal5_input.g");;
F:=FreeGroup(5);;f:=GeneratorsOfGroup(F);;
orders22:=[];;
for A in atlas4_22 do
 rel:=List(A.words,w->Product(List(w,i->f[i])));;
 tab:=CosetTableFromGensAndRels(f{[1..4]},rel,[]);;
 if Length(tab[1])<>A.order then Error("Atlas complete presentation order");fi;
 Add(orders22,[A.label,Length(tab[1])]);
od;
Print("PASS primary Atlas complete marked presentations ",Length(orders22),"\n");
results22:=[];;at:=0;;
for row in rows5_22 do
 A:=First(atlas4_22,x->x.label=row[1][1]);;B:=First(atlas4_22,x->x.label=row[1][2]);;
 rel:=Concatenation(List(A.words,w->Product(List(w,i->f[i]))),List(B.words,w->Product(List(w,i->f[i+1]))),[Comm(f[1],f[5])]);;
 tab:=CosetTableFromGensAndRels(f,rel,[]);;n:=Length(tab[1]);;
 if n<>row[2] then Error("Universal amalgam order mismatch",row,n);fi;
 Add(results22,[row[1],n]);at:=at+1;
 Print("ROW ",at," ",row[1]," order=",n,"\n");
od;
PrintTo("phase22_N009_universal5_orders.json",results22,"\n");
PrintTo("phase22_N009_atlas4_presentation_orders.json",orders22,"\n");
Print("PASS ",Length(results22)," finite universal amalgams, exact complete coset tables; all eight rank-five rows are finite.\n");
QUIT;
