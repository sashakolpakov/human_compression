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
D:=P177Graph("120_022",120,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60],[[1, 63], [1, 70], [1, 98], [1, 105], [2, 63], [2, 105], [2, 118], [2, 119], [3, 62], [3, 74], [3, 76], [3, 104], [4, 62], [4, 76], [4, 117], [4, 120], [5, 61], [5, 62], [5, 70], [5, 98], [6, 61], [6, 77], [6, 89], [6, 113], [7, 65], [7, 79], [7, 88], [7, 99], [8, 69], [8, 75], [8, 96], [8, 119], [9, 61], [9, 77], [9, 91], [9, 115], [10, 65], [10, 79], [10, 90], [10, 108], [11, 75], [11, 85], [11, 94], [11, 119], [12, 61], [12, 62], [12, 118], [12, 119], [13, 63], [13, 74], [13, 79], [13, 104], [14, 87], [14, 95], [14, 112], [14, 118], [15, 78], [15, 86], [15, 101], [15, 108], [16, 84], [16, 92], [16, 94], [16, 115], [17, 68], [17, 72], [17, 100], [17, 116], [18, 69], [18, 70], [18, 96], [18, 100], [19, 71], [19, 80], [19, 85], [19, 120], [20, 64], [20, 97], [20, 112], [20, 118], [21, 73], [21, 78], [21, 86], [21, 99], [22, 84], [22, 93], [22, 94], [22, 113], [23, 72], [23, 100], [23, 107], [23, 114], [24, 70], [24, 85], [24, 94], [24, 100], [25, 69], [25, 71], [25, 81], [25, 120], [26, 63], [26, 79], [26, 117], [26, 120], [27, 78], [27, 89], [27, 105], [27, 113], [28, 76], [28, 84], [28, 88], [28, 99], [29, 87], [29, 95], [29, 98], [29, 110], [30, 66], [30, 97], [30, 103], [30, 117], [31, 93], [31, 106], [31, 110], [31, 114], [32, 68], [32, 75], [32, 103], [32, 116], [33, 73], [33, 82], [33, 102], [33, 107], [34, 74], [34, 80], [34, 85], [34, 102], [35, 64], [35, 83], [35, 91], [35, 111], [36, 67], [36, 81], [36, 90], [36, 109], [37, 64], [37, 97], [37, 98], [37, 110], [38, 86], [38, 95], [38, 103], [38, 117], [39, 67], [39, 93], [39, 110], [39, 116], [40, 66], [40, 72], [40, 97], [40, 104], [41, 75], [41, 103], [41, 107], [41, 114], [42, 68], [42, 73], [42, 83], [42, 102], [43, 69], [43, 74], [43, 81], [43, 102], [44, 82], [44, 87], [44, 91], [44, 111], [45, 80], [45, 90], [45, 106], [45, 109], [46, 78], [46, 91], [46, 105], [46, 115], [47, 76], [47, 84], [47, 90], [47, 108], [48, 66], [48, 77], [48, 101], [48, 108], [49, 65], [49, 92], [49, 96], [49, 115], [50, 92], [50, 106], [50, 112], [50, 114], [51, 71], [51, 82], [51, 101], [51, 107], [52, 64], [52, 83], [52, 89], [52, 109], [53, 67], [53, 81], [53, 88], [53, 111], [54, 72], [54, 86], [54, 95], [54, 104], [55, 67], [55, 92], [55, 112], [55, 116], [56, 68], [56, 71], [56, 83], [56, 101], [57, 82], [57, 87], [57, 89], [57, 109], [58, 80], [58, 88], [58, 106], [58, 111], [59, 66], [59, 73], [59, 77], [59, 99], [60, 65], [60, 93], [60, 96], [60, 113]]);;
R:=P177Census(D);;Need(Size(R.F)=240);;
PrintTo("current_c4_descent/120_022.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_022 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
