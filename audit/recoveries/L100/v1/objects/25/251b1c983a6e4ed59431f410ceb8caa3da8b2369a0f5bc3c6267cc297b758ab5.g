LoadPackage("grape");;
SizeScreen([100000,24]);;
R188Check:=function(b,s) if not b then Error(Concatenation("phase188: ",s));fi;end;;
R188Data:=function(colors,edges)
 return rec(colors:=colors,edges:=Set(List(edges,Set)),n:=Length(colors));
end;;
R188Graph:=function(d)
 return Graph(Group(()),[1..d.n],OnPoints,function(a,b)return Set([a,b]) in d.edges;end,true);
end;;
R188Pair:=function(d)
 local palette,classes,n,r,aug,A,C,K;
 n:=d.n;palette:=Set(d.colors);r:=Length(palette);
 classes:=List(palette,c->Filtered([1..n],i->d.colors[i]=c));
 aug:=Graph(Group(()),[1..n+r],OnPoints,function(a,b)
  if a<=n and b<=n then return Set([a,b]) in d.edges;fi;
  if a>n and b>n then return false;fi;
  if a<=n then return d.colors[a]=palette[b-n];fi;
  return d.colors[b]=palette[a-n];
 end,true);
 A:=AutGroupGraph(aug,[[1..n],[n+1..n+r]]);
 C:=Action(A,[1..n],OnPoints);
 R188Check(Size(C)=Size(A),"palette encoding not faithful");
 K:=AutGroupGraph(R188Graph(d),classes);
 R188Check(IsSubgroup(C,K) and IsNormal(C,K),"kernel normality");
 return [C,K];
end;;
