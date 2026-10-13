Need:=function(ok) if not ok then Error("L059 cubic census invalid"); fi; end;;
Read("maximal_descent.g");;

# Exact rank-two marked-geometry census for explicitly constructed graphs.
# This is a new bounded census, not a replay of the unrecovered historical lists.
LoadPackage("grape");;
SetAssertionLevel(1);;

P177Graph := function(label, n, black, edges)
  local E, graph, white;
  E := Set(List(edges, Set));
  white := Difference([1..n], black);
  Need( ForAll(E,e->Length(e)=2 and Length(Intersection(e,black))=1));
  graph := Graph(Group(()), [1..n], OnPoints, function(a,b) return Set([a,b]) in E; end, true);
  Need( IsConnectedGraph(graph));
  return rec(label:=label,n:=n,black:=Set(black),white:=white,edges:=E,graph:=graph);
end;;

P177Max := function(upper,lower)
  local degree, action;
  degree := Index(upper,lower);
  Need(degree>1);
  action := Action(upper,RightCosets(upper,lower),OnRight);
  if Transitivity(action,[1..degree])>=2 then return "2T"; fi;
  if IsPrimitive(action,[1..degree]) then return "M"; fi;
  return "X";
end;;

P177Census := function(data)
  local A, F, classes, edge, b, w, witnesses, H, H0, H1, B, D, duals,
        row, cls, maxcode, normcode, maxorder, dualorder, suborders;
  A := AutGroupGraph(data.graph,[data.black,data.white]);
  F := AutGroupGraph(data.graph);
  Need(IsTransitive(A,data.edges,OnSets));
  edge := data.edges[1];
  b := Intersection(edge,data.black)[1]; w := Intersection(edge,data.white)[1];
  classes := L059Descent(A,data.edges);
  witnesses := [];
  for cls in classes do
    H := Representative(cls);
    if IsTransitive(H,data.edges,OnSets) then
      H0 := Stabilizer(H,b); H1 := Stabilizer(H,w); B := Intersection(H0,H1);
      Need(Size(ClosureGroup(H0,H1))=Size(H));
      Need(Size(Core(H,B))=1);
      Need(Index(H,B)=Length(data.edges));
      maxcode := List([[H0,B],[H1,B],[H,H0],[H,H1]],p->P177Max(p[1],p[2]));
      normcode := List([H,H0,H1,B],K->IsNormal(A,K));
      D := Stabilizer(Normalizer(F,H),edge,OnSets);
      duals := Filtered(Elements(D),g->b^g=w);
      if IsEmpty(duals) then dualorder:=0; else dualorder:=Minimum(List(duals,Order)); fi;
      maxorder := Maximum(List(ConjugacyClasses(H),c->Order(Representative(c))));
      row := rec(H:=H,H0:=H0,H1:=H1,B:=B,maxcode:=maxcode,normcode:=normcode,
                 dualorder:=dualorder,maxorder:=maxorder,
                 group_order:=Size(H),subgroup_orders:=List([H0,H1,B],Size),
                 structure:=List([H,H0,H1,B],StructureDescription));
      Add(witnesses,row);
    fi;
  od;
  Print(data.label," vertices=",data.n," edges=",Length(data.edges)," Aut+=",Size(A),
        " Aut=",Size(F)," subgroup_classes=",Length(classes)," geometries=",Length(witnesses),"\n");
  Print("MAX ",Collected(List(witnesses,r->r.maxcode)),"\n");
  Print("NORM ",Collected(List(witnesses,r->r.normcode)),"\n");
  return rec(label:=data.label,n:=data.n,black:=data.black,white:=data.white,edges:=data.edges,
             A:=A,F:=F,base_edge:=edge,b:=b,w:=w,retained_edge_transitive_classes:=Length(classes),search:=L059Search,witnesses:=witnesses);
end;;


t:=Runtime();;
D:=P177Graph("VT3_64_2",64,[1, 3, 4, 5, 7, 11, 13, 17, 20, 21, 22, 24, 26, 28, 29, 31, 32, 33, 34, 38, 40, 42, 43, 44, 47, 56, 57, 58, 61, 62, 63, 64],[[1, 12], [1, 19], [1, 30], [2, 5], [2, 7], [2, 64], [3, 9], [3, 41], [3, 52], [4, 39], [4, 53], [4, 55], [5, 9], [5, 37], [6, 7], [6, 47], [6, 62], [7, 45], [8, 22], [8, 33], [8, 64], [9, 13], [10, 11], [10, 22], [10, 47], [11, 18], [11, 52], [12, 34], [12, 38], [13, 46], [13, 59], [14, 24], [14, 33], [14, 61], [15, 24], [15, 32], [15, 42], [16, 20], [16, 40], [16, 56], [17, 23], [17, 30], [17, 50], [18, 58], [18, 63], [19, 33], [19, 43], [20, 35], [20, 59], [21, 25], [21, 27], [21, 50], [22, 25], [23, 56], [23, 57], [24, 36], [25, 31], [26, 36], [26, 45], [26, 48], [27, 34], [27, 44], [28, 41], [28, 48], [28, 54], [29, 49], [29, 51], [29, 59], [30, 62], [31, 46], [31, 48], [32, 50], [32, 52], [34, 60], [35, 42], [35, 64], [36, 57], [37, 57], [37, 63], [38, 41], [38, 55], [39, 47], [39, 56], [40, 54], [40, 60], [42, 55], [43, 46], [43, 53], [44, 45], [44, 51], [49, 61], [49, 62], [51, 58], [53, 58], [54, 61], [60, 63]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_64_2.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_64_2 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
