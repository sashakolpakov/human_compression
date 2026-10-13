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
D:=P177Graph("120_021",120,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60],[[1, 61], [1, 62], [1, 105], [1, 106], [2, 61], [2, 62], [2, 77], [2, 78], [3, 77], [3, 78], [3, 93], [3, 94], [4, 93], [4, 94], [4, 109], [4, 110], [5, 65], [5, 66], [5, 109], [5, 110], [6, 65], [6, 66], [6, 81], [6, 82], [7, 81], [7, 82], [7, 97], [7, 98], [8, 97], [8, 98], [8, 113], [8, 114], [9, 69], [9, 70], [9, 113], [9, 114], [10, 69], [10, 70], [10, 85], [10, 86], [11, 85], [11, 86], [11, 101], [11, 102], [12, 101], [12, 102], [12, 117], [12, 118], [13, 73], [13, 74], [13, 117], [13, 118], [14, 73], [14, 74], [14, 89], [14, 90], [15, 89], [15, 90], [15, 105], [15, 106], [16, 62], [16, 63], [16, 118], [16, 119], [17, 62], [17, 63], [17, 66], [17, 67], [18, 66], [18, 67], [18, 70], [18, 71], [19, 70], [19, 71], [19, 74], [19, 75], [20, 74], [20, 75], [20, 78], [20, 79], [21, 78], [21, 79], [21, 82], [21, 83], [22, 82], [22, 83], [22, 86], [22, 87], [23, 86], [23, 87], [23, 90], [23, 91], [24, 90], [24, 91], [24, 94], [24, 95], [25, 94], [25, 95], [25, 98], [25, 99], [26, 98], [26, 99], [26, 102], [26, 103], [27, 102], [27, 103], [27, 106], [27, 107], [28, 106], [28, 107], [28, 110], [28, 111], [29, 110], [29, 111], [29, 114], [29, 115], [30, 114], [30, 115], [30, 118], [30, 119], [31, 63], [31, 64], [31, 107], [31, 108], [32, 63], [32, 64], [32, 79], [32, 80], [33, 79], [33, 80], [33, 95], [33, 96], [34, 95], [34, 96], [34, 111], [34, 112], [35, 67], [35, 68], [35, 111], [35, 112], [36, 67], [36, 68], [36, 83], [36, 84], [37, 83], [37, 84], [37, 99], [37, 100], [38, 99], [38, 100], [38, 115], [38, 116], [39, 71], [39, 72], [39, 115], [39, 116], [40, 71], [40, 72], [40, 87], [40, 88], [41, 87], [41, 88], [41, 103], [41, 104], [42, 103], [42, 104], [42, 119], [42, 120], [43, 75], [43, 76], [43, 119], [43, 120], [44, 75], [44, 76], [44, 91], [44, 92], [45, 91], [45, 92], [45, 107], [45, 108], [46, 61], [46, 64], [46, 117], [46, 120], [47, 61], [47, 64], [47, 65], [47, 68], [48, 65], [48, 68], [48, 69], [48, 72], [49, 69], [49, 72], [49, 73], [49, 76], [50, 73], [50, 76], [50, 77], [50, 80], [51, 77], [51, 80], [51, 81], [51, 84], [52, 81], [52, 84], [52, 85], [52, 88], [53, 85], [53, 88], [53, 89], [53, 92], [54, 89], [54, 92], [54, 93], [54, 96], [55, 93], [55, 96], [55, 97], [55, 100], [56, 97], [56, 100], [56, 101], [56, 104], [57, 101], [57, 104], [57, 105], [57, 108], [58, 105], [58, 108], [58, 109], [58, 112], [59, 109], [59, 112], [59, 113], [59, 116], [60, 113], [60, 116], [60, 117], [60, 120]]);;
R:=P177Census(D);;Need(Size(R.F)=240);;
PrintTo("current_c4_descent/120_021.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_021 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
