# Reuse literal prefix centralizers; the acquired enumeration is unchanged.
batchCentralizers:=[];;batchCentralizerHits:=0;;
BatchPointwiseStabilizer:=function(marks)
 local St,prefix,mark,row,found;
 St:=A;prefix:=[];
 for mark in marks do
  Add(prefix,mark);found:=false;
  for row in batchCentralizers do
   if row.marks=prefix then
    St:=row.group;found:=true;batchCentralizerHits:=batchCentralizerHits+1;break;
   fi;
  od;
  if not found then
   Print("BATCH_CENTRALIZER_BEGIN LENGTH ",Length(prefix)," TIME ",Runtime(),"\n");
   St:=Centralizer(St,mark);
   Add(batchCentralizers,rec(marks:=ShallowCopy(prefix),group:=St));
   Print("BATCH_CENTRALIZER_END LENGTH ",Length(prefix)," TIME ",Runtime(),"\n");
  fi;
 od;
 return St;
end;;
RunLiteralBatchBranch:=function(branch,rank,marks)
 local order,lo,hi,t,k,selected,H,St,D;
 if rank<4 or Length(marks)<>3 then Error("batch rank or prefix length");fi;
 Print("BATCH_BRANCH_BEGIN ",branch," R ",rank," TIME ",Runtime(),"\n");
 if ForAny(marks,x->not x in G or Order(x)<>2) then Error("frontier mark");fi;
 order:=[];lo:=1;hi:=rank;
 while lo<=hi do Add(order,lo);if lo<>hi then Add(order,hi);fi;lo:=lo+1;hi:=hi-1;od;
 t:=List([1..rank],x->());for k in [1..3] do t[order[k]]:=marks[k];od;
 selected:=Set(order{[1..3]});H:=Group(t{selected});
 if not PartialC(t,selected,H) or H=G then Error("invalid proper prefix");fi;
 St:=BatchPointwiseStabilizer(marks);
 nodes:=List([0..rank],x->0);leaves:=[];
 VisitEnds(rank,order,t,selected,H,St);
 D:=Maximum(Filtered([0..rank],i->nodes[i+1]>0));
 Print("BATCH_BRANCH_RESULT ",branch," R ",rank," D ",D," NODES ",nodes," LEAF_COUNT ",Length(leaves),"\n");
 Print("BATCH_BRANCH_TUPLES ",branch," R ",rank," ",leaves,"\n");
 Print("COMPLETE_BATCH_BRANCH ",branch," R ",rank," TIME ",Runtime(),"\n");
 return rec(depth:=D,nodes:=nodes,leaves:=leaves);
end;;
