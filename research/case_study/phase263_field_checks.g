# Independent applications: native PSL groups, independently chosen local marks.
Need263:=function(ok,msg) if not ok then Print("PHASE263_REJECT ",msg,"\n");QUIT_GAP(2);fi;end;;
Mark263:=function(G,r,A)
 local i,j,B;
 Need263(Length(Set(r))=4 and ForAll(r,x->Order(x)=2),"actual distinct involutions");
 for i in [1..4] do for j in [1..4] do if AbsInt(i-j)>1 then Need263(r[i]*r[j]=r[j]*r[i],"distant commutations");fi;od;od;
 Need263(Subgroup(G,r)=G and Subgroup(G,r{[1..3]})=A,"full group and exact first end");
 B:=Subgroup(G,r{[2..4]});return Size(B);
end;;
Exceptional263:=function(p,kind)
 local G,H,T,I,a,b,c,r,D,Z,z,B;
 G:=PSL(2,p);
 if kind="A5" then
  Need263(p mod 20 in [1,19] and p<>19,"A5 progression");T:=AlternatingGroup(5);
  a:=(1,2)(3,4);c:=(1,3)(2,4);
  b:=First(Elements(T),x->Order(x)=2 and Order(a*x)=5 and Order(x*c)=3 and Group(a,x,c)=T);
 else
  Need263(p mod 24 in [1,23],"S4 progression");T:=SymmetricGroup(4);
  a:=(1,2);c:=(1,2)(3,4);
  b:=First(Elements(T),x->Order(x)=2 and Order(a*x)=3 and Order(x*c)=4 and Group(a,x,c)=T);
 fi;
 Need263(b<>fail,"literal local marking");
 H:=First(MaximalSubgroupClassReps(G),x->Size(x)=Size(T) and IsomorphismGroups(T,x)<>fail);
 Need263(H<>fail,"correct retained maximal subgroup");I:=IsomorphismGroups(T,H);r:=List([a,b,c],x->Image(I,x));
 D:=Subgroup(G,r{[1,2]});Z:=Centralizer(G,D);
 Need263(Size(Z)=2 and Size(Centralizer(H,D))=1,"external torus halfturn");z:=First(Elements(Z),x->x<>One(G));Add(r,z);
 B:=Mark263(G,r,H);Need263(B=Size(G),"opposite end full");
 Print("INDEPENDENT_PSL_FAMILY ",kind," p=",p," order=",Size(G)," ends=",[Size(H),B]," type=",List([1..3],i->Order(r[i]*r[i+1]))," PASS\n");
end;;
Extension263:=function(q)
 local G,inv,a,b,c,cs,N,r,k,Z,z,B;
 G:=PSL(2,q);inv:=Filtered(Elements(ConjugacyClass(G,First(AsList(G),x->Order(x)=2))),x->true);
 a:=inv[1];cs:=Filtered(Elements(Centralizer(G,a)),x->Order(x)=2 and x<>a);
 if q mod 4=1 then N:=(q-1)/2;else N:=(q+1)/2;fi;
 r:=fail;
 for b in inv do k:=Order(a*b);if k>2 and IsOddInt(k) and N mod k=0 then
  for c in cs do if Order(b*c)>2 and Subgroup(G,[a,b,c])=G then r:=[a,b,c];break;fi;od;
 fi;if r<>fail then break;fi;od;
 Need263(r<>fail,"extension-field full rank-three hypothesis");
 Z:=Centralizer(G,Subgroup(G,r{[1,2]}));Need263(Size(Z)=2,"extension-field common centralizer");z:=First(Elements(Z),x->x<>One(G));Add(r,z);
 B:=Mark263(G,r,G);
 Print("INDEPENDENT_NONPRIME_EXTENSION q=",q," order=",Size(G)," N=",N," type=",List([1..3],i->Order(r[i]*r[i+1]))," otherend=",B," PASS\n");
end;;
for p in [59,61] do Exceptional263(p,"A5");od;
for p in [71,97] do Exceptional263(p,"S4");od;
for q in [25,49] do Extension263(q);od;
Print("PHASE263_FIELD_PASS\n");QUIT;
