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
D:=P177Graph("120_065",120,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60],[[1, 80], [1, 94], [1, 109], [1, 114], [2, 71], [2, 97], [2, 108], [2, 113], [3, 83], [3, 90], [3, 94], [3, 115], [4, 65], [4, 71], [4, 89], [4, 112], [5, 63], [5, 87], [5, 115], [5, 117], [6, 65], [6, 86], [6, 100], [6, 118], [7, 63], [7, 75], [7, 81], [7, 101], [8, 68], [8, 73], [8, 82], [8, 100], [9, 61], [9, 75], [9, 109], [9, 120], [10, 62], [10, 73], [10, 97], [10, 105], [11, 64], [11, 74], [11, 80], [11, 112], [12, 78], [12, 104], [12, 113], [12, 117], [13, 76], [13, 83], [13, 86], [13, 98], [14, 81], [14, 89], [14, 91], [14, 103], [15, 68], [15, 72], [15, 87], [15, 110], [16, 61], [16, 92], [16, 96], [16, 118], [17, 66], [17, 93], [17, 101], [17, 105], [18, 70], [18, 82], [18, 95], [18, 114], [19, 99], [19, 108], [19, 116], [19, 120], [20, 62], [20, 69], [20, 77], [20, 90], [21, 64], [21, 69], [21, 85], [21, 107], [22, 74], [22, 84], [22, 104], [22, 119], [23, 67], [23, 76], [23, 78], [23, 111], [24, 79], [24, 88], [24, 91], [24, 98], [25, 85], [25, 103], [25, 106], [25, 110], [26, 72], [26, 84], [26, 96], [26, 102], [27, 67], [27, 92], [27, 93], [27, 107], [28, 66], [28, 70], [28, 88], [28, 119], [29, 95], [29, 106], [29, 111], [29, 116], [30, 77], [30, 79], [30, 99], [30, 102], [31, 79], [31, 93], [31, 110], [31, 113], [32, 72], [32, 98], [32, 107], [32, 114], [33, 84], [33, 89], [33, 93], [33, 116], [34, 66], [34, 72], [34, 90], [34, 111], [35, 64], [35, 88], [35, 116], [35, 118], [36, 66], [36, 85], [36, 99], [36, 117], [37, 64], [37, 76], [37, 82], [37, 102], [38, 67], [38, 74], [38, 81], [38, 99], [39, 62], [39, 76], [39, 110], [39, 119], [40, 61], [40, 74], [40, 98], [40, 106], [41, 63], [41, 73], [41, 79], [41, 111], [42, 77], [42, 103], [42, 114], [42, 118], [43, 75], [43, 84], [43, 85], [43, 97], [44, 82], [44, 90], [44, 92], [44, 104], [45, 67], [45, 71], [45, 88], [45, 109], [46, 62], [46, 91], [46, 95], [46, 117], [47, 65], [47, 94], [47, 102], [47, 106], [48, 69], [48, 81], [48, 96], [48, 113], [49, 100], [49, 107], [49, 115], [49, 119], [50, 61], [50, 70], [50, 78], [50, 89], [51, 63], [51, 70], [51, 86], [51, 108], [52, 73], [52, 83], [52, 103], [52, 120], [53, 68], [53, 75], [53, 77], [53, 112], [54, 80], [54, 87], [54, 92], [54, 97], [55, 86], [55, 104], [55, 105], [55, 109], [56, 71], [56, 83], [56, 95], [56, 101], [57, 68], [57, 91], [57, 94], [57, 108], [58, 65], [58, 69], [58, 87], [58, 120], [59, 96], [59, 105], [59, 112], [59, 115], [60, 78], [60, 80], [60, 100], [60, 101]]);;
R:=P177Census(D);;Need(Size(R.F)=240);;
PrintTo("current_c4_descent/120_065.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_065 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
