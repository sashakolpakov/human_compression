LoadPackage("LINS");;

# Every variable in the search and its lambda closures is local. The search is
# the unmodified all-normal-subgroup LINS interface, with its default options.
HyperbolicCheck := function(marking, M, expected)
  local H, subsets, groups, a, b, i, k, J, omitted, pars, maps, bases,
        incident, common, wanted, objects, cosets, p, checks, loc;
  H := Group(marking);
  if List(marking,Order) <> [2,2,2,2] then return rec(ok:=false,reason:="involutions"); fi;
  if List([1..4],i->List([1..4],k->Order(marking[i]*marking[k])))<>M then
    return rec(ok:=false,reason:="pair_orders");
  fi;
  subsets:=Combinations([1..4]);
  groups:=List(subsets,J->Subgroup(H,marking{J}));
  pars:=List([1..4],i->groups[Position(subsets,Difference([1..4],[i]))]);
  loc:=List(pars,Size);
  # Finite diagram permits projective spherical residues. Do not impose universal local orders.
  for a in [1..16] do for b in [1..16] do
    if Intersection(groups[a],groups[b]) <> groups[Position(subsets,Intersection(subsets[a],subsets[b]))] then
      return rec(ok:=false,reason:="intersection",failed_pair:=[a,b]);
    fi;
  od; od;
  # Objects of type k are literal right cosets of the maximal parabolic.
  # Their incidence with the base object of type i is exactly its orbit under Gi.
  # Check every base flag and every missing type, including the empty flag.
  checks:=0; objects:=[];
  for k in [1..4] do
    cosets:=RightCosets(H,pars[k]);
    p:=Position(cosets,RightCoset(pars[k],One(H)));
    maps:=ActionHomomorphism(H,cosets,OnRight);
    incident:=List([1..4],i->Set(Orbit(Image(maps,pars[i]),p)));
    Add(objects,Length(cosets));
    for J in Combinations(Difference([1..4],[k])) do
      common:=[1..Length(cosets)];
      for i in J do common:=Intersection(common,incident[i]); od;
      omitted:=Difference([1..4],J);
      wanted:=Set(Orbit(Image(maps,groups[Position(subsets,omitted)]),p));
      if common<>wanted then
        return rec(ok:=false,reason:="flag_transitivity",failed_flag:=[J,k],sizes:=[Length(common),Length(wanted)]);
      fi;
      checks:=checks+1;
    od;
  od;
  return rec(ok:=true,intersection_checks:=256,flag_checks:=checks,objects:=objects,local_orders:=loc);
end;;

RunHyperbolic := function(M,expected,bound,out)
  local F,x,rels,i,j,G,start,gr,nodes,node,N,index,action,H,marking,
        counts,result,small,sm,degree,accepted,qualified,divisor,record,n,checks;
  if bound>LINS_MaxIndex then Error("LINS classification-table bound exceeded"); fi;
  Reset(GlobalMersenneTwister,193314); Reset(GlobalRandomSource,193314);
  F:=FreeGroup("a","b","c","d"); x:=GeneratorsOfGroup(F);
  rels:=List(x,g->g^2);
  for i in [1..4] do for j in [i+1..4] do Add(rels,(x[i]*x[j])^M[i][j]); od; od;
  G:=F/rels; divisor:=Lcm(Concatenation(List([1..4],i->List([i+1..4],j->2*M[i][j])))); start:=Runtime();
  Print("BEGIN_BOUND ",bound," LINS_MAX ",LINS_MaxIndex,"\n");
  gr:=LowIndexNormalSubgroupsSearchForAll(G,bound);
  nodes:=List(gr); counts:=[]; accepted:=[]; qualified:=[];
  Print("NORMAL_SEARCH_RETURNED ",Length(nodes)," MS ",Runtime()-start,"\n");
  PrintTo(out,"hyperbolic_records := [\n");
  for n in [1..Length(nodes)] do
    node:=nodes[n]; index:=Index(node); Add(counts,index);
    if index mod divisor=0 then
      N:=Grp(node); action:=FactorCosetAction(G,N); H:=Image(action);
      marking:=List(GeneratorsOfGroup(G),g->Image(action,g));
      if Size(H)<>index or Group(marking)<>H then Error("quotient action is not faithful"); fi;
      result:=HyperbolicCheck(marking,M,expected);
      Print("CHECK_NODE ",n," INDEX ",index," RESULT ",result,"\n");
      if result.ok then
        small:=SmallerDegreePermutationRepresentation(H); sm:=List(marking,g->Image(small,g));
        if Size(Image(small))<>index or Size(Group(sm))<>index then Error("compact map not injective"); fi;
        checks:=HyperbolicCheck(sm,M,expected);
        if checks<>result then Error("compact checks differ"); fi;
        degree:=LargestMovedPoint(Group(sm));
        record:=rec(node:=n,order:=index,degree:=degree,permutations:=List(sm,g->ListPerm(g,degree)),checks:=checks);
        if not IsEmpty(accepted) then AppendTo(out,",\n"); fi;
        AppendTo(out,record); Add(accepted,[n,index,degree]);
      fi;
    fi;
  od;
  AppendTo(out,"\n];\n");
  Print("INDEX_MULTIPLICITIES ",Collected(counts),"\nACCEPTED ",accepted,"\n");
  Print("COMPLETE_HYPERBOLIC_BOUND ",bound," NORMALS ",Length(nodes)," ACCEPTED ",Length(accepted)," MS ",Runtime()-start,"\n");
end;;
