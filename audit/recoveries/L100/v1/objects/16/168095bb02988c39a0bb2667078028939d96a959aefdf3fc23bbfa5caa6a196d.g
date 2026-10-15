# Three small fixtures: merge old class, add a new same-rank class, add a new rank.
MakeTinyIncrement:=function(G,t,newts,expected,out)
 local gs,A,B,old,aut,par,rank,member,row,i,all,classes,p,q,equal,oracle;
 gs:=GeneratorsOfGroup(G);A:=AutomorphismGroup(G);rank:=Length(t);B:=Intersection(t);
 par:=List([1..rank],i->Group(Concatenation(List(t{Difference([1..rank],[i])},GeneratorsOfGroup))));
 member:=rec(rank:=rank,source:=[2,1],target:=[2,1],type_permutation:=(),generator_images:=gs);
 old:=rec(group_generators:=gs,automorphism_order:=Size(A),input_rows:=[[2,"tiny_acquired_old",[1,1,0],[rank]]],counts:=[[rank,1,1]],
  representatives:=[rec(borel_id:=2,borel_order:=Size(B),source_index:=1,panels:=t,parabolics:=par)],members:=[member]);
 aut:=rec(group_generators:=gs,automorphism_order:=Size(A),automorphism_generator_images:=List(GeneratorsOfGroup(A),a->List(gs,g->Image(a,g))));
 PrintTo(Concatenation(out,"/old.g"),"L100PartialFusion:=",old,";\nL100FullAutData:=",aut,";\n");
 PrintTo(Concatenation(out,"/new_done.g"),"borelResult:=",rec(id:=1,order:=1,levels:=[3,Length(newts),0],geometries:=newts),";\n");
 row:=[1,Concatenation(out,"/new_done.g"),[3,Length(newts),0],List(newts,Length)];
 RunIncrementalFusion(G,[TrivialSubgroup(G)],old,aut,row,out);
 Read(Concatenation(out,"/result.g"));
 if L100CompleteAutFusion.counts<>expected or L100CompleteAutFusion.members{[1..1]}<>old.members then Error("tiny incremental result");fi;
 # Independent complete automorphism/type orbit oracle on all input families.
 all:=Concatenation([par],List(newts,t->List([1..Length(t)],i->Group(Concatenation(List(t{Difference([1..Length(t)],[i])},GeneratorsOfGroup))))));classes:=[];
 for p in all do
  equal:=false;
  for q in classes do
   if Length(p)=Length(q) and ForAny(Elements(A),a->ForAny(Elements(SymmetricGroup(Length(p))),perm->List(p,H->Image(a,H))=Permuted(q,perm))) then equal:=true;break;fi;
  od;
  if not equal then Add(classes,p);fi;
 od;
 if Length(classes)<>Sum(expected,e->e[3]) then Error("independent tiny orbit count");fi;
 Print("PASS_TINY_INCREMENT counts=",expected,"\n");
end;
