# Genuine primitive coset-action predicate via a complete maximality test.
# No accepted census or unproved primitive-action metadata is imported.
Read("shadow_residues_sparse.g");;
L096MaximalByDoubleCosets:=function(G,H)
 local d,g,K,n,outside,orders;
 if H=G then return rec(value:=false,index:=1,reason:="degree_one_excluded",tested:=0);fi;
 n:=0;orders:=[];outside:=Filtered(DoubleCosets(G,H,H),d->not Representative(d) in H);
 for d in outside do
  g:=Representative(d);n:=n+1;K:=ClosureGroup(H,g);Add(orders,Size(K));
  if Size(K)<Size(G) then
   return rec(value:=false,index:=Index(G,H),tested:=n,outside_double_cosets:=Length(outside),generated_orders:=orders,
    intermediate_order:=Size(K),intermediate_generators:=List(GeneratorsOfGroup(K),x->ListPerm(x,LargestMovedPoint(G))),
    outside_representative:=ListPerm(g,LargestMovedPoint(G)));
  fi;
 od;
 return rec(value:=true,index:=Index(G,H),tested:=n,outside_double_cosets:=Length(outside),generated_orders:=orders);
end;;
L096SparseLocal:=L096Local;;
L096Local:=function(G,H,labels)
 local r,order,i,c,checked,truths,indices,certs;
 r:=L096SparseLocal(G,H,labels);
 Unbind(r.primitivity_status);checked:=[];truths:=[];indices:=[];certs:=[];
 order:=SortedList([1..Length(H)],function(i,j)
  if Index(G,H[i])=Index(G,H[j]) then return i<j;fi;
  return Index(G,H[i])<Index(G,H[j]);end);
 for i in order do
  c:=L096MaximalByDoubleCosets(G,H[i]);Add(certs,c);
  Add(checked,labels[i]);Add(indices,Index(G,H[i]));Add(truths,c.value);
  if c.value then break;fi;
 od;
 r.primitive_checked_types:=checked;r.primitive_types:=truths;
 r.primitive_checked_degrees:=indices;r.primitive_certificates:=certs;
 r.primitivity_status:="computed_exact_double_coset_maximality";
 return r;
end;;
L096SparseAllResidues:=L096AllResidues;;
L096AllResidues:=function(inp)
 local r;
 r:=L096SparseAllResidues(inp);
 if IsBound(r.residues) then
  Unbind(r.retained_RWPRI);Unbind(r.retained_RWPRI_basis);
  r.filters.RWPRI:=ForAll(r.residues,x->ForAny(x.primitive_types,y->y));
  r.tested_geometry_checks_pass:=ForAll(RecNames(r.filters),s->r.filters.(s));
  r.source_filter_pass:=r.tested_geometry_checks_pass;
 fi;
 return r;
end;;
