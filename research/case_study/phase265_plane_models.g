# Literal flag relations and complete deleted-pencil residue graphs.
Need:=function(b,s) if not b then Error(s);fi;end;
Normalize:=function(v)
 local a;
 a:=First(v,x->not IsZero(x));Need(a<>fail,"nonzero projective vector");return v/a;
end;
Affine:=function(d,q)
 local K,V,dirs,v,w,lines;
 K:=GF(q);V:=Tuples(Elements(K),d);dirs:=Set(List(Filtered(V,v->not IsZero(v)),Normalize));lines:=[];
 for v in V do for w in dirs do AddSet(lines,Set(List(Elements(K),a->Position(V,v+a*w))));od;od;
 return rec(name:=Concatenation("AG",String(d),",",String(q)),v:=Length(V),blocks:=lines);
end;
Projective:=function(d,q)
 local K,V,lines,i,j,L,a,b;
 K:=GF(q);V:=Set(List(Filtered(Tuples(Elements(K),d+1),v->not IsZero(v)),Normalize));lines:=[];
 for i in [1..Length(V)] do for j in [i+1..Length(V)] do
  L:=[];
  for a in Elements(K) do for b in Elements(K) do
   if not (IsZero(a) and IsZero(b)) then AddSet(L,Position(V,Normalize(a*V[i]+b*V[j])));fi;
  od;od;AddSet(lines,L);
 od;od;
 return rec(name:=Concatenation("PG",String(d),",",String(q)),v:=Length(V),blocks:=lines);
end;
Check:=function(S,expectedComponents,expectedGirth,expectedDiameter)
 local v,blocks,k,r,flags,p,L,D,E,i,j,cs,cp,want,outside,right,a,M,adj,root,dist,parent,queue,pos,x,y,girth,diam,comps,seen,profile;
 v:=S.v;blocks:=S.blocks;k:=Length(blocks[1]);r:=(v-1)/(k-1);
 Need(ForAll(blocks,L->Length(L)=k),"line uniformity");
 Need(ForAll(Combinations([1..v],2),P->Number(blocks,L->IsSubset(L,P))=1),"unique joining line");
 Need(ForAll([1..v],p->Number(blocks,L->p in L)=r),"point uniformity");
 flags:=[];for p in [1..v] do for L in blocks do if p in L then Add(flags,[p,L]);fi;od;od;
 D:=List(flags,f->Filtered([1..Length(flags)],j->f[1] in flags[j][2] and not flags[j][1] in f[2]));
 E:=List([1..Length(flags)],j->Filtered([1..Length(flags)],i->j in D[i]));
 Need(ForAll(D,row->Length(row)=v-k),"literal directed degrees");
 for i in [1..Length(flags)] do for j in [i+1..Length(flags)] do
  cs:=Length(Intersection(D[i],D[j]));cp:=Length(Intersection(E[i],E[j]));
  if flags[i][1]=flags[j][1] then Need(cs=(r-2)*(k-1),"same-point signature");else Need(cs in [0,k-2],"different-point signature");fi;
  if flags[i][2]=flags[j][2] then Need(cp=(k-2)*(r-1),"same-line signature");else Need(cp in [0,r-2],"different-line signature");fi;
 od;od;
 L:=blocks[1];p:=L[1];outside:=Difference([1..v],L);right:=[];
 for a in Difference(L,[p]) do for M in blocks do if a in M and M<>L then Add(right,[a,M]);fi;od;od;
 adj:=List([1..Length(outside)+Length(right)],i->[]);
 for i in [1..Length(outside)] do for j in [1..Length(right)] do
  if outside[i] in right[j][2] then Add(adj[i],Length(outside)+j);Add(adj[Length(outside)+j],i);fi;
 od;od;
 Need(Set(List(adj,Length))=[k-1],"every residue degree");
 girth:=Length(adj)+1;diam:=0;comps:=[];seen:=[];
 for root in [1..Length(adj)] do
  dist:=List(adj,x->-1);parent:=List(adj,x->0);dist[root]:=0;queue:=[root];pos:=1;
  while pos<=Length(queue) do
   x:=queue[pos];pos:=pos+1;
   for y in adj[x] do
    if dist[y]=-1 then dist[y]:=dist[x]+1;parent[y]:=x;Add(queue,y);
    elif parent[x]<>y then girth:=Minimum(girth,dist[x]+dist[y]+1);fi;
   od;
  od;
  diam:=Maximum(diam,Maximum(dist));
  if not root in seen then Add(comps,Length(queue));UniteSet(seen,Set(queue));fi;
 od;
 Need(Length(comps)=expectedComponents and girth=expectedGirth and diam=expectedDiameter,"entire residue invariants");
 Print("PHASE265_PLANE_PASS ",S.name," flags",Length(flags)," all_signature_pairs",Length(flags)*(Length(flags)-1)/2,
 " residue_components",comps," girth",girth," diameter",diam,"\n");
end;
Check(Projective(2,2),1,8,4);
Check(Projective(2,3),1,6,4);
Check(Projective(2,4),1,6,4);
Check(Projective(2,5),1,6,4);
Check(Affine(2,3),1,12,6);
Check(Affine(2,4),1,6,4);
Check(Affine(2,5),1,6,4);
Check(Projective(3,2),3,8,4);
Check(Affine(3,3),4,12,6);
Print("PHASE265_ALL_NINE_MODELS_PASS\n");
QUIT;
