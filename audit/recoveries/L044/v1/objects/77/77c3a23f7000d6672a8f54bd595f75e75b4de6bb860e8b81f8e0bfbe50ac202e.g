# Points (a,b) with a in F2^3 and b in F2, numbered 2*a+b+1.
bit:=function(a,j) return QuoInt(a,2^j) mod 2;end;;
Flip:=function(a) return (2*a+1,2*a+2);end;;
flips:=List([0..7],Flip);;
translations:=List([0..2],j->PermList(List([1..16],p->
 2*(QuoInt(p-1,2)+(1-2*bit(QuoInt(p-1,2),j))*2^j)+(p-1) mod 2+1)));;
cycleCoords:=PermList(List([1..16],function(p)
 local a,b; a:=QuoInt(p-1,2);b:=(p-1)mod 2;
 return 2*(bit(a,2)+2*bit(a,0)+4*bit(a,1))+b+1;
end));;
transvection:=PermList(List([1..16],function(p)
 local a,b; a:=QuoInt(p-1,2);b:=(p-1)mod 2;
 return 2*((bit(a,0)+bit(a,1))mod 2+2*bit(a,1)+4*bit(a,2))+b+1;
end));;
W:=Group(Concatenation(List([2..8],j->flips[1]*flips[j]),translations));;
N:=Group(Concatenation(flips,translations,[cycleCoords,transvection]));;
if Size(W)<>1024 or Size(N)<>344064 or not IsNormal(N,W) or
 not IsSubgroup(AlternatingGroup(16),W) or not IsTransitive(W,[1..16]) then
 Error("cube model");fi;
Print("CUBE_MODEL ",Size(W)," ",Size(N)," involutions ",
 Number(Elements(W),x->Order(x)=2),"\n");
