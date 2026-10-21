# Exact finite coset recognition and all-rank geometric shadow tests.
# This is geometric shadow IP, not distinguished-generator subgroup IP.
SizeScreen([1000000,1000000]);;
L096ComputeShadow:=true;;
L096RankTwoShortcut:=true;;
L096JSON:=function(x)
 local names;
 if x=true then return "true";elif x=false then return "false";
 elif IsInt(x) then return String(x);
 elif IsList(x) and Length(x)=0 then return "[]";
 elif IsString(x) then return Concatenation("\"",x,"\"");
 elif IsRecord(x) then names:=Set(RecNames(x));return Concatenation("{",JoinStringsWithSeparator(List(names,n->Concatenation(L096JSON(n),":",L096JSON(x.(n)))),","),"}");
 elif IsList(x) then return Concatenation("[",JoinStringsWithSeparator(List(x,L096JSON),","),"]");fi;
 Error("unsupported output type");
end;;
L096Local:=function(G,H,labels)
 local n,sets,HG,acts,base,sh,i,T,C,phi,pt,expected,j,ft,ext,
 K,dc,h,inter,a,sx,sf,inc,U,q,good,witness,tested,failures,
 allgood,witness_tests,primitive,connected,generated,degree;
 n:=Length(H);sets:=Combinations([1..n]);
 HG:=List(sets,T->Intersection(Concatenation([G],H{T})));
 acts:=[];base:=[];sh:=[];primitive:=[];
 for i in [1..n] do
  C:=RightCosets(G,H[i]);phi:=ActionHomomorphism(G,C,OnRight);
  pt:=Position(C,RightCoset(H[i],One(G)));degree:=Length(C);
  Add(acts,phi);Add(base,pt);
  Add(sh,List(HG,A->Set(Orbit(Image(phi,A),pt))));
  if not ForAny(primitive,x->x) then Add(primitive,degree>=2 and IsPrimitive(Image(phi),[1..degree]));fi;
 od;
 ft:=true;ext:=0;
 for i in [1..n] do for T in [1..Length(sets)] do
  if not i in sets[T] then
   expected:=[1..Index(G,H[i])];
   for j in sets[T] do expected:=Intersection(expected,sh[i][Position(sets,[j])]);od;
   if expected<>sh[i][T] then ft:=false;fi;ext:=ext+1;
  fi;
 od;od;
 generated:=Group(Concatenation(List(H,GeneratorsOfGroup)));
 connected:=n<2 or generated=G;
 if not ft then return rec(types:=labels,order:=Size(G),parabolic_orders:=List(H,Size),flag_transitive:=false,extension_tests:=ext,primitive_checked_types:=labels{[1..Length(primitive)]},primitive_types:=primitive,connected:=connected);fi;
 if n=1 then
  phi:=acts[1];degree:=Index(G,H[1]);
  return rec(types:=labels,order:=Size(G),parabolic_orders:=List(H,Size),flag_transitive:=true,extension_tests:=ext,primitive_checked_types:=labels{[1..Length(primitive)]},primitive_types:=primitive,connected:=true,panel_size:=degree,firm:=degree>=2,two_transitive:=degree>=2 and Length(Orbits(Image(phi,H[1]),[1..degree]))=2);
 fi;
 if n>=3 and not L096ComputeShadow then return rec(types:=labels,order:=Size(G),parabolic_orders:=List(H,Size),flag_transitive:=true,extension_tests:=ext,primitive_checked_types:=labels{[1..Length(primitive)]},primitive_types:=primitive,connected:=connected,shadow_computed:=false);fi;
 allgood:=[];tested:=0;failures:=[];witness_tests:=0;
 for i in [1..n] do
  good:=true;
  if n=2 and L096RankTwoShortcut then
   j:=3-i;sx:=sh[i][Position(sets,[j])];
   for dc in DoubleCosets(G,H[j],H[j]) do
    h:=Representative(dc);if h in H[j] then continue;fi;inter:=Intersection(sx,OnSets(sx,Image(acts[i],h)));tested:=tested+1;
    if Length(inter)>1 and Length(inter)<>Index(G,H[i]) then
     good:=false;Add(failures,rec(type:=labels[i],element_type:=labels[j],flag_types:=[labels[j]],representative:=ListPerm(h,LargestMovedPoint(G)),intersection:=inter,method:="rank_two_common_neighbors"));break;
    fi;
   od;
  else
   for j in Difference([1..n],[i]) do
    K:=Intersection(H[i],H[j]);sx:=sh[i][Position(sets,[j])];
    for T in [1..Length(sets)] do
     if Length(sets[T])=0 or i in sets[T] then continue;fi;
     for dc in DoubleCosets(H[i],Intersection(H[i],HG[T]),K) do
      h:=Representative(dc);sf:=OnSets(sh[i][T],Image(acts[i],h));
      inter:=Intersection(sx,sf);a:=Length(inter);tested:=tested+1;
      if a<=1 then continue;fi;
      inc:=base[j] in OnSets(sh[j][T],Image(acts[j],h));
      if a=Minimum(Length(sx),Length(sf)) and inc then continue;fi;
      witness:=false;
      for U in [1..Length(sets)] do
       if i in sets[U] or Length(sh[i][U])<>a then continue;fi;
       for q in RightTransversal(K,Intersection(K,HG[U])) do
        witness_tests:=witness_tests+1;
        if OnSets(sh[i][U],Image(acts[i],q))<>inter then continue;fi;
        if ForAll(sets[U],u->base[u]^Image(acts[u],q) in OnSets(sh[u][T],Image(acts[u],h))) then witness:=true;break;fi;
       od;
       if witness then break;fi;
      od;
      if not witness then
       good:=false;Add(failures,rec(type:=labels[i],element_type:=labels[j],flag_types:=labels{sets[T]},representative:=ListPerm(h,LargestMovedPoint(G)),intersection:=inter,method:="complete_double_coset_witness_search"));break;
      fi;
     od;
     if not good then break;fi;
    od;
    if not good then break;fi;
   od;
  fi;
  Add(allgood,good);
 od;
 return rec(types:=labels,order:=Size(G),parabolic_orders:=List(H,Size),flag_transitive:=ft,extension_tests:=ext,primitive_checked_types:=labels{[1..Length(primitive)]},primitive_types:=primitive,connected:=connected,type_results:=allgood,IP:=ForAll(allgood,x->x),WIP:=ForAny(allgood,x->x),orbit_tests:=tested,witness_tests:=witness_tests,negative_witnesses:=failures);
