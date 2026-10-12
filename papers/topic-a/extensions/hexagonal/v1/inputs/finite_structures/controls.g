# Run after loading shape_engine.g. These check genuine structural distinctions.
Must:=function(b,label) Assert(0,b);Print("CONTROL ",label,"\n");end;;
C:=n->["atom",["cyclic",n]];;
TestE:=function(p,n) return ["atom",["elementary",p,n]]; end;;
A:=n->["atom",["A",n]];;
S:=n->["atom",["S",n]];;
Q:=QuaternionGroup(IsPermGroup,8);;
Must(FindShape(Q,["colon",C(4),C(2)])=fail,"nonsplit_Q8_is_not_C4_semidirect_C2");;
Must(FindShape(Q,["dot",C(4),C(2)])<>fail,"Q8_has_nonsplit_extension_shape");;
Must(FindShape(AlternatingGroup(4),["direct",TestE(2,2),C(3)])=fail,"A4_is_not_V4_direct_C3");;
Must(FindShape(AlternatingGroup(4),["colon",TestE(2,2),C(3)])<>fail,"A4_split_positive_control");;
Must(FindShape(ElementaryAbelianGroup(IsPermGroup,8),["atom",["special",2,1,2]])=fail,"elementary8_is_not_extraspecial8");;
Must(FindShape(CyclicGroup(IsPermGroup,9),TestE(3,2))=fail,"cyclic9_is_not_elementary9");;
Must(FindShape(DihedralGroup(IsPermGroup,8),["atom",["Q8"]])=fail,"dihedral8_is_not_quaternion8");;
Must(FindShape(SymmetricGroup(3),["colon",C(3),C(2)])<>fail,"S3_split_positive_control");;
Must(FindShape(CyclicGroup(IsPermGroup,6),S(3))=fail,"cyclic6_is_not_S3");;
Print("PASS_NINE_STRUCTURAL_CONTROLS\n");;QUIT;
