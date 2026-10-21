# Independent native projective-line constructions. No phase257 code imported.
Need261:=function(ok,msg) if not ok then Print("PHASE261_REJECT ",msg,"\n");QUIT_GAP(2);fi;end;;
Mob261:=function(p,M)
 local x,num,den,im;
 im:=[];
 for x in [0..p] do
  if x=p then num:=M[1][1] mod p;den:=M[2][1] mod p;
  else num:=(M[1][1]*x+M[1][2]) mod p;den:=(M[2][1]*x+M[2][2]) mod p;fi;
  if den=0 then Add(im,p+1);else Add(im,((num*PowerModInt(den,p-2,p)) mod p)+1);fi;
 od;
 Need261(Set(im)=[1..p+1],"actual nonsingular projective matrix");return PermList(im);
end;;
Ambient261:=function(p)
 local z,G;
 z:=First([2..p-1],n->PowerModInt(n,(p-1)/2,p)=p-1);
 G:=Group(List([[[1,1],[0,1]],[[0,-1],[1,0]],[[z,0],[0,1]]],M->Mob261(p,M)));
 Need261(Size(G)=p*(p^2-1),"independent PGL ambient");return G;
end;;
Check261:=function(label,p,G,r,ends)
 local i,j,A,B,L,signs;
 Need261(Length(Set(r))=4 and ForAll(r,x->Order(x)=2),"four distinct actual involutions");
 for i in [1..4] do for j in [1..4] do
  if AbsInt(i-j)>1 then Need261(Order(r[i]*r[j])=2,"commuting distinct distant generators");fi;
 od;od;
 A:=Subgroup(G,r{[1..3]});B:=Subgroup(G,r{[2..4]});L:=DerivedSubgroup(G);
 Need261(Size(L)=Size(G)/2,"actual derived PSL subgroup");
 Need261(Size(Subgroup(G,r))=Size(G),"whole PGL marking");
 Need261([Size(A),Size(B)]=ends,"both exact end group orders");
 signs:=List(r,x->x in L);
 if label="PSL/PGL" then Need261(A=L and signs=[true,true,true,false],"actual PSL first end and determinant cosets");fi;
 if label="A5/PGL" then Need261(signs=[true,true,true,false],"A5 inside and added involution outside PSL");fi;
 if label="S4/PGL" then Need261(signs{[1..3]}=[false,false,false],"tetrahedral markers outside PSL");fi;
 Print("P261_FAMILY ",label," p=",p," G=",Size(G)," ends=",ends," type=",List([1..3],i->Order(r[i]*r[i+1]))," PSLmarkers=",signs," PASS\n");
 return true;
end;;
Constant261:=function(p,kind)
 local G,r,n;
 if kind="PGL/PGL" then Need261(p>3 and p mod 4=3,"PGL/PGL prime progression");
 else Need261(p mod 12=5,"PSL/PGL prime progression");fi;
 G:=Ambient261(p);r:=List([[[0,1],[1,0]],[[1,0],[1,-1]],[[-1,0],[0,1]],[[1,-2],[2,-1]]],M->Mob261(p,M));n:=Size(G);
 if kind="PGL/PGL" then Check261(kind,p,G,r,[n,n]);else Check261(kind,p,G,r,[n/2,n]);fi;
 return r;
