# Add actual primitive coset-action checks to the unchanged sparse shadow core.
# No prior-census geometry premise is retained by this wrapper.
Read("shadow_residues_sparse.g");;
L096SparseLocal:=L096Local;;
L096Local:=function(G,H,labels)
 local r,order,i,C,phi,degree,checked,truths,indices;
 r:=L096SparseLocal(G,H,labels);
 Unbind(r.primitivity_status);checked:=[];truths:=[];indices:=[];
 order:=SortedList([1..Length(H)],function(i,j)
  if Index(G,H[i])=Index(G,H[j]) then return i<j;fi;
  return Index(G,H[i])<Index(G,H[j]);end);
 for i in order do
  degree:=Index(G,H[i]);Add(checked,labels[i]);Add(indices,degree);
  if degree<2 then Add(truths,false);
  else
   C:=RightCosets(G,H[i]);phi:=ActionHomomorphism(G,C,OnRight);
   Add(truths,IsPrimitive(Image(phi),[1..degree]));
  fi;
  if truths[Length(truths)] then break;fi;
 od;
 r.primitive_checked_types:=checked;r.primitive_types:=truths;
 r.primitive_checked_degrees:=indices;
 r.primitivity_status:="computed_actual_coset_actions_in_increasing_index_order";
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
