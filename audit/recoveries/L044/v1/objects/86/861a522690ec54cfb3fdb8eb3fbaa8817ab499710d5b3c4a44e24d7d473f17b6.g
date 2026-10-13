# L044 primitive-parabolic finite boundary, GAP 4.15.1/PrimGrp.
# The prefix census body is reused verbatim from accepted L047, apart from
# its name and returned report. New target ranks are explicitly listed below.
# Required computational premise, not a diagnostic or source rank table.
# Exhaustive connected string C-markings in the bounded primitive residuals.
# Search symmetries only conjugate the entire fixed prefix; every pruning test
# is necessary for an independent string C-marking. Accepted tuples get full IP.
SizeScreen([100000,100000]);;
L044Census:=function(n,id,target,maxrank)
 local G,inv,solutions,nodes,recursor,AllIP,Independent,N,pp,sol;
 if id=0 then G:=AlternatingGroup(n);else G:=PrimitiveGroup(n,id);fi;solutions:=[];nodes:=List([0..maxrank],x->0);N:=Normalizer(SymmetricGroup(n),G);
 inv:=Concatenation(List(Filtered(ConjugacyClasses(G),c->Order(Representative(c))=2),Elements));
 Independent:=function(gs)
  local H,i;
  H:=Subgroup(G,gs);
  return ForAll([1..Length(gs)],i->Subgroup(G,gs{Difference([1..Length(gs)],[i])})<>H);
 end;
 AllIP:=function(gs)
  local H,m,k,v,i;
  H:=List([0..2^Length(gs)-1],m->Subgroup(G,gs{Filtered([1..Length(gs)],i->QuoInt(m,2^(i-1)) mod 2=1)}));
  for m in [0..Length(H)-1] do for k in [0..Length(H)-1] do
   v:=Sum(Filtered([0..Length(gs)-1],i->QuoInt(m,2^i) mod 2=1 and QuoInt(k,2^i) mod 2=1),i->2^i);
   if Intersection(H[m+1],H[k+1])<>H[v+1] then return false;fi;
  od;od;return true;
 end;
 recursor:=function(gs,stab,H)
  local cand,reps,x,new,J,types,i,tail,mid,cent,q;
  nodes[Length(gs)+1]:=nodes[Length(gs)+1]+1;
  if H=G then
   if Length(gs)>=target and AllIP(gs) then
    types:=List([1..Length(gs)-1],i->Order(gs[i]*gs[i+1]));
    Add(solutions,rec(types:=types,gens:=gs));
   fi;return;
  fi;
  if Length(gs)>=maxrank or Index(G,H)<2^Maximum(0,target-Length(gs)) then return;fi;
  q:=Maximum(0,target-Length(gs)-1);
  if q>0 and Length(gs)>0 then
   cent:=Centralizer(G,H);
   if Index(cent,Centre(H))<2^q then return;fi;
  fi;
  cand:=Filtered(inv,x->not x in H and ForAll(gs{[1..Maximum(0,Length(gs)-1)]},y->x*y=y*x));
  if Length(gs)>0 then cand:=Filtered(cand,x->x*gs[Length(gs)]<>gs[Length(gs)]*x);fi;
  reps:=List(OrbitsDomain(stab,cand,OnPoints),o->o[1]);
  for x in reps do
   new:=Concatenation(gs,[x]);J:=Subgroup(G,new);
   if Independent(new) then
    tail:=Subgroup(G,new{[2..Length(new)]});
    mid:=Subgroup(G,gs{[2..Length(gs)]});
    if Intersection(H,tail)=mid then recursor(new,Centralizer(stab,x),J);fi;
   fi;
  od;
 end;
 Print("START n=",n," id=",id," order=",Size(G)," target=",target," max=",maxrank," involutions=",Length(inv),"\n");
 recursor([],N,TrivialSubgroup(G));
 Print("CASE n=",n," id=",id," order=",Size(G)," nodes=",nodes," complete_high_markings=",Length(solutions),"\n");
 Print("MARKINGS=",solutions,"\n");
 for sol in solutions do
  Print("SOLUTION|",n,"|",id,"|",sol.types,"|",List(sol.gens,x->List([1..n],i->i^x)),"\n");
 od;
 return rec(nodes:=nodes,solutions:=solutions);
