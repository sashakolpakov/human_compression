# Complete finite premises of the uniform signed-end proof.
Read("signed_model.g");
Need:=function(b,s) if not b then Error(s);fi;end;
AllIP:=function(s)
 local sets,groups,I,J,c;
 sets:=Combinations([1..Length(s)]);
 groups:=List(sets,I->Group(Concatenation([()],s{I})));
 c:=0;
 for I in [1..Length(sets)] do for J in [1..Length(sets)] do
  Need(Intersection(groups[I],groups[J])=groups[Position(sets,Intersection(sets[I],sets[J]))],"subset intersection");c:=c+1;
 od;od;
 return c;
end;
Run:=function(e,t)
 local s,sw,v,f,p,N,M,L,full,actual,i,j,gens,c,orbs,old,X,P,leaf;
 s:=Cap(t,e);Need(Length(s)=t-e/2,"rank");
 sw:=List([1..t-1],i->(i,i+1)*(t+i,t+i+1));
 v:=List([1..t],i->(i,t+i));
 for i in [1..Length(s)] do
  Need(Order(s[i])=2 and SignPerm(s[i])=1,"even involution");
  if i+2<=Length(s) then for j in [i+2..Length(s)] do Need(s[i]*s[j]=s[j]*s[i],"string");od;fi;
 od;
 f:=Product(v{[t-e+1..t]});p:=t-e-1;
 Need((s[p-1]*s[p])^3=f,"separating cube");
 full:=Group(Concatenation(sw,List([1..t-1],i->v[i]*v[i+1])));
 Need(Group(s)=full and Size(full)=2^(t-1)*Factorial(t),"full signed group");
 N:=Group(Concatenation(sw{[1..p]},[f]));
 Need(Group(s{[1..p]})=N,"prefix N");
 gens:=Concatenation(sw{[1..p+1]},List([1..p+2],i->v[i]*Product(v{[p+3..t]})));
 M:=Group(gens);Need(Group(s{[1..p+1]})=M,"prefix M");
 if e=4 then
  L:=Group(Concatenation(sw{[1..t-3]},List([1..t-3],i->v[i]*v[i+1]),[v[t-1]*v[t],sw[t-1]]));
  Need(Group(s{[1..p+2]})=L,"prefix L");
 fi;
 # Check the exact restriction-kernel inclusions at both finite starts.
 old:=Group(());X:=[1];
 for i in [1..Length(s)] do
  P:=Group(s{[1..i]});Need(IsSubgroup(old,Stabilizer(P,Difference([1..2*t],X),OnTuples)),"leaf kernel");
  old:=P;X:=Orbit(P,1);
 od;
 c:=AllIP(s);
 Print("CAP ",e," ",t," order ",Size(full)," pairs ",c," type ",List([1..Length(s)-1],i->Order(s[i]*s[i+1])),"\n");
 return c;
end;
count:=Run(2,5)+Run(4,7);;
Need(count=1280,"pair total");
Print("ALL_SIGNED_CAP_CERTIFICATES_PASS 1280\n");
QUIT;
