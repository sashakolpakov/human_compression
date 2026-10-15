# Keep every normal kernel whose quotient order divides the prescribed target.
# Finite Coxeter seed enumeration is acquired; default LINS module/intersection
# computations and their classification inputs remain explicit premises.
CoxeterDivisorOptions:=function(M,target)
 local seed;
 if not IsPosInt(target) or target>LINS_MaxIndex then Error("admitted positive target index");fi;
 seed:=function(gr)
  local F,entry,epis,h,res,root;
  if IndexBound(gr)<>target then Error("fixed divisor bound identity");fi;
  root:=LinsRoot(gr);F:=Grp(root);
  if not IsFpGroup(F)or not IsWholeFamily(F)then Error("whole fp Coxeter source required");fi;
  for entry in LINS_TargetsQuotient do
   if entry[1]>target then break;fi;
   if target mod entry[1]<>0 then continue;fi;
   Print("DIVISOR_COXETER_TARGET_BEGIN ",entry[1],"\n");
   epis:=CoxeterTargetEpis(F,entry[2],M);
   for h in epis do
    res:=LINS_AddGroup_Caller(gr,root,Kernel(h),LINS_DefaultOptions,"exact divisor Coxeter seed: ");
    if res=Terminate then Error("unexpected early termination");fi;
   od;
  od;
  Print("DIVISOR_ALL_SEEDS_COMPLETE\n");
 end;
 return rec(InitGraph:=seed,FilterTQuotients:=function(gr,targets)return [];end,
  DoCut:=function(gr,rH)return target mod Index(rH)<>0;end,
  DoPQuotient:=function(gr,rH,p)return target mod (Index(rH)*p)=0;end,
  DoPModule:=function(gr,rH,p,index)return target mod index=0;end,
  DoIntersection:=function(gr,rH,rK,index)return target mod index=0;end);
end;;
