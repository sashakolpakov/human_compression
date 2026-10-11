# Exploratory, not part of the frozen proof boundary.
for q in [27,81,243] do
 for id in [1..NrSmallGroups(q)] do
  g:=SmallGroup(q,id);
  if not IsAbelian(g) and ForAny(NormalSubgroups(g),n->IsCyclic(n) and IsCyclic(FactorGroup(g,n))) then
   subs:=List(ConjugacyClassesSubgroups(g),Representative);
   cyc:=Filtered(subs,IsCyclic);
   for u in cyc do for v0 in cyc do for v in ConjugacyClassSubgroups(g,v0) do
    h:=ClosureGroup(u,v);
    if Size(h)*Size(Intersection(u,v))<>Size(u)*Size(v) then
     Print("NONPERMUTABLE ",[q,id]," subgroup orders ",[Size(u),Size(v)]," generated ",Size(h),"\n");
     QUIT_GAP(0);
    fi;
   od; od; od;
  fi;
 od;
 Print("checked ",q,"\n");
od;
QUIT_GAP(0);
