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
D:=P177Graph("080_017",80,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79],[[1, 2], [1, 20], [1, 34], [1, 41], [2, 3], [2, 35], [2, 42], [3, 4], [3, 36], [3, 43], [4, 5], [4, 37], [4, 44], [5, 6], [5, 38], [5, 45], [6, 7], [6, 39], [6, 46], [7, 8], [7, 40], [7, 47], [8, 9], [8, 21], [8, 48], [9, 10], [9, 22], [9, 49], [10, 11], [10, 23], [10, 50], [11, 12], [11, 24], [11, 51], [12, 13], [12, 25], [12, 52], [13, 14], [13, 26], [13, 53], [14, 15], [14, 27], [14, 54], [15, 16], [15, 28], [15, 55], [16, 17], [16, 29], [16, 56], [17, 18], [17, 30], [17, 57], [18, 19], [18, 31], [18, 58], [19, 20], [19, 32], [19, 59], [20, 33], [20, 60], [21, 41], [21, 43], [21, 76], [22, 42], [22, 44], [22, 77], [23, 43], [23, 45], [23, 78], [24, 44], [24, 46], [24, 79], [25, 45], [25, 47], [25, 80], [26, 46], [26, 48], [26, 61], [27, 47], [27, 49], [27, 62], [28, 48], [28, 50], [28, 63], [29, 49], [29, 51], [29, 64], [30, 50], [30, 52], [30, 65], [31, 51], [31, 53], [31, 66], [32, 52], [32, 54], [32, 67], [33, 53], [33, 55], [33, 68], [34, 54], [34, 56], [34, 69], [35, 55], [35, 57], [35, 70], [36, 56], [36, 58], [36, 71], [37, 57], [37, 59], [37, 72], [38, 58], [38, 60], [38, 73], [39, 41], [39, 59], [39, 74], [40, 42], [40, 60], [40, 75], [41, 61], [42, 62], [43, 63], [44, 64], [45, 65], [46, 66], [47, 67], [48, 68], [49, 69], [50, 70], [51, 71], [52, 72], [53, 73], [54, 74], [55, 75], [56, 76], [57, 77], [58, 78], [59, 79], [60, 80], [61, 62], [61, 80], [62, 63], [63, 64], [64, 65], [65, 66], [66, 67], [67, 68], [68, 69], [69, 70], [70, 71], [71, 72], [72, 73], [73, 74], [74, 75], [75, 76], [76, 77], [77, 78], [78, 79], [79, 80]]);;
R:=P177Census(D);;Need(Size(R.F)=320);;
PrintTo("current_c4_descent/080_017.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 080_017 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
