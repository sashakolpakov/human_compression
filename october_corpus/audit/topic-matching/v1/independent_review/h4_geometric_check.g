# Independent 120-cell model from exact Coxeter reflection matrices.
# No presentation coset table, author census routine or source orbit list is used.
SizeScreen([100000,24]);;
NeedH4:=function(b,s) if not b then Error(s);fi;end;;
labelsH4:=[5,3,3];;
gramH4:=IdentityMat(4);;
for iH4 in [1..3] do
 cH4:=-(E(2*labelsH4[iH4])+E(2*labelsH4[iH4])^-1)/2;
 gramH4[iH4][iH4+1]:=cH4;gramH4[iH4+1][iH4]:=cH4;
od;
refsH4:=[];;
for iH4 in [1..4] do
 mH4:=IdentityMat(4);
 for jH4 in [1..4] do mH4[jH4][iH4]:=mH4[jH4][iH4]-2*gramH4[jH4][iH4];od;
 NeedH4(mH4*mH4=IdentityMat(4),"exact reflection involution");Add(refsH4,mH4);
od;
for iH4 in [1..4] do for jH4 in [iH4+1..4] do
 if jH4=iH4+1 then pH4:=labelsH4[iH4];else pH4:=2;fi;
 NeedH4(Order(refsH4[iH4]*refsH4[jH4])=pH4,"exact marked Coxeter order");
od;od;
vH4:=Inverse(gramH4)[1];;
NeedH4(ForAll(refsH4{[2..4]},x->vH4*x=vH4),"fundamental weight stabilizer");
pointsH4:=Orbit(Group(refsH4),vH4,OnRight);;
NeedH4(Length(pointsH4)=600,"600 exact 120-cell vertices");
permsH4:=List(refsH4,m->PermList(List(pointsH4,v->Position(pointsH4,v*m))));;
groupH4:=Group(permsH4);;
NeedH4(Size(groupH4)=14400,"full spherical action order");
baseH4:=Position(pointsH4,vH4);;
stabH4:=Stabilizer(groupH4,baseH4);;
NeedH4(stabH4=Group(permsH4{[2..4]}) and Size(stabH4)=24,"actual base stabilizer");
betaH4:=Product(permsH4);;
NeedH4(Order(betaH4)=30 and ForAll([1..600],i->pointsH4[i^(betaH4^15)]=-pointsH4[i]),"actual antipode");
orbitsH4:=OrbitsDomain(groupH4,Combinations([1..600],2),OnSets);;
NeedH4(Length(orbitsH4)=35 and Sum(orbitsH4,Length)=179700,"all unordered pairs");
orbitIndexH4:=function(w)
 local pair;
 pair:=Set([baseH4,baseH4^w]);
 NeedH4(Length(pair)=2,"distinct endpoints");
 return PositionProperty(orbitsH4,o->pair in o);
end;;
oldH4:=List([1..15],i->orbitIndexH4(betaH4^i));;
NeedH4(Length(Set(oldH4))=15,"fifteen distinct old power classes");
# These are the proposed correction words being tested, not presumed classes.
missingWordsH4:=[[-3,3,-1,3600],[-4,0,-2,1200],[-4,3,-1,7200],
 [-5,0,-2,2400],[-5,3,-1,7200],[-4,3,-2,3600],[-6,3,-1,7200],
 [-9,1,4,1200],[-5,3,-2,7200],[-7,3,-1,14400],[-5,3,-3,1800],
 [-8,3,-1,7200],[-7,3,-2,7200],[-6,3,-4,1200],[-9,3,-1,3600],
 [-8,3,-2,7200],[-7,3,-4,2400],[-10,3,-1,7200],[-7,3,-5,1200],[-10,3,-2,3600]];;
newH4:=[];;
for rowH4 in missingWordsH4 do
 ixH4:=orbitIndexH4(betaH4^rowH4[1]*permsH4[rowH4[2]+1]*betaH4^rowH4[3]);
 NeedH4(not ixH4 in oldH4 and not ixH4 in newH4,"genuinely new correction orbit");
 NeedH4(Length(orbitsH4[ixH4])=rowH4[4],"correction orbit size");Add(newH4,ixH4);
od;
NeedH4(Union(oldH4,newH4)=[1..35],"complete corrected representatives");
NeedH4(Length(OrbitsDomain(stabH4,[1..600]))=45,"45 ordered stabilizer orbits");
Print("PASS_H4_GEOMETRIC_MODEL vertices=600 group=14400 stabilizer=24 ordered=45 unordered=35 old=15 missing=20\n");
Print("ORBIT_SIZE_MULTIPLICITIES ",Collected(List(orbitsH4,Length)),"\n");
Print("EXACT_GRAM ",gramH4,"\n");
QUIT;
