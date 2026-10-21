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
D:=P177Graph("120_028",120,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60],[[1, 65], [1, 87], [1, 105], [1, 118], [2, 65], [2, 87], [2, 119], [2, 120], [3, 65], [3, 69], [3, 98], [3, 107], [4, 63], [4, 69], [4, 98], [4, 101], [5, 62], [5, 63], [5, 105], [5, 118], [6, 61], [6, 64], [6, 65], [6, 107], [7, 66], [7, 67], [7, 87], [7, 109], [8, 68], [8, 69], [8, 91], [8, 108], [9, 71], [9, 72], [9, 85], [9, 105], [10, 61], [10, 63], [10, 64], [10, 101], [11, 62], [11, 66], [11, 83], [11, 109], [12, 64], [12, 68], [12, 91], [12, 102], [13, 71], [13, 81], [13, 85], [13, 120], [14, 62], [14, 63], [14, 119], [14, 120], [15, 67], [15, 87], [15, 90], [15, 94], [16, 69], [16, 79], [16, 88], [16, 108], [17, 72], [17, 80], [17, 105], [17, 117], [18, 66], [18, 78], [18, 98], [18, 116], [19, 74], [19, 92], [19, 106], [19, 118], [20, 75], [20, 76], [20, 89], [20, 109], [21, 67], [21, 68], [21, 86], [21, 106], [22, 76], [22, 77], [22, 85], [22, 86], [23, 72], [23, 73], [23, 89], [23, 107], [24, 62], [24, 83], [24, 90], [24, 94], [25, 64], [25, 79], [25, 88], [25, 102], [26, 80], [26, 81], [26, 117], [26, 120], [27, 61], [27, 78], [27, 94], [27, 116], [28, 74], [28, 92], [28, 114], [28, 119], [29, 75], [29, 84], [29, 89], [29, 90], [30, 67], [30, 79], [30, 86], [30, 114], [31, 77], [31, 84], [31, 86], [31, 117], [32, 72], [32, 89], [32, 96], [32, 101], [33, 66], [33, 95], [33, 98], [33, 103], [34, 93], [34, 97], [34, 106], [34, 118], [35, 76], [35, 109], [35, 112], [35, 115], [36, 68], [36, 83], [36, 99], [36, 106], [37, 76], [37, 82], [37, 85], [37, 99], [38, 73], [38, 81], [38, 107], [38, 112], [39, 77], [39, 78], [39, 91], [39, 110], [40, 70], [40, 71], [40, 92], [40, 110], [41, 70], [41, 75], [41, 100], [41, 116], [42, 73], [42, 74], [42, 100], [42, 108], [43, 61], [43, 94], [43, 95], [43, 103], [44, 93], [44, 97], [44, 114], [44, 119], [45, 84], [45, 90], [45, 112], [45, 115], [46, 79], [46, 83], [46, 99], [46, 114], [47, 82], [47, 84], [47, 99], [47, 117], [48, 81], [48, 96], [48, 101], [48, 112], [49, 77], [49, 88], [49, 95], [49, 110], [50, 70], [50, 80], [50, 93], [50, 110], [51, 70], [51, 100], [51, 103], [51, 115], [52, 73], [52, 97], [52, 100], [52, 102], [53, 78], [53, 82], [53, 91], [53, 111], [54, 71], [54, 92], [54, 111], [54, 113], [55, 75], [55, 104], [55, 113], [55, 116], [56, 74], [56, 96], [56, 104], [56, 108], [57, 82], [57, 88], [57, 95], [57, 111], [58, 80], [58, 93], [58, 111], [58, 113], [59, 103], [59, 104], [59, 113], [59, 115], [60, 96], [60, 97], [60, 102], [60, 104]]);;
R:=P177Census(D);;Need(Size(R.F)=480);;
PrintTo("current_c4_descent/120_028.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_028 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
