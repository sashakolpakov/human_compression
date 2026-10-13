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
D:=P177Graph("120_026",120,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60],[[1, 61], [1, 72], [1, 81], [1, 84], [2, 61], [2, 81], [2, 86], [2, 105], [3, 62], [3, 73], [3, 82], [3, 92], [4, 61], [4, 99], [4, 109], [4, 119], [5, 62], [5, 82], [5, 87], [5, 117], [6, 61], [6, 92], [6, 104], [6, 119], [7, 69], [7, 71], [7, 109], [7, 111], [8, 93], [8, 95], [8, 110], [8, 112], [9, 72], [9, 77], [9, 84], [9, 90], [10, 66], [10, 75], [10, 108], [10, 110], [11, 79], [11, 81], [11, 106], [11, 119], [12, 62], [12, 98], [12, 115], [12, 118], [13, 69], [13, 93], [13, 111], [13, 112], [14, 75], [14, 97], [14, 108], [14, 111], [15, 66], [15, 81], [15, 95], [15, 119], [16, 62], [16, 90], [16, 103], [16, 118], [17, 87], [17, 89], [17, 106], [17, 117], [18, 67], [18, 70], [18, 114], [18, 115], [19, 63], [19, 79], [19, 89], [19, 94], [20, 94], [20, 100], [20, 113], [20, 116], [21, 76], [21, 82], [21, 105], [21, 118], [22, 86], [22, 91], [22, 105], [22, 107], [23, 73], [23, 80], [23, 85], [23, 92], [24, 77], [24, 99], [24, 103], [24, 109], [25, 73], [25, 88], [25, 104], [25, 108], [26, 63], [26, 71], [26, 99], [26, 116], [27, 68], [27, 76], [27, 86], [27, 93], [28, 65], [28, 69], [28, 97], [28, 113], [29, 68], [29, 70], [29, 98], [29, 112], [30, 72], [30, 97], [30, 111], [30, 120], [31, 70], [31, 75], [31, 88], [31, 115], [32, 67], [32, 100], [32, 113], [32, 114], [33, 63], [33, 82], [33, 94], [33, 118], [34, 64], [34, 88], [34, 108], [34, 117], [35, 71], [35, 96], [35, 99], [35, 114], [36, 63], [36, 68], [36, 93], [36, 116], [37, 69], [37, 78], [37, 91], [37, 97], [38, 68], [38, 77], [38, 103], [38, 112], [39, 72], [39, 85], [39, 102], [39, 120], [40, 75], [40, 77], [40, 88], [40, 90], [41, 70], [41, 74], [41, 83], [41, 98], [42, 74], [42, 76], [42, 86], [42, 101], [43, 64], [43, 84], [43, 117], [43, 120], [44, 83], [44, 95], [44, 101], [44, 110], [45, 64], [45, 65], [45, 87], [45, 100], [46, 78], [46, 92], [46, 104], [46, 107], [47, 71], [47, 80], [47, 85], [47, 109], [48, 66], [48, 67], [48, 96], [48, 110], [49, 79], [49, 90], [49, 103], [49, 106], [50, 80], [50, 98], [50, 102], [50, 115], [51, 73], [51, 96], [51, 104], [51, 114], [52, 65], [52, 74], [52, 83], [52, 100], [53, 74], [53, 84], [53, 101], [53, 120], [54, 67], [54, 79], [54, 89], [54, 96], [55, 83], [55, 89], [55, 101], [55, 106], [56, 64], [56, 78], [56, 87], [56, 107], [57, 91], [57, 94], [57, 107], [57, 116], [58, 65], [58, 80], [58, 102], [58, 113], [59, 76], [59, 85], [59, 102], [59, 105], [60, 66], [60, 78], [60, 91], [60, 95]]);;
R:=P177Census(D);;Need(Size(R.F)=240);;
PrintTo("current_c4_descent/120_026.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_026 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
