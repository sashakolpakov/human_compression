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
D:=P177Graph("120_023",120,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60],[[1, 63], [1, 70], [1, 86], [1, 98], [2, 63], [2, 70], [2, 82], [2, 111], [3, 75], [3, 88], [3, 94], [3, 108], [4, 75], [4, 88], [4, 96], [4, 101], [5, 61], [5, 62], [5, 86], [5, 98], [6, 61], [6, 83], [6, 109], [6, 112], [7, 64], [7, 71], [7, 79], [7, 107], [8, 68], [8, 87], [8, 89], [8, 119], [9, 65], [9, 73], [9, 101], [9, 118], [10, 61], [10, 85], [10, 96], [10, 109], [11, 64], [11, 71], [11, 87], [11, 102], [12, 68], [12, 86], [12, 89], [12, 104], [13, 71], [13, 101], [13, 114], [13, 118], [14, 64], [14, 82], [14, 88], [14, 111], [15, 63], [15, 94], [15, 105], [15, 108], [16, 62], [16, 93], [16, 117], [16, 120], [17, 66], [17, 74], [17, 82], [17, 99], [18, 76], [18, 84], [18, 110], [18, 115], [19, 78], [19, 84], [19, 97], [19, 116], [20, 74], [20, 92], [20, 100], [20, 120], [21, 72], [21, 85], [21, 114], [21, 115], [22, 77], [22, 90], [22, 104], [22, 117], [23, 62], [23, 93], [23, 97], [23, 102], [24, 72], [24, 82], [24, 99], [24, 114], [25, 76], [25, 81], [25, 100], [25, 110], [26, 75], [26, 87], [26, 116], [26, 119], [27, 78], [27, 80], [27, 111], [27, 116], [28, 65], [28, 73], [28, 98], [28, 106], [29, 74], [29, 92], [29, 94], [29, 103], [30, 73], [30, 85], [30, 93], [30, 115], [31, 65], [31, 104], [31, 110], [31, 117], [32, 76], [32, 89], [32, 96], [32, 101], [33, 61], [33, 62], [33, 118], [33, 119], [34, 70], [34, 83], [34, 92], [34, 112], [35, 70], [35, 79], [35, 92], [35, 107], [36, 67], [36, 79], [36, 95], [36, 105], [37, 67], [37, 80], [37, 90], [37, 111], [38, 67], [38, 90], [38, 98], [38, 106], [39, 69], [39, 91], [39, 118], [39, 119], [40, 66], [40, 83], [40, 106], [40, 113], [41, 69], [41, 91], [41, 95], [41, 103], [42, 78], [42, 85], [42, 91], [42, 96], [43, 67], [43, 81], [43, 105], [43, 112], [44, 69], [44, 72], [44, 97], [44, 102], [45, 66], [45, 80], [45, 107], [45, 113], [46, 77], [46, 95], [46, 103], [46, 113], [47, 68], [47, 84], [47, 97], [47, 109], [48, 68], [48, 100], [48, 109], [48, 120], [49, 77], [49, 90], [49, 99], [49, 108], [50, 69], [50, 72], [50, 80], [50, 107], [51, 76], [51, 83], [51, 89], [51, 106], [52, 65], [52, 87], [52, 102], [52, 110], [53, 66], [53, 74], [53, 86], [53, 104], [54, 71], [54, 94], [54, 103], [54, 114], [55, 64], [55, 84], [55, 88], [55, 115], [56, 63], [56, 105], [56, 117], [56, 120], [57, 78], [57, 91], [57, 99], [57, 108], [58, 73], [58, 81], [58, 93], [58, 112], [59, 77], [59, 81], [59, 100], [59, 113], [60, 75], [60, 79], [60, 95], [60, 116]]);;
R:=P177Census(D);;Need(Size(R.F)=240);;
PrintTo("current_c4_descent/120_023.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_023 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
