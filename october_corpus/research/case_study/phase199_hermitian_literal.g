# Independent direct projective-coordinate check of the source's two
# nontrivial rank-two residues. No author norm-shell or coset code is read.
P199Require:=function(ok,msg) if not ok then Error(msg);fi;end;;
P199BFS:=function(adj,root)
 local d,p,Q,pos,x,y,girth;
 d:=List(adj,x->-1);p:=List(adj,x->0);d[root]:=0;Q:=[root];pos:=1;girth:=infinity;
 while pos<=Length(Q) do
  x:=Q[pos];pos:=pos+1;
  for y in adj[x] do
   if d[y]=-1 then d[y]:=d[x]+1;p[y]:=x;Add(Q,y);
   elif p[x]<>y and p[y]<>x then girth:=Minimum(girth,d[x]+d[y]+1);fi;
  od;
 od;
 P199Require(not -1 in d,"disconnected literal residue");
 return [Maximum(d),girth];
end;;
P199Parameters:=function(left,right,relation)
 local adj,i,j,rows,g;
 adj:=List([1..Length(left)+Length(right)],i->[]);
 for i in [1..Length(left)] do for j in [1..Length(right)] do
  if relation(left[i],right[j]) then
   Add(adj[i],Length(left)+j);Add(adj[Length(left)+j],i);
  fi;
 od;od;
 rows:=List([1..Length(adj)],i->P199BFS(adj,i));
 return rec(vertices:=[Length(left),Length(right)],
  degrees:=[Set(List(adj{[1..Length(left)]},Length)),Set(List(adj{[Length(left)+1..Length(adj)]},Length))],
  diameters:=[Maximum(List(rows{[1..Length(left)]},x->x[1])),Maximum(List(rows{[Length(left)+1..Length(rows)]},x->x[1]))],
  girth:=Minimum(List(rows,x->x[2])));
end;;
P199Literal:=function(q)
 local F,vecs,points,blocks,v,B,p,Q,left,right,R,S,expected,x,y;
 F:=GF(q^2);
 vecs:=Set(List(Filtered(Tuples(Elements(F),3),v->not IsZero(v)),
       v->v/First(v,x->not IsZero(x))));
 points:=Filtered(vecs,v->Sum(List(v,x->x^(q+1)))=Zero(F));
 blocks:=Set(Filtered(List(vecs,v->Filtered([1..Length(points)],
       i->Sum([1..3],j->v[j]*points[i][j])=Zero(F))),B->Length(B)=q+1));
 P199Require(Length(points)=q^3+1 and Length(blocks)=q^2*(q^2-q+1),"literal unital counts");
 P199Require(ForAll(Combinations([1..Length(points)],2),pair->Number(blocks,B->IsSubset(B,pair))=1),"literal unital Steiner property");
 B:=blocks[1];
 left:=Difference([1..Length(points)],B);
 right:=Concatenation(List(B,p->List(Filtered(blocks,Q->Q<>B and p in Q),Q->[p,Q])));
 P199Require(ForAll(right,x->Intersection(B,x[2])=[x[1]]),"literal flag-to-block bridge");
 R:=P199Parameters(left,right,function(x,flag)return x in flag[2] and x<>flag[1];end);
 expected:=6;if IsEvenInt(q) then expected:=5;fi;
 P199Require(R.vertices=[q*(q^2-1),(q+1)*(q^2-1)] and
   R.degrees=[[q+1],[q]] and R.diameters=[expected,6] and R.girth=8,"literal block-residue labels");
 p:=1;left:=Difference([1..Length(points)],[p]);right:=Filtered(blocks,Q->not p in Q);
 S:=P199Parameters(left,right,function(x,Q)return x in Q;end);
 P199Require(S.vertices=[q^3,q^3*(q-1)] and S.degrees=[[q^2-1],[q+1]] and
   S.diameters=[4,4] and S.girth=6,"literal point-residue labels");
 Print("P199_LITERAL_HERMITIAN ",rec(q:=q,unital_points:=Length(points),unital_blocks:=Length(blocks),block_residue:=R,point_residue:=S),"\n");
end;;
for q in [3,4,5] do P199Literal(q);od;
Print("P199_LITERAL_HERMITIAN_PASS\n");
QUIT;
