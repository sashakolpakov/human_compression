# Finite audit of the source-isomorphic norm-shell/root-coset residue model.
P186HRequire:=function(test,msg)if not test then Error(msg);fi;end;;
P186HDist:=function(adj,root)
 local ds,queue,pos,x,y,par,cycle;
 ds:=List(adj,x->-1);par:=List(adj,x->0);ds[root]:=0;queue:=[root];pos:=1;cycle:=infinity;
 while pos<=Length(queue) do
  x:=queue[pos];pos:=pos+1;
  for y in adj[x] do
   if ds[y]=-1 then ds[y]:=ds[x]+1;par[y]:=x;Add(queue,y);
   elif par[x]<>y and par[y]<>x then cycle:=Minimum(cycle,ds[x]+ds[y]+1);fi;
  od;
 od;
 P186HRequire(not -1 in ds,"disconnected root-coset incidence graph");
 return [Maximum(ds),cycle];
end;;
P186HCheck:=function(q)
 local F,G,E,U,roots,flags,H,C,n,m,adj,i,j,dp,dl,expected;
 F:=GF(q);G:=SL(2,q);E:=Elements(G);
 U:=Group(List(Elements(F),t->[[One(F),t],[Zero(F),One(F)]]));
 roots:=Orbit(G,U,OnPoints);
 P186HRequire(Length(roots)=q+1 and ForAll(roots,H->Size(H)=q),"root groups");
 flags:=[];
 for H in roots do
  for C in RightCosets(G,H) do Add(flags,Set(List(AsList(C),g->Position(E,g))));od;
 od;
 n:=Length(E);m:=Length(flags);
 P186HRequire(n=q*(q^2-1) and m=(q+1)*(q^2-1),"residue type counts");
 P186HRequire(Length(Set(flags))=m,"duplicate flag supports");
 adj:=List([1..n+m],i->[]);
 for j in [1..m] do for i in flags[j] do Add(adj[i],n+j);Add(adj[n+j],i);od;od;
 P186HRequire(Set(List(adj{[1..n]},Length))=[q+1] and Set(List(adj{[n+1..n+m]},Length))=[q],"residue degrees");
 dp:=P186HDist(adj,1);dl:=P186HDist(adj,n+1);
 expected:=6;if IsEvenInt(q) then expected:=5;fi;
 P186HRequire(dp[1]=expected and dl[1]=6 and dp[2]=8 and dl[2]=8,"diameter or cycle length");
 Print("P186_HERMITIAN_LABEL ",rec(q:=q,points:=n,flags:=m,edges:=Sum(adj,Length)/2,point_diameter:=dp[1],flag_diameter:=dl[1],girth:=dp[2]),"\n");
end;;
for q in [3,4,5,7,8,9,11,13,16] do P186HCheck(q);od;
Print("P186_HERMITIAN_LABELS_PASS\n");
QUIT;
