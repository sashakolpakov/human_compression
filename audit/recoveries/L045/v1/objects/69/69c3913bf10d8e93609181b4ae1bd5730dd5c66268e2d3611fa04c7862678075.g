ReadFieldControls := function()
  local q, k, g, h, a, s, t, fields, pairs, i, deg, j, eps, n, count, total;
  deg := function(x,q,bound)
    return First(DivisorsInt(bound), e -> x^(q^e)=x);
  end;
  total := 0;
  for q in [4,5,7,8,9,11] do
    k := GF(q^6);
    g := Z(q^6)^((q^6-1)/(q^3+1));
    h := Z(q^2)^(q-1);
    if not (Order(g)=q^3+1 and Order(h)=q+1 and
            deg(g^2,q,6)=6 and deg(h^2,q,2)=2) then
      Error("literal finite-field degree failure");
    fi;
    a := Z(q^2);
    if not a in k then Error("quadratic subfield inclusion"); fi;
    fields := [];
    for s in [1,q] do
      for t in [1,q] do
        pairs := Set(Concatenation([[Zero(k),Zero(k)]],
                    List([0..q^2-2],i->[a^(s*i),a^(t*i)])));
        AddSet(fields,pairs);
      od;
    od;
    if Length(fields)<>2 or not ForAll(fields,x->Length(x)=q^2) then
      Error("relative field structure count");
    fi;
    n := (q^3+1)/Gcd(2,q-1);
    count := 0;
    for j in [1..n] do
      if Gcd(j,n)=1 then
        for eps in Set([One(k),-One(k)]) do
          if deg(eps*g^j,q,6)<>6 or deg(eps*h^j,q,2)<>2 then
            Error("normalizer degree failure");
          fi;
          count := count+1;
        od;
      fi;
    od;
    total := total+count;
    Print("FIELD ",q," ",Order(g)," ",Order(h)," ",Length(fields)," ",count,"\n");
  od;
  Print("COMPLETE_D4_FIELD_CONTROLS ",total,"\n");
end;
ReadFieldControls();
QUIT;
