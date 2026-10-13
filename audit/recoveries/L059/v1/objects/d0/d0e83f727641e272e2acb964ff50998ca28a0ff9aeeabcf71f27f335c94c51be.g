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
D:=P177Graph("VT3_146_9",146,[1, 2, 3, 5, 8, 9, 14, 15, 16, 19, 22, 24, 28, 30, 35, 36, 38, 40, 43, 44, 49, 50, 51, 52, 53, 56, 57, 58, 60, 65, 67, 68, 69, 70, 74, 76, 78, 79, 80, 82, 83, 84, 85, 87, 89, 91, 93, 95, 99, 102, 103, 104, 108, 110, 112, 115, 120, 122, 123, 124, 125, 129, 131, 132, 134, 135, 136, 137, 138, 139, 142, 145, 146],[[1, 20], [1, 55], [1, 77], [2, 21], [2, 55], [2, 94], [3, 23], [3, 27], [3, 98], [4, 28], [4, 35], [4, 67], [5, 21], [5, 86], [5, 88], [6, 19], [6, 57], [6, 132], [7, 19], [7, 93], [7, 108], [8, 59], [8, 71], [8, 90], [9, 61], [9, 106], [9, 107], [10, 16], [10, 91], [10, 135], [11, 36], [11, 79], [11, 110], [12, 51], [12, 52], [12, 95], [13, 70], [13, 76], [13, 84], [14, 86], [14, 109], [14, 144], [15, 96], [15, 105], [15, 126], [16, 111], [16, 143], [17, 76], [17, 83], [17, 123], [18, 51], [18, 85], [18, 102], [19, 119], [20, 69], [20, 145], [21, 56], [22, 25], [22, 37], [22, 117], [23, 44], [23, 51], [24, 29], [24, 63], [24, 140], [25, 28], [25, 60], [26, 60], [26, 68], [26, 132], [27, 40], [27, 124], [28, 39], [29, 82], [29, 93], [30, 41], [30, 88], [30, 106], [31, 79], [31, 125], [31, 134], [32, 57], [32, 108], [32, 139], [33, 40], [33, 44], [33, 49], [34, 99], [34, 103], [34, 129], [35, 48], [35, 97], [36, 39], [36, 117], [37, 65], [37, 68], [38, 46], [38, 77], [38, 114], [39, 137], [40, 90], [41, 95], [41, 112], [42, 80], [42, 125], [42, 129], [43, 94], [43, 116], [43, 127], [44, 100], [45, 95], [45, 102], [45, 120], [46, 82], [46, 145], [47, 83], [47, 84], [47, 146], [48, 89], [48, 146], [49, 126], [49, 133], [50, 59], [50, 64], [50, 116], [52, 73], [52, 100], [53, 114], [53, 121], [53, 141], [54, 76], [54, 87], [54, 99], [55, 131], [56, 127], [56, 144], [57, 143], [58, 92], [58, 109], [58, 111], [59, 89], [60, 105], [61, 65], [61, 136], [62, 79], [62, 123], [62, 137], [63, 104], [63, 129], [64, 78], [64, 142], [65, 81], [66, 67], [66, 89], [66, 115], [67, 105], [68, 119], [69, 81], [69, 107], [70, 92], [70, 144], [71, 124], [71, 142], [72, 102], [72, 110], [72, 134], [73, 112], [73, 135], [74, 81], [74, 118], [74, 119], [75, 87], [75, 103], [75, 139], [77, 78], [78, 94], [80, 101], [80, 113], [82, 121], [83, 97], [84, 127], [85, 98], [85, 101], [86, 112], [87, 92], [88, 131], [90, 115], [91, 100], [91, 133], [93, 118], [96, 122], [96, 132], [97, 137], [98, 138], [99, 128], [101, 134], [103, 140], [104, 113], [104, 121], [106, 120], [107, 131], [108, 140], [109, 135], [110, 130], [111, 139], [113, 138], [114, 142], [115, 126], [116, 146], [117, 136], [118, 145], [120, 130], [122, 133], [122, 143], [123, 128], [124, 141], [125, 128], [130, 136], [138, 141]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_146_9.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_146_9 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
