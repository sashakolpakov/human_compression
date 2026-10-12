# Concrete local 2T obstructions in the supplied M12 archive; no shadow search.
Read("shadow_residues.g");;
Read("data_m12/inputs.g");;
for inp in L096Inputs do
 G:=Group(Concatenation(inp.parabolic_generators));;H:=[];;for gs in inp.parabolic_generators do Add(H,Subgroup(G,gs));od;n:=Length(H);;B:=Intersection(H);;
 for i in [1..n] do
  P:=Intersection(H{Difference([1..n],[i])});;C:=RightCosets(P,B);;a:=ActionHomomorphism(P,C,OnRight);;o:=List(Orbits(Image(a,B),[1..Length(C)]),Length);;
  if Length(o)<>2 then
   Print("PANEL_FAILURE|",L096JSON(rec(member:=inp.member,active_row:=inp.active,construction_row:=inp.construction,remaining_type:=i,panel_order:=Size(P),borel_order:=Size(B),panel_size:=Length(C),image_order:=Size(Image(a)),kernel_order:=Size(Kernel(a)),point_stabilizer_orbit_lengths:=SortedList(o))),"\n");
  fi;
 od;
od;
Print("PASS_PANEL_OBSTRUCTIONS\n");QUIT;
