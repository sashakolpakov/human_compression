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
D:=P177Graph("108_010",108,[1, 4, 6, 7, 10, 11, 15, 19, 21, 22, 25, 26, 30, 33, 34, 36, 37, 40, 41, 42, 44, 45, 48, 50, 51, 52, 55, 56, 58, 59, 62, 63, 66, 68, 70, 71, 72, 77, 80, 81, 83, 87, 89, 91, 92, 94, 96, 102, 103, 104, 105, 106, 107, 108],[[1, 46], [1, 82], [1, 84], [1, 99], [2, 25], [2, 41], [2, 70], [2, 106], [3, 15], [3, 42], [3, 58], [3, 80], [4, 57], [4, 64], [4, 65], [4, 95], [5, 42], [5, 45], [5, 59], [5, 103], [6, 14], [6, 20], [6, 23], [6, 64], [7, 13], [7, 47], [7, 73], [7, 79], [8, 22], [8, 30], [8, 83], [8, 106], [9, 37], [9, 55], [9, 66], [9, 105], [10, 54], [10, 65], [10, 98], [10, 99], [11, 47], [11, 93], [11, 95], [11, 101], [12, 21], [12, 41], [12, 102], [12, 108], [13, 51], [13, 55], [13, 59], [14, 40], [14, 91], [14, 108], [15, 76], [15, 88], [15, 90], [16, 36], [16, 52], [16, 62], [16, 87], [17, 33], [17, 83], [17, 96], [17, 105], [18, 34], [18, 50], [18, 66], [18, 83], [19, 75], [19, 86], [19, 90], [19, 93], [20, 36], [20, 51], [20, 68], [21, 23], [21, 74], [21, 100], [22, 46], [22, 74], [22, 98], [23, 26], [23, 48], [24, 25], [24, 37], [24, 59], [24, 80], [25, 69], [25, 73], [26, 49], [26, 79], [26, 101], [27, 70], [27, 102], [27, 104], [27, 107], [28, 56], [28, 62], [28, 72], [28, 96], [29, 34], [29, 45], [29, 55], [29, 92], [30, 31], [30, 53], [30, 69], [31, 42], [31, 63], [31, 71], [32, 52], [32, 58], [32, 71], [32, 94], [33, 43], [33, 53], [33, 90], [34, 74], [34, 97], [35, 37], [35, 45], [35, 58], [35, 72], [36, 39], [36, 79], [37, 85], [38, 44], [38, 45], [38, 50], [38, 71], [39, 40], [39, 56], [39, 104], [40, 76], [40, 78], [41, 95], [41, 98], [42, 46], [43, 63], [43, 89], [43, 91], [44, 61], [44, 67], [44, 78], [46, 92], [47, 70], [47, 87], [48, 73], [48, 95], [48, 97], [49, 56], [49, 91], [49, 102], [50, 69], [50, 85], [51, 65], [51, 97], [52, 64], [52, 78], [53, 77], [53, 80], [54, 68], [54, 104], [54, 108], [55, 82], [56, 90], [57, 89], [57, 94], [57, 108], [58, 75], [59, 99], [60, 71], [60, 77], [60, 81], [60, 89], [61, 63], [61, 83], [61, 92], [62, 75], [62, 101], [63, 76], [64, 81], [65, 87], [66, 73], [66, 100], [67, 81], [67, 91], [67, 96], [68, 74], [68, 82], [69, 103], [70, 99], [72, 78], [72, 88], [75, 77], [76, 94], [77, 85], [79, 107], [80, 84], [81, 101], [82, 107], [84, 105], [84, 106], [85, 96], [86, 87], [86, 94], [86, 104], [88, 92], [88, 105], [89, 93], [93, 102], [97, 103], [98, 103], [100, 106], [100, 107]]);;
R:=P177Census(D);;Need(Size(R.F)=864);;
PrintTo("current_c4_descent/108_010.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 108_010 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
