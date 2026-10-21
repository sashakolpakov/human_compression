# Exact replacement only for the finite-target epimorphism seeds in LINS.
# Identity images are included: this enumerates all presentation quotients,
# not only smooth quotients. Inner conjugation never changes a kernel.
CoxeterTargetEpis := function(F,Q,M)
  local all,visit,result,gens,counts;
  all:=Filtered(Elements(Q),x->x^2=One(Q)); gens:=GeneratorsOfGroup(F);
  if Length(gens)<>Length(M) then Error("wrong marked presentation arity"); fi;
  counts:=List([1..Length(M)+1],i->0); result:=[];
  visit:=function(tuple,st)
    local k,candidates,orbits,orb,y,h;
    k:=Length(tuple)+1; counts[k]:=counts[k]+1;
    if k>Length(M) then
      if Size(Group(tuple))=Size(Q) then
        h:=GroupHomomorphismByImages(F,Q,gens,tuple);
        if h=fail or not IsSurjective(h) then Error("epimorphism check failed"); fi;
        Add(result,h);
      fi;
      return;
    fi;
    candidates:=Filtered(all,y->ForAll([1..k-1],i->(tuple[i]*y)^M[i][k]=One(Q)));
    orbits:=OrbitsDomain(st,candidates,OnPoints);
    for orb in orbits do
      y:=orb[1]; visit(Concatenation(tuple,[y]),Centralizer(st,y));
    od;
  end;
  visit([],Q);
  Print("COXETER_TARGET_COMPLETE ",Size(Q)," COUNTS ",counts," EPIS ",Length(result),"\n");
  return result;
end;;

CoxeterSeedOptions := function(M)
  local seed;
  seed:=function(gr)
    local F,entry,epis,h,res,root;
    root:=LinsRoot(gr); F:=Grp(root);
    if not IsFpGroup(F) or not IsWholeFamily(F) then Error("fp Coxeter source required"); fi;
    for entry in LINS_TargetsQuotient do
      if entry[1]>IndexBound(gr) then break; fi;
      Print("COXETER_TARGET_BEGIN ",entry[1],"\n");
      epis:=CoxeterTargetEpis(F,entry[2],M);
      for h in epis do
        res:=LINS_AddGroup_Caller(gr,root,Kernel(h),LINS_DefaultOptions,"exact Coxeter seed: ");
        if res=Terminate then Error("unexpected early termination"); fi;
      od;
    od;
    Print("COXETER_ALL_SEEDS_COMPLETE\n");
  end;
  return rec(InitGraph:=seed,FilterTQuotients:=function(gr,targets) return []; end);
end;;
