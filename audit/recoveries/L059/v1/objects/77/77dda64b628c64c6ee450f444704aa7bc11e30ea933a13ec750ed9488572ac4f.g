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
D:=P177Graph("120_058",120,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60],[[1, 61], [1, 62], [1, 76], [1, 77], [2, 61], [2, 62], [2, 71], [2, 72], [3, 66], [3, 67], [3, 71], [3, 72], [4, 66], [4, 67], [4, 76], [4, 77], [5, 62], [5, 63], [5, 86], [5, 87], [6, 62], [6, 63], [6, 81], [6, 82], [7, 67], [7, 68], [7, 81], [7, 82], [8, 67], [8, 68], [8, 86], [8, 87], [9, 63], [9, 64], [9, 96], [9, 97], [10, 63], [10, 64], [10, 91], [10, 92], [11, 68], [11, 69], [11, 91], [11, 92], [12, 68], [12, 69], [12, 96], [12, 97], [13, 64], [13, 65], [13, 106], [13, 107], [14, 64], [14, 65], [14, 101], [14, 102], [15, 69], [15, 70], [15, 101], [15, 102], [16, 69], [16, 70], [16, 106], [16, 107], [17, 61], [17, 65], [17, 116], [17, 117], [18, 61], [18, 65], [18, 111], [18, 112], [19, 66], [19, 70], [19, 111], [19, 112], [20, 66], [20, 70], [20, 116], [20, 117], [21, 72], [21, 73], [21, 87], [21, 88], [22, 72], [22, 73], [22, 82], [22, 83], [23, 77], [23, 78], [23, 82], [23, 83], [24, 77], [24, 78], [24, 87], [24, 88], [25, 81], [25, 85], [25, 97], [25, 98], [26, 81], [26, 85], [26, 92], [26, 93], [27, 86], [27, 90], [27, 92], [27, 93], [28, 86], [28, 90], [28, 97], [28, 98], [29, 91], [29, 95], [29, 107], [29, 108], [30, 91], [30, 95], [30, 102], [30, 103], [31, 96], [31, 100], [31, 102], [31, 103], [32, 96], [32, 100], [32, 107], [32, 108], [33, 101], [33, 105], [33, 117], [33, 118], [34, 101], [34, 105], [34, 112], [34, 113], [35, 106], [35, 110], [35, 112], [35, 113], [36, 106], [36, 110], [36, 117], [36, 118], [37, 71], [37, 75], [37, 116], [37, 120], [38, 71], [38, 75], [38, 111], [38, 115], [39, 76], [39, 80], [39, 111], [39, 115], [40, 76], [40, 80], [40, 116], [40, 120], [41, 83], [41, 84], [41, 109], [41, 110], [42, 83], [42, 84], [42, 104], [42, 105], [43, 88], [43, 89], [43, 104], [43, 105], [44, 88], [44, 89], [44, 109], [44, 110], [45, 93], [45, 94], [45, 119], [45, 120], [46, 93], [46, 94], [46, 114], [46, 115], [47, 98], [47, 99], [47, 114], [47, 115], [48, 98], [48, 99], [48, 119], [48, 120], [49, 73], [49, 74], [49, 108], [49, 109], [50, 73], [50, 74], [50, 103], [50, 104], [51, 78], [51, 79], [51, 103], [51, 104], [52, 78], [52, 79], [52, 108], [52, 109], [53, 84], [53, 85], [53, 118], [53, 119], [54, 84], [54, 85], [54, 113], [54, 114], [55, 89], [55, 90], [55, 113], [55, 114], [56, 89], [56, 90], [56, 118], [56, 119], [57, 74], [57, 75], [57, 99], [57, 100], [58, 74], [58, 75], [58, 94], [58, 95], [59, 79], [59, 80], [59, 94], [59, 95], [60, 79], [60, 80], [60, 99], [60, 100]]);;
R:=P177Census(D);;Need(Size(R.F)=3840);;
PrintTo("current_c4_descent/120_058.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_058 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
