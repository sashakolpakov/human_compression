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
D:=P177Graph("150_009",150,[1, 2, 3, 6, 8, 10, 11, 12, 16, 26, 28, 30, 32, 33, 34, 37, 41, 43, 44, 47, 49, 52, 56, 57, 58, 61, 62, 67, 68, 69, 70, 73, 76, 77, 78, 79, 81, 83, 84, 86, 87, 88, 90, 91, 95, 96, 98, 99, 101, 105, 107, 108, 109, 114, 117, 118, 124, 126, 127, 128, 130, 131, 132, 133, 135, 137, 138, 141, 142, 143, 145, 147, 148, 149, 150],[[1, 15], [1, 35], [1, 66], [1, 116], [2, 51], [2, 64], [2, 74], [2, 134], [3, 54], [3, 85], [3, 97], [3, 110], [4, 57], [4, 62], [4, 127], [4, 133], [5, 37], [5, 83], [5, 99], [5, 142], [6, 63], [6, 66], [6, 104], [6, 115], [7, 30], [7, 90], [7, 91], [7, 109], [8, 38], [8, 112], [8, 144], [8, 146], [9, 56], [9, 61], [9, 148], [9, 150], [10, 38], [10, 82], [10, 92], [10, 111], [11, 18], [11, 19], [11, 74], [11, 123], [12, 14], [12, 25], [12, 39], [12, 40], [13, 76], [13, 98], [13, 133], [13, 141], [14, 79], [14, 132], [14, 148], [15, 41], [15, 138], [15, 147], [16, 72], [16, 93], [16, 106], [16, 125], [17, 33], [17, 52], [17, 62], [17, 135], [18, 32], [18, 33], [18, 68], [19, 26], [19, 95], [19, 114], [20, 70], [20, 96], [20, 130], [20, 142], [21, 32], [21, 43], [21, 67], [21, 83], [22, 28], [22, 79], [22, 98], [22, 149], [23, 44], [23, 84], [23, 137], [23, 149], [24, 87], [24, 88], [24, 109], [24, 124], [25, 49], [25, 127], [25, 130], [26, 64], [26, 71], [26, 103], [27, 37], [27, 67], [27, 69], [27, 73], [28, 31], [28, 35], [28, 102], [29, 41], [29, 43], [29, 84], [29, 124], [30, 63], [30, 71], [30, 104], [31, 57], [31, 79], [31, 143], [32, 92], [32, 123], [33, 60], [33, 80], [34, 36], [34, 40], [34, 50], [34, 113], [35, 41], [35, 118], [36, 78], [36, 127], [36, 133], [37, 100], [37, 106], [38, 49], [38, 128], [39, 49], [39, 61], [39, 108], [40, 77], [40, 132], [41, 129], [42, 78], [42, 117], [42, 135], [42, 145], [43, 111], [43, 129], [44, 45], [44, 59], [44, 100], [45, 67], [45, 73], [45, 105], [46, 98], [46, 131], [46, 138], [46, 141], [47, 54], [47, 72], [47, 119], [47, 120], [48, 52], [48, 95], [48, 108], [48, 135], [49, 82], [50, 77], [50, 79], [50, 148], [51, 87], [51, 88], [51, 147], [52, 82], [52, 146], [53, 61], [53, 70], [53, 107], [53, 150], [54, 90], [54, 145], [55, 78], [55, 81], [55, 131], [55, 145], [56, 89], [56, 94], [56, 104], [57, 113], [57, 136], [58, 59], [58, 92], [58, 111], [58, 140], [59, 132], [59, 149], [60, 68], [60, 87], [60, 128], [61, 65], [62, 80], [62, 113], [63, 88], [63, 101], [64, 81], [64, 95], [65, 108], [65, 127], [65, 130], [66, 86], [66, 99], [67, 92], [68, 129], [68, 139], [69, 100], [69, 110], [69, 122], [70, 89], [70, 112], [71, 90], [71, 150], [72, 86], [72, 117], [73, 97], [73, 119], [74, 81], [74, 114], [75, 81], [75, 117], [75, 131], [75, 135], [76, 115], [76, 116], [76, 121], [77, 85], [77, 110], [78, 113], [80, 95], [80, 108], [82, 126], [83, 93], [83, 111], [84, 139], [84, 140], [85, 91], [85, 137], [86, 115], [86, 120], [87, 123], [88, 94], [89, 107], [89, 148], [90, 119], [91, 103], [91, 122], [93, 99], [93, 126], [94, 101], [94, 118], [96, 115], [96, 116], [96, 144], [97, 114], [97, 145], [98, 136], [99, 116], [100, 105], [101, 112], [101, 144], [102, 118], [102, 138], [102, 147], [103, 109], [103, 150], [104, 118], [105, 120], [105, 125], [106, 126], [106, 142], [107, 110], [107, 122], [109, 134], [112, 142], [114, 119], [117, 125], [120, 141], [121, 131], [121, 133], [121, 138], [122, 137], [123, 128], [124, 134], [124, 139], [125, 141], [126, 146], [128, 146], [129, 143], [130, 144], [132, 140], [134, 147], [136, 143], [136, 149], [137, 140], [139, 143]]);;
R:=P177Census(D);;Need(Size(R.F)=300);;
PrintTo("current_c4_descent/150_009.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 150_009 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
