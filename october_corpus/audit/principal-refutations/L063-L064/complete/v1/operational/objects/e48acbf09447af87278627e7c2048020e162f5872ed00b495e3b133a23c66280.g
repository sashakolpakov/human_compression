SetInfoLevel(InfoWarning,0);;
F:=GF(512);;ff:=AsList(F);;o:=One(F);;z:=Zero(F);;alpha:=Z(512);;k:=alpha^73;;
if Order(k)<>7 or alpha in GF(8) then Error("field parameters");fi;
K:=Filtered(ff,x->x^8=x);;T:=Set(Concatenation(List(K,a->List(K,b->a+alpha*b))));;
if Length(K)<>8 or Length(T)<>64 then Error("literal subspaces");fi;
ToPerm:=function(M)
 local A,x,num,den,y,idx;A:=[];
 for idx in [1..513] do
  if idx=513 then num:=M[1][1];den:=M[2][1];else x:=ff[idx];num:=M[1][1]*x+M[1][2];den:=M[2][1]*x+M[2][2];fi;
  if den=z then Add(A,513);else y:=num/den;Add(A,Position(ff,y));fi;
 od;
 if Set(A)<>[1..513] then Error("not bijective");fi;
 return PermList(A);
end;;
u:=ToPerm([[o,o],[z,o]]);;v:=ToPerm([[o,alpha],[z,o]]);;w:=ToPerm([[z,o],[o,z]]);;d:=ToPerm([[k,z],[z,k^-1]]);;
H:=Group(u,w,d);;Q:=Group(u,v,d);;B:=Group(u,d);;G:=Group(u,v,w,d);;
orders:=List([G,H,Q,B],Size);;
if orders<>[134217216,504,448,56] or Intersection(H,Q)<>B then Error("actual groups/intersection");fi;
ht:=ActionHomomorphism(H,RightCosets(H,B),OnRight);;qt:=ActionHomomorphism(Q,RightCosets(Q,B),OnRight);;
ha:=Image(ht);;qa:=Image(qt);;
if [NrMovedPoints(ha),NrMovedPoints(qa),Size(Kernel(ht)),Size(Kernel(qt))]<>[9,8,1,8] then Error("actual local actions");fi;
if Length(Orbit(ha,[1,2],OnTuples))<>72 or Length(Orbit(qa,[1,2],OnTuples))<>56 then Error("local two-transitivity");fi;
planes:=Set(List(Difference(ff,K),x->Set(Concatenation(List(K,a->List(K,b->a+x*b))))));;
if Length(planes)<>9 then Error("plane inventory");fi;
Print("PASS INDEPENDENT_GAP_GF512 orders=",orders," intersection=56 local_degrees=[9,8] kernels=[1,8] ordered_pair_orbits=[72,56] planes=9\n");
QUIT_GAP(0);
