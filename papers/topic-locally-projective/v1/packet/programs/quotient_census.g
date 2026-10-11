# Full required census; run from the packet root. GAP exact algorithms are retained.
Read("programs/ambient_marking.g");;
Read("programs/source_maximals.g");;
CensusL084:=function()
 local cls,cc,prod,ClassIndex,bad,omid,omcent,rows,good,rejected,goodEdges,
 i,n,ncls,ni,invol,hn,dn,j,k,idx,maxidx,anchors,h,row,target,children,
 targets,child,niBad,x,b,q,witnesses,genfile,reportfile,types,t,par;
 t:=Runtime();
 cls:=ConjugacyClasses(W);
 ClassIndex:=function(x)
  return PositionProperty(cls,c->Order(Representative(c))=Order(x) and x in c);
 end;
 prod:=Set(Concatenation(List(Elements(H0),u->List(Elements(H3),v->u*v))));
 CheckL084(Length(prod)=1200,"complete end product");
 bad:=Set(List(Difference(prod,[One(W),om]),ClassIndex));
 omid:=ClassIndex(om);omcent:=Size(Centralizer(W,om));
 CheckL084(Length(cls)=180 and Length(bad)=47 and not omid in bad,"element classes");
 cc:=ConjugacyClassesSubgroups(W);
 CheckL084(Length(cc)=1262,"complete subgroup-class census");
 Print("CLASSES ",Length(cc),"\n");
 rows:=[];good:=[];rejected:=[];goodEdges:=[];
 for i in [1..Length(cc)] do
  n:=Representative(cc[i]);ncls:=ConjugacyClasses(n);
  ni:=List(ncls,c->ClassIndex(Representative(c)));
  niBad:=Intersection(ni,bad);
  if niBad=[] then
   Add(good,i);
   invol:=Sum(Filtered([1..Length(ni)],j->ni[j]=omid),j->Size(ncls[j]));
   hn:=omcent*invol/(60*Size(n));dn:=Size(W)/(120*Size(n))-hn/2;
   CheckL084(IsInt(hn) and IsInt(dn) and hn>=0 and dn>=0,"integer facet counts");
   Add(rows,[i,Size(n),dn,hn]);
  else Add(rejected,[i,niBad[1]]);fi;
 od;
 CheckL084(Length(good)=137,"all semisparse classes");
 CheckL084(Number(rows,r->r[4]=0)=65,"all dodecahedral facets");
 CheckL084(Number(rows,r->r[3]=0)=1,"all hemi-dodecahedral facets");
 CheckL084(Number(rows,r->r[3]>0 and r[4]>0)=71,"mixed facets");
 for i in good do
  n:=Representative(cc[i]);
  for k in MaximalSubgroupClassReps(n) do
   idx:=PositionProperty(cc,c->Size(Representative(c))=Size(k) and k in c);
   CheckL084(idx in good,"downward closure");AddSet(goodEdges,[i,idx]);
  od;
 od;
 maxidx:=Difference(good,Set(List(goodEdges,e->e[2])));
 CheckL084(Length(maxidx)=26 and Length(goodEdges)=349,"complete maximal containment");
 anchors:=[];
 for row in sourceMax do
  h:=Group(row[2]);idx:=PositionProperty(cc,c->Size(Representative(c))=Size(h) and h in c);
  Add(anchors,[row[1],idx,Size(h)]);
 od;
 CheckL084(Set(List(Filtered(anchors,a->not a[2] in good),a->a[1]))=[13,70,95,127],"literal maximal deletions");
 CheckL084(Set(List(Filtered(anchors,a->a[2] in good),a->a[2]))=maxidx,"all surviving literal maxima");
 # These children are identified by literal source inclusion rows, group type,
 # and (for row 91) the printed normalizer quotient order.
 targets:=List([13,70,95,127],lab->[lab,Group(First(sourceMax,a->a[1]=lab)[2])]);
 h:=targets[1][2];children:=List(ConjugacyClassesSubgroups(h),Representative);
 for row in [[78,45],[111,15]] do
  target:=Filtered(children,k->Size(k)=row[2]);
  CheckL084(Length(target)=1 and IsCyclic(target[1]),"unique cyclic child of row13");
  Add(targets,[row[1],target[1]]);
 od;
 h:=targets[2][2];children:=List(ConjugacyClassesSubgroups(h),Representative);
 target:=Filtered(children,k->Size(k)=30 and IsCyclic(k));
 CheckL084(Length(target)=1,"unique cyclic row90");Add(targets,[90,target[1]]);
 target:=Filtered(children,k->Size(k)=30 and not IsAbelian(k) and Index(Normalizer(W,k),k)=12);
 CheckL084(Length(target)=1 and StructureDescription(target[1])="C3 x D10","row91 type and normalizer");
 Add(targets,[91,target[1]]);
 SortBy(targets,a->a[1]);witnesses:=[];
 for row in targets do
  h:=row[2];ncls:=ConjugacyClasses(h);
  x:=First(List(ncls,Representative),u->ClassIndex(u) in bad);
  CheckL084(x<>fail,"each deleted row fails conjugacy avoidance");
  b:=First(Difference(prod,[One(W),om]),u->IsConjugate(W,x,u));
  q:=RepresentativeAction(W,x,b);
  CheckL084(q<>fail and q in W and x in h and x^q=b and b in prod and not b in [One(W),om],"actual missed conjugate witness");
  idx:=PositionProperty(cc,c->Size(Representative(c))=Size(h) and h in c);
  Add(witnesses,[row[1],idx,Size(h),Order(x),ClassIndex(x)]);
  PrintTo(Concatenation("witness_",String(row[1]),".g"),
   "# Literal permutation witness for deleted source row ",row[1],"\n",
   "rejectedGenerators:=",GeneratorsOfGroup(h),";;\n",
   "violatingElement:=",x,";;\n","conjugator:=",q,";;\n","endProductElement:=",b,";;\n");
 od;
 CheckL084(List(witnesses,a->a[1])=[13,70,78,90,91,95,111,127],"all eight literal deletion labels");
 # Every subgroup representative is retained in the computational evidence.
 genfile:="computed_subgroups.g";PrintTo(genfile,"# Fresh complete GAP subgroup-class representatives.\nsubgroupGenerators:=[\n");
 for i in [1..Length(cc)] do
  AppendTo(genfile,GeneratorsOfGroup(Representative(cc[i])));
  if i<Length(cc) then AppendTo(genfile,",");fi;AppendTo(genfile,"\n");
 od;AppendTo(genfile,"];;\n");
 # Normalizer quotients and subgroup descriptions are computed for every survivor.
 types:=List(good,function(i)
  local n; n:=Representative(cc[i]);
  return [i,StructureDescription(n),StructureDescription(Normalizer(W,n)/n)];
 end);
 reportfile:="census.json";
 PrintTo(reportfile,"{\n\"ambient_order\":",Size(W),",\n\"subgroup_classes\":",Length(cc),
 ",\n\"element_classes\":",Length(cls),",\n\"bad_classes\":",bad,
 ",\n\"omega_class\":",omid,",\n\"omega_centralizer\":",omcent,
 ",\n\"survivors\":",rows,",\n\"rejected\":",rejected,
 ",\n\"maximal_indices\":",maxidx,",\n\"maximal_edges\":",goodEdges,
 ",\n\"source_maximal_anchors\":",anchors,",\n\"deletion_witnesses\":",witnesses,
 ",\n\"survivor_types\":",types,"\n}\n");
 Print("L084_CENSUS_PASS classes=1262 survivors=137 maximal=26 section_regular=66 same_local=65 mixed=71 milliseconds=",Runtime()-t,"\n");
end;;
CensusL084();
QUIT;