end;;
Exceptional261:=function(p,kind,expectfull)
 local G,L,T,H,iso,marks,a,c,b,D,Z,z,r,ends;
 G:=Ambient261(p);L:=DerivedSubgroup(G);
 if expectfull and kind="S4" then Need261(p>5 and p mod 8 in [3,5],"S4 prime progression");fi;
 if expectfull and kind="A5" then Need261(p mod 20 in [9,11],"A5 prime progression");fi;
 if kind="S4" then
  T:=SymmetricGroup(4);H:=First(MaximalSubgroupClassReps(G),h->Size(h)=24 and IsomorphismGroups(T,h)<>fail);
  Need261(H<>fail and not IsSubgroup(L,H),"S4 embedding outside PSL");marks:=[(1,2),(2,3),(3,4)];
 else
  T:=AlternatingGroup(5);H:=First(MaximalSubgroupClassReps(L),h->Size(h)=60 and IsomorphismGroups(T,h)<>fail);
  Need261(H<>fail,"A5 embedding in PSL");a:=(1,2)(3,4);c:=(1,3)(2,4);
  b:=First(Elements(T),x->Order(x)=2 and Order(a*x)=5 and Order(x*c)=3 and Size(Group(a,x,c))=60);
  Need261(b<>fail,"hemi-dodecahedral marking exists");marks:=[a,b,c];
 fi;
 iso:=IsomorphismGroups(T,H);r:=List(marks,x->Image(iso,x));
 D:=Subgroup(G,r{[1,2]});Z:=Centralizer(G,D);Need261(Size(Z)=2,"exact common centralizer");z:=First(Elements(Z),x->Order(x)=2);Add(r,z);
 if expectfull then Check261(Concatenation(kind,"/PGL"),p,G,r,[Size(H),Size(G)]);
 else
  ends:=[Size(Subgroup(G,r{[1..3]})),Size(Subgroup(G,r{[2..4]}))];
  if kind="S4" then Need261(p=5 and ends=[24,24] and Size(Subgroup(G,r))=120,"p5 exceptional two-small-ends control");
  else Need261(p=19 and z in L and Size(Subgroup(G,r))=Size(L),"wrong progression retains only PSL control");fi;
  Print("P261_EXCLUDED_CONTROL ",kind," p=",p," whole=",Size(Subgroup(G,r))," ends=",ends," PASS\n");
 fi;
end;;
Local261:=function()
 local S,odd,invol,b,c,d,n,orders,F,r,rels,i,j,k,W;
 S:=SymmetricGroup(4);odd:=Filtered(Elements(S),x->Order(x)=2 and SignPerm(x)=-1);
 invol:=Filtered(Elements(S),x->Order(x)=2);n:=0;orders:=[];
 for b in odd do for c in odd do if Order(b*c)=3 then for d in invol do
  if d<>b and b*d=d*b then
   n:=n+1;Add(orders,Order(c*d));Need261(Size(Group(b,c,d))=24 and Order(c*d) in [3,4],"complete S4 local alternatives");
  fi;
 od;fi;od;od;
 Need261(n=48 and Collected(orders)=[[3,24],[4,24]],"exact S4 local case census");
 for k in [3,4] do
  F:=FreeGroup(4);r:=GeneratorsOfGroup(F);rels:=List(r,x->x^2);
  for i in [1..4] do for j in [i+1..4] do
   if j=i+1 then if i=3 then Add(rels,(r[i]*r[j])^k);else Add(rels,(r[i]*r[j])^3);fi;
   else Add(rels,(r[i]*r[j])^2);fi;
  od;od;
  W:=F/rels;Need261(Size(W)=([120,384])[k-2],"actual finite Coxeter presentation order");
  Print("P261_COXETER [3,3,",k,"] ORDER ",Size(W)," PASS\n");
 od;
 Print("P261_LOCAL_S4_CASES48_PASS\n");
end;;
Local261();
for p in [7,11,19,23] do Constant261(p,"PGL/PGL");od;
for p in [5,17,29,41] do Constant261(p,"PSL/PGL");od;
for p in [11,13,19,29,37] do Exceptional261(p,"S4",true);od;
for p in [11,29,31,71] do Exceptional261(p,"A5",true);od;
Exceptional261(5,"S4",false);Exceptional261(19,"A5",false);
G261:=Ambient261(13);;R261:=List([[[0,1],[1,0]],[[1,0],[1,-1]],[[-1,0],[0,1]],[[1,-2],[2,-1]]],M->Mob261(13,M));;
Need261(Size(Subgroup(G261,R261))=Size(G261)/2,"wrong constant-matrix progression control");
Print("P261_EXCLUDED_CONTROL CONSTANT p13 PSL_ONLY PASS\nPHASE261_INDEPENDENT_FAMILIES_PASS\n");
QUIT_GAP(0);
