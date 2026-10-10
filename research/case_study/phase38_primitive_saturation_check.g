# Exact diagnostics for the new primitive-saturation and residue formulas.
# Proofs remain in phase38_primitive_saturation.md; finite samples are not
# a substitute for its all-parameter argument.
SetInfoLevel(InfoWarning,0);;
CheckSaturation := function(g,rs)
  local d,sets,sub,h,phi,phih,m,i,omit,omith,maxs,matches,checks;
  d:=Length(rs); sets:=Combinations([1..d]); phi:=FrattiniSubgroup(g);
  checks:=0;
  for sub in sets do
    if IsEmpty(sub) then h:=TrivialSubgroup(g); else h:=Group(rs{sub}); fi;
    phih:=FrattiniSubgroup(h);
    if phih<>Intersection(h,phi) then Error("Frattini restriction"); fi;
    if Index(h,phih)<>2^Length(sub) and
       Index(h,phih)<>3^Length(sub) then Error("basis dimension"); fi;
    checks:=checks+1;
  od;
  maxs:=MaximalSubgroups(g);
  for i in [1..d] do
    omit:=Difference([1..d],[i]);
    if IsEmpty(omit) then omith:=TrivialSubgroup(g); else omith:=Group(rs{omit}); fi;
    m:=ClosureGroup(phi,omith);
    matches:=Filtered(maxs,x->IsSubgroup(x,omith));
    if Length(matches)<>1 or matches[1]<>m then Error("unique maximal overgroup"); fi;
    if Index(m,omith)<>Index(phi,FrattiniSubgroup(omith)) then
      Error("saturation fiber"); fi;
  od;
  return checks;
end;;

cases := [[5],[6],[7],[5,6],[6,6],[5,7],[6,5,6],[5,6,5]];;
totalSubsets:=0;; totalResidueIndices:=0;; iso:=fail;;
for ns in cases do
  d:=Length(ns)+2; f:=FreeGroup(d); r:=GeneratorsOfGroup(f);
  rel:=List(r,x->x^2);
  for i in [1..d] do
    for j in [i+1..d] do
      if j=i+1 then Add(rel,(r[i]*r[j])^4);
      else Add(rel,Comm(r[i],r[j])); fi;
    od;
  od;
  for i in [1..d-2] do
    t:=r[i]*r[i+1]*r[i+2]*r[i+1];
    u:=r[i+2]*r[i+1]*r[i]*r[i+1]; n:=ns[i];
    if n mod 2=1 then
      qpow:=2^((n-3)/2); Append(rel,[t^qpow,u^qpow]);
    else
      qpow:=2^((n-4)/2); Append(rel,[t^qpow*u^qpow,t^(-qpow)*u^qpow]);
    fi;
  od;
  if d>=4 then
    for i in [1..d-3] do
      Add(rel,Comm((r[i]*r[i+1])^2,(r[i+2]*r[i+3])^2));
    od;
  fi;
  q:=f/rel; iso:=IsomorphismPermGroup(q); g:=Image(iso);
  rs:=List(GeneratorsOfGroup(q),x->Image(iso,x));
  CheckSaturation(g,rs);
  gamma:=CommutatorSubgroup(DerivedSubgroup(g),g);
  sets:=Combinations([1..d]); count:=0;
  for sub in sets do
    if IsEmpty(sub) then h:=TrivialSubgroup(g); else h:=Group(rs{sub}); fi;
    gh:=CommutatorSubgroup(DerivedSubgroup(h),h);
    if gh<>Intersection(gamma,h) then Error("gamma3 restriction"); fi;
    excess:=Sum(Filtered([1..d-2],j->IsSubset(sub,[j..j+2])),j->ns[j]-5);
    edges:=Number([1..d-1],j->j in sub and j+1 in sub);
    if Size(gh)<>2^excess then Error("parabolic local-kernel formula"); fi;
    if Size(h)<>2^(Length(sub)+edges+excess) then Error("parabolic order"); fi;
    for i in sub do
      omitted:=Difference(sub,[i]);
      if IsEmpty(omitted) then hi:=TrivialSubgroup(g); else hi:=Group(rs{omitted}); fi;
      deg:=Number(sub,j->AbsInt(i-j)=1);
      affected:=Sum(Filtered([1..d-2],j->IsSubset(sub,[j..j+2]) and i in [j..j+2]),j->ns[j]-5);
      if Index(h,hi)<>2^(1+deg+affected) then Error("residue-index formula"); fi;
      gh_i:=CommutatorSubgroup(DerivedSubgroup(hi),hi);
      if Index(h,hi)<>2^(1+deg)*Index(gh,gh_i) then Error("graded residue fiber"); fi;
      if (Index(h,hi)=2)<>(deg=0) then Error("primitive isolation criterion"); fi;
      count:=count+1;
    od;
  od;
  totalSubsets:=totalSubsets+Length(sets); totalResidueIndices:=totalResidueIndices+count;
  Print("PASS square_parameters=",ns," subsets=",Length(sets)," residue_indices=",count,"\n");
od;

# General Theorem1 does not assume involutory generators, IP or p=2.
for pair in [[8,2],[8,4],[16,4],[27,3],[81,3]] do
  g:=SmallGroup(pair); rs:=MinimalGeneratingSet(g);
  count:=CheckSaturation(g,rs);
  Print("PASS generic_group=",pair," rank=",Length(rs)," subsets=",count,"\n");
od;
Print("PASS all saturation and forest formulas; square_subsets=",totalSubsets,
      " square_residue_indices=",totalResidueIndices,"\n");
QUIT;
