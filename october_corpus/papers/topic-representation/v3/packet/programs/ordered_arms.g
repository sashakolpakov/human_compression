# Optional finite diagnostics for the uniform rigid-arm theorem.
# Full proof is written; these three small tuples are not a general certificate.
if LoadPackage("grape")=fail then Error("GRAPE unavailable");fi;
Need:=function(b,s) if not b then Error(Concatenation("L126_ARMS_REJECT ",s));fi;end;
Arms:=function(d,split)
 local tuples,colors,edges,t,center,i,k,last,v,n,cls,palette,aug,C,K,base,
       gr,A,cor,kernel,p,res,seen,perm,expected;
 tuples:=PermutationsList([1..d]);colors:=List([1..d],x->1);edges:=[];
 for t in tuples do
  center:=Length(colors)+1;
  if split then Add(colors,2+(1-SignPerm(PermList(t)))/2);else Add(colors,2);fi;
  for i in [1..d] do
   last:=center;
   for k in [1..i] do
    v:=Length(colors)+1;Add(colors,10+10*i+k);
    Add(edges,Set([last,v]));last:=v;
   od;
   Add(edges,Set([last,t[i]]));
  od;
 od;
 n:=Length(colors);edges:=Set(edges);palette:=Set(colors);
 cls:=List(palette,c->Filtered([1..n],i->colors[i]=c));
 gr:=Graph(Group(()),[1..n],OnPoints,function(a,b)return Set([a,b]) in edges;end,true);
 aug:=Graph(Group(()),[1..n+Length(palette)],OnPoints,function(a,b)
  if a<=n and b<=n then return Set([a,b]) in edges;fi;
  if a>n and b>n then return false;fi;
  if a<=n then return colors[a]=palette[b-n];fi;
  return colors[b]=palette[a-n];
 end,true);
 A:=AutGroupGraph(aug,[[1..n],[n+1..n+Length(palette)]]);
 C:=Action(A,[1..n],OnPoints);K:=AutGroupGraph(gr,cls);
 Need(Size(A)=Size(C),"faithful palette encoding");
 Need(ForAll(GeneratorsOfGroup(C),g->OnSets([1..d],g)=[1..d]),"recognizable old objects");
 res:=Action(C,[1..d],OnPoints);
 Need(res=SymmetricGroup(d),"full restriction action");
 kernel:=Stabilizer(C,[1..d],OnTuples);Need(Size(kernel)=1,"ordered rigidity");
 expected:=Factorial(d);if split then expected:=expected/2;fi;
 Need(Size(K)=expected and Size(C)=Factorial(d),"complete group pair");
 Print("ARMS_PASS d=",d," split=",split," vertices=",n," C=",Size(C)," K=",Size(K),"\n");
end;
Arms(3,false);Arms(4,false);Arms(4,true);
Print("L126_ORDERED_ARMS_COMPLETE\n");QUIT;
