Need:=function(ok,msg)if not ok then Error(msg);fi;end;
Lines:=function(F)local o,z,x,y,L;o:=One(F);z:=Zero(F);L:=[];
 for x in F do for y in F do Add(L,[o,x,y]);od;od;for x in F do Add(L,[z,o,x]);od;Add(L,[z,z,o]);return L;end;
Perms:=function(L,ms)return List(ms,m->Permutation(m,L,OnLines));end;
CheckIP:=function(gs)
 local ss,gg,S,i,j,k,answer;
 ss:=Combinations([1..Length(gs)]);gg:=[];
 for S in ss do if IsEmpty(S)then Add(gg,Group(()));else Add(gg,Group(gs{S}));fi;od;
 answer:=true;for i in [1..Length(ss)]do for j in [1..Length(ss)]do
  k:=Position(ss,Intersection(ss[i],ss[j]));if Intersection(gg[i],gg[j])<>gg[k]then answer:=false;fi;
 od;od;return answer;
end;
Generic:=function(q,a,withv)
 local F,o,z,D,A,t,L,ps,G,H,N,K,ks,xy,M,orders,expected,m,es,gs,ip,pos,neg;
 F:=GF(q);o:=One(F);z:=Zero(F);D:=[DiagonalMat([o,-o,-o]),DiagonalMat([-o,o,-o]),DiagonalMat([-o,-o,o])];
 A:=[[a,-a-o,z],[a-o,-a,z],[z,z,-o]];t:=StructuralCopy(A);if withv then t[3][1]:=o;t[3][2]:=-o;fi;
 L:=Lines(F);ps:=Perms(L,Concatenation(D,[t,A]));G:=Group(ps{[1,2,3,4]});H:=Group(ps{[1,2,3,5]});
 K:=Field([a]);ks:=Size(K);m:=Lcm(Order(ps[1]*ps[5]),2);expected:=2*m;
 if withv then
  M:=[];for xy in Cartesian(Elements(K),Elements(K))do Add(M,[[o,z,z],[z,o,z],[xy[1],xy[2],o]]);od;
  N:=Group(Perms(L,M));Need(Size(N)=ks^2 and IsNormal(G,N) and Size(Intersection(N,H))=1,"actual translation kernel");
  Need(ClosureGroup(N,H)=G,"actual complement generates whole group");expected:=expected*ks^2;
 fi;
 Need(Size(G)=expected,"generic exact order");orders:=List([1,2,3],i->Order(ps[i]*ps[4]));
 if withv then Need(orders[1]=Order(ps[1]*ps[5]) and orders[2]=Order(ps[2]*ps[5]) and orders[3]=2*Characteristic(F),"generic exact types");fi;
 pos:=0;neg:=0;
 for es in Combinations([1,2,3],2)do gs:=[ps[es[1]],ps[4],ps[es[2]]];ip:=CheckIP(gs);
  if withv then Need(ip,"all generic outer pairs full IP");fi;
  if ip then pos:=pos+1;if not withv then Need(2 in orders{es} and IsOddInt(Maximum(orders{es})) and Size(G)=4*Maximum(orders{es}),"dihedral degenerate exact type");fi;
  else neg:=neg+1;fi;
 od;
 Print("GENERIC ",q," ",Position(Elements(F),a)," ",withv," ",ks," ",Size(G)," ",orders[1]," ",orders[2]," ",orders[3]," ",pos," ",neg," 192 PASS\n");
