# Native Mathieu designs, exact full automorphism groups, and explicit
# derived-plane isomorphisms. This is finite GAP/GRAPE evidence, not Lean.
LoadPackage("design");;
LoadPackage("grape");;
SizeScreen([100000,24]);;
if not IsBound(P186_OUTPUT) then P186_OUTPUT:="/private/tmp/phase186_witt_witness.json";fi;
P186Require:=function(test,msg) if not test then Error(msg);fi;end;;
P186Models:=rec();;
P186Plane:=function()
 local F,raw,vecs,blocks,p,normal,linear,semilinear;
 F:=GF(4);raw:=Filtered(Tuples(AsList(F),3),x->not IsZero(x));
 vecs:=Set(List(raw,x->x/First(x,y->y<>Zero(F))));
 blocks:=Set(List(vecs,n->Filtered([1..21],i->Sum([1..3],j->n[j]*vecs[i][j])=Zero(F))));
 P186Require(Length(vecs)=21 and Length(blocks)=21,"plane size");
 P186Require(Set(List(blocks,Length))=[5],"plane line size");
 normal:=function(v,m) local w;w:=v*m;return w/First(w,x->x<>Zero(F));end;
 linear:=Action(SL(3,4),vecs,normal);
 semilinear:=Group(Concatenation(GeneratorsOfGroup(Action(GL(3,4),vecs,normal)),[PermList(List(vecs,v->Position(vecs,List(v,x->x^2))))]));
 P186Require(Size(linear)=20160 and Size(semilinear)=120960,"coordinate collineation groups");
 return rec(vectors:=vecs,codes:=List(vecs,x->List(x,a->Position([Zero(F),One(F),Z(4),Z(4)^2],a)-1)),blocks:=blocks,design:=BlockDesign(21,blocks),linear:=linear,semilinear:=semilinear);
end;;
P186Stabilizers:=function(v,t,k,G,blocks,plane)
 local B,H,hom,N,C,complements,T,M,MC,Q,Z,j,R,rem,db,target,
       iso,pm,J,img,pointwise,pi,labels,expected,outer;
 B:=blocks[1];H:=Stabilizer(G,B,OnSets);
 hom:=ActionHomomorphism(H,B,OnPoints);N:=Kernel(hom);
 P186Require(Size(N)=16 and IsElementaryAbelian(N),"block kernel is not 2^4");
 P186Require(Image(hom)=AlternatingGroup(k),"block action not A_k");
 complements:=ComplementClassesRepresentatives(H,N);
 P186Require(Length(complements)>0,"no complement to block kernel");C:=complements[1];
 P186Require(Size(Intersection(C,N))=1 and Size(C)*Size(N)=Size(H),"bad block complement");
 T:=B{[1..t-1]};M:=Stabilizer(H,T,OnSets);MC:=Stabilizer(C,T,OnSets);
 P186Require(Size(Intersection(MC,N))=1 and Size(MC)*16=Size(M),"marked split failure");
 P186Require(Image(hom,M)=Stabilizer(AlternatingGroup(k),[1..t-1],OnSets),"marked alternating subset action");
 if v=22 then
  Q:=PCore(M,2);Z:=Centre(Q);
  P186Require(Size(Q)=64 and Size(Z)=4 and IsElementaryAbelian(Z),"M22 marked central 2^2");
  P186Require(IsElementaryAbelian(FactorGroup(Q,Z)),"M22 marked central quotient not 2^4");
  P186Require(IsomorphismGroups(FactorGroup(M,Q),SymmetricGroup(3))<>fail,"M22 marked quotient not S3");
  P186Require(Length(ComplementClassesRepresentatives(M,Q))>0,"M22 marked outer split");
 fi;
 labels:=[];
 for j in [1..t-2] do
  R:=[1..j];rem:=Difference([1..v],R);
  db:=Set(List(Filtered(blocks,B->IsSubset(B,R)),B->List(Difference(B,R),x->Position(rem,x))));
  if j=t-2 then target:=rec(design:=plane.design,native:=plane.linear,full:=plane.semilinear);
  else target:=P186Models.(String(v-j));fi;
  iso:=GraphIsomorphism(
   rec(graph:=IncidenceGraphSupportBlockDesign(BlockDesign(v-j,db)),colourClasses:=[[1..v-j],[v-j+1..v-j+Length(db)]]),
   rec(graph:=IncidenceGraphSupportBlockDesign(target.design),colourClasses:=[[1..v-j],[v-j+1..v-j+Length(db)]]));
  P186Require(iso<>fail,"ordinary derived model not isomorphic");
  pm:=PermList(List([1..v-j],i->i^iso));
  P186Require(Set(List(db,B->OnSets(B,pm)))=Set(target.design.blocks),"ordinary map block check");
  J:=Stabilizer(G,R,OnSets);pi:=ActionHomomorphism(J,rem,OnPoints);
  P186Require(Size(Kernel(pi))=1,"ordinary residual action has kernel");img:=Image(pi)^pm;
  pointwise:=Stabilizer(G,R,OnTuples);
  P186Require(Image(pi,pointwise)^pm=target.native,"pointwise ordinary action not native group");
  if j=1 then P186Require(img=target.native,"point ordinary stabilizer");
  elif j=t-2 then
   P186Require(IsSubgroup(target.full,img) and Size(img)=20160*Factorial(j),"projective ordinary outer group");
   if j=2 then
    outer:=FactorGroup(img,target.native);
    P186Require(Size(outer)=2 and Length(ComplementClassesRepresentatives(img,target.native))>0,"projective index-two extension not split");
   else P186Require(img=target.full,"full projective semilinear action");fi;
  else P186Require(img=target.full,"ordinary full derived action");fi;
  Add(labels,rec(j:=j,order:=Size(J),point_map:=List([1..v-j],i->i^pm)));
 od;
 Print("P186_FIGURE3_STABILIZERS ",rec(v:=v,block_order:=Size(H),block_kernel_order:=Size(N),block_complement_order:=Size(C),marked_order:=Size(M),marked_complement_order:=Size(MC),ordinary:=labels),"\n");
 AppendTo(P186_OUTPUT,",\"block_order\":",Size(H),",\"block_kernel_order\":",Size(N),",\"block_complement_order\":",Size(C),",\"marked_order\":",Size(M),",\"marked_complement_order\":",Size(MC),",\"ordinary_orders\":",List(labels,x->x.order),",\"ordinary_point_maps\":",List(labels,x->x.point_map),",\"block_kernel_generators\":",List(GeneratorsOfGroup(N),g->List([1..v],i->i^g)),",\"block_complement_generators\":",List(GeneratorsOfGroup(C),g->List([1..v],i->i^g)));
