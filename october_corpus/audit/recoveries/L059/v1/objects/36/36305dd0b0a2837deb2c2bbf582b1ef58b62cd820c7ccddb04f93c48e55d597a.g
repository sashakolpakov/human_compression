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
D:=P177Graph("120_029",120,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60],[[1, 62], [1, 89], [1, 90], [1, 119], [2, 62], [2, 75], [2, 89], [2, 112], [3, 62], [3, 69], [3, 91], [3, 120], [4, 84], [4, 90], [4, 102], [4, 119], [5, 69], [5, 87], [5, 91], [5, 103], [6, 62], [6, 73], [6, 109], [6, 120], [7, 80], [7, 89], [7, 97], [7, 118], [8, 69], [8, 83], [8, 96], [8, 97], [9, 86], [9, 90], [9, 101], [9, 113], [10, 75], [10, 87], [10, 95], [10, 112], [11, 84], [11, 88], [11, 93], [11, 102], [12, 73], [12, 84], [12, 94], [12, 109], [13, 79], [13, 80], [13, 95], [13, 97], [14, 83], [14, 85], [14, 96], [14, 105], [15, 75], [15, 86], [15, 107], [15, 113], [16, 63], [16, 89], [16, 110], [16, 118], [17, 69], [17, 72], [17, 97], [17, 111], [18, 70], [18, 90], [18, 101], [18, 104], [19, 80], [19, 81], [19, 91], [19, 100], [20, 61], [20, 76], [20, 106], [20, 119], [21, 73], [21, 82], [21, 110], [21, 114], [22, 83], [22, 86], [22, 100], [22, 106], [23, 82], [23, 86], [23, 106], [23, 115], [24, 85], [24, 87], [24, 98], [24, 103], [25, 87], [25, 88], [25, 93], [25, 95], [26, 63], [26, 67], [26, 102], [26, 110], [27, 72], [27, 73], [27, 110], [27, 111], [28, 70], [28, 88], [28, 99], [28, 104], [29, 74], [29, 81], [29, 98], [29, 100], [30, 76], [30, 78], [30, 106], [30, 112], [31, 82], [31, 85], [31, 105], [31, 114], [32, 66], [32, 82], [32, 115], [32, 116], [33, 65], [33, 80], [33, 91], [33, 108], [34, 61], [34, 64], [34, 92], [34, 119], [35, 70], [35, 83], [35, 92], [35, 100], [36, 66], [36, 75], [36, 107], [36, 117], [37, 84], [37, 85], [37, 94], [37, 98], [38, 63], [38, 77], [38, 109], [38, 115], [39, 76], [39, 81], [39, 96], [39, 113], [40, 76], [40, 77], [40, 113], [40, 114], [41, 78], [41, 107], [41, 118], [41, 120], [42, 66], [42, 72], [42, 108], [42, 116], [43, 70], [43, 72], [43, 92], [43, 108], [44, 74], [44, 79], [44, 95], [44, 105], [45, 63], [45, 65], [45, 108], [45, 109], [46, 64], [46, 68], [46, 92], [46, 93], [47, 66], [47, 88], [47, 99], [47, 117], [48, 74], [48, 77], [48, 98], [48, 115], [49, 71], [49, 77], [49, 114], [49, 117], [50, 78], [50, 79], [50, 103], [50, 107], [51, 64], [51, 81], [51, 96], [51, 104], [52, 71], [52, 78], [52, 112], [52, 116], [53, 61], [53, 101], [53, 118], [53, 120], [54, 67], [54, 74], [54, 102], [54, 105], [55, 65], [55, 71], [55, 111], [55, 117], [56, 64], [56, 65], [56, 104], [56, 111], [57, 68], [57, 71], [57, 93], [57, 116], [58, 61], [58, 67], [58, 94], [58, 101], [59, 68], [59, 79], [59, 99], [59, 103], [60, 67], [60, 68], [60, 94], [60, 99]]);;
R:=P177Census(D);;Need(Size(R.F)=1920);;
PrintTo("current_c4_descent/120_029.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_029 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
