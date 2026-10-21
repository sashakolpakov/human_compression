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
D:=P177Graph("120_066",120,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60],[[1, 68], [1, 71], [1, 93], [1, 118], [2, 78], [2, 82], [2, 91], [2, 98], [3, 72], [3, 86], [3, 95], [3, 99], [4, 74], [4, 83], [4, 96], [4, 111], [5, 77], [5, 89], [5, 101], [5, 118], [6, 61], [6, 71], [6, 103], [6, 109], [7, 73], [7, 97], [7, 114], [7, 117], [8, 100], [8, 102], [8, 106], [8, 120], [9, 76], [9, 85], [9, 107], [9, 117], [10, 62], [10, 65], [10, 84], [10, 97], [11, 62], [11, 69], [11, 85], [11, 115], [12, 64], [12, 104], [12, 108], [12, 113], [13, 67], [13, 81], [13, 88], [13, 110], [14, 66], [14, 75], [14, 103], [14, 112], [15, 64], [15, 65], [15, 67], [15, 99], [16, 63], [16, 74], [16, 79], [16, 116], [17, 82], [17, 102], [17, 104], [17, 115], [18, 70], [18, 89], [18, 95], [18, 113], [19, 90], [19, 105], [19, 107], [19, 110], [20, 87], [20, 94], [20, 114], [20, 120], [21, 76], [21, 81], [21, 96], [21, 119], [22, 80], [22, 84], [22, 88], [22, 101], [23, 73], [23, 92], [23, 100], [23, 109], [24, 83], [24, 91], [24, 93], [24, 108], [25, 70], [25, 75], [25, 80], [25, 92], [26, 68], [26, 69], [26, 106], [26, 111], [27, 66], [27, 90], [27, 94], [27, 116], [28, 61], [28, 63], [28, 77], [28, 119], [29, 78], [29, 86], [29, 87], [29, 112], [30, 72], [30, 79], [30, 98], [30, 105], [31, 67], [31, 72], [31, 94], [31, 117], [32, 77], [32, 81], [32, 92], [32, 97], [33, 71], [33, 85], [33, 96], [33, 100], [34, 73], [34, 84], [34, 95], [34, 112], [35, 78], [35, 90], [35, 102], [35, 117], [36, 62], [36, 72], [36, 104], [36, 110], [37, 74], [37, 98], [37, 113], [37, 118], [38, 99], [38, 101], [38, 105], [38, 119], [39, 75], [39, 86], [39, 108], [39, 118], [40, 61], [40, 66], [40, 83], [40, 98], [41, 61], [41, 70], [41, 86], [41, 116], [42, 63], [42, 103], [42, 107], [42, 114], [43, 68], [43, 82], [43, 87], [43, 109], [44, 65], [44, 76], [44, 104], [44, 111], [45, 63], [45, 66], [45, 68], [45, 100], [46, 64], [46, 73], [46, 80], [46, 115], [47, 81], [47, 101], [47, 103], [47, 116], [48, 69], [48, 90], [48, 96], [48, 114], [49, 89], [49, 106], [49, 108], [49, 109], [50, 88], [50, 93], [50, 113], [50, 119], [51, 75], [51, 82], [51, 95], [51, 120], [52, 79], [52, 83], [52, 87], [52, 102], [53, 74], [53, 91], [53, 99], [53, 110], [54, 84], [54, 92], [54, 94], [54, 107], [55, 69], [55, 76], [55, 79], [55, 91], [56, 67], [56, 70], [56, 105], [56, 112], [57, 65], [57, 89], [57, 93], [57, 115], [58, 62], [58, 64], [58, 78], [58, 120], [59, 77], [59, 85], [59, 88], [59, 111], [60, 71], [60, 80], [60, 97], [60, 106]]);;
R:=P177Census(D);;Need(Size(R.F)=240);;
PrintTo("current_c4_descent/120_066.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_066 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
