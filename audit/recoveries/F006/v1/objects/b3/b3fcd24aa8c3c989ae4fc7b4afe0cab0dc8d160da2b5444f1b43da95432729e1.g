# Private bounded search. No source theorem or classification is assumed here.
# Enumerate normalized C-markings, characters and the two missing neighbors.
SizeScreen([100000,100000]);;
Independent:=function(ambient,gs)
 local H,i;
 H:=Subgroup(ambient,gs);
 return ForAll([1..Length(gs)],i->Subgroup(ambient,gs{Difference([1..Length(gs)],[i])})<>H);
end;;
AllIP:=function(ambient,gs)
 local masks,groups,a,b,inter;
 masks:=List([0..2^Length(gs)-1],m->Filtered([1..Length(gs)],i->QuoInt(m,2^(i-1)) mod 2=1));
 groups:=List(masks,s->Subgroup(ambient,gs{s}));
 for a in [1..Length(masks)] do for b in [a+1..Length(masks)] do
  inter:=Intersection(masks[a],masks[b]);
  if Length(inter)=Minimum(Length(masks[a]),Length(masks[b])) then continue;fi;
  if Intersection(groups[a],groups[b])<>groups[Position(masks,inter)] then return false;fi;
 od;od;
 return true;
end;;
LiftDiagonal:=function(h,k)
 return PermList(Concatenation(List([1..k],i->i^h),List([1..k],i->k+i^h)));
end;;
RunNormalizedRank:=function(H,k,label,rank)
 local N,inv,nodes,markings,extension_counts,solutions,r,W,Target,Recurse,Extend,output;
 N:=Normalizer(SymmetricGroup(k),H);
 inv:=Filtered(Elements(H),h->Order(h)=2);
 r:=PermList(Concatenation([k+1..2*k],[1..k]));
 W:=Group(Concatenation([r],GeneratorsOfGroup(SymmetricGroup([1..k])),GeneratorsOfGroup(SymmetricGroup([k+1..2*k]))));
 Target:=Group((1,2));
 nodes:=List([0..rank],i->0);markings:=0;extension_counts:=[0,0,0,0,0,0];solutions:=[];
 Extend:=function(gs)
  local bits,hom,C,l,left,right,dist,xc,yc,xs,ys,x,y,i,full,J,stab,orbs;
  for bits in [0..2^rank-1] do
   hom:=GroupHomomorphismByImages(H,Target,gs,List([1..rank],i->(1,2)^(QuoInt(bits,2^(i-1)) mod 2)));
   if hom=fail then continue;fi;
   extension_counts[1]:=extension_counts[1]+1;
   C:=List([1..rank],i->LiftDiagonal(gs[i],k)*r^(QuoInt(bits,2^(i-1)) mod 2));
   for l in [0..rank] do
    left:=C{[1..l]};right:=C{[l+1..rank]};
    if not ForAll(left,x->ForAll(right,y->x*y=y*x)) then continue;fi;
    dist:=Minimum(l+1,rank+1-l);
    full:=Concatenation(left,[(),r,()],right);
    if ForAny([1..Length(full)],i->1^full[i]>k and Minimum(i-1,Length(full)-i)<dist) then continue;fi;
    extension_counts[2]:=extension_counts[2]+1;
    xc:=Centralizer(W,Group(Concatenation(left{[1..Maximum(0,l-1)]},right,[()])));
    yc:=Centralizer(W,Group(Concatenation(left,right{[Minimum(2,Length(right)+1)..Length(right)]},[()])));
    xs:=Filtered(Elements(xc),x->Order(x)=2 and x*r<>r*x and (1^x<=k or Minimum(l,rank+2-l)>=dist));
    ys:=Filtered(Elements(yc),y->Order(y)=2 and y*r<>r*y and (1^y<=k or Minimum(l+2,rank-l)>=dist));
    extension_counts[3]:=extension_counts[3]+Length(xs);
    extension_counts[4]:=extension_counts[4]+Length(ys);
    # Quotient x choices by simultaneous conjugations fixing r and all of C.
    stab:=Centralizer(W,Group(Concatenation(C,[r])));
    orbs:=OrbitsDomain(stab,xs,OnPoints);
    for x in List(orbs,o->o[1]) do for y in ys do
     if x*y<>y*x then continue;fi;
     full:=Concatenation(left,[x,r,y],right);
     J:=Group(full);
     if not IsTransitive(J,[1..2*k]) then continue;fi;
     extension_counts[5]:=extension_counts[5]+1;
     if not Independent(W,full) then continue;fi;
     extension_counts[6]:=extension_counts[6]+1;
     if AllIP(W,full) then Add(solutions,rec(C:=gs,character_bits:=bits,split:=l,gens:=full));fi;
    od;od;
   od;
  od;
 end;
 Recurse:=function(gs,stab,J)
  local cand,reps,x,new,K;
  nodes[Length(gs)+1]:=nodes[Length(gs)+1]+1;
  if Length(gs)=rank then
   if J=H and AllIP(H,gs) then markings:=markings+1;Extend(gs);fi;
   return;
  fi;
  if J=H or Index(H,J)<2^(rank-Length(gs)) then return;fi;
  cand:=Filtered(inv,x->not x in J and ForAll(gs{[1..Maximum(0,Length(gs)-1)]},y->x*y=y*x));
  reps:=List(OrbitsDomain(stab,cand,OnPoints),o->o[1]);
  for x in reps do
   new:=Concatenation(gs,[x]);K:=Subgroup(H,new);
   if Independent(H,new) then Recurse(new,Centralizer(stab,x),K);fi;
  od;
 end;
 Recurse([],N,TrivialSubgroup(H));
 output:=rec(label:=label,k:=k,rank:=rank,nodes:=nodes,markings:=markings,extension_counts:=extension_counts,solutions:=solutions);
 Print("BOUNDARY_RESULT=",output,"\n");
 if markings=0 then Error("No maximal marking found");fi;
 return output;
end;;
RunNormalized:=function(H,k,label)
 return RunNormalizedRank(H,k,label,k-2);
end;;
RunProduct:=function(a,b)
 local H;
 H:=Group(Concatenation(GeneratorsOfGroup(SymmetricGroup([1..a])),GeneratorsOfGroup(SymmetricGroup([a+1..a+b]))));
 return RunNormalized(H,a+b,Concatenation("S",String(a),"xS",String(b)));
end;;
