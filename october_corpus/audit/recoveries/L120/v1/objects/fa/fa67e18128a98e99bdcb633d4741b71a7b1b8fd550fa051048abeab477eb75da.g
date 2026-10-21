SizeScreen([1000000,1000000]);;
Read(intervalFile);;
Read(inputFile);;
Need:=function(b,s)if not b then Error(s);fi;end;;
Need(IsInt(degree) and degree>=5 and degree<>6,"natural full automorphisms");;
Need(IsInt(rankLimit) and rankLimit>=3 and rankLimit<degree,"fixed rank interval");;
if kind="symmetric" then G:=SymmetricGroup(degree);elif kind="even" then G:=AlternatingGroup(degree);else Error("fixed group kind");fi;;checks:=0;;count:=0;;
for indices in ids do
 Need(IsList(indices) and Length(indices)>=3 and Length(indices)<=rankLimit,"mark rank");
 Need(ForAll(indices,i->IsInt(i) and i>=1 and i<=Length(ivs)),"literal mark indices");
 t:=List(indices,i->ivs[i]);;
 Need(ForAll(t,x->IsPerm(x) and x in G),"actual permutation domain");
 answer:=IntervalStringIP(t);;
 Need(answer.ok and Group(t)=G,"actual string C-marking and target");
 Need(answer.checks=(Length(t)-1)*(Length(t)-2)/2,"every interval checked");
 checks:=checks+answer.checks;count:=count+1;
 Print("SOLUTION|",List(t,g->List([1..degree],x->x^g)),"\n");
od;
Print("DEGREE|",degree,"\nRANK_LIMIT|",rankLimit,"\nVALIDATED_TUPLES|",count,
 "\nINTERVAL_CHECKS|",checks,"\nCOMPLETE_FINITE_INTERVAL_VALIDATION\n");
QUIT;
