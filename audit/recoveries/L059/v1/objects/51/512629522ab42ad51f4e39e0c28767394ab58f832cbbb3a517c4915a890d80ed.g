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
D:=P177Graph("VT3_162_25",162,[1, 2, 6, 7, 8, 9, 10, 12, 13, 16, 17, 18, 19, 20, 21, 22, 24, 26, 29, 31, 32, 33, 34, 35, 36, 37, 39, 44, 46, 47, 48, 53, 54, 57, 65, 66, 68, 69, 72, 76, 77, 80, 85, 90, 91, 93, 95, 99, 100, 102, 103, 104, 106, 109, 110, 112, 113, 116, 117, 119, 123, 124, 126, 127, 129, 130, 132, 137, 138, 139, 140, 143, 145, 146, 153, 154, 155, 157, 158, 159, 162],[[1, 27], [1, 28], [1, 96], [2, 51], [2, 61], [2, 156], [3, 10], [3, 32], [3, 93], [4, 6], [4, 140], [4, 155], [5, 7], [5, 21], [5, 138], [6, 62], [6, 82], [7, 25], [7, 67], [8, 88], [8, 94], [8, 122], [9, 87], [9, 121], [9, 152], [10, 120], [10, 152], [11, 16], [11, 46], [11, 116], [12, 52], [12, 98], [12, 160], [13, 28], [13, 122], [13, 150], [14, 57], [14, 129], [14, 146], [15, 91], [15, 132], [15, 143], [16, 45], [16, 150], [17, 56], [17, 82], [17, 149], [18, 27], [18, 50], [18, 128], [19, 73], [19, 78], [19, 151], [20, 92], [20, 133], [20, 136], [21, 49], [21, 50], [22, 74], [22, 86], [22, 141], [23, 33], [23, 53], [23, 123], [24, 38], [24, 40], [24, 128], [25, 26], [25, 132], [26, 71], [26, 107], [27, 36], [28, 93], [29, 75], [29, 92], [29, 96], [30, 47], [30, 65], [30, 102], [31, 52], [31, 64], [31, 115], [32, 60], [32, 149], [33, 125], [33, 151], [34, 43], [34, 128], [34, 148], [35, 63], [35, 105], [35, 120], [36, 84], [36, 161], [37, 89], [37, 92], [37, 131], [38, 39], [38, 124], [39, 94], [39, 144], [40, 129], [40, 157], [41, 85], [41, 126], [41, 162], [42, 80], [42, 100], [42, 154], [43, 69], [43, 110], [44, 58], [44, 83], [44, 135], [45, 54], [45, 159], [46, 83], [46, 147], [47, 111], [47, 131], [48, 97], [48, 133], [48, 147], [49, 72], [49, 76], [50, 139], [51, 117], [51, 123], [52, 57], [53, 79], [53, 96], [54, 67], [54, 105], [55, 112], [55, 119], [55, 159], [56, 153], [56, 162], [57, 79], [58, 104], [58, 139], [59, 85], [59, 102], [59, 146], [60, 77], [60, 117], [61, 65], [61, 80], [62, 68], [62, 159], [63, 127], [63, 137], [64, 80], [64, 137], [65, 148], [66, 74], [66, 88], [66, 125], [67, 123], [68, 86], [68, 161], [69, 98], [69, 152], [70, 106], [70, 116], [70, 124], [71, 130], [71, 158], [72, 74], [72, 131], [73, 91], [73, 124], [75, 106], [75, 130], [76, 115], [76, 149], [77, 97], [77, 101], [78, 100], [78, 119], [79, 140], [81, 104], [81, 109], [81, 153], [82, 158], [83, 99], [84, 126], [84, 137], [85, 121], [86, 90], [87, 90], [87, 106], [88, 127], [89, 95], [89, 112], [90, 156], [91, 111], [93, 118], [94, 155], [95, 142], [95, 144], [97, 143], [98, 112], [99, 107], [99, 142], [100, 118], [101, 145], [101, 146], [102, 150], [103, 107], [103, 118], [103, 141], [104, 156], [105, 157], [108, 127], [108, 130], [108, 145], [109, 122], [109, 160], [110, 125], [110, 147], [111, 113], [113, 120], [113, 135], [114, 119], [114, 139], [114, 145], [115, 116], [117, 144], [121, 138], [126, 142], [129, 141], [132, 160], [133, 154], [134, 138], [134, 154], [134, 155], [135, 140], [136, 153], [136, 157], [143, 161], [148, 158], [151, 162]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_162_25.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_162_25 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
