named_direct_records:=[];;named_series_records:=[];;named_dot_record:=rec();;linear_bridge:=rec();;
P:="/Users/sasha/medusa/research/leemans/corpus106_L033_hyperbolic_names_v1";;
Read(Concatenation(P,"/direct.g"));;Read(Concatenation(P,"/series.g"));;Read(Concatenation(P,"/dot.g"));;
Need:=function(b,msg)if not b then Error(msg);fi;end;;
# Independent enumeration of every invertible binary 3x3 map, without GL().
vectors:=Tuples([0,1],3);;maps:=[];;matrix:=[];;elements:=[];;N:=Group(());;
for bits in Tuples([0,1],9)do
 matrix:=List([1..3],i->bits{[3*i-2..3*i]});;
 images:=List(vectors,v->Position(vectors,List([1..3],j->Sum([1..3],i->v[i]*matrix[i][j])mod 2)));;
 if Length(Set(images))=8 then Add(maps,PermList(images));fi;
od;
L:=Group(linear_bridge.domain);;Need(Length(maps)=168 and Set(Elements(L))=Set(maps),"complete binary linear action");;
translations:=List(vectors,a->PermList(List(vectors,v->Position(vectors,List([1..3],i->(v[i]+a[i])mod 2)))));;
T:=Group(translations);;F:=Group(Concatenation(GeneratorsOfGroup(T),GeneratorsOfGroup(L)));;
Need(Size(T)=8 and IsRegular(T,[1..8]) and IsElementaryAbelian(T),"regular translations");;
Need(Size(F)=1344 and IsNormal(F,T) and Size(Intersection(T,L))=1,"actual affine decomposition");;
f:=GroupHomomorphismByImages(L,PSL(2,7),linear_bridge.domain,linear_bridge.images);;Need(f<>fail and IsBijective(f),"literal L7 bridge");;
Print("BINARY_LINEAR_MAPS 512 168 8 1344\n");
# Check all element squares for all twelve kernels; explicit products for extraspecial row.
count:=0;;elementtests:=0;;
for row in named_series_records do
 N:=Group(row.kernel);;elements:=Elements(N);;Need(Length(elements)=row.kernel_order,"kernel elements");;
 if row.name="extra32_S3_S3"then
  central:=Filtered(elements,x->ForAll(elements,y->x*y=y*x));;
  comms:=List(Cartesian(elements,elements),p->p[1]^-1*p[2]^-1*p[1]*p[2]);;
  sq:=Group(List(elements,x->x*x));;commgroup:=Group(comms);;centerGroup:=Group(central);;
  Need(Length(central)=2 and commgroup=centerGroup and IsSubgroup(centerGroup,sq),"literal extraspecial products");;
  Need(Size(N/centerGroup)=16 and IsElementaryAbelian(N/centerGroup),"extraspecial elementary quotient");;
  Print("EXTRASPECIAL_ALL_PRODUCTS ",Length(comms)," ",Size(centerGroup)," ",Size(sq),"\n");
 else
  Need(ForAll(elements,x->x*x=One(N)),"every kernel element has exponent two");;
 fi;
 count:=count+1;;elementtests:=elementtests+Length(elements);;
od;
Need(count=12,"twelve series kernels");;
# Construct the central row's actual quotient, rather than only its generator tests.
r:=named_dot_record;;D:=Group(r.base);;C:=Group(r.central_kernel);;N:=Group(r.preimage_kernel);;U:=Group(r.quotient_complement_lifts);;
Need(Size(D)=3840 and Size(C)=4 and IsCyclic(C)and IsSubgroup(Centre(D),C),"central C4");;
projection:=NaturalHomomorphismByNormalSubgroup(D,C);;Q:=Image(projection);;QN:=Image(projection,N);;QU:=Image(projection,U);;
Need(Size(Q)=960 and Size(QN)=16 and IsElementaryAbelian(QN)and IsNormal(Q,QN),"actual E16 quotient");;
Need(Size(QU)=60 and Size(Intersection(QN,QU))=1 and ClosureGroup(QN,QU)=Q,"quotient complement");;
f:=GroupHomomorphismByImages(QU,AlternatingGroup(5),List(r.quotient_complement_lifts,x->Image(projection,x)),r.A5_images);;
Need(f<>fail and IsBijective(f),"quotient A5 explicit isomorphism");;
common:=Intersection(C,DerivedSubgroup(D));;Need(Size(common)>1,"nonsplit derived obstruction");;
Print("CENTRAL_QUOTIENT ",Size(Q)," ",Size(QN)," ",Size(QU)," ",Size(common),"\n");
# Both normal L16 inclusions have faithful, hence genuinely outer, index-two action.
faithful:=0;;
for r in named_direct_records do
 if r.name="PSL2_16_split_C2"then
  D:=Group(r.domain);;H:=Group(Concatenation(r.domain,[r.outside_involution]));;
  action:=ConjugatorAutomorphism(H,r.outside_involution);;
  Need(Size(D)=4080 and Size(H)=8160 and IsNormal(H,D)and Size(Centralizer(H,D))=1,"faithful outer L16 action");;
  Need(not r.outside_involution in D,"outside genuinely different coset");;
  faithful:=faithful+1;;
 fi;
od;
Need(faithful=2,"two faithful rows");;
Print("PASS_INDEPENDENT_GROUP_CERTIFICATES 512 168 ",elementtests," 1024 960 2\n");
QUIT;
