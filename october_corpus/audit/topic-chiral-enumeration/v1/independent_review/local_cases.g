# Independent rotation-coordinate test: no author Python implementation imported.
Need := function(b,s) if not b then Error("INDEPENDENT_REJECT ",s); fi; end;;
d := 0;;
for p in [5,7,11] do
  tr := PermList(List([0..p-1], x -> ((x+1) mod p)+1));;
  d := First([2..p-1], x -> Order(ZmodpZObj(x,p))=p-1);;
  sc := PermList(List([0..p-1], x -> ((d*x) mod p)+1));;
  G := Group(tr,sc);; A := AutomorphismGroup(G);;
  nr := 0;; regular := 0;; types := [];;
  for s in Elements(G) do
    if Order(s)>2 then
      for t in Elements(G) do
        if Order(t)>2 and Order(s*t)=2 and Group(s,t)=G then
          cs := Group(s);; ct := Group(t);; cu := Group(s*t);;
          if Size(Intersection(cs,ct))=1 and Size(Intersection(cs,cu))=1 and Size(Intersection(ct,cu))=1 then
            nr := nr+1;; AddSet(types,[Order(s),Order(t)]);;
            f := GroupHomomorphismByImages(G,G,[s,t],[s^-1,s^2*t]);;
            if f<>fail then regular:=regular+1; fi;
          fi;
        fi;
      od;
    fi;
  od;
  expected := [2,4,8][Position([5,7,11],p)];;
  Need(Size(G)=p*(p-1),"full affine group");;
  Need(nr/Size(A)=expected,"independent oriented census");;
  Need(nr/(2*Size(A))=expected/2,"independent mirror quotient");;
  Need(regular=0,"no classical reflection automorphism");;
  Print("INDEPENDENT_AFFINE ",p," order ",Size(G)," aut ",Size(A)," raw ",nr," oriented ",nr/Size(A)," unrooted ",nr/(2*Size(A))," types ",types,"\n");
od;
# Source final regular-output qualification: verify the literal hemi-icosahedral
# involutions independently and then their rotation data.
# Use explicit source-application markers with its zero-based points shifted by 1.
r0:=(2,4)(3,5);;r1:=(1,4)(3,5);;r2:=(2,5)(3,4);;
G:=Group(r0,r1,r2);;r:=[r0,r1,r2];;
P:=List(Combinations([1..3]),I->Group(Concatenation([One(G)],r{I})));;
sets:=Combinations([1..3]);;
for i in [1..8] do for j in [1..8] do
 Need(Intersection(P[i],P[j])=P[Position(sets,Intersection(sets[i],sets[j]))],"literal hemi IP");
od;od;
Need(Size(G)=60 and Order(r0*r1)=3 and Order(r1*r2)=5,"hemi size and type");;
Need(Group(r0*r1,r1*r2)=G,"full even subgroup in nonorientable example");;
Print("INDEPENDENT_NONORIENTABLE 60 120 PASS\n");
Print("INDEPENDENT_ALL_PASS\n");
QUIT;
