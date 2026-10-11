# An affine frame-transitive semilinear group need not contain GL(2,q).
# This is an exact finite source-clause diagnostic, not the uniform proof.
Need := function(b,s) if not b then Error(s); fi; end;
F:=GF(9); z:=Z(9); o:=One(F); zero:=Zero(F);
V:=Tuples(Elements(F),2);
ToPerm:=function(A,e)
 return PermList(List(V,v->Position(V,List(v,x->x^(3^e))*A)));
end;
I:=IdentityMat(2,F);
slm:=GeneratorsOfGroup(SL(2,9));
slp:=List(slm,A->ToPerm(A,0));
squares:=ToPerm([[z^2,zero],[zero,o]],0);
twist:=ToPerm([[z,zero],[zero,o]],1);
H:=Group(Concatenation(slp,[squares,twist]));
SLP:=Group(slp); GLP:=Group(List(GeneratorsOfGroup(GL(2,9)),A->ToPerm(A,0)));
Need(Size(SLP)=720,"SL order");
Need(Size(H)=5760 and Size(GLP)=5760,"equal frame-group orders");
Need(IsSubgroup(H,SLP),"SL inclusion");
Need(not IsSubgroup(H,GLP),"literal GL containment fails");
frame:=[Position(V,[o,zero]),Position(V,[zero,o])];
Need(Size(Stabilizer(H,frame,OnTuples))=1,"regular frame action");
Need(Length(Orbit(H,frame,OnTuples))=5760,"all independent frames");
translations:=List([[o,zero],[zero,o],[z,zero],[zero,z]],
 w->PermList(List(V,v->Position(V,v+w))));
G:=Group(Concatenation(GeneratorsOfGroup(H),translations));
Need(Size(G)=466560,"affine group order");
origin:=Position(V,[zero,zero]);
Need(Size(Stabilizer(G,Concatenation([origin],frame),OnTuples))=1,"triangle stabilizer");
Need(Size(G)=81*80*72,"full ordered triangle orbit size");
lines:=Set(Concatenation(List(V,v->List(Filtered(V,w->w<>[zero,zero]),
 w->Set(List(Elements(F),a->Position(V,v+a*w)))))));
Need(Length(lines)=90,"affine line count");
Need(ForAll(GeneratorsOfGroup(G),g->ForAll(lines,L->OnSets(L,g) in lines)),"literal line preservation");
Need(15*14*13>Size(AlternatingGroup(7)),"A7 cannot be 3-transitive on15 points");
# Removing the SL-fiber hypothesis makes determinant transitivity insufficient.
F3:=GF(3);e3:=One(F3);z3:=Zero(F3);V3:=Tuples(Elements(F3),2);
diag3:=Group(List([[[ -e3,z3],[z3,e3]],[[e3,z3],[z3,-e3]]],
 A->PermList(List(V3,v->Position(V3,v*A)))));
frame3:=[Position(V3,[e3,z3]),Position(V3,[z3,e3])];
Need(Size(diag3)=4 and Length(Orbit(diag3,frame3,OnTuples))=4 and 4<48,"determinant-only weakening rejected");
Print("PHASE265_NO_SL_CONTROL_PASS determinant_image2 frame_orbit4_not48\n");
Print("PHASE265_FRAME_CONTROL_PASS H5760 G466560 lines90 full_triangle_orbit GL_not_contained A7_degree15_excluded\n");
QUIT;
