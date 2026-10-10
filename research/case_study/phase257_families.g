# Author certificate. Matrices act on actual one-dimensional row spaces.
# The independent phase261 implementation uses fractional linear maps.
Need257:=function(ok,msg)
 if not ok then Print("PHASE257_REJECT ",msg,"\n");QUIT_GAP(2);fi;
end;;
Ambient257:=function(p)
 local F,V,L,lines,hom,G;
 Need257(IsPrimeInt(p) and p>3,"prime greater than three");
 F:=GF(p);L:=GL(2,p);V:=[One(F),Zero(F)];
 lines:=Orbit(L,V,OnLines);hom:=ActionHomomorphism(L,lines,OnLines);G:=Image(hom);
 Need257(Length(lines)=p+1 and Size(Kernel(hom))=p-1 and Size(G)=p*(p^2-1),"faithful projective-line quotient");
 return rec(p:=p,field:=F,linear:=L,hom:=hom,group:=G,socle:=DerivedSubgroup(G));
end;;
Check257:=function(tag,X,r,leftorder,rightorder)
 local i,j,A,B;
 Need257(Length(r)=4 and Length(Set(r))=4 and ForAll(r,x->Order(x)=2),"four distinct involutions");
 for i in [1..4] do for j in [1..4] do
  if AbsInt(i-j)>1 then Need257(r[i]*r[j]=r[j]*r[i],"distant commutation");fi;
 od;od;
 Need257(Size(Subgroup(X.group,r))=Size(X.group),"generate full PGL");
 A:=Subgroup(X.group,r{[1..3]});B:=Subgroup(X.group,r{[2..4]});
 Need257(Size(A)=leftorder and Size(B)=rightorder,"two exact end orders");
 Print("P257_SAMPLE ",tag," PRIME ",X.p," ORDER ",Size(X.group)," ENDS ",[Size(A),Size(B)]," TYPE ",List([1..3],i->Order(r[i]*r[i+1]))," PSL ",List(r,x->x in X.socle)," PASS\n");
 Print("P257_MARKS ",tag," PRIME ",X.p," ",r,"\n");
end;;
Constant257:=function(p,mixed)
 local X,mats,r,n;
 Need257((mixed and p mod 12=5) or (not mixed and p>3 and p mod 4=3),"constant-family prime condition");
 X:=Ambient257(p);
 mats:=List([[[0,1],[1,0]],[[1,0],[1,-1]],[[-1,0],[0,1]],[[1,-2],[2,-1]]],M->M*One(X.field));
 r:=List(mats,M->Image(X.hom,M));n:=Size(X.group);
 if mixed then Check257("PSL_PGL",X,r,n/2,n);else Check257("PGL_PGL",X,r,n,n);fi;
end;;
Exceptional257:=function(p,kind)
 local X,S,H,iso,localmarks,r,Z,d,n;
 X:=Ambient257(p);
 if kind="S4" then
  Need257(p>5 and p mod 8 in [3,5],"S4-family prime condition");
  S:=SymmetricGroup(4);localmarks:=[(1,2),(2,3),(3,4)];
  H:=First(MaximalSubgroupClassReps(X.group),K->Size(K)=24 and IsomorphismGroups(S,K)<>fail);
  Need257(H<>fail and not IsSubgroup(X.socle,H),"S4 outside PSL");
 else
  Need257(p mod 20 in [9,11],"A5-family prime condition");
  S:=AlternatingGroup(5);localmarks:=[(1,2)(3,4),(2,4)(3,5),(1,3)(2,4)];
  Need257(Size(Group(localmarks))=60 and Order(localmarks[1]*localmarks[2])=5 and Order(localmarks[2]*localmarks[3])=3 and localmarks[1]*localmarks[3]=localmarks[3]*localmarks[1],"explicit retained A5 marking");
  H:=First(MaximalSubgroupClassReps(X.socle),K->Size(K)=60 and IsomorphismGroups(S,K)<>fail);
  Need257(H<>fail,"A5 subgroup in PSL");
 fi;
 iso:=IsomorphismGroups(S,H);Need257(iso<>fail,"local subgroup isomorphism");
 r:=List(localmarks,x->Image(iso,x));Z:=Centralizer(X.group,Subgroup(X.group,r{[1,2]}));
 Need257(Size(Z)=2,"unique nonidentity dihedral centralizer");d:=First(Elements(Z),x->Order(x)=2);
 if kind="S4" then Need257(not d in H,"centralizer outside local S4");
 else Need257(not d in X.socle,"centralizer outside PSL");fi;
 Add(r,d);n:=Size(X.group);Check257(Concatenation(kind,"_PGL"),X,r,Size(H),n);
end;;
for p in [7,11,19,31] do Constant257(p,false);od;
for p in [5,17,29,53] do Constant257(p,true);od;
for p in [11,13,19,37] do Exceptional257(p,"S4");od;
for p in [11,29,31,89] do Exceptional257(p,"A5");od;
Print("PHASE257_FAMILIES_PASS SAMPLES16\n");
QUIT_GAP(0);