end;;
L096AllResidues:=function(inp)
 local G,H,n,sets,HG,J,K,rest,P,r,res,byrank,k,rows,filters,result;
 G:=Group(Concatenation(inp.parabolic_generators));n:=Length(inp.parabolic_generators);
 if Size(G)<>inp.expected_order or not IsSimpleGroup(G) then Error("wrong source group");fi;
 H:=List(inp.parabolic_generators,gs->Subgroup(G,gs));sets:=Combinations([1..n]);
 HG:=List(sets,T->Intersection(Concatenation([G],H{T})));res:=[];
 for J in sets do
  if Length(J)=n then continue;fi;
  K:=HG[Position(sets,J)];rest:=Difference([1..n],J);P:=List(rest,i->Intersection(K,H[i]));
  r:=L096Local(K,P,rest);r.fixed_types:=J;r.residue_rank:=Length(rest);r.flag_orbit_size:=Index(G,K);Add(res,r);
  if not r.flag_transitive then return rec(member:=inp.member,active_row:=inp.active,construction_row:=inp.construction,published_label_verified:=false,order:=Size(G),rank:=n,source_filter_pass:=false,unclassified_reason:="flag_transitivity_failed",failed_residue:=r);fi;
 od;
 byrank:=[];
 for k in [2..n] do
  if k>=3 and not L096ComputeShadow then continue;fi;
  rows:=Filtered(res,r->r.residue_rank=k);
  Add(byrank,rec(rank:=k,base_residues:=Length(rows),actual_residues:=Sum(rows,r->r.flag_orbit_size),IPk:=ForAll(rows,r->r.IP),WIPk:=ForAll(rows,r->r.WIP)));
 od;
 rows:=Filtered(res,r->r.residue_rank=1);
 filters:=rec(flag_transitive:=true,firm:=ForAll(rows,r->r.firm),residually_connected:=ForAll(res,r->r.connected),RWPRI:=ForAll(res,r->ForAny(r.primitive_types,x->x)),twoT1:=ForAll(rows,r->r.two_transitive),IP2:=byrank[1].IPk);
 result:=rec(member:=inp.member,active_row:=inp.active,construction_row:=inp.construction,published_label_verified:=false,order:=Size(G),rank:=n,borel_order:=Size(HG[Position(sets,[1..n])]),parabolic_orders:=List(H,Size),filters:=filters,source_filter_pass:=ForAll(RecNames(filters),s->filters.(s)),by_rank:=byrank,computed_all_ranks:=L096ComputeShadow,IP:=L096ComputeShadow and ForAll(byrank,r->r.IPk),WIP:=L096ComputeShadow and ForAll(byrank,r->r.WIPk),residues:=res);
 if not L096ComputeShadow then Unbind(result.IP);Unbind(result.WIP);fi;
 return result;
end;;
