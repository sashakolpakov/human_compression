Read("shadow_residues_sparse.g");;Read("archive_data/inputs.g");;
for row in [7,8,9,10,11] do
 H:=List(L096Inputs[row].parabolic_generators,Group);I:=[1..3];r:=[];
 for J in Filtered(Combinations(I),s->Length(s)>0) do
  K:=Intersection(List(J,i->H[i]));
  d:=rec(types:=J,order:=Size(K),derived_order:=Size(DerivedSubgroup(K)),center_order:=Size(Centre(K)),class_shape:=SortedList(List(ConjugacyClasses(K),c->[Order(Representative(c)),Size(c)])));
  Add(r,d);
 od;
 Print("STRUCTURE|",L096JSON(rec(row:=row,subgroups:=r)),"\n");
od;
Print("PASS_LOCAL_STRUCTURE\n");QUIT;
