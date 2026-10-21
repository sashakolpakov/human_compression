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
D:=P177Graph("120_038",120,[1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 26, 27, 28, 29, 30, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 71, 72, 73, 74, 75, 81, 82, 83, 84, 85, 91, 92, 93, 94, 95, 101, 102, 103, 104, 105, 116, 117, 118, 119, 120],[[1, 11], [1, 21], [1, 31], [1, 51], [2, 54], [2, 69], [2, 87], [2, 99], [3, 24], [3, 47], [3, 67], [3, 108], [4, 13], [4, 46], [4, 78], [4, 96], [5, 33], [5, 77], [5, 86], [5, 109], [6, 59], [6, 64], [6, 83], [6, 94], [7, 29], [7, 43], [7, 63], [7, 105], [8, 37], [8, 73], [8, 82], [8, 104], [9, 17], [9, 42], [9, 75], [9, 92], [10, 20], [10, 30], [10, 40], [10, 60], [11, 41], [11, 71], [11, 91], [12, 29], [12, 65], [12, 94], [12, 117], [13, 27], [13, 39], [13, 58], [14, 37], [14, 43], [14, 61], [14, 84], [15, 59], [15, 73], [15, 81], [15, 116], [16, 24], [16, 68], [16, 99], [16, 113], [17, 23], [17, 34], [17, 55], [18, 54], [18, 77], [18, 90], [18, 112], [19, 33], [19, 47], [19, 70], [19, 89], [20, 50], [20, 80], [20, 100], [21, 44], [21, 61], [21, 101], [22, 59], [22, 74], [22, 91], [22, 104], [23, 64], [23, 93], [23, 120], [24, 38], [24, 56], [25, 37], [25, 42], [25, 72], [25, 116], [26, 54], [26, 79], [26, 100], [26, 109], [27, 69], [27, 97], [27, 111], [28, 33], [28, 46], [28, 76], [28, 112], [29, 35], [29, 52], [30, 49], [30, 70], [30, 110], [31, 74], [31, 81], [31, 102], [32, 59], [32, 65], [32, 105], [32, 120], [33, 57], [34, 44], [34, 62], [34, 83], [35, 41], [35, 75], [35, 118], [36, 54], [36, 68], [36, 108], [36, 111], [37, 53], [38, 50], [38, 78], [38, 115], [39, 49], [39, 66], [39, 87], [40, 79], [40, 90], [40, 106], [41, 69], [41, 88], [42, 68], [42, 107], [43, 79], [43, 98], [44, 77], [44, 114], [45, 90], [45, 99], [45, 109], [45, 111], [46, 65], [46, 103], [47, 74], [47, 95], [48, 81], [48, 94], [48, 104], [48, 120], [49, 73], [49, 119], [50, 64], [50, 85], [51, 62], [51, 84], [51, 93], [52, 71], [52, 92], [52, 102], [53, 63], [53, 101], [53, 117], [55, 72], [55, 82], [55, 118], [56, 80], [56, 96], [56, 106], [57, 67], [57, 110], [57, 113], [58, 76], [58, 86], [58, 115], [60, 66], [60, 89], [60, 97], [61, 96], [61, 115], [62, 109], [62, 112], [63, 90], [63, 100], [64, 106], [65, 86], [66, 104], [66, 116], [67, 81], [67, 91], [68, 82], [69, 102], [70, 92], [70, 118], [71, 87], [71, 111], [72, 99], [72, 108], [73, 97], [74, 113], [75, 89], [75, 110], [76, 94], [76, 105], [77, 93], [78, 84], [78, 101], [79, 117], [80, 83], [80, 120], [82, 98], [83, 107], [84, 114], [85, 96], [85, 108], [85, 113], [86, 95], [87, 103], [88, 92], [88, 105], [88, 117], [89, 119], [91, 114], [93, 107], [95, 110], [95, 112], [97, 103], [98, 101], [98, 116], [100, 119], [102, 114], [103, 115], [106, 119], [107, 118]]);;
R:=P177Census(D);;Need(Size(R.F)=960);;
PrintTo("current_c4_descent/120_038.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_038 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
