Read("pyramid_flags.g");;
Need:=function(ok,label)
 if not ok then Print("FAIL ",label,"\n");QUIT_GAP(1);fi;
end;;
G:=Group(s);;Need(Size(G)=3627970560,"literal monodromy order");;
A:=Group(s{[1,2,3]});;B:=Group(s{[2,3,4]});;C:=Group(s{[2,3]});;T:=Intersection(A,B);;
Need(List([A,B,C,T],Size)=[110592,110592,24,48],"parabolic orders");;
Need(Intersection(Group(s{[1,2]}),C)=Group(s[2]),"left end intersection");;
Need(Intersection(C,Group(s{[3,4]}))=Group(s[3]),"right end intersection");;
d:=List([[3,4,1,2,5,6,7,8,9,10],[1,2,5,6,3,4,8,7,10,9],
 [1,2,3,4,7,8,5,6,10,9],[2,1,4,3,6,5,9,10,7,8]],PermList);;
D:=Group(d);;Need(Size(D)=3840,"explicit quotient order");;
pi:=GroupHomomorphismByImages(G,D,s,d);;Need(pi<>fail,"marked map is a homomorphism");;
Need(Image(pi)=D,"marked quotient surjectivity");;
N:=Kernel(pi);;Need(Size(N)=944784,"actual quotient kernel order");;
NT:=Intersection(N,T);;NC:=Intersection(N,C);;
Need(IsSubgroup(C,NT) and NT=NC and Size(NC)=2,"defect-preserving kernel condition");;
# Negative control: an overgroup of the kernel killing a genuine defect.
kappa:=First(Elements(T),x->not x in C);;
Nbad:=NormalClosure(G,ClosureGroup(N,kappa));;
Need(not IsSubgroup(C,Intersection(Nbad,T)),"control must reject lost defect");;
Print("{\"status\":\"PASS\",\"G_order\":",Size(G),",\"end_orders\":[",Size(A),",",Size(B),"],\"middle_order\":",Size(C),",\"top_intersection_order\":",Size(T),",\"D_order\":",Size(D),",\"kernel_order\":",Size(N),",\"kernel_top_intersection\":",Size(NT),",\"kernel_middle_intersection\":",Size(NC),",\"negative_kernel_order\":",Size(Nbad),",\"negative_kernel_top_intersection\":",Size(Intersection(Nbad,T)),",\"negative_kernel_middle_intersection\":",Size(Intersection(Nbad,C)),",\"D_generators\":",List(d,x->List([1..10],i->i^x)),",\"gap_version\":\"",GAPInfo.Version,"\"}\n");
QUIT_GAP(0);
