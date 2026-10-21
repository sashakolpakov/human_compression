# The single required finite presentation identification, extracted from the
# accepted Topic E universal row [4,3,3]/[3,4,3]. Optional finite validations
# are in separate complete programs, not premises of the uniform proof.
Need:=function(b,m) if not b then Error(m);fi;end;
Vects:=Tuples([0,1],4);
PermOf:=f->PermList(List(Vects,v->Position(Vects,f(v))));
r0:=PermOf(v->[(v[1]+1)mod 2,v[2],v[3],v[4]]);
r1:=PermOf(v->[v[1],(v[1]+v[2])mod 2,v[3],(v[3]+v[4])mod 2]);
r2:=PermOf(v->[(v[1]+v[2])mod 2,v[2],(v[3]+v[4])mod 2,v[4]]);
r3:=PermOf(v->[v[1],v[2],v[3],(v[4]+1)mod 2]);
rr:=[r0,r1,r2,r3];G:=Group(rr);Need(Size(G)=96,"explicit base order");
F:=FreeGroup(4);x:=GeneratorsOfGroup(F);
rels:=Concatenation(List(x,a->a^2),[(x[1]*x[2])^4,(x[2]*x[3])^3,
 (x[3]*x[4])^4,(x[1]*x[3])^2,(x[1]*x[4])^2,(x[2]*x[4])^2,
 (x[1]*x[2]*x[3])^3,(x[2]*x[3]*x[4])^3]);
U:=F/rels;Need(Size(U)=96,"exact retained universal presentation");
h:=GroupHomomorphismByImages(U,G,GeneratorsOfGroup(U),rr);
Need(h<>fail and IsBijective(h),"actual marked source identification");
Print("SOURCE_BASE96_MARKED_IDENTIFICATION_PASS\n");
