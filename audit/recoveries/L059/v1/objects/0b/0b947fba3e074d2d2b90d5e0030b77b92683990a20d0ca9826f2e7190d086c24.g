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
D:=P177Graph("VT3_144_106",144,[1, 4, 5, 8, 9, 10, 11, 13, 14, 16, 19, 20, 23, 24, 27, 30, 31, 34, 35, 37, 42, 43, 45, 47, 48, 49, 52, 53, 54, 60, 61, 62, 63, 64, 65, 66, 67, 70, 72, 73, 75, 79, 80, 83, 85, 86, 87, 88, 91, 95, 96, 98, 100, 101, 104, 105, 106, 107, 109, 116, 117, 118, 119, 120, 126, 127, 130, 132, 133, 136, 139, 143],[[1, 6], [1, 18], [1, 94], [2, 48], [2, 60], [2, 83], [3, 11], [3, 20], [3, 30], [4, 55], [4, 102], [4, 123], [5, 6], [5, 7], [5, 21], [6, 54], [7, 48], [7, 136], [8, 32], [8, 71], [8, 112], [9, 74], [9, 90], [9, 92], [10, 28], [10, 74], [10, 111], [11, 40], [11, 71], [12, 14], [12, 72], [12, 104], [13, 59], [13, 82], [13, 131], [14, 81], [14, 110], [15, 80], [15, 87], [15, 132], [16, 29], [16, 32], [16, 144], [17, 31], [17, 65], [17, 118], [18, 23], [18, 86], [19, 92], [19, 128], [19, 131], [20, 56], [20, 111], [21, 65], [21, 70], [22, 35], [22, 49], [22, 79], [23, 32], [23, 129], [24, 44], [24, 84], [24, 93], [25, 47], [25, 53], [25, 106], [26, 72], [26, 91], [26, 119], [27, 77], [27, 113], [27, 140], [28, 47], [28, 60], [29, 43], [29, 96], [30, 77], [30, 103], [31, 114], [31, 128], [33, 73], [33, 95], [33, 132], [34, 36], [34, 50], [34, 84], [35, 68], [35, 129], [36, 70], [36, 120], [37, 58], [37, 89], [37, 97], [38, 106], [38, 117], [38, 139], [39, 45], [39, 63], [39, 73], [40, 107], [40, 120], [41, 79], [41, 109], [41, 133], [42, 50], [42, 89], [42, 122], [43, 58], [43, 69], [44, 63], [44, 105], [45, 129], [45, 142], [46, 95], [46, 107], [46, 126], [47, 134], [48, 84], [49, 56], [49, 122], [50, 64], [51, 72], [51, 87], [51, 100], [52, 68], [52, 134], [52, 141], [53, 69], [53, 76], [54, 115], [54, 138], [55, 64], [55, 67], [56, 118], [57, 73], [57, 85], [57, 139], [58, 66], [59, 62], [59, 67], [60, 121], [61, 78], [61, 99], [61, 110], [62, 77], [62, 141], [63, 144], [64, 68], [65, 69], [66, 71], [66, 113], [67, 78], [70, 108], [74, 107], [75, 102], [75, 110], [75, 138], [76, 101], [76, 104], [78, 96], [79, 114], [80, 82], [80, 94], [81, 109], [81, 143], [82, 136], [83, 99], [83, 144], [85, 103], [85, 115], [86, 90], [86, 134], [87, 122], [88, 114], [88, 125], [88, 137], [89, 116], [90, 130], [91, 94], [91, 112], [92, 127], [93, 116], [93, 127], [95, 131], [96, 128], [97, 106], [97, 132], [98, 112], [98, 123], [98, 137], [99, 100], [100, 111], [101, 124], [101, 141], [102, 139], [103, 105], [104, 108], [105, 124], [108, 126], [109, 142], [113, 143], [115, 118], [116, 135], [117, 121], [117, 137], [119, 124], [119, 125], [120, 123], [121, 133], [125, 127], [126, 142], [130, 135], [130, 138], [133, 140], [135, 143], [136, 140]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_144_106.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_144_106 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
