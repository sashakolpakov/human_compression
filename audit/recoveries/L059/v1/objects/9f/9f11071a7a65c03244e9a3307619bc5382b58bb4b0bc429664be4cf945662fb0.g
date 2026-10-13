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
D:=P177Graph("126_003",126,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125],[[1, 44], [1, 84], [1, 86], [1, 126], [2, 43], [2, 45], [2, 85], [2, 87], [3, 44], [3, 46], [3, 86], [3, 88], [4, 45], [4, 47], [4, 87], [4, 89], [5, 46], [5, 48], [5, 88], [5, 90], [6, 47], [6, 49], [6, 89], [6, 91], [7, 48], [7, 50], [7, 90], [7, 92], [8, 49], [8, 51], [8, 91], [8, 93], [9, 50], [9, 52], [9, 92], [9, 94], [10, 51], [10, 53], [10, 93], [10, 95], [11, 52], [11, 54], [11, 94], [11, 96], [12, 53], [12, 55], [12, 95], [12, 97], [13, 54], [13, 56], [13, 96], [13, 98], [14, 55], [14, 57], [14, 97], [14, 99], [15, 56], [15, 58], [15, 98], [15, 100], [16, 57], [16, 59], [16, 99], [16, 101], [17, 58], [17, 60], [17, 100], [17, 102], [18, 59], [18, 61], [18, 101], [18, 103], [19, 60], [19, 62], [19, 102], [19, 104], [20, 61], [20, 63], [20, 103], [20, 105], [21, 62], [21, 64], [21, 104], [21, 106], [22, 63], [22, 65], [22, 105], [22, 107], [23, 64], [23, 66], [23, 106], [23, 108], [24, 65], [24, 67], [24, 107], [24, 109], [25, 66], [25, 68], [25, 108], [25, 110], [26, 67], [26, 69], [26, 109], [26, 111], [27, 68], [27, 70], [27, 110], [27, 112], [28, 69], [28, 71], [28, 111], [28, 113], [29, 70], [29, 72], [29, 112], [29, 114], [30, 71], [30, 73], [30, 113], [30, 115], [31, 72], [31, 74], [31, 114], [31, 116], [32, 73], [32, 75], [32, 115], [32, 117], [33, 74], [33, 76], [33, 116], [33, 118], [34, 75], [34, 77], [34, 117], [34, 119], [35, 76], [35, 78], [35, 118], [35, 120], [36, 77], [36, 79], [36, 119], [36, 121], [37, 78], [37, 80], [37, 120], [37, 122], [38, 79], [38, 81], [38, 121], [38, 123], [39, 80], [39, 82], [39, 122], [39, 124], [40, 81], [40, 83], [40, 123], [40, 125], [41, 82], [41, 84], [41, 124], [41, 126], [42, 43], [42, 83], [42, 85], [42, 125], [43, 86], [43, 126], [44, 85], [44, 87], [45, 86], [45, 88], [46, 87], [46, 89], [47, 88], [47, 90], [48, 89], [48, 91], [49, 90], [49, 92], [50, 91], [50, 93], [51, 92], [51, 94], [52, 93], [52, 95], [53, 94], [53, 96], [54, 95], [54, 97], [55, 96], [55, 98], [56, 97], [56, 99], [57, 98], [57, 100], [58, 99], [58, 101], [59, 100], [59, 102], [60, 101], [60, 103], [61, 102], [61, 104], [62, 103], [62, 105], [63, 104], [63, 106], [64, 105], [64, 107], [65, 106], [65, 108], [66, 107], [66, 109], [67, 108], [67, 110], [68, 109], [68, 111], [69, 110], [69, 112], [70, 111], [70, 113], [71, 112], [71, 114], [72, 113], [72, 115], [73, 114], [73, 116], [74, 115], [74, 117], [75, 116], [75, 118], [76, 117], [76, 119], [77, 118], [77, 120], [78, 119], [78, 121], [79, 120], [79, 122], [80, 121], [80, 123], [81, 122], [81, 124], [82, 123], [82, 125], [83, 124], [83, 126], [84, 85], [84, 125]]);;
R:=P177Census(D);;Need(Size(R.F)=504);;
PrintTo("current_c4_descent/126_003.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 126_003 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
