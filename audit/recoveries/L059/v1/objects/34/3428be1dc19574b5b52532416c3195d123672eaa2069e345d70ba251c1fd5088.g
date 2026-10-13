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
D:=P177Graph("108_017",108,[1, 2, 3, 4, 5, 6, 7, 8, 9, 28, 29, 30, 31, 32, 33, 34, 35, 36, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 91, 92, 93, 94, 95, 96, 97, 98, 99],[[1, 10], [1, 17], [1, 19], [1, 37], [2, 11], [2, 13], [2, 20], [2, 77], [3, 15], [3, 16], [3, 38], [3, 78], [4, 20], [4, 39], [4, 104], [4, 107], [5, 37], [5, 76], [5, 101], [5, 108], [6, 21], [6, 78], [6, 102], [6, 105], [7, 21], [7, 38], [7, 83], [7, 85], [8, 19], [8, 76], [8, 82], [8, 89], [9, 39], [9, 77], [9, 87], [9, 88], [10, 28], [10, 35], [10, 55], [11, 29], [11, 31], [11, 92], [12, 33], [12, 34], [12, 56], [12, 93], [13, 57], [13, 68], [13, 71], [14, 55], [14, 65], [14, 72], [14, 91], [15, 66], [15, 69], [15, 93], [16, 47], [16, 49], [16, 56], [17, 46], [17, 53], [17, 91], [18, 51], [18, 52], [18, 57], [18, 92], [19, 28], [19, 64], [20, 29], [20, 50], [21, 51], [21, 65], [22, 29], [22, 59], [22, 62], [22, 66], [23, 49], [23, 56], [23, 63], [23, 64], [24, 30], [24, 51], [24, 57], [24, 60], [25, 30], [25, 65], [25, 91], [25, 95], [26, 28], [26, 49], [26, 94], [26, 99], [27, 50], [27, 66], [27, 93], [27, 97], [28, 100], [29, 86], [30, 87], [30, 101], [31, 41], [31, 44], [31, 102], [32, 38], [32, 45], [32, 85], [32, 100], [33, 39], [33, 42], [33, 87], [34, 74], [34, 76], [34, 101], [35, 73], [35, 80], [35, 85], [36, 78], [36, 79], [36, 86], [36, 102], [37, 46], [37, 70], [38, 47], [39, 72], [40, 47], [40, 71], [40, 95], [40, 98], [41, 70], [41, 92], [41, 99], [42, 48], [42, 93], [42, 96], [43, 48], [43, 55], [43, 59], [43, 72], [44, 46], [44, 58], [44, 63], [45, 57], [45, 61], [45, 71], [46, 90], [47, 103], [48, 89], [48, 105], [49, 88], [50, 90], [50, 104], [51, 105], [52, 76], [52, 81], [52, 89], [53, 75], [53, 79], [53, 104], [54, 73], [54, 77], [54, 88], [54, 103], [55, 73], [56, 74], [58, 74], [58, 83], [58, 90], [59, 86], [59, 89], [60, 75], [60, 84], [60, 87], [61, 75], [61, 100], [61, 104], [62, 73], [62, 103], [62, 108], [63, 102], [63, 106], [64, 82], [64, 106], [65, 83], [66, 108], [67, 74], [67, 81], [67, 83], [67, 107], [68, 77], [68, 80], [68, 106], [69, 75], [69, 78], [69, 84], [70, 84], [70, 108], [71, 82], [72, 107], [79, 91], [79, 98], [80, 96], [80, 97], [81, 92], [81, 94], [82, 98], [84, 99], [85, 97], [86, 98], [88, 99], [90, 97], [94, 100], [94, 107], [95, 101], [95, 103], [96, 105], [96, 106]]);;
R:=P177Census(D);;Need(Size(R.F)=432);;
PrintTo("current_c4_descent/108_017.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 108_017 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
