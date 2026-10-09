LoadPackage("grape");
LogTo("research/leemans/kneser_matrix_check.log");
CheckKneserTensor := function(n,k,r)
 local N,subsets,vertices,graph,auts,expected;
 N:=n+k*(r-2);
 subsets:=Combinations([1..N],k);
 vertices:=Cartesian([1..r],subsets);
 graph:=Graph(Group(()),vertices,function(a,g)return a;end,
   function(a,b) return a[1]<>b[1] and IsEmpty(Intersection(a[2],b[2]));end,true);
 auts:=AutGroupGraph(graph);
 expected:=Factorial(N)*Factorial(r);
 Print("n=",n," k=",k," r=",r," N=",N," vertices=",Length(vertices),
       " graph_Aut_order=",Size(auts)," predicted=",expected,"\n");
 if Size(auts)<>expected then Error("Automorphism prediction failed");fi;
end;
for pars in [[5,2,2],[5,2,3],[6,2,3],[7,3,3],[3,1,3]] do
 CallFuncList(CheckKneserTensor,pars);
od;
Print("ALL PASS\n");
LogTo();
QUIT;
