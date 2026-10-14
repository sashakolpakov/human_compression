# Complete bounded part of the projective-line classification.
SetInfoLevel(InfoWarning,0);
IsLocalTwo := function(H,B)
 local k;k:=Index(H,B);
 return k>=2 and Size(B) mod (k-1)=0 and Length(DoubleCosets(H,B,B))=2;
end;
ActSub := function(H,g)return H^g;end;
ActAut := function(H,a)return Image(a,H);end;
ImagesList := function(gs,q)return List(gs,g->List([1..q+1],i->i^g));end;
GraphData := function(G,H,K)
 local B,C0,C1,C,E,edges,z,phi,A,depths,root,stab,path,choices,s,x;
 B:=Intersection(H,K);C0:=RightCosets(G,H);C1:=RightCosets(G,K);C:=Concatenation(C0,C1);
 edges:=[];
 for z in RightTransversal(G,B) do Add(edges,[Position(C0,RightCoset(H,z)),Length(C0)+Position(C1,RightCoset(K,z))]);od;
 if Length(Set(edges))<>Index(G,B) then Error("Duplicate edge");fi;
 E:=List(C,c->[]);for z in edges do Add(E[z[1]],z[2]);Add(E[z[2]],z[1]);od;
 phi:=ActionHomomorphism(G,C,OnRight);A:=Image(phi);
 if Size(A)<>Size(G) then Error("Unfaithful action");fi;
 depths:=[];
 for root in [1,Length(C0)+1] do
  stab:=Stabilizer(A,root);path:=[root];s:=0;
  while s<20 do
   choices:=Set(E[path[Length(path)]]);
   if Length(path)>1 then RemoveSet(choices,path[Length(path)-1]);fi;
   if Length(Orbits(stab,choices))<>1 then break;fi;
   x:=choices[1];Add(path,x);stab:=Stabilizer(stab,x);s:=s+1;
  od;
  if s=20 then Error("Unexpected unbounded arc depth");fi;
  Add(depths,s);
 od;
 return [Length(C0),Length(C1),depths,edges];
end;
CheckField := function(q)
 local G,C,reps,all,H,K,B,sgn,n,A,NA,NG,candidates,oi,oa,maxH,selected,x,
       ids,i,j,g,swaps,ordered,unordered,graph,row;
 G:=PSL(2,q);C:=ConjugacyClassesSubgroups(G);reps:=List(C,Representative);all:=Concatenation(List(C,AsList));A:=AutomorphismGroup(G);
 if Size(G)<>q*(q^2-1)/Gcd(2,q-1) then Error("Ambient order");fi;
 Print("FIELD ",[q,Size(G),Length(C),Length(all),Size(A)],"\nEND_FIELD\n");
 for sgn in [-1,1] do
  n:=(q+sgn)/Gcd(2,q-1);selected:=Filtered(reps,H->Size(H)=2*n and IsDihedralGroup(H));
  if Length(selected)<>1 then Error("Full torus class inventory");fi;
  for H in selected do
   maxH:=Length(IntermediateSubgroups(G,H).subgroups)=0;candidates:=[];
   for K in all do
    if Size(K)>=Size(G) or H=K then continue;fi;
    B:=Intersection(H,K);
    if IsLocalTwo(H,B) and IsLocalTwo(K,B) and (maxH or Length(IntermediateSubgroups(G,K).subgroups)=0) then
     if ClosureGroup(H,K)<>G then Error("Generation");fi;Add(candidates,K);
    fi;
   od;
   NG:=Normalizer(G,H);NA:=Stabilizer(A,H,ActAut);oi:=Orbits(NG,candidates,ActSub);oa:=Orbits(NA,candidates,ActAut);
   Print("TORUS ",[q,sgn,Size(H),maxH,Length(candidates),Length(oi),Length(oa)],"\nEND_TORUS\n");
   for x in oa do
    K:=x[1];B:=Intersection(H,K);ids:=Filtered([1..Length(oi)],i->oi[i][1] in x);swaps:=[];
    for i in ids do
     g:=RepresentativeAction(G,oi[i][1],H,ActSub);
     if g=fail then j:=i;else j:=PositionProperty(oi,z->H^g in z);fi;
     if not j in ids then Error("Swap leaves the automorphism orbit");fi;
     Add(swaps,[i,j]);
     if j<>i then
      Print("SWAP ",[q,ImagesList(GeneratorsOfGroup(G),q),ImagesList(GeneratorsOfGroup(H),q),ImagesList(GeneratorsOfGroup(oi[i][1]),q),ImagesList(GeneratorsOfGroup(H^g),q),List([1..q+1],a->a^g)],"\nEND_SWAP\n");
     fi;
    od;
    for row in swaps do if not [row[2],row[1]] in swaps then Error("Swap is not involutory on classes");fi;od;
    ordered:=Length(ids);unordered:=(ordered+Number(swaps,z->z[1]=z[2]))/2;
    if not IsInt(unordered) then Error("Unordered count");fi;
    graph:=GraphData(G,H,K);
    row:=[q,sgn,Size(H),Size(K),Size(B),ordered,unordered,Length(IntermediateSubgroups(G,K).subgroups)=0,StructureDescription(K),StructureDescription(B),graph];
    Print("ROW ",row,"\nEND_ROW\n");
   od;
  od;
 od;
end;
for q in [4,5,7,8,9,11,13,16,17,19,23,25,29,31] do CheckField(q);od;
Print("PASS_COMPLETE_L076_FINITE_CLASSIFICATION\n");
QUIT_GAP(0);
