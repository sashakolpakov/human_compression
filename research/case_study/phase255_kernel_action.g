# Independent check of the kernel-line classification by conjugation action.
# HMarks and GMarks are the actual regenerated permutations, supplied literally.
Check255:=function(b,s)
 if not b then Print("PHASE255_REJECT ",s,"\n");QUIT_GAP(2);fi;
end;;
H:=Group(HMarks);;G:=Group(GMarks);;
pi:=GroupHomomorphismByImages(H,G,HMarks,GMarks);;
Check255(pi<>fail and Image(pi)=G,"marked epimorphism");;
N:=Kernel(pi);;
Check255(Size(H)=73728 and Size(G)=18432 and Size(N)=4 and IsElementaryAbelian(N),"group and kernel orders");;
nonidentity:=Filtered(Elements(N),x->x<>One(H));;
actions:=List(HMarks,h->Permutation(h,nonidentity,OnPoints));;
fixed:=Filtered(nonidentity,x->ForAll(HMarks,h->x^h=x));;
Check255(Size(Group(actions))=2 and Length(fixed)=1,"exact conjugation action on the three kernel lines");;
centralLine:=Group(fixed);;
HA:=Subgroup(H,HMarks{[1,2,3]});;HB:=Subgroup(H,HMarks{[2,3,4]});;
GA:=Subgroup(G,GMarks{[1,2,3]});;GB:=Subgroup(G,GMarks{[2,3,4]});;
GC:=Subgroup(G,GMarks{[2,3]});;GD:=Intersection(GA,GB);;
Check255(Size(HA)=Size(GA) and Size(HB)=Size(GB),"faithful ends");;
Check255(Size(HA)=576 and Size(HB)=1152 and Size(GC)=24 and Size(GD)=48,"literal end and defect data");;
defects:=Set(List(Filtered(Elements(GD),x->not x in GC),g->
 PreImagesRepresentative(RestrictedMapping(pi,HA),g)*
 PreImagesRepresentative(RestrictedMapping(pi,HB),g)^-1));;
Check255(Length(defects)=1 and ForAll(defects,x->x in N and not x in centralLine),"all 24 outside-middle elements give the same surviving discrepancy");;
Check255(Size(Intersection(N,Center(H)))=2,"central kernel line");;
Print("PHASE255_PASS group=",Size(H)," base=",Size(G)," kernel=",AbelianInvariants(N),
 " conjugation_action=",Size(Group(actions))," fixed_nonzero=",Length(fixed),
 " noncentral_discrepancies=",Length(defects)," unique_C_quotient_order=",Size(H)/Size(centralLine),"\n");
QUIT_GAP(0);
