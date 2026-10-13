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
D:=P177Graph("128_040",128,[1, 3, 4, 6, 9, 11, 13, 16, 18, 19, 21, 23, 25, 26, 28, 33, 36, 38, 39, 41, 43, 45, 47, 50, 52, 54, 58, 59, 60, 62, 65, 69, 73, 77, 82, 85, 86, 88, 89, 91, 92, 94, 95, 97, 99, 100, 103, 105, 106, 108, 110, 112, 113, 114, 115, 119, 121, 122, 123, 124, 125, 126, 127, 128],[[1, 2], [1, 5], [1, 61], [1, 83], [2, 6], [2, 13], [2, 110], [3, 7], [3, 14], [3, 46], [3, 109], [4, 8], [4, 15], [4, 76], [4, 102], [5, 16], [5, 36], [5, 97], [6, 17], [6, 37], [6, 75], [7, 18], [7, 38], [7, 126], [8, 19], [8, 39], [8, 122], [9, 17], [9, 20], [9, 40], [9, 117], [10, 21], [10, 41], [10, 92], [10, 127], [11, 22], [11, 42], [11, 57], [11, 93], [12, 23], [12, 43], [12, 112], [12, 124], [13, 44], [13, 67], [13, 76], [14, 23], [14, 77], [14, 113], [15, 41], [15, 45], [15, 91], [16, 34], [16, 46], [16, 78], [17, 47], [17, 89], [18, 48], [18, 79], [18, 111], [19, 49], [19, 63], [19, 80], [20, 43], [20, 50], [20, 126], [21, 51], [21, 81], [21, 107], [22, 52], [22, 82], [22, 99], [23, 53], [23, 83], [24, 45], [24, 47], [24, 54], [24, 123], [25, 48], [25, 55], [25, 64], [25, 96], [26, 31], [26, 49], [26, 56], [26, 81], [27, 28], [27, 39], [27, 123], [27, 127], [28, 57], [28, 72], [28, 84], [29, 58], [29, 85], [29, 103], [29, 114], [30, 36], [30, 59], [30, 100], [30, 119], [31, 60], [31, 86], [31, 108], [32, 33], [32, 38], [32, 112], [32, 125], [33, 40], [33, 61], [33, 87], [34, 88], [34, 95], [34, 115], [35, 62], [35, 89], [35, 94], [35, 121], [36, 90], [36, 102], [37, 85], [37, 91], [37, 112], [38, 51], [38, 93], [39, 68], [39, 83], [40, 73], [40, 113], [41, 61], [41, 79], [42, 62], [42, 85], [42, 108], [43, 49], [43, 84], [44, 58], [44, 92], [44, 113], [45, 74], [45, 93], [46, 47], [46, 82], [47, 63], [48, 54], [48, 94], [49, 95], [50, 68], [50, 71], [50, 96], [51, 97], [51, 114], [52, 70], [52, 90], [52, 98], [53, 99], [53, 105], [53, 115], [54, 87], [54, 107], [55, 59], [55, 88], [55, 110], [56, 58], [56, 89], [56, 99], [57, 77], [57, 100], [58, 116], [59, 101], [59, 117], [60, 66], [60, 102], [60, 118], [61, 103], [62, 76], [62, 104], [63, 92], [63, 105], [64, 69], [64, 97], [64, 106], [65, 72], [65, 98], [65, 107], [65, 116], [66, 82], [66, 103], [66, 121], [67, 69], [67, 100], [67, 115], [68, 108], [68, 119], [69, 109], [69, 120], [70, 86], [70, 94], [70, 114], [71, 77], [71, 125], [71, 128], [72, 91], [72, 105], [73, 74], [73, 81], [73, 111], [74, 110], [74, 121], [75, 95], [75, 106], [75, 119], [76, 124], [77, 80], [78, 86], [78, 112], [78, 122], [79, 108], [79, 115], [80, 97], [80, 121], [81, 100], [82, 101], [83, 94], [84, 110], [84, 114], [85, 109], [86, 117], [87, 99], [87, 119], [88, 98], [88, 118], [89, 120], [90, 113], [90, 123], [91, 101], [92, 118], [93, 95], [96, 103], [96, 105], [98, 124], [101, 128], [102, 125], [104, 106], [104, 123], [104, 126], [106, 116], [107, 122], [109, 127], [111, 124], [111, 128], [116, 125], [117, 127], [118, 126], [120, 122], [120, 128]]);;
R:=P177Census(D);;Need(Size(R.F)=512);;
PrintTo("current_c4_descent/128_040.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_040 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
