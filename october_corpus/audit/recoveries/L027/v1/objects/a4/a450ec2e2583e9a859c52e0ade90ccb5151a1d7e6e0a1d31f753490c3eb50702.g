Need:=function(ok,msg)if not ok then Error(msg);fi;end;
Model:=function(q,a)
 local F,o,z,D,t,lines,u,v,perms,ends,i,j,r,s,w,G,A,B,m,n,ip;
 F:=GF(q);o:=One(F);z:=Zero(F);D:=[DiagonalMat([o,-o,-o]),DiagonalMat([-o,o,-o]),DiagonalMat([-o,-o,o])];
 t:=[[a,-a-o,z],[a-o,-a,z],[o,-o,-o]];
 Need(t^2=IdentityMat(3,F),"involution");lines:=[];
 for u in F do for v in F do Add(lines,[o,u,v]);od;od;
 for u in F do Add(lines,[z,o,u]);od;Add(lines,[z,z,o]);
 perms:=List(Concatenation(D,[t]),m->Permutation(m,lines,OnLines));
 for ends in Combinations([1,2,3],2) do
  r:=perms[ends[1]];s:=perms[4];w:=perms[ends[2]];G:=Group(r,s,w);A:=Group(r,s);B:=Group(s,w);
  ip:=Intersection(A,B)=Group(s);m:=Order(r*s);n:=Order(s*w);
  Print("MODEL ",q," a=",a," ends=",ends," order=",Size(G)," type=",m,",",n," IP=",ip,"\n");
 od;
end;
for q in [5,7,9,11,13,25] do for a in GF(q) do if a<>Zero(GF(q)) and a<>One(GF(q)) and a<>-One(GF(q)) then Model(q,a);fi;od;od;
QUIT;
