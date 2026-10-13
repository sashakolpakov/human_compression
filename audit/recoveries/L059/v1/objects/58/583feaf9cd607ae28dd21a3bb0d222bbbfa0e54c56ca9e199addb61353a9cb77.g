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
D:=P177Graph("VT3_144_60",144,[1, 2, 3, 4, 5, 6, 7, 12, 16, 17, 19, 22, 23, 27, 28, 30, 31, 32, 34, 39, 40, 41, 42, 43, 44, 45, 46, 49, 51, 52, 53, 54, 55, 56, 60, 63, 66, 70, 74, 76, 78, 81, 84, 89, 95, 96, 100, 104, 107, 108, 109, 111, 113, 114, 115, 116, 117, 118, 121, 122, 123, 126, 127, 129, 131, 132, 133, 136, 137, 142, 143, 144],[[1, 59], [1, 72], [1, 130], [2, 9], [2, 18], [2, 73], [3, 75], [3, 120], [3, 124], [4, 37], [4, 58], [4, 85], [5, 33], [5, 37], [5, 57], [6, 37], [6, 91], [6, 125], [7, 69], [7, 87], [7, 88], [8, 81], [8, 100], [8, 113], [9, 108], [9, 144], [10, 19], [10, 53], [10, 96], [11, 113], [11, 122], [11, 136], [12, 24], [12, 79], [12, 99], [13, 49], [13, 54], [13, 108], [14, 23], [14, 34], [14, 133], [15, 28], [15, 116], [15, 127], [16, 59], [16, 119], [16, 124], [17, 65], [17, 79], [17, 103], [18, 40], [18, 122], [19, 36], [19, 48], [20, 39], [20, 42], [20, 70], [21, 30], [21, 34], [21, 54], [22, 33], [22, 80], [22, 102], [23, 105], [23, 110], [24, 122], [24, 133], [25, 41], [25, 43], [25, 51], [26, 30], [26, 115], [26, 131], [27, 61], [27, 80], [27, 94], [28, 71], [28, 92], [29, 43], [29, 118], [29, 123], [30, 57], [31, 72], [31, 82], [31, 139], [32, 33], [32, 35], [32, 50], [34, 141], [35, 60], [35, 107], [36, 45], [36, 121], [38, 46], [38, 89], [38, 127], [39, 62], [39, 97], [40, 69], [40, 130], [41, 80], [41, 139], [42, 120], [42, 134], [43, 119], [44, 77], [44, 92], [44, 128], [45, 71], [45, 119], [46, 64], [46, 140], [47, 49], [47, 63], [47, 89], [48, 95], [48, 131], [49, 106], [50, 109], [50, 132], [51, 90], [51, 134], [52, 93], [52, 94], [52, 98], [53, 68], [53, 73], [54, 101], [55, 88], [55, 91], [55, 112], [56, 86], [56, 88], [56, 92], [57, 114], [58, 129], [58, 137], [59, 129], [60, 62], [60, 87], [61, 70], [61, 78], [62, 131], [63, 83], [63, 99], [64, 123], [64, 126], [65, 115], [65, 143], [66, 67], [66, 135], [66, 138], [67, 96], [67, 116], [68, 81], [68, 137], [69, 89], [70, 91], [71, 143], [72, 76], [73, 117], [74, 75], [74, 83], [74, 102], [75, 116], [76, 93], [76, 106], [77, 78], [77, 107], [78, 110], [79, 104], [81, 106], [82, 109], [82, 144], [83, 118], [84, 97], [84, 101], [84, 102], [85, 104], [85, 121], [86, 113], [86, 118], [87, 137], [90, 127], [90, 136], [93, 133], [94, 117], [95, 125], [95, 130], [96, 139], [97, 104], [98, 132], [98, 142], [99, 114], [100, 125], [100, 140], [101, 136], [103, 108], [103, 142], [105, 126], [105, 143], [107, 140], [109, 120], [110, 144], [111, 128], [111, 135], [111, 141], [112, 126], [112, 132], [114, 134], [115, 138], [117, 124], [121, 141], [123, 135], [128, 142], [129, 138]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_144_60.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_144_60 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