end;;

L044Omega:=n->Length(FactorsInt(n));;
L044TwoRank:=function(G)
 local P,C;
 P:=SylowSubgroup(G,2);
 C:=ConjugacyClassesSubgroups(P);
 return LogInt(Maximum(List(Filtered(C,c->IsElementaryAbelian(Representative(c))),c->Size(Representative(c)))),2);
end;;
L044Finite:=function()
 local n,id,G,r,cl,cb,iv,H,disposition,residual,expected,t,caseid,R,
 M24orders,bound,control;
 residual:=[];
 for n in [12..24] do
  for id in [1..NrPrimitiveGroups(n)] do
   G:=PrimitiveGroup(n,id);
   if Size(G)>=Factorial(n)/2 or not ForAll(GeneratorsOfGroup(G),g->SignPerm(g)=1) then continue;fi;
   r:=QuoInt(n-3,2)+1;disposition:="";
   if L044Omega(Size(G))<r then disposition:="order_chain";
   else
    cl:=Filtered(ConjugacyClasses(G),c->Order(Representative(c))=2);
    H:=Subgroup(G,Concatenation(List(cl,Elements)));
    cb:=List(cl,c->1+L044Omega(QuoInt(Size(G),Size(c))));
    if H<>G then disposition:="not_involution_generated";
    elif Maximum(cb)<r then disposition:="endpoint_centralizer_chain";
    elif [n,id]=[12,1] or [n,id]=[13,7] then
     t:=L044TwoRank(G);
     if t<>2 or 2*t>=r then Error("two-rank bound failed");fi;
     disposition:="alternating_colours_two_rank_2";
    elif [n,id]=[15,4] then
     if IsomorphismGroups(G,AlternatingGroup(8))=fail or 6>=r then Error("A8 Whiston bound failed");fi;
     disposition:="A8_Whiston_six";
    elif [n,id]=[24,1] then
     M24orders:=Set(List(cl,c->QuoInt(Size(G),Size(c))));
     if M24orders<>[7680,21504] or r-2<9 or Maximum(M24orders)>=2^(2*r-4) then Error("M24 endpoint-tail bound failed");fi;
     disposition:="M24_Conder_tail";
    else Add(residual,[n,id]);disposition:="new_exact_prefix_census";
    fi;
   fi;
   Print("SCREEN|",n,"|",id,"|",Size(G),"|",r,"|",disposition,"\n");
  od;
 od;
 expected:=Concatenation([[12,2]],List([7,10,11,12,13,15,16,17,18,19,20],id->[16,id]));
 if residual<>expected then Error("unexpected primitive frontier");fi;
 G:=PrimitiveGroup(12,2);
 if L044TwoRank(G)<>3 then Error("M12 rank upper limit");fi;
 R:=L044Census(12,2,5,6);
 if Length(R.solutions)<>0 then Error("M12 high marking exists");fi;
 for caseid in [7,10,11,12,13,15,16,17,18,19,20] do
  G:=PrimitiveGroup(16,caseid);H:=Socle(G);
  if Size(H)<>16 or not IsElementaryAbelian(H) then Error("affine16 irreducible module boundary");fi;
  # The accepted normal-module/Whiston argument bounds rank by seven.
  # This fresh search excludes the only remaining rank, exactly seven.
  R:=L044Census(16,caseid,7,7);
  if Length(R.solutions)<>0 then Error("affine16 rank-seven marking exists");fi;
 od;
 for n in [25..63] do
  bound:=n*Product([0..LogInt(n,2)-1],j->n-2^j);
  r:=QuoInt(n-3,2)+1;
  if bound>=2^(2*r-1) then Error("Maroti finite integer interval");fi;
 od;
 control:=L044Census(6,1,3,3);
 if Length(control.solutions)=0 then Error("positive A5 marking control lost");fi;
 Print("PASS_L044_PRIMITIVE_BOUNDARY|residuals=12|integer_cases=39|positive_A5=",Length(control.solutions),"\n");
end;;
L044Finite();
QUIT;
