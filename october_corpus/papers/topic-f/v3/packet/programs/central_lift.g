# Central cyclic lift of the odd-exponent construction in arXiv:2508.20654.
# Run: gap -q research/leemans/central_lift.g
# The independent checks use GAP's exact finite polycyclic group algorithms.

VerifyCentralLift := function(p, m)
  local r, f, col, i, P, pc, beta, s, sgimages, sig, Aut2, G0,
        embP, embSig, b0, s0, sig0, a0, c0, C, D, eG, eC, x,
        a, b, H, invmap, K, phi, target, result, t, hpc;
  if not IsPrimeInt(p) or p < 5 or m < 6 or m mod 2 <> 0 or m > p+1 then
    Error("Require odd prime p >= 5 and even 6 <= m <= p+1");
  fi;
  r := m-2;
  f := FreeGroup(r+1);
  col := SingleCollector(f, List([1..r+1], i -> p));
  SetPower(col,1,f.(r+1));
  for i in [2..r] do
    SetConjugate(col,i,1,f.(i)*f.(i+1));
  od;
  UpdatePolycyclicCollector(col);
  P := GroupByRws(col);
  pc := Pcgs(P);
  beta := pc[1];
  s := pc[2];
  if Size(P) <> p^(m-1) then Error("Wrong base p-group order"); fi;
  sig := GroupHomomorphismByImages(P,P,[beta,s],[beta^-1,s]);
  if sig=fail or not IsBijective(sig) or Order(sig) <> 2 then
    Error("Base involutory automorphism fails");
  fi;
  Aut2 := Group(sig);
  G0 := SemidirectProduct(Aut2,P);
  embSig := Embedding(G0,1);
  embP := Embedding(G0,2);
  b0 := Image(embP,beta);
  s0 := Image(embP,s);
  sig0 := Image(embSig,sig);
  a0 := b0*s0;
  c0 := s0^-1*sig0;
  if Size(Group(a0,c0)) <> 2*p^(m-1) then Error("Base generation fails"); fi;
  if [Order(a0),Order(c0),Order(a0*c0)] <> [p^2,2*p,2] then
    Error("Base orders fail");
  fi;
  if Size(Intersection(Group(a0),Group(c0))) <> 1 then Error("Base IP fails"); fi;
  if GroupHomomorphismByImages(G0,G0,[a0,c0],[a0^-1,c0^-1]) <> fail then
    Error("Base is reflexible");
  fi;
  target := CyclicGroup(IsPcGroup,p);
  phi := GroupHomomorphismByImages(G0,target,[a0,c0],
            [GeneratorsOfGroup(target)[1],GeneratorsOfGroup(target)[1]^-1]);
  if phi=fail or not IsSurjective(phi) then Error("Fiber map fails"); fi;
  C := CyclicGroup(IsPcGroup,p^2);
  D := DirectProduct(G0,C);
  eG := Embedding(D,1);
  eC := Embedding(D,2);
  x := Image(eC,GeneratorsOfGroup(C)[1]);
  a := Image(eG,a0)*x;
  b := Image(eG,c0)*x^-1;
  H := Group(a,b);
  if Size(H) <> 2*p^m then Error("Lift size fails"); fi;
  if [Order(a),Order(b),Order(a*b)] <> [p^2,2*p^2,2] then
    Error("Lift orders fail");
  fi;
  if Size(Intersection(Group(a),Group(b))) <> 1 then Error("Lift IP fails"); fi;
  K := Group(b^(2*p));
  if Size(K) <> p or not IsNormal(H,K) then Error("Lift kernel fails"); fi;
  invmap := GroupHomomorphismByImages(H,H,[a,b],[a^-1,b^-1]);
  if invmap <> fail then Error("Lift is reflexible"); fi;
  result := rec(p:=p, m:=m, base_order:=Size(G0), order:=Size(H),
    type:=[Order(a),Order(b)], product_order:=Order(a*b),
    cyclic_intersection_order:=Size(Intersection(Group(a),Group(b))),
    lift_kernel_order:=Size(K), reversal_homomorphism_exists:=invmap<>fail,
    tight:=Size(H)=Order(a)*Order(b));
  Print(result,"\n");
  return result;
end;

Print("GAP ",GAPInfo.Version,"\n");
VerifyCentralLift(5,6);;
VerifyCentralLift(7,6);;
VerifyCentralLift(7,8);;
QUIT;
