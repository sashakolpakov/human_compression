# New bounded label invariants, not a repeat of any shadow or subgroup census.
# Run from study root. The two whole retained input files remain required data.
SizeScreen([1000000,1000000]);;
Need:=function(b,s) if not b then Error(s);fi;end;;
Girth:=function(adj)
 local n,best,s,d,p,q,u,v;
 n:=Length(adj);best:=n+1;
 for s in [1..n] do
  d:=List([1..n],i->-1);p:=List([1..n],i->0);d[s]:=0;q:=[s];
  for u in q do for v in adj[u] do
   if d[v]=-1 then d[v]:=d[u]+1;p[v]:=u;Add(q,v);
   elif p[u]<>v then best:=Minimum(best,d[u]+d[v]+1);fi;
  od;od;
 od;return best;
end;;
CheckM22:=function(inputs)
 local G,A,OnH,k,H,ix,iy,C,x,D,y,good,rr,ss,ii,jj,fixed,K,P,Q,pp,qq,adj,i,j;
 G:=Group(Concatenation(inputs[1].parabolic_generators));
 A:=AutomorphismGroup(G);OnH:=function(H,a)return Image(a,H);end;
 Need(Size(A)=887040,"retained M22 automorphism model");
 for k in [3,5] do
  H:=List(inputs[k].parabolic_generators,Group);ix:=[];iy:=[];
  for i in [1..3] do if Size(H[i])=48 then Add(ix,i);else Add(iy,i);fi;od;
  Need(Length(ix)=2 and Length(iy)=1 and Size(H[iy[1]])=660,"M22 signature");
  C:=Stabilizer(A,H[iy[1]],OnH);x:=RepresentativeAction(C,H[ix[1]],H[ix[2]],OnH);
  if x=fail then good:=false;else
   D:=Stabilizer(C,H[ix[2]],OnH);
   y:=RepresentativeAction(D,Image(x,H[ix[2]]),H[ix[1]],OnH);
   good:=y<>fail;
   if good then
    Need(Image(x*y,H[ix[1]])=H[ix[2]] and Image(x*y,H[ix[2]])=H[ix[1]],"actual family swap");
   fi;
  fi;
  Need(good=(k=5),"M22 expected correlation distinction");
  Print("M22_SWAP|",k,"|",Size(C),"|",good,"\n");
 od;
 for rr in inputs do
  if rr.member="prior_m22.rk4" and rr.active in [11,12] then
   H:=List(rr.parabolic_generators,Group);ss:=List(H,h->Index(G,h));
   ii:=Position(ss,1540);jj:=Position(ss,330);fixed:=Difference([1..4],[ii,jj]);
   K:=Intersection(List(fixed,j->H[j]));P:=Intersection(K,H[ii]);Q:=Intersection(K,H[jj]);
   pp:=List(RightCosets(K,P),AsSet);qq:=List(RightCosets(K,Q),AsSet);
   adj:=List([1..Length(pp)+Length(qq)],i->[]);
   for i in [1..Length(pp)] do for j in [1..Length(qq)] do
    if Intersection(pp[i],qq[j])<>[] then Add(adj[i],Length(pp)+j);Add(adj[Length(pp)+j],i);fi;
   od;od;
   Need(Set(List(adj,Length))=[3],"cubic residue");
   if rr.active=11 then Need(Girth(adj)=8 and Length(adj)=30,"4.7 residue");
   else Need(Girth(adj)=6 and Length(adj)=14,"4.8 residue");fi;
   Print("M22_RESIDUE|",rr.active,"|",Size(K),"|",Length(adj),"|",Girth(adj),"|",adj,"\n");
  fi;
 od;
end;;
CheckJ3:=function(inputs)
 local G,k,H,ix,iy,C,i,good,z,B;
 G:=Group(Concatenation(inputs[1].parabolic_generators));
 for k in [9,10,11] do
  H:=List(inputs[k].parabolic_generators,Group);ix:=[];iy:=[];
  for i in [1..3] do if Size(H[i])=96 then Add(ix,i);else Add(iy,i);fi;od;
  Need(Length(ix)=2 and Length(iy)=1,"J3 signature");
  C:=H[iy[1]];Need(Size(C)=2448,"PSL2(17) parabolic");
  Need(Normalizer(G,C)=C,"complete normalizer domain");
  good:=[];
  for z in Elements(C) do
   if H[ix[1]]^z=H[ix[2]] and H[ix[2]]^z=H[ix[1]] then Add(good,z);fi;
  od;
  B:=Intersection(H);Need(Size(B)=8,"J3 Borel");
  Need(ForAll(good,z->z^2 in B),"actual central involution");
  if k=10 then Need(Length(good)=0,"3.9 absent inner swap");
  else Need(Length(good)=8,"3.8 central swap");fi;
  Print("J3_SWAP|",k,"|",Size(C),"|",Length(good),"|",true,"\n");
 od;
end;;
Read("topic_D_L096_M22_extension/prior_inputs.g");;
CheckM22(L096Inputs);;
Read("topic_D_L096_J3_extension/archive_data/inputs.g");;
CheckJ3(L096Inputs);;
Print("LABEL_INVARIANTS_PASS\n");
QUIT;
