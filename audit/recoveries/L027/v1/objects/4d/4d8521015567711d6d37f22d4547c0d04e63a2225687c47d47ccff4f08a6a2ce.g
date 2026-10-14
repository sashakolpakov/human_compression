Need:=function(ok,message) if not ok then Error(message);fi;end;
Elementary:=function(F,i,j,x) local m; m:=IdentityMat(3,F);m[i][j]:=m[i][j]+x;return m;end;
M:=function(F,x,y) local m; m:=IdentityMat(3,F);m[2][1]:=x;m[2][3]:=y;return m;end;
SameGroup:=function(A,B) return Size(A)=Size(B) and ForAll(GeneratorsOfGroup(A),g->g in B) and ForAll(GeneratorsOfGroup(B),g->g in A);end;
ChecksIP:=function(gs)
 local subsets,groups,S,T,i,j,k,answer,count;
 subsets:=Combinations([1..Length(gs)]);groups:=[];
 for S in subsets do if IsEmpty(S) then Add(groups,TrivialSubgroup(Group(gs)));else Add(groups,Group(gs{S}));fi;od;
 answer:=true;count:=0;
 for i in [1..Length(subsets)] do for j in [1..Length(subsets)] do
   k:=Position(subsets,Intersection(subsets[i],subsets[j]));
   if not SameGroup(Intersection(groups[i],groups[j]),groups[k]) then answer:=false;fi;count:=count+1;
 od;od;return [answer,count];
end;
Model3:=function(q,a,b,c)
 local F,r,s,t,G,K,n,k,D,N,expected,ip,u,v,Q,w,xx,yy,zz,allvectors;
 F:=GF(q);r:=Elementary(F,1,3,a);s:=Elementary(F,3,1,One(F));t:=Elementary(F,1,3,b)*Elementary(F,2,3,c);
 Need(t<>IdentityMat(3,F) and t<>r,"distinct third mark");G:=Group(r,s,t);D:=Group(r,s);
 if b=Zero(F) or b=a then
   K:=Field([a]);n:=Size(K);k:=Order(r*s);expected:=n^2*2*k;
   N:=Group(List(Cartesian(Elements(K),Elements(K)),xy->M(F,c*xy[1],c*xy[2])));
   Need(IsNormal(G,N) and Size(N)=n^2 and Size(Intersection(N,D))=1,"actual rank3 module");
   ip:=ChecksIP([r,s,t]);Need(ip[1],"rank3 affine full IP");
 else
   K:=Field([a,b]);n:=Size(K);expected:=n*(n^2-1);ip:=[true,0];
   if c<>Zero(F) then
     Q:=v->(v[1]^2+a*v[1]*v[3]+a*v[3]^2)/(b*(a+b))+v[2]^2/c^2;
     allvectors:=Cartesian(Elements(F),Elements(F),Elements(F));
     for w in [r,s,t] do for v in allvectors do Need(Q(w*v)=Q(v),"actual preserved conic");od;od;
   fi;
 fi;
 Need(Size(G)=expected,"rank3 exact group order");
 Print("MODEL3 ",q," ",Position(Elements(F),a)," ",Position(Elements(F),b)," ",Position(Elements(F),c)," ",n," ",Size(G)," ",ip[2]," PASS\n");
end;
Model4:=function(q,a,b)
 local F,gs,K,n,k,G,D,N0,N3,A,B,ip,x,y,expected;
 F:=GF(q);gs:=[Elementary(F,2,3,One(F)),Elementary(F,3,1,a),Elementary(F,1,3,b),Elementary(F,2,1,One(F))];
 K:=Field([a*b]);n:=Size(K);k:=Order(gs[2]*gs[3]);G:=Group(gs);D:=Group(gs{[2,3]});
 N0:=Group(List(Cartesian(Elements(K),Elements(K)),xy->M(F,a*xy[1],xy[2])));
 N3:=Group(List(Cartesian(Elements(K),Elements(K)),xy->M(F,xy[1],b*xy[2])));
 A:=Group(gs{[1,2,3]});B:=Group(gs{[2,3,4]});
 Need(SameGroup(A,ClosureGroup(N0,D)) and SameGroup(B,ClosureGroup(N3,D)),"actual rank4 ends");
 Need(IsNormal(A,N0) and IsNormal(B,N3),"actual rank4 modules normal");
 Need(Size(N0)=n^2 and Size(N3)=n^2,"rank4 module dimensions");
 ip:=ChecksIP(gs);Need(ip[1]=(not a in K),"exact rank4 IP criterion");
 if a in K then
   Need(SameGroup(N0,N3) and SameGroup(A,B) and Size(G)=n^2*2*k,"failure equality case");
 else
   Need(Size(Intersection(N0,N3))=1 and SameGroup(Intersection(A,B),D),"actual disjoint modules");
   Need(Size(G)=n^4*2*k,"actual rank4 semidirect order");
 fi;
 Print("MODEL4 ",q," ",Position(Elements(F),a)," ",Position(Elements(F),b)," ",n," ",Size(G)," ",ip[1]," ",ip[2]," PASS\n");
end;
for q in [2,4,8] do
 F:=GF(q);o:=One(F);z:=Zero(F);
 for a in Elements(F) do if a<>z then
   Model3(q,a,z,o);Model3(q,a,a,o);
   for b in Elements(F) do if b<>z and b<>a then Model3(q,a,b,z);Model3(q,a,b,o);fi;od;
   for b in Elements(F) do if b<>z then Model4(q,a,b);fi;od;
 fi;od;
od;
F:=GF(16);o:=One(F);a:=PrimitiveElement(F);t:=a^5;
Model4(16,a,t/a);Model4(16,t,t);
# Actual triangular positive and excluded markings.
F:=GF(4);o:=One(F);z:=Zero(F);a:=PrimitiveElement(F);
r:=Elementary(F,1,2,o);s:=Elementary(F,2,3,o);t:=Elementary(F,1,2,a);
Need(Size(Group(r,s,t))=32 and ChecksIP([r,s,t])[1],"triangular wreath positive");
t:=r*Elementary(F,1,3,a);Need(Size(Group(r,s,t))=16 and not ChecksIP([r,s,t])[1],"triangular common commutator excluded");
# Exhaustive independent check of the elation commutation rule over GF(2).
F:=GF(2);id:=IdentityMat(3,F);invs:=Filtered(Elements(SL(3,2)),g->Order(g)=2);count:=0;
for a in invs do for b in invs do if a<>b then
 N:=a-id;P:=b-id;
 samecentre:=RankMat(Concatenation(TransposedMat(N),TransposedMat(P)))=1;
 sameaxis:=RankMat(Concatenation(N,P))=1;
 Need((a*b=b*a)=(samecentre or sameaxis),"all GF2 commuting elations");count:=count+1;
fi;od;od;
Print("TRIANGULAR 2 COMMUTATION ",count," PASS\nPASS_ALL_EVEN_CONTROLS\n");QUIT;
