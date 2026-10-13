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
D:=P177Graph("120_031",120,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60],[[1, 61], [1, 62], [1, 103], [1, 104], [2, 61], [2, 62], [2, 79], [2, 80], [3, 79], [3, 80], [3, 97], [3, 98], [4, 97], [4, 98], [4, 115], [4, 116], [5, 73], [5, 74], [5, 115], [5, 116], [6, 73], [6, 74], [6, 91], [6, 92], [7, 91], [7, 92], [7, 109], [7, 110], [8, 67], [8, 68], [8, 109], [8, 110], [9, 67], [9, 68], [9, 85], [9, 86], [10, 85], [10, 86], [10, 103], [10, 104], [11, 62], [11, 63], [11, 116], [11, 117], [12, 62], [12, 63], [12, 68], [12, 69], [13, 68], [13, 69], [13, 74], [13, 75], [14, 74], [14, 75], [14, 80], [14, 81], [15, 80], [15, 81], [15, 86], [15, 87], [16, 86], [16, 87], [16, 92], [16, 93], [17, 92], [17, 93], [17, 98], [17, 99], [18, 98], [18, 99], [18, 104], [18, 105], [19, 104], [19, 105], [19, 110], [19, 111], [20, 110], [20, 111], [20, 116], [20, 117], [21, 63], [21, 64], [21, 105], [21, 106], [22, 63], [22, 64], [22, 81], [22, 82], [23, 81], [23, 82], [23, 99], [23, 100], [24, 99], [24, 100], [24, 117], [24, 118], [25, 75], [25, 76], [25, 117], [25, 118], [26, 75], [26, 76], [26, 93], [26, 94], [27, 93], [27, 94], [27, 111], [27, 112], [28, 69], [28, 70], [28, 111], [28, 112], [29, 69], [29, 70], [29, 87], [29, 88], [30, 87], [30, 88], [30, 105], [30, 106], [31, 64], [31, 65], [31, 118], [31, 119], [32, 64], [32, 65], [32, 70], [32, 71], [33, 70], [33, 71], [33, 76], [33, 77], [34, 76], [34, 77], [34, 82], [34, 83], [35, 82], [35, 83], [35, 88], [35, 89], [36, 88], [36, 89], [36, 94], [36, 95], [37, 94], [37, 95], [37, 100], [37, 101], [38, 100], [38, 101], [38, 106], [38, 107], [39, 106], [39, 107], [39, 112], [39, 113], [40, 112], [40, 113], [40, 118], [40, 119], [41, 65], [41, 66], [41, 107], [41, 108], [42, 65], [42, 66], [42, 83], [42, 84], [43, 83], [43, 84], [43, 101], [43, 102], [44, 101], [44, 102], [44, 119], [44, 120], [45, 77], [45, 78], [45, 119], [45, 120], [46, 77], [46, 78], [46, 95], [46, 96], [47, 95], [47, 96], [47, 113], [47, 114], [48, 71], [48, 72], [48, 113], [48, 114], [49, 71], [49, 72], [49, 89], [49, 90], [50, 89], [50, 90], [50, 107], [50, 108], [51, 61], [51, 66], [51, 115], [51, 120], [52, 61], [52, 66], [52, 67], [52, 72], [53, 67], [53, 72], [53, 73], [53, 78], [54, 73], [54, 78], [54, 79], [54, 84], [55, 79], [55, 84], [55, 85], [55, 90], [56, 85], [56, 90], [56, 91], [56, 96], [57, 91], [57, 96], [57, 97], [57, 102], [58, 97], [58, 102], [58, 103], [58, 108], [59, 103], [59, 108], [59, 109], [59, 114], [60, 109], [60, 114], [60, 115], [60, 120]]);;
R:=P177Census(D);;Need(Size(R.F)=240);;
PrintTo("current_c4_descent/120_031.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_031 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
