VerifyNamed:=function(core,data,bad)
 local V,lin,aff,g,gens,i,e,bridge,models,r,row,H,D,M,f,N,K,C,U,z,t,expected,seen,iso;
 Read(Concatenation(data,"/direct.g"));Read(Concatenation(data,"/series.g"));Read(Concatenation(data,"/dot.g"));
 if bad=1 then named_direct_records[1].images[1]:=();fi;
 if bad=2 then named_series_records[1].kernel:=[()];fi;
 if bad=3 then named_series_records[6].outer:=[()];fi;
 if bad=4 then named_dot_record.central_kernel:=[named_dot_record.central_kernel[1]^2];fi;
 if bad=5 then linear_bridge.images:=List(linear_bridge.images,g->());fi;
 V:=Tuples(GF(2),3);lin:=Group(List(GeneratorsOfGroup(GL(3,2)),g->PermList(List(V,v->Position(V,v*g)))));
 if Group(linear_bridge.domain)<>lin then Error("linear bridge domain");fi;
 bridge:=GroupHomomorphismByImages(lin,PSL(2,7),linear_bridge.domain,linear_bridge.images);if bridge=fail or not IsBijective(bridge)then Error("linear bridge isomorphism");fi;
 gens:=ShallowCopy(GeneratorsOfGroup(lin));for i in [1..3]do e:=List([1..3],j->Zero(GF(2)));e[i]:=One(GF(2));Add(gens,PermList(List(V,v->Position(V,v+e))));od;aff:=Group(gens);if Size(aff)<>1344 then Error("affine exact order");fi;
 models:=rec(affine_GL3_2_times_C2:=DirectProduct(aff,Group((1,2))),S6_times_C2:=DirectProduct(SymmetricGroup(6),Group((1,2))),S6_times_S3:=DirectProduct(SymmetricGroup(6),SymmetricGroup(3)),affine_GL3_2_times_C2sq:=DirectProduct(aff,Group((1,2)),Group((1,2))),PSL2_7_times_S3sq:=DirectProduct(PSL(2,7),SymmetricGroup(3),SymmetricGroup(3)),A5sq_split_C2:=DirectProduct(AlternatingGroup(5),AlternatingGroup(5)),PSL2_16_split_C2:=PSL(2,16));seen:=[];
 for r in named_direct_records do
  Read(Concatenation(core,"/censuses/",r.type,"/records.g"));row:=First(hyperbolic_records,x->x.node=r.node);if row=fail then Error("core node");fi;H:=Group(List(row.permutations,PermList));M:=models.(r.name);D:=Group(r.domain);
  if Size(H)<>r.order or Group(r.model)<>M or not IsSubgroup(H,D)then Error("actual direct model");fi;
  f:=GroupHomomorphismByImages(D,M,r.domain,r.images);if f=fail or not IsBijective(f)then Error("direct model exact isomorphism");fi;
  if IsBound(r.outside_involution)then
   t:=r.outside_involution;if not t in H or Order(t)<>2 or t in D or not IsNormal(H,D)or Index(H,D)<>2 or Group(Concatenation(r.domain,[t]))<>H then Error("actual split index2");fi;
   if r.name="PSL2_16_split_C2"and Size(Centralizer(H,D))<>1 then Error("faithful PSL2 extension");fi;
  elif D<>H then Error("full direct group domain");fi;
  Add(seen,[r.type,r.node]);Print("DIRECT_VERIFIED ",r.type," ",r.node,"\n");
 od;
 for r in named_series_records do
  Read(Concatenation(core,"/censuses/",r.type,"/records.g"));row:=First(hyperbolic_records,x->x.node=r.node);if row=fail then Error("core node");fi;H:=Group(List(row.permutations,PermList));D:=Group(r.base);N:=Group(r.kernel);K:=Group(r.complement);
  if Size(H)<>r.order or not IsSubgroup(H,D)or not IsNormal(H,D)or not IsSubgroup(D,N)or not IsNormal(D,N)or Size(N)<>r.kernel_order or not IsSubgroup(D,K)or Size(Intersection(N,K))<>1 or Group(Concatenation(r.kernel,r.complement))<>D then Error("actual split kernel");fi;
  if r.name="extra32_S3_S3"then
   C:=Centre(N);if Size(C)<>2 or DerivedSubgroup(N)<>C or not ForAll(GeneratorsOfGroup(N),g->g^2 in C)then Error("extraspecial kernel");fi;
  elif not IsElementaryAbelian(N)then Error("elementary kernel");fi;
  if r.recipe="S5"then M:=SymmetricGroup(5);elif r.recipe="S3S3"then M:=DirectProduct(SymmetricGroup(3),SymmetricGroup(3));else M:=AlternatingGroup(5);fi;
  if Group(r.model)<>M then Error("literal complement model");fi;f:=GroupHomomorphismByImages(K,M,r.complement,r.images);if f=fail or not IsBijective(f)then Error("complement exact isomorphism");fi;
  U:=D;
  if IsBound(r.outer)then
   for t in r.outer do
    if not t in H or Order(t)<>2 or t in U then Error("split outer involution");fi;C:=Group(Concatenation(GeneratorsOfGroup(U),[t]));if not IsNormal(C,U)or Index(C,U)<>2 then Error("split index2 step");fi;U:=C;
   od;
  fi;
  if IsBound(r.central)then
   for z in r.central do
    if not z in Centre(H)or Order(z)<>2 or z in U then Error("direct central factor");fi;U:=Group(Concatenation(GeneratorsOfGroup(U),[z]));
   od;
  fi;
  if U<>H then Error("complete series group");fi;Add(seen,[r.type,r.node]);Print("SERIES_VERIFIED ",r.type," ",r.node,"\n");
 od;
 r:=named_dot_record;Read(Concatenation(core,"/censuses/3334/records.g"));row:=First(hyperbolic_records,x->x.node=r.node);H:=Group(List(row.permutations,PermList));D:=Group(r.base);C:=Group(r.central_kernel);N:=Group(r.preimage_kernel);U:=Group(r.quotient_complement_lifts);
 if not IsSubgroup(H,D)or not IsNormal(H,D)or Size(D)<>3840 or Index(H,D)<>2 or not IsSubgroup(Centre(D),C)or Size(C)<>4 or not IsCyclic(C)or Size(Intersection(C,DerivedSubgroup(D)))=1 then Error("central nonsplit obstruction");fi;
 if not IsNormal(D,N)or Size(N)<>64 or not IsSubgroup(N,C)or not ForAll(GeneratorsOfGroup(N),g->g^2 in C)or not ForAll(GeneratorsOfGroup(N),g->ForAll(GeneratorsOfGroup(N),z->Comm(g,z)in C))then Error("E16 quotient kernel");fi;
 f:=GroupHomomorphismByImages(U,AlternatingGroup(5),r.quotient_complement_lifts,r.A5_images);
 if f=fail or not IsSurjective(f)or Kernel(f)<>C or Intersection(N,U)<>C or Group(Concatenation(GeneratorsOfGroup(N),GeneratorsOfGroup(U)))<>D then Error("quotient split A5");fi;
 t:=r.outer;if not t in H or Order(t)<>2 or t in D or Group(Concatenation(r.base,[t]))<>H then Error("dot final split2");fi;Add(seen,[r.type,r.node]);
 expected:=[["3334",8],["3334",9],["3334",11],["3334",12],["3334",13],["3335",5],["3434",24],["3434",27],["3434",36],["3434",38],["3434",40],["3434",45],["353",5],["435",12],["435",14],["435",15],["435",16],["535",5],["535",6],["5333",14],["5333",19],["5333",20]];
 if Set(seen)<>Set(expected)or Length(seen)<>22 then Error("complete exact row inventory");fi;
 Print("COMPLETE_NAMED_VERIFICATION 22\n");
end;;
