out := "/private/tmp/L122_small243_candidates.jsonl";;
PrintTo(out, "");;
total := 0;;
for gid in [1..66] do
  G := SmallGroup(243,gid);;
  A := AutomorphismGroup(G);;
  sigmas := Filtered(List(ConjugacyClasses(A),Representative),s->Order(s) in [9,27,81]);;
  Print("GROUP ",gid," aut ",Size(A)," sigmas ",Length(sigmas),"\n");;
  if Length(sigmas)=0 then continue; fi;
  subs := AllSubgroups(G);;
  for si in [1..Length(sigmas)] do
    sigma := sigmas[si];;
    for hi in [1..Length(subs)] do
      H := subs[hi];;
      if Index(G,H)<27 or Index(G,H)>81 then continue; fi;
      H1 := Image(sigma,H);;
      if H=H1 or Image(sigma^3,H)<>H then continue; fi;
      Hs := [H,H1,Image(sigma^2,H)];;
      # Disconnected input families are legitimate, but avoid obvious repeated copies.
      if Size(ClosureGroup(ClosureGroup(H,H1),Hs[3]))<>Size(G) then continue; fi;
      cs := List(Hs,h->RightCosets(G,h));;
      n := Length(cs[1]);;
      reps := Concatenation(List(cs,c->List(c,Representative)));;
      pos := function(i,g) return (i-1)*n+PositionProperty(cs[i],c->g in c); end;;
      adj := List([1..3*n],x->[]);;
      for g in Elements(G) do
        vv := List([1..3],i->pos(i,g));;
        for i in [1..3] do for j in [1..3] do
          if i<>j then AddSet(adj[vv[i]],vv[j]); fi;
        od; od;
      od;
      gens := List(GeneratorsOfGroup(G),g->List([1..3*n],v->pos(QuoInt(v-1,n)+1,reps[v]*g)));;
      sp := List([1..3*n],v->pos((QuoInt(v-1,n)+1) mod 3+1,Image(sigma,reps[v])));;
      total := total+1;;
      AppendTo(out,"{\"gid\":",gid,",\"sigma_class\":",si,",\"subgroup_index\":",hi,",\"n\":",n,",\"adj\":",adj,",\"gens\":",gens,",\"sigma\":",sp,"}\n");;
    od;
  od;
  Print("TOTAL ",total,"\n");;
od;
Print("DONE ",total,"\n");;
QUIT;
