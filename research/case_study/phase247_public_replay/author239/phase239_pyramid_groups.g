SizeScreen([1000000,1000000]);;
Read("orientation_input.g");;
Need:=function(ok,label)
 if not ok then Print("FAIL ",label,"\n");QUIT_GAP(1);fi;
end;;
Q:=Group(s);; A:=Group(s{[1,2,3]});; B:=Group(s{[2,3,4]});;
C:=Group(s{[2,3]});; T:=Intersection(A,B);;
Need(List([Q,A,B,C,T],Size)=[61440,12288,12288,24,3072],"orientation parabolics");;
possible:=Filtered(Elements(T),x->ForAll(middlePoints,b->b^x in allowedImages));;
J:=Group(possible);;
Need(Size(J)=Length(possible),"constraints themselves form a subgroup");;
Need(Size(J)=48 and IsSubgroup(J,C),"bounded top intersection and middle");;
D:=Group(d);; pi:=GroupHomomorphismByImages(Q,D,s,d);;
Need(pi<>fail and Image(pi)=D,"actual marked orientation quotient");;
N:=Kernel(pi);; NJ:=Intersection(N,J);; NC:=Intersection(N,C);;
Need(Size(D)=3840 and Size(N)=16,"fixed quotient and kernel");;
Need(NJ=NC and Size(NC)=2,"uniform defect-preserving kernel");;
# Removing the middle-layer constraints admits precisely the hidden defects
# that the integer affine argument must exclude.
NT:=Intersection(N,T);;
Need(not IsSubgroup(C,NT),"control without center constraints must fail");;
Print("{\"status\":\"PASS\",\"orders\":",List([Q,A,B,C,T,J,D,N,NJ,NC,NT],Size),
 ",\"possible_elements\":",Length(possible),",\"constraint_set_is_subgroup\":true,",
 "\"kernel_intersection_equality\":true,\"missing_center_control\":\"REJECTED\",",
 "\"D_generators\":",List(d,x->List([1..10],i->i^x)),
 ",\"gap_version\":\"",GAPInfo.Version,"\"}\n");
QUIT_GAP(0);
