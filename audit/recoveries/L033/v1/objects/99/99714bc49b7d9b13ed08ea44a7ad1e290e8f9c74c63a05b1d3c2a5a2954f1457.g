MakeReadWriteGlobal("LINS_FindPModules");;
LINS_FindPModules := function(gr, rH, p, opts)
    local
    G,      # group:        located in the root node of LINS graph `gr`.
    H,      # group:        located in the node `rH`.
    n,      # pos-int:      index bound of LINS graph `gr`.
    Iso,    # isomorphism:  from `H` into fp-group
    IH,     # fp-group:     image under `Iso`, isomorphic to `H`
    P,      # quotsys:      p-quotient of `IH` of class 1
    Mu,     # epimorphism:  from `IH` into `P`
    M,      # pc-group:     image under `Mu`
    GenM,   # [elm]:        generators of `M`, basis of $GF(p) G$ module `M`
    gens,   # [matrix]:     matrices, action of generators of `G` on `M`
    x,      # elm:          loop var, generator of `G`
    y,      # elm:          loop var, elm of `H` with maps
            #               under `Mu` and `Iso` to a generator of `M`
    word,   # elm:          word in `M`, $y ^ x$ via a
            #               "conjugation" action of `G` on `M`
    gen,    # matrix:       over $GF(p)$, encoding action of `x` on `M`
    GM,     # module:       from MeatAxe, representation of
            #               $GF(p) G$ module `M` by `gens`
    MM,     # [module]:     from MeatAxe, all maximal modules of `GM`
    m,      # module:       loop variable, maximal module in `MM`
    V,      # vectorspace:  $GF(p) ^ d$, where $d$ is the dimension of `GM`
    s,      # pos-int:      index of `m` in `V`, which equals index $[H : K]$
    PsiHom, # epimorphism:  from `V` to $V/m$
    Q,      # vectorspace:  image under `PsiHom`
    O,      # [elm]:        all elements of Q, in bijection with
            #               elements of $H/K$
    GenIH,  # [elm]:        generators of `IH`
    PhiHom, # epimorphism:  from `H` into `p`-quotient $H/K$, identification
            #               of `Q` as a quotient of `H` via `Mu`
    K,      # group:        subgroup of `H` with `p`-quotient, normal in `G`
    rK,     # LINS node:    containing `K`
    isNew,  # boolean:      whether the group `K` is new in `gr`
    nrFound,# pos-int:      number of newly found normal subgroups
    data;   # tuple:        [`rK`, `isNew`]

    # Check if `p`-quotients have been computed already from this group
    if p in LinsNodeTriedPrimes(rH) then
        return [false, 0];
    fi;
    AddSet(LinsNodeTriedPrimes(rH), p);

    # Initialize data
    n := IndexBound(gr);
    G :=Grp(LinsRoot(gr));
    H := Grp(rH);
    nrFound := 0;

    # Isomorphism onto the fp-group of `H`
    Print("PROFILE_BEGIN_FP index=",Index(rH)," p=",p," time=",Runtime(),"\n");
    Iso := IsomorphismFpGroup(H);
    Print("PROFILE_END_FP time=",Runtime(),"\n");
    IH := Image(Iso);

    # Create the Isomorphism to the group structure of the `p`-Module `M`
    Print("PROFILE_BEGIN_PQUOTIENT time=",Runtime(),"\n");
    P := PQuotient(IH, p, 1, LINS_MaxPGenerators);
    Print("PROFILE_END_PQUOTIENT time=",Runtime(),"\n");
    Mu := EpimorphismQuotientSystem(P);
    M := Image(Mu);
    GenM := GeneratorsOfGroup(M);

    # If `M` is trivial we skip this prime
    if IsEmpty(GenM) then
        return [false, 0];
    fi;

    # Define the group action of `G` on the `p`-Module `M`
    # For every generator in `G` we store the action on `M` in form of a matrix
    Print("PROFILE_BEGIN_ACTION dim=",Length(GenM)," time=",Runtime(),"\n");
    gens := [];
    for x in GeneratorsOfGroup(G) do
        gen := [];
        for y in GenM do
            y := PreImagesRepresentative(Iso, PreImagesRepresentative(Mu, y));
            word := Image(Mu, Image(Iso, x * y * x ^ (-1) ));
            Add(gen, LINS_ExponentSum(Length(GenM), p, word));
        od;
        Add(gens, gen);
    od;

    # Compute the maximal submodules of `M`
    GM := GModuleByMats(gens, FiniteField(p));
    Print("PROFILE_BEGIN_MAXSUB time=",Runtime(),"\n");
    MM := MTX.BasesMaximalSubmodules(GM);
    Print("PROFILE_END_MAXSUB count=",Length(MM)," time=",Runtime(),"\n");
    V := FiniteField(p) ^ (Length(GenM));

    # Translate every submodule of `M` into a normal subgroup of `H`
    # with elementary abelian `p`-quotient
    for m in MM do

        # Check wether the index will be greater than `n`
        m := Subspace(V, m);
        s := p ^ ( Dimension(V) - Dimension(m) );
        if s > n / Index(G, H) then
            continue;
        fi;

        if not opts.DoPModule(gr, rH, p, s * rH!.Index) then
            continue;
        fi;

        # Compute the natural homomorphism from `V` to $V/m$
        PsiHom := NaturalHomomorphismBySubspace(V, m);
        Q := Image(PsiHom);
        O := Elements(Q);
        GenIH := GeneratorsOfGroup(IH);

        # Compute the subgroup `K` with $H/K$ being an
        # elementary abelian `p`-group
        PhiHom :=  GroupHomomorphismByImagesNC(H, SymmetricGroup(Length(O)),
            LINS_PullBackH(GenM, p, List(GeneratorsOfGroup(H), x->Image(Iso, x)), O, Mu, PsiHom));

        K := Kernel(PhiHom);
        if opts.DoSetParent then
            LINS_SetParent(K, G);
        fi;

        # Add the subgroup `K` to LINS graph `gr`
        if Index(G, K) <= n then
            data := LINS_AddGroup(gr, K, [rH], true, opts);
            rK := data[1];
            isNew := data[2];
            if isNew then
                nrFound := nrFound + 1;
                Info(InfoLINS, 3, LINS_tab3,
                    "Prime ", LINS_red, "p = ", p, LINS_reset, ". ",
                    "Found new normal subgroup ", LINS_red, "K = ", K, LINS_reset,
                    " of index ", LINS_red, Index(G, K), LINS_reset, ".");
            fi;
            if isNew and opts.DoTerminate(gr, rH, rK) then
                gr!.TerminatedUnder := rH;
                gr!.TerminatedAt := rK;
                return [true, nrFound];
            fi;
            # If the index is sufficient small,
            # compute `p`-quotients under the subgroup `K`
            if p <= n / Index(G, K) then
                LINS_FindPModules(gr, rK, p, opts);
            fi;
        fi;
    od;

    return [false, nrFound];
end;;
MakeReadOnlyGlobal("LINS_FindPModules");;
