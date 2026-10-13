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
D:=P177Graph("128_037",128,[1, 3, 4, 6, 9, 11, 13, 16, 18, 19, 21, 23, 24, 25, 30, 33, 35, 36, 37, 39, 41, 42, 44, 47, 49, 53, 54, 56, 59, 62, 68, 69, 73, 75, 77, 78, 80, 83, 86, 87, 88, 90, 91, 92, 95, 99, 103, 105, 108, 110, 111, 112, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 127, 128],[[1, 2], [1, 5], [1, 46], [1, 85], [2, 6], [2, 13], [2, 90], [3, 7], [3, 14], [3, 76], [3, 89], [4, 8], [4, 15], [4, 17], [4, 43], [5, 16], [5, 33], [5, 90], [6, 17], [6, 34], [6, 104], [7, 18], [7, 35], [7, 99], [8, 19], [8, 36], [8, 119], [9, 10], [9, 20], [9, 55], [9, 107], [10, 21], [10, 37], [10, 118], [11, 22], [11, 38], [11, 45], [11, 84], [12, 23], [12, 39], [12, 44], [12, 83], [13, 40], [13, 67], [13, 104], [14, 41], [14, 68], [14, 99], [15, 42], [15, 69], [15, 119], [16, 43], [16, 66], [16, 70], [17, 44], [17, 68], [18, 45], [18, 71], [18, 126], [19, 46], [19, 65], [19, 72], [20, 47], [20, 73], [20, 118], [21, 48], [21, 63], [21, 74], [22, 49], [22, 75], [22, 117], [23, 38], [23, 50], [23, 76], [24, 26], [24, 51], [24, 98], [24, 114], [25, 27], [25, 48], [25, 52], [25, 67], [26, 53], [26, 77], [26, 125], [27, 30], [27, 62], [27, 80], [28, 54], [28, 78], [28, 88], [28, 122], [29, 30], [29, 44], [29, 62], [29, 83], [30, 55], [30, 79], [31, 42], [31, 69], [31, 86], [31, 105], [32, 41], [32, 68], [32, 87], [32, 121], [33, 45], [33, 66], [33, 71], [34, 68], [34, 80], [34, 105], [35, 81], [35, 106], [35, 126], [36, 65], [36, 82], [36, 107], [37, 43], [37, 63], [37, 70], [38, 39], [38, 117], [39, 46], [39, 72], [40, 47], [40, 83], [40, 108], [41, 84], [41, 96], [42, 64], [42, 85], [43, 44], [45, 86], [46, 87], [47, 67], [47, 102], [48, 88], [48, 111], [49, 89], [49, 101], [49, 109], [50, 90], [50, 103], [50, 110], [51, 91], [51, 111], [51, 125], [52, 80], [52, 92], [52, 112], [53, 93], [53, 100], [53, 113], [54, 94], [54, 97], [54, 114], [55, 78], [55, 95], [56, 57], [56, 93], [56, 97], [56, 106], [57, 59], [57, 103], [57, 108], [58, 59], [58, 86], [58, 103], [58, 105], [59, 98], [59, 115], [60, 92], [60, 112], [60, 123], [60, 128], [61, 91], [61, 95], [61, 111], [61, 116], [62, 64], [62, 85], [63, 87], [63, 121], [64, 99], [64, 116], [65, 88], [65, 122], [66, 120], [66, 127], [67, 88], [69, 89], [69, 109], [70, 117], [70, 122], [71, 83], [71, 108], [72, 118], [72, 127], [73, 93], [73, 102], [73, 113], [74, 111], [74, 119], [74, 128], [75, 94], [75, 101], [75, 114], [76, 103], [76, 120], [77, 84], [77, 96], [77, 100], [78, 79], [78, 97], [79, 90], [79, 110], [80, 81], [81, 91], [81, 105], [82, 92], [82, 121], [82, 125], [84, 86], [85, 87], [89, 120], [91, 106], [92, 107], [93, 123], [94, 118], [94, 127], [95, 104], [95, 107], [96, 119], [96, 128], [97, 108], [98, 112], [98, 124], [99, 115], [100, 120], [100, 127], [101, 123], [101, 128], [102, 110], [102, 124], [104, 116], [106, 123], [109, 121], [109, 125], [110, 126], [112, 115], [113, 117], [113, 122], [114, 124], [115, 116], [124, 126]]);;
R:=P177Census(D);;Need(Size(R.F)=512);;
PrintTo("current_c4_descent/128_037.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_037 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
