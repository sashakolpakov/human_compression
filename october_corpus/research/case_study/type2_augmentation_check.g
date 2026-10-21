# Exact permutation certificates for the augmentation-module Type (2) family.
LogTo("research/leemans/type2_augmentation_check.log");
CheckType2 := function(p)
  local r,s,v,a,b,c,G,A,B,k,x,y,aa,bb,cc,H,AA,BB;
  r:=PermList(List([1..2*p],k->2*((-QuoInt(k-1,2)) mod p)+((k-1) mod 2)+1));
  s:=PermList(List([1..2*p],k->2*((1-QuoInt(k-1,2)) mod p)+((k-1) mod 2)+1));
  v:=(3,4)*(2*p-1,2*p);
  a:=r; b:=s; c:=v*r;
  G:=Group(a,b,c); A:=Group(a,b); B:=Group(b,c);
  if List([a,b,c],Order)<>[2,2,2] or Order(a*c)<>2 then Error("base involution/string failure"); fi;
  if List([a*b,b*c],Order)<>[p,p] then Error("base type failure"); fi;
  if Size(G)<>2^p*p then Error("base generation failure"); fi;
  if Intersection(A,B)<>Group(b) then Error("base intersection failure"); fi;
  x:=(2*p+1,2*p+2); y:=(2*p+3,2*p+4);
  aa:=a*x; bb:=b; cc:=c*y;
  H:=Group(aa,bb,cc); AA:=Group(aa,bb); BB:=Group(bb,cc);
  if List([aa,bb,cc],Order)<>[2,2,2] or Order(aa*cc)<>2 then Error("lift involution/string failure"); fi;
  if List([aa*bb,bb*cc],Order)<>[2*p,2*p] then Error("lift type failure"); fi;
  if Size(H)<>2^(p+2)*p then Error("lift generation failure"); fi;
  if Intersection(AA,BB)<>Group(bb) then Error("lift intersection failure"); fi;
  Print("p=",p," base_order=",Size(G)," base_type=",List([a*b,b*c],Order),
    " lifted_order=",Size(H)," lifted_type=",List([aa*bb,bb*cc],Order),
    " parabolic_intersection=",Size(Intersection(AA,BB))," PASS\n");
end;
for p in [3,5,7,11,13,17,19,23,29,31] do CheckType2(p); od;
LogTo();
QUIT;