end;
Triangular:=function(p,kind)
 local F,o,z,D,t,U,L,ps,G,es,gs,ip,ok,orders,expected,pos,neg,A2,A3,N2,N3,x,y,forms;
 F:=GF(p);o:=One(F);z:=Zero(F);D:=[DiagonalMat([o,-o,-o]),DiagonalMat([-o,o,-o]),DiagonalMat([-o,-o,o])];
 if kind="one"then t:=[[o,z,z],[o,-o,z],[z,z,-o]];expected:=4*p;
 elif kind="product"then t:=[[o,z,z],[o,-o,z],[o,z,-o]];expected:=4*p^2;
 else t:=[[o,-2*o,z],[z,-o,z],[o,-o,-o]];expected:=4*p^3;fi;
 L:=Lines(F);ps:=Perms(L,Concatenation(D,[t]));G:=Group(ps);Need(Size(G)=expected,"triangular actual group order");
 orders:=List([1,2,3],i->Order(ps[i]*ps[4]));pos:=0;neg:=0;
 for es in Combinations([1,2,3],2)do
  gs:=[ps[es[1]],ps[4],ps[es[2]]];ip:=CheckIP(gs);
  if kind="one"then ok:=es=[1,3];elif kind="product"then ok:=es<>[2,3];else ok:=true;fi;
  Need(ip=ok,"triangular full IP and failure");if ip then pos:=pos+1;else neg:=neg+1;fi;
 od;
 if kind="heis"then
  U:=function(x,y,z)return [[o,x,Zero(F)],[Zero(F),o,Zero(F)],[y,z,o]];end;
  A2:=Group(ps[2],ps[4]);A3:=Group(ps[3],ps[4]);
  N2:=Perms(L,List(Elements(F),x->U(x,Zero(F),x/(2*o))));
  N3:=Perms(L,List(Elements(F),y->U(Zero(F),y,-y)));
  Need(ForAll(N2,g->g in A2) and ForAll(N3,g->g in A3),"actual Heisenberg kernels");
  Need(Size(Group(N2))=p and Size(Group(N3))=p and Size(Intersection(Group(N2),Group(N3)))=1,"Heisenberg kernel sizes");
  forms:=Perms(L,List(Elements(F),x->U(x,Zero(F),x/(2*o))*D[2]));
  Need(ForAll(forms,g->g in A2),"second end d2 coset");
  forms:=Perms(L,List(Elements(F),x->U(2*o,x,x)*D[2]));
  Need(ForAll(forms,g->g in A3) and ForAll(forms,g->not g in A2),"actual excluded common d2 coset");
 fi;
 Print("TRIANGULAR ",p," ",kind," ",Size(G)," ",orders[1]," ",orders[2]," ",orders[3]," ",pos," ",neg," 192 PASS\n");
end;
SmallConics:=function()
 local ss,G,gs,a,c,b,types,got;
 ss:=[[(1,2),(2,3),(3,4)],[(1,2),(2,3),(1,2)(3,4)]];
 for gs in ss do Need(Group(gs)=SymmetricGroup(4) and CheckIP(gs),"literal S4 marking");Print("CONIC S4 ",Order(gs[1]*gs[2])," ",Order(gs[2]*gs[3])," 64 PASS\n");od;
 G:=AlternatingGroup(5);a:=(1,2)(3,4);c:=(1,3)(2,4);got:=[];
 for b in Elements(G)do if Order(b)=2 then
  gs:=[a,b,c];types:=[Order(a*b),Order(b*c)];
  if (types=[3,5] or types=[5,5]) and not types in got and Group(gs)=G and CheckIP(gs)then
   Add(got,types);Print("CONIC A5 ",types[1]," ",types[2]," 64 PASS\n");
  fi;
 fi;od;Need(Set(got)=Set([[3,5],[5,5]]),"two A5 types witnessed");
end;
Unipotents:=function(p)
 local F,I,N,J,X,r,s,A;
 F:=GF(p);I:=IdentityMat(3,F);N:=NullMat(3,3,F);N[1][2]:=One(F);N[2][3]:=One(F);J:=I+N;
 if p=2 then Need(Order(J)=4,"binary regular unipotent");Print("UNIPOTENT 2 4 PASS\n");
 else
  Need(Order(J)=p and RankMat(J-I)=2,"odd regular unipotent correction");X:=I+N+N^2/(2*One(F));r:=DiagonalMat([-One(F),One(F),-One(F)]);s:=r*X;
  Need(r^2=I and s^2=I and DeterminantMat(r)=One(F) and Order(r*s)=p,"literal inverted regular unipotent");
  A:=DiagonalMat([-One(F),-One(F),One(F)]);A[1][2]:=-One(F);r:=DiagonalMat([One(F),-One(F),-One(F)]);
  Need(Order(A)=2*p and r*A*r=A^-1,"maximal odd unipotent dihedral");Print("UNIPOTENT ",p," ",p," ",2*p," PASS\n");
 fi;
end;
for q in [3,5,7,9,11]do for a in GF(q)do if a<>One(GF(q)) and a<>-One(GF(q))then Generic(q,a,false);Generic(q,a,true);fi;od;od;
for p in [3,5,7]do for kind in ["one","product","heis"]do Triangular(p,kind);od;od;
SmallConics();for p in [2,3,5,7]do Unipotents(p);od;
Print("PASS_ALL_ODD_THREE_CONTROLS\n");QUIT;
