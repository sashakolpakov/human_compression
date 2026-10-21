for q in [7,11,13] do
 G:=PSL(2,q);;n:=LargestMovedPoint(G);;ivs:=Filtered(Elements(G),x->Order(x)=2);;b:=ivs[1];;found:=false;;tested:=0;;
 for a in ivs do
  if a=b then continue;fi;
  A:=Group(a,b);;
  for c in ivs do
   if c=a or c=b then continue;fi;
   tested:=tested+1;
   if Group(a,b,c)<>G then continue;fi;
   B:=Group(b,c);;H:=Intersection(A,B);;
   if Size(H)>2 then
    Print("COUNTEREXAMPLE|",q,"|",Size(G),"|",List([a,b,c],x->List([1..n],i->i^x)),"|",List([a*b,b*c,a*c],Order),"|",Size(A),"|",Size(B),"|",Size(H),"\n");
    Print("EXTRA_INTERSECTION|",First(Elements(H),x->not x in Group(b)),"\n");found:=true;break;
   fi;
  od;
  if found then break;fi;
 od;
 Print("CASE|",q,"|",tested,"|",found,"\n");
 if found then break;fi;
od;
Print("TERMINAL_PROBE\n");
QUIT;