end;;
P186Run:=function(v,t,k,plane)
 local G,A,H,orbs,small,seed,blocks,expected,allorbs,design,full,
       R,remaining,derived,ddesign,iso,pmap,mapped,B,g,counts,record,orbit_sizes;
 G:=MathieuGroup(v);A:=[1..t];expected:=Binomial(v,t)/Binomial(k,t);
 if v<20 then
  allorbs:=OrbitsDomain(G,Combinations([1..v],k),OnSets);
  small:=Filtered(allorbs,o->Length(o)=expected);
  P186Require(Length(small)=1,"small Witt orbit not unique");
  P186Require(ForAll(allorbs,o->Length(o)>=expected),"possible mixed block orbit");
  orbit_sizes:=SortedList(List(allorbs,Length));
  blocks:=Set(small[1]);
 else
  H:=Stabilizer(G,A,OnTuples);orbs:=Orbits(H,Difference([1..v],A));
  small:=Filtered(orbs,o->Length(o)=k-t);
  P186Require(Length(small)=1 and ForAll(orbs,o->Length(o)>=k-t),"large seed not unique");
  orbit_sizes:=SortedList(List(orbs,Length));
  seed:=Union(A,small[1]);blocks:=Set(Orbit(G,seed,OnSets));
 fi;
 P186Require(Length(blocks)=expected,"block count");
 counts:=List(Combinations([1..v],t),X->Number(blocks,B->IsSubset(B,X)));
 P186Require(Set(counts)=[1],"not a Steiner design");
 # Canonical group identification is a retained GAP-library input. The full
 # design automorphism computation itself is performed afresh by DESIGN.
 design:=BlockDesign(v,blocks);full:=AutGroupBlockDesign(design);
 P186Require(IsSubgroup(full,G),"native group not in full group");
 for g in GeneratorsOfGroup(full) do
  P186Require(Set(List(blocks,B->OnSets(B,g)))=blocks,"bad full-group generator");
 od;
 if v=22 then
  P186Require(Size(full)=2*Size(G),"M22 full group order");
  P186Require(Length(ComplementClassesRepresentatives(full,G))>0,"M22 full index-two extension not split");
 else P186Require(full=G,"full group differs from native Mathieu group");fi;
 P186Models.(String(v)):=rec(design:=design,native:=G,full:=full);
 Print("P186_FULL_AUT ",rec(v:=v,t:=t,k:=k,blocks:=Length(blocks),tested_subsets:=Length(counts),native_order:=Size(G),full_order:=Size(full)),"\n");
 if v<>11 then AppendTo(P186_OUTPUT,",\n");fi;
 AppendTo(P186_OUTPUT,"{\"v\":",v,",\"t\":",t,",\"k\":",k,",\"blocks\":",blocks,",\"orbit_sizes\":",orbit_sizes,",\"native_order\":",Size(G),",\"full_order\":",Size(full),",\"native_generators\":",List(GeneratorsOfGroup(G),g->List([1..v],i->i^g)),",\"full_generators\":",List(GeneratorsOfGroup(full),g->List([1..v],i->i^g)));
 if v>20 then
  R:=[1..t-2];remaining:=Difference([1..v],R);
  derived:=Set(List(Filtered(blocks,B->IsSubset(B,R)),B->List(Difference(B,R),p->Position(remaining,p))));
  P186Require(Length(remaining)=21 and Length(derived)=21,"derived sizes");
  ddesign:=BlockDesign(21,derived);
  iso:=GraphIsomorphism(
   rec(graph:=IncidenceGraphSupportBlockDesign(ddesign),colourClasses:=[[1..21],[22..42]]),
   rec(graph:=IncidenceGraphSupportBlockDesign(plane.design),colourClasses:=[[1..21],[22..42]]));
  P186Require(iso<>fail,"derived design is not PG(2,4)");
  pmap:=List([1..21],i->i^iso);
  P186Require(Set(pmap)=[1..21],"not a point bijection");
  mapped:=Set(List(derived,B->Set(List(B,i->pmap[i]))));
  P186Require(mapped=plane.blocks,"explicit incidence map failure");
  # Check every one of the 441 point/line incidences, including non-incidences.
  P186Require(ForAll(derived,B->ForAll([1..21],i->(i in B)=(pmap[i] in plane.blocks[Position(plane.blocks,Set(List(B,j->pmap[j])))]))),"incidence equivalence");
  Print("P186_DERIVED_PLANE ",rec(v:=v,derived_at:=R,remaining_points:=remaining,point_map:=pmap,derived_blocks:=derived,target_blocks:=plane.blocks),"\n");
  AppendTo(P186_OUTPUT,",\"derived_at\":[",JoinStringsWithSeparator(List(R,String),","),"],\"remaining_points\":",remaining,",\"point_map\":",pmap,",\"derived_blocks\":",derived);
  P186Stabilizers(v,t,k,G,blocks,plane);
 fi;
 AppendTo(P186_OUTPUT,"}");
 Print("P186_WITT_MODEL ",rec(v:=v,blocks:=blocks,generators:=GeneratorsOfGroup(G),full_generators:=GeneratorsOfGroup(full)),"\n");
end;;
P186PG:=P186Plane();;
PrintTo(P186_OUTPUT,"{\"gap_version\":\"",GAPInfo.Version,"\",\"design_version\":\"",PackageInfo("design")[1].Version,"\",\"grape_version\":\"",PackageInfo("grape")[1].Version,"\",\"field_polynomial\":\"z^2+z+1\",\"plane_vectors\":",P186PG.codes,",\"plane_blocks\":",P186PG.blocks,",\"cases\":[\n");
Print("P186_PG4_VECTORS ",P186PG.vectors,"\n");
P186Run(11,4,5,P186PG);
P186Run(12,5,6,P186PG);
P186Run(22,3,6,P186PG);
P186Run(23,4,7,P186PG);
P186Run(24,5,8,P186PG);
AppendTo(P186_OUTPUT,"\n],\"projective_labels\":{\"v\":21");
P186Stabilizers(21,2,5,P186PG.linear,P186PG.blocks,P186PG);
AppendTo(P186_OUTPUT,"}}\n");
Print("P186_WITT_DERIVED_AND_FULL_AUT_PASS\n");
QUIT;
