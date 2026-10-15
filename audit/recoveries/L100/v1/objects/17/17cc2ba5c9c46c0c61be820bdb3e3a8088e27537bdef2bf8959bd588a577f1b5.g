# Read-only structural audit of returned anchors in the exact loaded G/reps model.
# No search function, maximal-inclusion generation, or RunBorel call is loaded.
borelResult:=rec();;borelCheckpoint:=rec();;
AuditJoin:=function(B,panels)
 local H,P;
 H:=B;for P in panels do H:=ClosureGroup(H,P);od;return H;
end;;
AuditOne:=function(row)
 local bid,B,d,levels,r,c,panels,previous,expectedFull,t,actual,first,A;
 bid:=row[1];B:=reps[bid];
 borelResult:=rec();Read(Concatenation(AUDIT_DIR,"/b",String(bid),"_done.g"));d:=borelResult;
 if not IsRecord(d) or not IsBound(d.id) or d.id<>bid or not IsBound(d.order) or d.order<>Size(B)
    or not IsBound(d.levels) or not IsBound(d.geometries) then Error("returned identity");fi;
 levels:=d.levels;
 if levels<>row[2] or List(d.geometries,Length)<>row[3] then Error("done/transcript mismatch");fi;
 if B=G then
  if levels<>[] or d.geometries<>[] then Error("top Borel must have no panels");fi;
 else
  if Length(levels)<2 or Length(levels)>Length(FactorsInt(Index(G,B)))+1
     or not ForAll(levels,IsInt) or levels[1]<=0 or levels[Length(levels)]<>0
     or not ForAll(levels{[1..Length(levels)-1]},n->n>0) then Error("nonterminal level sequence");fi;
  panels:=fail;expectedFull:=[];
  for r in [2..Length(levels)] do
   borelCheckpoint:=rec();
   Read(Concatenation(AUDIT_DIR,"/b",String(bid),"_r",String(r),".g"));c:=borelCheckpoint;
   if not IsBound(c.id) or c.id<>bid or not IsBound(c.order) or c.order<>Size(B)
      or not IsBound(c.rank) or c.rank<>r or not IsBound(c.panels) or not IsBound(c.level)
      or not IsBound(c.geometries) then Error("checkpoint identity");fi;
   if panels=fail then
    panels:=c.panels;
    if not IsList(panels) or Length(Set(panels))<>Length(panels)
       or not ForAll(panels,P->IsGroup(P) and IsSubgroup(G,P) and IsSubgroup(P,B) and P<>B) then Error("invalid panel list");fi;
    A:=Image(ActionHomomorphism(Normalizer(G,B),panels,OnPoints));
    first:=List(Orbits(A,[1..Length(panels)]),o->[o[1]]);
    if Length(first)<>levels[1] then Error("first level count");fi;
    expectedFull:=List(Filtered(first,t->panels[t[1]]=G),t->panels{t});
   elif c.panels<>panels then Error("changed panel list");fi;
   if not IsList(c.level) or Length(c.level)<>levels[r] then Error("checkpoint level count");fi;
   for t in c.level do
    if not IsList(t) or Length(t)<>r or Length(Set(t))<>r
       or not ForAll(t,i->IsInt(i) and i>=1 and i<=Length(panels)) then Error("invalid family indices");fi;
    if AuditJoin(B,panels{t})=G then Add(expectedFull,panels{t});fi;
   od;
   if c.geometries<>expectedFull then Error("checkpoint full family accumulation");fi;
  od;
  if d.geometries<>expectedFull then Error("final full family accumulation");fi;
 fi;
 Print("AUDITED ",row,"\n");
end;;
for auditRow in AUDIT_ROWS do AuditOne(auditRow);od;
Print("PASS_RETURNED_ANCHOR_AUDIT\n");
