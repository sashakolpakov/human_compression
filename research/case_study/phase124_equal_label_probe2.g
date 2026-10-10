CosetTableDefaultMaxLimit:=200000;;
Probe:=function(d,n)
 local f,r,rels,i,j,k,g,s,a,ct,marks,p,subs,mask,meet,I,J;
 f:=FreeGroup(d);r:=GeneratorsOfGroup(f);rels:=List(r,x->x^2);
 for i in [1..d-1] do for j in [i+1..d] do
  if j=i+1 then Add(rels,(r[i]*r[j])^n);else Add(rels,(r[i]*r[j])^2);fi;
 od;od;
 for i in [1..d-2] do for k in [1..n-1] do Add(rels,((r[i+1]*r[i+2])^k*(r[i]*r[i+1])^k)^2);od;od;
 g:=f/rels;s:=GeneratorsOfGroup(g);a:=Subgroup(g,s{[1..d-1]});
 Print("START d=",d," n=",n,"\n");
 ct:=CosetTable(g,a);marks:=List([1..d],i->PermList(ct[2*i-1]));p:=Group(marks);
 Print("facet index=",Length(ct[1])," image order=",Size(p)," marking orders=",List([1..d-1],i->Order(marks[i]*marks[i+1])),"\n");
 subs:=[];for mask in [0..2^d-1] do I:=Filtered([1..d],i->QuoInt(mask,2^(i-1)) mod 2=1);Add(subs,Subgroup(p,marks{I}));od;
 for i in [0..2^d-1] do for j in [i..2^d-1] do
  I:=Filtered([0..d-1],k->QuoInt(i,2^k) mod 2=1);J:=Filtered([0..d-1],k->QuoInt(j,2^k) mod 2=1);meet:=Sum(Intersection(I,J),k->2^k);
  if Intersection(subs[i+1],subs[j+1])<>subs[meet+1] then Print("IP FAIL ",i," ",j,"\n");return;fi;
 od;od;Print("IP PASS every pair\n");
end;;
Probe(5,3);Probe(5,4);Probe(5,5);Probe(4,7);
QUIT;
