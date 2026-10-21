# Exact fixed certificate. No Atlas download or search is used.
LoadPackage("ctbllib");;
if DefaultStabChainOptions.random<>1000 then Error("guaranteed permutation verification required");fi;
F:=GF(9);;z:=Z(9);;one:=One(F);;zero:=Zero(F);;
decode:=L->List(L,row->List(row,function(a) if a=-1 then return zero;else return z^a;fi;end));;
J:=Reversed(IdentityMat(5,F));;
bar:=M->List(M,row->List(row,x->x^3));;
s0:=DiagonalMat([-one,one,one,one,-one]);;
s2:=IdentityMat(5,F);;s2[1][1]:=zero;;s2[5][5]:=zero;;s2[1][5]:=one;;s2[5][1]:=one;;s2[3][3]:=-one;;
s1:=decode([[7,3,7,-1,4],[5,6,-1,4,-1],[3,4,4,-1,5],[5,4,4,2,1],[-1,7,1,7,5]]);;
r:=[s0,s1,s2];;
if not ForAll(r,s->Order(s)=2 and DeterminantMat(s)=one and s*J*TransposedMat(bar(s))=J) then Error("matrix hypotheses");fi;
if List(r,s->RankMat(s-IdentityMat(5,F)))<>[2,2,2] then Error("wrong involution class");fi;
if [Order(s0*s1),Order(s1*s2),Order(s0*s2)]<>[5,5,2] then Error("wrong string type");fi;
# Enumerate the isotropic projective points directly, without a group orbit.
points:=[];;v:=[];;
for j in [1..5] do
 for tail in Tuples(Elements(F),5-j) do
  v:=Concatenation(List([1..j-1],i->zero),[one],tail);;
  if Sum([1..5],i->v[i]*v[6-i]^3)=zero then Add(points,v);fi;
 od;
od;
if Length(points)<>2440 then Error("wrong point set");fi;
perms:=List(r,s->Permutation(s,points,OnLines));;
P:=Group(perms);;
if Size(P)<>258190571520 then Error("proper generated subgroup");fi;
subsets:=Combinations([1..3]);;
subs:=List(subsets,I->Subgroup(P,perms{I}));;
for i in [1..8] do for j in [1..8] do
 k:=Position(subsets,Intersection(subsets[i],subsets[j]));;
 if Intersection(subs[i],subs[j])<>subs[k] then Error("intersection property");fi;
od;od;
# Actual table class positions are identified by orders and centralizer sizes.
T:=CharacterTable("U5(3)");;irr:=Irr(T);;cl:=SizesConjugacyClasses(T);;
if Size(T)<>Size(P) or Length(irr)<>150 then Error("wrong table");fi;
tpos:=Filtered([1..150],i->OrdersClassRepresentatives(T)[i]=2 and SizesCentralizers(T)[i]=580608);;
fpos:=Filtered([1..150],i->OrdersClassRepresentatives(T)[i]=5);;
if tpos<>[3] or fpos<>[19] then Error("class route changed");fi;
mult:=List(irr,c->(c[1]+5*c[tpos[1]]+4*c[fpos[1]])/10);;
pow2:=PowerMap(T,2);;
fs:=List(irr,c->Sum([1..150],i->cl[i]*c[pow2[i]])/Size(T));;
if fs<>Indicator(T,2) then Error("direct indicator sum disagrees");fi;
if not ForAll(mult,m->IsInt(m) and m>0) or Minimum(mult{[2..150]})<>8 then Error("polytopal multiplicities");fi;
negative:=Filtered([1..150],i->fs[i]=-1);;
if List(negative,i->irr[i][1])<>[60,3660,7320,10980,14580] then Error("quaternionic character list");fi;
low:=Filtered([1..150],i->irr[i][1]<3846);;
if Length(low)<>24 or Minimum(List(Difference([1..150],low),i->irr[i][1]))<>4270 then Error("column-bound cutoff");fi;
if not ForAll(low,i->mult[i]>=1) then Error("low-degree table");fi;
# A compact stabilizer-chain order witness for the fixed permutation group.
chain:=StabChain(P);;orbitlengths:=[];;
while IsBound(chain.stabilizer) do Add(orbitlengths,Length(chain.orbit));chain:=chain.stabilizer;od;
if Product(orbitlengths)<>Size(P) then Error("stabilizer-chain product");fi;
Print("STATUS=PASS\npoints=",Length(points),"\ngroup_order=",Size(P),"\nchain_orbit_lengths=",orbitlengths,"\n");
Print("subset_orders=",List([1..8],i->[subsets[i],Size(subs[i])]),"\nIP_pairs=64\n");
Print("class_data=",List(Filtered([1..150],i->OrdersClassRepresentatives(T)[i] in [2,5]),i->[i,OrdersClassRepresentatives(T)[i],cl[i],SizesCentralizers(T)[i]]),"\n");
Print("low_degree_rows=",List(low,i->[i,irr[i][1],irr[i][3],irr[i][19],fs[i],mult[i]]),"\n");
Print("quaternionic_rows=",List(negative,i->[i,irr[i][1],mult[i]]),"\n");
Print("all_multiplicities=",mult,"\n");
Print("gap_version=",GAPInfo.Version,"\nctbllib_version=",PackageInfo("ctbllib")[1].Version,"\n");
QUIT;
