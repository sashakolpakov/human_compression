SizeScreen([100000,100000]);;
F:=FreeGroup("a","b","c","d");;a:=F.1;;b:=F.2;;c:=F.3;;d:=F.4;;
base:=[a^2,b^2,c^2,d^2,(a*b)^3,(a*c)^6,(a*d)^2,(b*c)^2,(b*d)^6,(c*d)^3,(d*(c*a)^2*c)^2,(a*(b*d)^2)^2,(b*(a*c)^2*a)^2];;
ProdSet:=function(H,K) return Set(Concatenation(List(Elements(H),h->List(Elements(K),k->h*k))));end;;
Helly:=function(H,K,L) return ProdSet(Intersection(H,K),Intersection(H,L))=Intersection(Elements(H),ProdSet(K,L));end;;
Tor:=function(diag,s)
 local T,x,y,z,r;
 T:=FreeGroup("x","y","z");x:=T.1;y:=T.2;z:=T.3;
 r:=[x^2,y^2,z^2,(x*y)^3,(y*z)^6,(x*z)^2];
 if diag then Add(r,(x*(y*z)^2)^(2*s));else Add(r,(x*(y*z)^2*y)^s);fi;
 return T/r;
end;;
iso:=fail;;iv:=fail;;P:=fail;;gens:=[];;h:=[];;maxs:=[];;small:=fail;;degree:=0;;markers:=[];;
for n in [3,6] do
 t:=n/3;;
 U:=F/Concatenation(base,[(c*(d*b)^2*d)^n]);;iso:=IsomorphismPermGroup(U);;P:=Image(iso);;gens:=List(GeneratorsOfGroup(U),x->Image(iso,x));;
 if Size(P)<>720*t^6 then Error("original exact order");fi;
 # Verify literal modified word in the ORIGINAL presented group.
 if (gens[3]*(gens[4]*gens[2])^2)^(2*t)<>One(P) then Error("new relator in original");fi;
 V:=F/Concatenation(base,[(c*(d*b)^2)^(2*t)]);;iv:=IsomorphismPermGroup(V);;VP:=Image(iv);;vg:=List(GeneratorsOfGroup(V),x->Image(iv,x));;
 if (vg[3]*(vg[4]*vg[2])^2*vg[4])^n<>One(VP) then Error("old relator in modified");fi;
 if Size(VP)<>Size(P) or Order(vg[2]*vg[4])<>6 then Error("modified order/edge");fi;
 h:=List([0..15],m->Subgroup(P,gens{Filtered([1..4],i->QuoInt(m,2^(i-1)) mod 2=1)}));;
 for m in [0..15] do for k in [0..15] do
  v:=Sum(Filtered([0..3],i->QuoInt(m,2^i) mod 2=1 and QuoInt(k,2^i) mod 2=1),i->2^i);
  if Intersection(h[m+1],h[k+1])<>h[v+1] then Error("IP");fi;
 od;od;
 maxs:=List([1..4],i->h[16-2^(i-1)]);;
 for inds in Combinations([1..4],3) do if not Helly(maxs[inds[1]],maxs[inds[2]],maxs[inds[3]]) then Error("global triple Helly");fi;od;
 for i in [1..4] do
  subs:=List(Difference([1..4],[i]),j->Intersection(maxs[i],maxs[j]));
  if not Helly(subs[1],subs[2],subs[3]) then Error("local Helly");fi;
 od;
 # Ordered maps: omitted0=(c,d,b), omitted1=(d,c,a), omitted2=(a,b,d), omitted3=(b,a,c).
 markers:=[[gens[3],gens[4],gens[2]],[gens[4],gens[3],gens[1]],[gens[1],gens[2],gens[4]],[gens[2],gens[1],gens[3]]];;
 toroids:=[Tor(true,t),Tor(false,2),Tor(true,1),Tor(false,2)];;
 orders:=[36*t^2,48,36,48];;
 for i in [1..4] do
  if List([[1,2],[2,3],[1,3]],p->Order(markers[i][p[1]]*markers[i][p[2]]))<>[3,6,2] then Error("rank-two collapse");fi;
  T:=toroids[i];map:=GroupHomomorphismByImages(T,maxs[i],GeneratorsOfGroup(T),markers[i]);
  if map=fail or Size(T)<>orders[i] or Size(maxs[i])<>orders[i] or Size(Image(map))<>orders[i] then Error("marked toroid isomorphism");fi;
 od;
 covering:=Tor(false,n);;mp:=GroupHomomorphismByImages(covering,maxs[1],GeneratorsOfGroup(covering),markers[1]);;
 if mp=fail or Size(covering)<>12*n^2 or Size(Image(mp))<>orders[1] then Error("claimed toroid cover");fi;
 Print("CASE ",n," original=",Size(P)," modified=",Size(VP)," parabolics=",List(maxs,Size)," marked_toroids=PASS IP=256 localHelly=4 globalHelly=4 coverdegree=3\n");
 small:=SmallerDegreePermutationRepresentation(P);;sg:=List(gens,x->Image(small,x));;degree:=LargestMovedPoint(Image(small));;
 Print("GENERATORS ",n," ",List(sg,x->ListPerm(x,degree)),"\n");
od;
Print("GAP_VERSION ",GAPInfo.Version,"\nPASS_EXACT_SOURCE_SECTION5\n");
QUIT;
