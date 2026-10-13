LoadPackage("grape");;
Need:=function(ok) if not ok then Error("independent L059 control failed");fi;end;;
Read("/Users/sasha/medusa/research/leemans/corpus106_L059_principal_v1/maximal_descent.g");;
Read("/Users/sasha/medusa/research/leemans/corpus106_L059_principal_v1/maximal_descent_arcs.g");;
Read("subdivision_markings.g");;
CosetRows:=L059SubdivisionRows;;
Read("subdivision_actual_actions.g");;
SameClasses:=function(A,L,R)
 local unused,H,j;
 if Length(L)<>Length(R) then return false;fi;
 unused:=[1..Length(R)];
 for H in L do
  j:=PositionProperty(unused,i->IsConjugate(A,H,R[i]));
  if j=fail then return false;fi;
  Remove(unused,j);
 od;
 return IsEmpty(unused);
end;;
Graphs:=[];;
Add(Graphs,rec(name:="cycle4",n:=4,black:=[1,3],edges:=[[1,2],[2,3],[3,4],[1,4]]));;
Add(Graphs,rec(name:="cycle6",n:=6,black:=[1,3,5],edges:=[[1,2],[2,3],[3,4],[4,5],[5,6],[1,6]]));;
Add(Graphs,rec(name:="K33",n:=6,black:=[1,2,3],edges:=Concatenation(List([1..3],u->List([4..6],v->[u,v])))));;
Add(Graphs,rec(name:="cube",n:=8,black:=[1,4,6,7],edges:=Filtered(Combinations([1..8],2),e->Number([0..2],i->QuoInt(e[1]-1,2^i) mod 2<>QuoInt(e[2]-1,2^i) mod 2)=1)));;
Add(Graphs,rec(name:="K4",n:=4,black:=fail,edges:=Combinations([1..4],2)));;
RunControls:=function()
 local edgeTotal,arcTotal,extensionTotal,data,edgeSet,X,F,arcs,allF,reference,candidate,A,allA,referenceE,candidateE,R,extended,oldRows,newRows;
edgeTotal:=0;;arcTotal:=0;;extensionTotal:=0;;
for data in Graphs do
 edgeSet:=Set(List(data.edges,Set));;
 X:=Graph(Group(()),[1..data.n],OnPoints,function(u,v)return Set([u,v]) in edgeSet;end,true);;
 F:=AutGroupGraph(X);;
 arcs:=Concatenation(List(edgeSet,e->[e,Reversed(e)]));;
 allF:=List(ConjugacyClassesSubgroups(F),Representative);;
 reference:=Filtered(allF,H->IsTransitive(H,arcs,OnTuples));;
 candidate:=List(L059DescentArcs(F,arcs),Representative);;
 Need(SameClasses(F,candidate,reference));
 Need(not SameClasses(F,Concatenation(candidate,[candidate[1]]),reference));
 Need(not SameClasses(F,candidate{[2..Length(candidate)]},reference));
 arcTotal:=arcTotal+Length(reference);
 if data.black<>fail then
  A:=Stabilizer(F,Set(data.black),OnSets);;
  allA:=List(ConjugacyClassesSubgroups(A),Representative);;
  referenceedgeSet:=Filtered(allA,H->IsTransitive(H,edgeSet,OnSets));;
  candidateedgeSet:=List(L059Descent(A,edgeSet),Representative);;
  Need(SameClasses(A,candidateE,referenceE));
  edgeTotal:=edgeTotal+Length(referenceE);
  if ForAll([1..data.n],u->Number(edgeSet,e->u in e)=3) then
   R:=rec(F:=F,A:=A,edges:=edgeSet,label:=data.name,n:=data.n,witnesses:=List(candidateE,H->rec(H:=H)));;
   extended:=L059SubdivisionFromBipartite(R);;
   Need(SameClasses(F,List(extended.witnesses,r->r.H),reference));
   oldRows:=CosetRows(F,edgeSet,reference);;
   newRows:=L059SubdivisionRows(F,edgeSet,reference);;
   Need(oldRows=newRows);
   extensionTotal:=extensionTotal+Length(reference);
  fi;
 fi;
 Print("CONTROL ",data.name," Aut=",Size(F)," arc_classes=",Length(reference),"\n");
od;
Print("PASS_METHOD_CONTROLS graphs=",Length(Graphs)," edge_classes=",edgeTotal," arc_classes=",arcTotal," extension_classes=",extensionTotal," missing_duplicate_controls=10\n");
end;;
RunControls();;
QUIT;
