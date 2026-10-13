Need:=function(ok) if not ok then Error("L059 descent invalid"); fi; end;;
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
D:=P177Graph("084_023",84,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],[[1, 47], [1, 49], [1, 64], [1, 66], [2, 66], [2, 76], [2, 78], [2, 83], [3, 49], [3, 55], [3, 74], [3, 83], [4, 64], [4, 68], [4, 70], [4, 77], [5, 47], [5, 60], [5, 72], [5, 77], [6, 45], [6, 53], [6, 78], [6, 80], [7, 48], [7, 58], [7, 60], [7, 74], [8, 45], [8, 51], [8, 68], [8, 76], [9, 55], [9, 58], [9, 71], [9, 80], [10, 55], [10, 59], [10, 63], [10, 70], [11, 56], [11, 60], [11, 62], [11, 79], [12, 46], [12, 59], [12, 62], [12, 68], [13, 54], [13, 56], [13, 72], [13, 78], [14, 43], [14, 46], [14, 47], [14, 53], [15, 48], [15, 50], [15, 65], [15, 76], [16, 62], [16, 65], [16, 67], [16, 71], [17, 56], [17, 61], [17, 68], [17, 73], [18, 61], [18, 79], [18, 80], [18, 81], [19, 54], [19, 67], [19, 70], [19, 81], [20, 46], [20, 50], [20, 73], [20, 80], [21, 63], [21, 72], [21, 73], [21, 75], [22, 50], [22, 59], [22, 60], [22, 81], [23, 43], [23, 51], [23, 57], [23, 81], [24, 44], [24, 51], [24, 61], [24, 74], [25, 44], [25, 53], [25, 62], [25, 75], [26, 64], [26, 71], [26, 79], [26, 84], [27, 48], [27, 57], [27, 73], [27, 84], [28, 45], [28, 55], [28, 65], [28, 75], [29, 45], [29, 54], [29, 57], [29, 64], [30, 46], [30, 66], [30, 69], [30, 71], [31, 48], [31, 56], [31, 66], [31, 82], [32, 49], [32, 52], [32, 53], [32, 79], [33, 49], [33, 51], [33, 59], [33, 82], [34, 52], [34, 54], [34, 65], [34, 82], [35, 44], [35, 58], [35, 67], [35, 78], [36, 47], [36, 57], [36, 58], [36, 63], [37, 44], [37, 63], [37, 69], [37, 82], [38, 43], [38, 67], [38, 76], [38, 77], [39, 74], [39, 75], [39, 77], [39, 84], [40, 61], [40, 69], [40, 70], [40, 83], [41, 50], [41, 52], [41, 72], [41, 83], [42, 43], [42, 52], [42, 69], [42, 84]]);;
R:=P177Census(D);;Need(Size(R.F)=336);;
PrintTo("current_c4_descent/084_023.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 084_023 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
