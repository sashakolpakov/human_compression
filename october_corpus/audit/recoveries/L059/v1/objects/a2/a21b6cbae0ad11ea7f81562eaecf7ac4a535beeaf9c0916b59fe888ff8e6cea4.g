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
D:=P177Graph("128_027",128,[1, 2, 3, 4, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 125, 126, 127, 128],[[1, 30], [1, 31], [1, 111], [1, 112], [2, 14], [2, 15], [2, 111], [2, 112], [3, 14], [3, 15], [3, 95], [3, 96], [4, 30], [4, 31], [4, 95], [4, 96], [5, 42], [5, 43], [5, 81], [5, 82], [6, 54], [6, 55], [6, 81], [6, 82], [7, 47], [7, 48], [7, 54], [7, 55], [8, 47], [8, 48], [8, 85], [8, 88], [9, 51], [9, 52], [9, 85], [9, 88], [10, 51], [10, 52], [10, 77], [10, 80], [11, 57], [11, 58], [11, 77], [11, 80], [12, 57], [12, 58], [12, 69], [12, 72], [13, 69], [13, 72], [13, 73], [13, 74], [14, 73], [14, 74], [15, 89], [15, 90], [16, 62], [16, 63], [16, 89], [16, 90], [17, 62], [17, 63], [17, 67], [17, 68], [18, 67], [18, 68], [18, 125], [18, 128], [19, 39], [19, 40], [19, 125], [19, 128], [20, 39], [20, 40], [20, 41], [20, 44], [21, 41], [21, 44], [21, 83], [21, 84], [22, 53], [22, 56], [22, 83], [22, 84], [23, 45], [23, 46], [23, 53], [23, 56], [24, 45], [24, 46], [24, 86], [24, 87], [25, 49], [25, 50], [25, 86], [25, 87], [26, 49], [26, 50], [26, 78], [26, 79], [27, 59], [27, 60], [27, 78], [27, 79], [28, 59], [28, 60], [28, 70], [28, 71], [29, 70], [29, 71], [29, 75], [29, 76], [30, 75], [30, 76], [31, 91], [31, 92], [32, 61], [32, 64], [32, 91], [32, 92], [33, 61], [33, 64], [33, 65], [33, 66], [34, 65], [34, 66], [34, 126], [34, 127], [35, 37], [35, 38], [35, 126], [35, 127], [36, 37], [36, 38], [36, 42], [36, 43], [37, 108], [37, 109], [38, 93], [38, 124], [39, 93], [39, 124], [40, 108], [40, 109], [41, 101], [41, 102], [42, 101], [42, 102], [43, 117], [43, 118], [44, 117], [44, 118], [45, 96], [45, 97], [46, 112], [46, 113], [47, 112], [47, 113], [48, 96], [48, 97], [49, 98], [49, 99], [50, 114], [50, 115], [51, 114], [51, 115], [52, 98], [52, 99], [53, 103], [53, 104], [54, 103], [54, 104], [55, 119], [55, 120], [56, 119], [56, 120], [57, 116], [57, 117], [58, 100], [58, 101], [59, 100], [59, 101], [60, 116], [60, 117], [61, 113], [61, 114], [62, 113], [62, 114], [63, 97], [63, 98], [64, 97], [64, 98], [65, 106], [65, 107], [66, 122], [66, 123], [67, 122], [67, 123], [68, 106], [68, 107], [69, 93], [69, 94], [70, 93], [70, 94], [71, 109], [71, 110], [72, 109], [72, 110], [73, 118], [73, 119], [74, 102], [74, 103], [75, 102], [75, 103], [76, 118], [76, 119], [77, 123], [77, 124], [78, 123], [78, 124], [79, 107], [79, 108], [80, 107], [80, 108], [81, 110], [81, 111], [82, 94], [82, 95], [83, 94], [83, 95], [84, 110], [84, 111], [85, 121], [85, 122], [86, 121], [86, 122], [87, 105], [87, 106], [88, 105], [88, 106], [89, 120], [89, 121], [90, 104], [90, 105], [91, 104], [91, 105], [92, 120], [92, 121], [99, 125], [99, 126], [100, 125], [100, 126], [115, 127], [115, 128], [116, 127], [116, 128]]);;
R:=P177Census(D);;Need(Size(R.F)=256);;
PrintTo("current_c4_descent/128_027.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_027 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
