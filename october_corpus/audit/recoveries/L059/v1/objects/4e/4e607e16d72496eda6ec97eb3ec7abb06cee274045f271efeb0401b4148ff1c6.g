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
D:=P177Graph("120_030",120,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60],[[1, 61], [1, 62], [1, 97], [1, 98], [2, 61], [2, 62], [2, 85], [2, 86], [3, 85], [3, 86], [3, 109], [3, 110], [4, 73], [4, 74], [4, 109], [4, 110], [5, 73], [5, 74], [5, 97], [5, 98], [6, 62], [6, 63], [6, 110], [6, 111], [7, 62], [7, 63], [7, 74], [7, 75], [8, 74], [8, 75], [8, 86], [8, 87], [9, 86], [9, 87], [9, 98], [9, 99], [10, 98], [10, 99], [10, 110], [10, 111], [11, 63], [11, 64], [11, 99], [11, 100], [12, 63], [12, 64], [12, 87], [12, 88], [13, 87], [13, 88], [13, 111], [13, 112], [14, 75], [14, 76], [14, 111], [14, 112], [15, 75], [15, 76], [15, 99], [15, 100], [16, 64], [16, 65], [16, 112], [16, 113], [17, 64], [17, 65], [17, 76], [17, 77], [18, 76], [18, 77], [18, 88], [18, 89], [19, 88], [19, 89], [19, 100], [19, 101], [20, 100], [20, 101], [20, 112], [20, 113], [21, 65], [21, 66], [21, 101], [21, 102], [22, 65], [22, 66], [22, 89], [22, 90], [23, 89], [23, 90], [23, 113], [23, 114], [24, 77], [24, 78], [24, 113], [24, 114], [25, 77], [25, 78], [25, 101], [25, 102], [26, 66], [26, 67], [26, 114], [26, 115], [27, 66], [27, 67], [27, 78], [27, 79], [28, 78], [28, 79], [28, 90], [28, 91], [29, 90], [29, 91], [29, 102], [29, 103], [30, 102], [30, 103], [30, 114], [30, 115], [31, 67], [31, 68], [31, 103], [31, 104], [32, 67], [32, 68], [32, 91], [32, 92], [33, 91], [33, 92], [33, 115], [33, 116], [34, 79], [34, 80], [34, 115], [34, 116], [35, 79], [35, 80], [35, 103], [35, 104], [36, 68], [36, 69], [36, 116], [36, 117], [37, 68], [37, 69], [37, 80], [37, 81], [38, 80], [38, 81], [38, 92], [38, 93], [39, 92], [39, 93], [39, 104], [39, 105], [40, 104], [40, 105], [40, 116], [40, 117], [41, 69], [41, 70], [41, 105], [41, 106], [42, 69], [42, 70], [42, 93], [42, 94], [43, 93], [43, 94], [43, 117], [43, 118], [44, 81], [44, 82], [44, 117], [44, 118], [45, 81], [45, 82], [45, 105], [45, 106], [46, 70], [46, 71], [46, 118], [46, 119], [47, 70], [47, 71], [47, 82], [47, 83], [48, 82], [48, 83], [48, 94], [48, 95], [49, 94], [49, 95], [49, 106], [49, 107], [50, 106], [50, 107], [50, 118], [50, 119], [51, 71], [51, 72], [51, 107], [51, 108], [52, 71], [52, 72], [52, 95], [52, 96], [53, 95], [53, 96], [53, 119], [53, 120], [54, 83], [54, 84], [54, 119], [54, 120], [55, 83], [55, 84], [55, 107], [55, 108], [56, 61], [56, 72], [56, 109], [56, 120], [57, 61], [57, 72], [57, 73], [57, 84], [58, 73], [58, 84], [58, 85], [58, 96], [59, 85], [59, 96], [59, 97], [59, 108], [60, 97], [60, 108], [60, 109], [60, 120]]);;
R:=P177Census(D);;Need(Size(R.F)=240);;
PrintTo("current_c4_descent/120_030.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_030 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
