# Structural validation of completed-level checkpoints. Completeness is acquired
# from the exact prior execution of the accepted loop, not inferred from these tests.
ValidateLevelResume:=function(bid,cps,counts)
 local B,panels,expected,A,levels,allFull,c,r,t,first;
 if Length(cps)<1 or Length(counts)<>Length(cps)+1 or counts[Length(counts)]=0 then return fail;fi;
 B:=reps[bid];panels:=cps[1].panels;
 if not IsList(panels) or Length(Set(panels))<>Length(panels)
  or not ForAll(panels,P->IsGroup(P) and IsSubgroup(G,P) and IsSubgroup(P,B) and P<>B) then return fail;fi;
 expected:=OvergroupsFromInclusions(B,maxinclusions);
 if Set(panels)<>Set(expected) then return fail;fi;
 A:=Image(ActionHomomorphism(Normalizer(G,B),panels,OnPoints));
 first:=List(Orbits(A,[1..Length(panels)]),o->[o[1]]);
 if Length(first)<>counts[1] then return fail;fi;
 levels:=[first];allFull:=List(Filtered(first,t->panels[t[1]]=G),t->panels{t});
 for r in [2..Length(counts)] do
  c:=cps[r-1];
  if not IsRecord(c) or not IsBound(c.id) or c.id<>bid or not IsBound(c.order) or c.order<>Size(B)
   or not IsBound(c.rank) or c.rank<>r or not IsBound(c.panels) or c.panels<>panels
   or not IsBound(c.level) or not IsBound(c.geometries) or Length(c.level)<>counts[r] then return fail;fi;
  for t in c.level do
   if not IsList(t) or Length(t)<>r or Length(Set(t))<>r
    or not ForAll(t,i->IsInt(i) and i>=1 and i<=Length(panels))
    or not t{[1..r-1]} in levels[r-1] then return fail;fi;
   if JoinPanels(B,panels{t})=G then Add(allFull,panels{t});fi;
  od;
  if c.geometries<>allFull then return fail;fi;
  Add(levels,c.level);
 od;
 if Length(levels)>=Length(FactorsInt(Index(G,B)))+1 then return fail;fi;
 return rec(panels:=panels,levels:=levels,geometries:=allFull);
end;
