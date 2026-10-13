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
D:=P177Graph("120_068",120,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60],[[1, 67], [1, 74], [1, 105], [1, 111], [2, 74], [2, 87], [2, 100], [2, 116], [3, 62], [3, 69], [3, 105], [3, 114], [4, 71], [4, 86], [4, 100], [4, 108], [5, 87], [5, 97], [5, 110], [5, 120], [6, 62], [6, 70], [6, 72], [6, 86], [7, 61], [7, 68], [7, 71], [7, 90], [8, 78], [8, 81], [8, 91], [8, 114], [9, 64], [9, 86], [9, 96], [9, 102], [10, 68], [10, 106], [10, 111], [10, 120], [11, 63], [11, 70], [11, 82], [11, 113], [12, 61], [12, 79], [12, 99], [12, 112], [13, 62], [13, 80], [13, 94], [13, 110], [14, 86], [14, 101], [14, 103], [14, 104], [15, 66], [15, 68], [15, 77], [15, 118], [16, 63], [16, 66], [16, 67], [16, 81], [17, 63], [17, 99], [17, 102], [17, 116], [18, 93], [18, 109], [18, 111], [18, 113], [19, 75], [19, 82], [19, 85], [19, 118], [20, 67], [20, 70], [20, 76], [20, 112], [21, 65], [21, 91], [21, 100], [21, 109], [22, 65], [22, 96], [22, 107], [22, 120], [23, 68], [23, 69], [23, 75], [23, 103], [24, 63], [24, 79], [24, 84], [24, 106], [25, 73], [25, 83], [25, 92], [25, 99], [26, 74], [26, 92], [26, 94], [26, 113], [27, 66], [27, 76], [27, 108], [27, 113], [28, 67], [28, 90], [28, 93], [28, 94], [29, 89], [29, 98], [29, 109], [29, 116], [30, 73], [30, 78], [30, 93], [30, 117], [31, 71], [31, 85], [31, 88], [31, 111], [32, 62], [32, 71], [32, 95], [32, 98], [33, 80], [33, 81], [33, 89], [33, 101], [34, 77], [34, 95], [34, 102], [34, 104], [35, 75], [35, 78], [35, 97], [35, 99], [36, 75], [36, 92], [36, 115], [36, 117], [37, 76], [37, 91], [37, 101], [37, 115], [38, 90], [38, 92], [38, 105], [38, 109], [39, 72], [39, 88], [39, 90], [39, 106], [40, 65], [40, 74], [40, 79], [40, 89], [41, 69], [41, 94], [41, 107], [41, 119], [42, 72], [42, 98], [42, 108], [42, 119], [43, 83], [43, 93], [43, 97], [43, 115], [44, 61], [44, 84], [44, 116], [44, 117], [45, 70], [45, 95], [45, 100], [45, 119], [46, 61], [46, 72], [46, 85], [46, 120], [47, 64], [47, 84], [47, 95], [47, 103], [48, 66], [48, 83], [48, 85], [48, 103], [49, 64], [49, 76], [49, 78], [49, 80], [50, 73], [50, 88], [50, 96], [50, 110], [51, 79], [51, 87], [51, 91], [51, 98], [52, 80], [52, 105], [52, 107], [52, 118], [53, 65], [53, 88], [53, 97], [53, 104], [54, 64], [54, 89], [54, 114], [54, 115], [55, 69], [55, 77], [55, 82], [55, 83], [56, 81], [56, 82], [56, 108], [56, 112], [57, 102], [57, 106], [57, 112], [57, 117], [58, 77], [58, 84], [58, 96], [58, 101], [59, 110], [59, 114], [59, 118], [59, 119], [60, 73], [60, 87], [60, 104], [60, 107]]);;
R:=P177Census(D);;Need(Size(R.F)=240);;
PrintTo("current_c4_descent/120_068.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_068 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
