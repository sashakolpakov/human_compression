# Reconstruct every exceptional spherical action from its literal Coxeter
# presentation, then enumerate ALL unordered pairs. No source orbit table is read.
SizeScreen([100000,24]);;
Check278:=function(t,m) if not t then Error("PHASE278_REJECT ",m);fi;end;;
rows278:=[
 [[3,5],120,12,5,[1,3,5],[30,30,6]],
 [[5,3],120,20,5,[1,2,3,4,5],[30,60,60,30,10]],
 [[3,4,3],1152,24,6,[1,3,4,6],[96,72,96,12]],
 [[3,3,5],14400,120,15,[1,4,6,7,9,10,12,15],[720,1200,720,1800,720,1200,720,60]],
 [[5,3,3],14400,600,15,[1..15],[]]
];;
# Short words beta^a t_j beta^b with ZERO-based source j, and unordered orbit size.
missing278:=[[-3,3,-1,3600],[-4,0,-2,1200],[-4,3,-1,7200],
 [-5,0,-2,2400],[-5,3,-1,7200],[-4,3,-2,3600],[-6,3,-1,7200],
 [-9,1,4,1200],[-5,3,-2,7200],[-7,3,-1,14400],[-5,3,-3,1800],
 [-8,3,-1,7200],[-7,3,-2,7200],[-6,3,-4,1200],[-9,3,-1,3600],
 [-8,3,-2,7200],[-7,3,-4,2400],[-10,3,-1,7200],[-7,3,-5,1200],[-10,3,-2,3600]];;
Census278:=function(row)
 local labels,n,F,r,rels,i,j,Q,q,ct,t,G,H,beta,alpha,h,vcount,pointorbs,
  pairs,orbs,orbitof,ix,z,oldids,missids,m,w,bad,allids,sz,pair,vertices,burnside,g,fix;
 labels:=row[1];n:=Length(labels)+1; F:=FreeGroup(n);r:=GeneratorsOfGroup(F);
 rels:=List(r,x->x^2);
 for i in [1..n] do for j in [i+1..n] do
  if j=i+1 then Add(rels,(r[i]*r[j])^labels[i]);else Add(rels,(r[i]*r[j])^2);fi;
 od;od;
 Q:=F/rels;q:=GeneratorsOfGroup(Q);ct:=CosetTable(Q,Subgroup(Q,q{[2..n]}));
 t:=List([1..n],i->PermList(ct[2*i-1]));G:=Group(t);H:=Group(t{[2..n]});
 vcount:=Length(ct[1]);vertices:=[1..vcount];
 Check278(Size(G)=row[2] and vcount=row[3],"spherical action order and degree");
 Check278(Set(Orbit(G,1))=vertices,"transitive action");
 Check278(H=Stabilizer(G,1),"actual vertex stabilizer");
 Check278(Size(H)*vcount=Size(G),"vertex action index");
 beta:=Product(t);h:=row[4];alpha:=beta^h;
 Check278(Order(beta)=2*h and Order(alpha)=2,"Coxeter element and antipode orders");
 Check278(ForAll(t,x->Comm(x,alpha)=()) and ForAll(vertices,x->x^alpha<>x),"central fixed-point-free antipode");
 pointorbs:=OrbitsDomain(H,vertices);
 pairs:=Combinations(vertices,2);orbs:=OrbitsDomain(G,pairs,OnSets);
 Check278(Union(orbs)=pairs and Sum(List(orbs,Length))=Binomial(vcount,2),"complete disjoint unordered pair census");
 # A second count uses the action on all elements and the fixed-pair formula.
 burnside:=0;
 for g in Elements(G) do
  fix:=vcount-NrMovedPoints(g);
  burnside:=burnside+Binomial(fix,2)+Number(CycleLengths(g,vertices),x->x=2);
 od;
 Check278(burnside=Length(orbs)*Size(G),"independent fixed-pair Burnside count");
 # For every orbit record all its representatives whose first endpoint is1.
 orbitof:=[];
 for ix in [1..Length(orbs)] do for pair in orbs[ix] do
  if 1 in pair then z:=First(pair,x->x<>1);Check278(not IsBound(orbitof[z]),"disjoint orbit assignment");orbitof[z]:=ix;fi;
 od;od;
 Check278(ForAll([2..vcount],i->IsBound(orbitof[i])),"all basepoint pairs assigned");
 oldids:=List(row[5],i->orbitof[1^(beta^i)]);
 Check278(Length(Set(oldids))=Length(oldids),"distinct old representatives");
 Check278(Length(orbs[Last(oldids)])=vcount/2 and ForAll(orbs[Last(oldids)],p->p[1]^alpha=p[2]),"antipodal matching orbit");
 if labels<>[5,3,3] then
  Check278(Set(oldids)=[1..Length(orbs)],"source representative list complete");
  Check278(List(oldids,i->Length(orbs[i]))=row[6],"exact source-ordered orbit sizes");
 else
  Check278(Length(pointorbs)=45 and Length(orbs)=35,"120-cell full census is35");
  Check278(Length(oldids)=15,"literal source list has15");
  missids:=[];
  for m in missing278 do
   w:=beta^m[1]*t[m[2]+1]*beta^m[3];z:=1^w;
   Check278(z<>1,"missing word moves basepoint");ix:=orbitof[z];
   Check278(not ix in oldids and not ix in missids,"missing orbit new and distinct");
   Check278(Length(orbs[ix])=m[4],"missing representative orbit size");Add(missids,ix);
  od;
  Check278(Length(missids)=20 and Union(oldids,missids)=[1..Length(orbs)],"corrected35 representatives exhaustive");
  Check278(Collected(List(orbs,Length))=[[300,1],[1200,6],[1800,1],[2400,2],[3600,6],[7200,18],[14400,1]],"full120-cell size multiplicities");
  Print("PHASE278_MISSING_WORDS ",missing278,"\n");
 fi;
 Print("PHASE278_ROW {\"labels\":",labels,",\"order\":",Size(G),",\"vertices\":",vcount,",\"stabilizer_order\":",Size(H),",\"coxeter_half_order\":",h,",\"point_orbit_sizes\":",List(pointorbs,Length),",\"unordered_orbit_sizes\":",List(orbs,Length),",\"burnside_numerator\":",burnside,",\"old_exponents\":",List(row[5],i->i),",\"old_orbit_sizes\":",List(oldids,i->Length(orbs[i])),",\"missing_orbits\":",Length(orbs)-Length(oldids),"}\n");
end;;
for row278 in rows278 do Census278(row278);od;
Print("PHASE278_EXCEPTIONAL_CENSUS_PASS five_actions all_pairs exact35_with20_missing\n");
QUIT;
