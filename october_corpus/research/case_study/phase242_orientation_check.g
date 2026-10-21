# Independent native-GAP reconstruction: D8 on four directions, no author generator input.
Need:=function(ok,label) if not ok then Error(label);fi;end;;
lin:=[(1,3),(1,2)(3,4),(2,4)];;L:=Group(lin);;els:=Elements(L);;
Need(Size(L)=8,"eight directions symmetries");;
idpos:=Position(els,());;
node:=function(k,x)return 8*k+Position(els,x);end;;
s:=[];;
for i in [0..3] do
 p:=[];
 for k in [0..4] do
  for x in els do
   if k=3-i then h:=k+1;y:=x;
   elif k=4-i then h:=k-1;y:=x;
   elif k<3-i then h:=k;y:=x*lin[i+1];
   else h:=k;y:=x*lin[i];fi;
   Add(p,node(h,y));
  od;
 od;
 Add(s,PermList(p));
od;
Orient:=Group(s);;A:=Group(s{[1,2,3]});;B:=Group(s{[2,3,4]});;
C:=Group(s{[2,3]});;T:=Intersection(A,B);;
# The only direction symmetries fixing the northeast diagonal are 1 and swap.
allowed:=[(),lin[2]];;
Jels:=Filtered(Elements(T),x->ForAll([1..3],k->els[((node(k,())^x)-1) mod 8+1] in allowed));;
J:=Group(Jels);;Need(Size(J)=Length(Jels),"constraint subgroup");;
d:=[(1,3)(2,4),(3,5)(4,6)(7,8)(9,10),(5,7)(6,8)(9,10),(1,2)(3,4)(5,6)(7,9)(8,10)];;
D:=Group(d);;pi:=GroupHomomorphismByImages(Orient,D,s,d);;
Need(pi<>fail and Image(pi)=D,"checked orientation-to-D map");;N:=Kernel(pi);;
Need(List([Orient,A,B,C,T,J,D,N],Size)=[61440,12288,12288,24,3072,48,3840,16],"all native orders");;
Need(IsSubgroup(J,C) and Intersection(N,J)=Intersection(N,C) and Size(Intersection(N,C))=2,"fixed intersection transport");;
Need(not IsSubgroup(C,Intersection(N,T)),"false weakening caught");;
# Standalone integrality and support check: every local facet isometry fixes h,
# and its shift components belong to {0,1}; this is not a field-order sample.
Print("PHASE242_NATIVE_ORIENTATION_PASS ",List([Orient,A,B,C,T,J,D,N,Intersection(N,J),Intersection(N,T)],Size),"\n");
Print("NO_CENTER_CONSTRAINT_REJECTED\n");
QUIT_GAP(0);
