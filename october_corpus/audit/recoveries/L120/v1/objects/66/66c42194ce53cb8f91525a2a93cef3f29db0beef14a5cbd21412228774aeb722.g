SizeScreen([100000,100000]);;
Read("/Users/sasha/medusa/research/leemans/topic_B_L044_small_maxima_v1/author_validation/A10/records.g");;
DualCounts:=function(label,G,N,lists)
 local rank,ts,t,h,count,self,witnesses,orders;
 for rank in [3..Length(lists)] do
  ts:=Filtered(lists[rank],t->Group(t)=G);
  if Length(ts)=0 then continue;fi;
  count:=Length(ts);self:=0;witnesses:=[];
  for t in ts do
   h:=RepresentativeAction(N,t,Reversed(t),OnTuples);
   if h<>fail then
    if List(t,x->x^h)<>Reversed(t) then Error("false reversal witness");fi;
    self:=self+1;Add(witnesses,List([1..LargestMovedPoint(N)],i->i^h));
   else Add(witnesses,fail);fi;
  od;
  if (count+self) mod 2<>0 then Error("nonintegral reversal orbit count");fi;
  Print("DUAL|",label,"|",rank,"|",count,"|",self,"|",(count+self)/2,"\n");
  Print("WITNESSES|",label,"|",rank,"|",witnesses,"\n");
 od;
end;;
lists:=[];;
for rank in [1..Length(recordedMarks)] do
 if IsBound(recordedMarks[rank]) then lists[rank]:=List(recordedMarks[rank],ids->List(ids,i->recordedInvolutions[i]));else lists[rank]:=[];fi;
od;
DualCounts("A10",AlternatingGroup(10),SymmetricGroup(10),lists);
Read("s5_arrays.g");;
tuples:=List(s5Arrays,a->List(a,PermList));;G:=Group(tuples[1]);;N:=Normalizer(SymmetricGroup(6),G);;
if Size(G)<>120 or Size(N)<>120 or IsomorphismGroups(G,SymmetricGroup(5))=fail then Error("S5 action identity");fi;
DualCounts("S5",G,N,List([1..4],r->Filtered(tuples,t->Length(t)=r)));
Print("PASS_RETAINED_LIST_DUALITY\n");QUIT;
