# Exact raw-presentation diagnostics, independent of the uniform RS proof.
SetAssertionLevel(1);
CheckMarking := function(G, expected, pairs)
    local size, P, mask, i, j, count, iso, gens, pair;
    size := Size(G);  # Todd--Coxeter/order computation of the actual fp group.
    Assert(0, size = expected);
    iso := IsomorphismPermGroup(G);
    gens := List(GeneratorsOfGroup(G), x -> Image(iso,x));
    G := Image(iso);
    Assert(0, Length(gens) >= 3);
    Assert(0, ForAll(gens,x->Order(x)=2));
    for pair in pairs do
        Assert(0, Order(gens[pair[1]]*gens[pair[2]])=pair[3]);
    od;
    P := [];
    for mask in [0..2^Length(gens)-1] do
        P[mask+1] := Subgroup(G, Filtered(gens, x -> QuoInt(mask, 2^(Position(gens,x)-1)) mod 2 = 1));
    od;
    count := 0;
    for i in [0..Length(P)-1] do
        for j in [0..Length(P)-1] do
            mask := Sum(Filtered([0..Length(gens)-1], k -> QuoInt(i,2^k) mod 2 = 1 and QuoInt(j,2^k) mod 2 = 1), k -> 2^k);
            Assert(0, Intersection(P[i+1],P[j+1]) = P[mask+1]); count := count+1;
        od;
    od;
    return [size,count];
end;
for pars in [[2,2],[2,3],[3,2],[3,3]] do
    p := pars[1]; s := pars[2]; F := FreeGroup("d","b","c");;
    d := F.1; b := F.2; c := F.3;
    rels := [d^2,b^2,c^2,(d*b)^2,(b*c)^(2*p),(d*c)^(2*p)];
    for j in [2..p-1] do Add(rels,((d*c)^(j-1)*d*b*(c*b)^(j-1))^2); od;
    Add(rels,((d*c)^(p-1)*d*b*(c*b)^(p-1))^s);
    result := CheckMarking(F/rels,(2*s)^p*2*p,[[1,2,2],[1,3,2*p],[2,3,2*p]]);
    Print("POLYGON ",p," ",s," ",result,"\n");
od;
for pars in [[3,2],[3,3]] do
    n := pars[1]; s := pars[2]; F := FreeGroup(n+1);; g := GeneratorsOfGroup(F);
    rels := List(g,x->x^2); pairs := [];
    for i in [1..n+1] do
        for j in [i+1..n+1] do
            m := 2;
            if (i=1 or i=2) and j=3 then m:=3; fi;
            if i>=3 and j=i+1 then
                m:=3; if j=n+1 then m:=4; fi;
            fi;
            Add(rels,(g[i]*g[j])^m);
            Add(pairs,[i,j,m]);
        od;
    od;
    w := g[1]*Product(g{[3..n+1]})*Product(Reversed(g{[3..n]}))*g[2];
    Add(rels,w^(2*s));
    result := CheckMarking(F/rels,(4*s)^n*Factorial(n)/2,pairs);
    Print("ORTHOPLEX ",n," ",s," ",result,"\n");
od;
Print("PHASE30_SOURCE_PRESENTATIONS_PASS\n");
QUIT;
