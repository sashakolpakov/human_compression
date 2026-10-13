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
D:=P177Graph("120_054",120,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60],[[1, 61], [1, 62], [1, 63], [1, 65], [2, 61], [2, 64], [2, 66], [2, 69], [3, 62], [3, 67], [3, 70], [3, 73], [4, 63], [4, 66], [4, 68], [4, 74], [5, 64], [5, 67], [5, 75], [5, 79], [6, 65], [6, 70], [6, 71], [6, 80], [7, 63], [7, 66], [7, 72], [7, 81], [8, 68], [8, 71], [8, 82], [8, 87], [9, 69], [9, 75], [9, 76], [9, 88], [10, 65], [10, 70], [10, 77], [10, 89], [11, 61], [11, 66], [11, 78], [11, 90], [12, 72], [12, 76], [12, 91], [12, 97], [13, 73], [13, 79], [13, 83], [13, 98], [14, 74], [14, 76], [14, 82], [14, 88], [15, 69], [15, 75], [15, 84], [15, 99], [16, 62], [16, 70], [16, 85], [16, 100], [17, 61], [17, 63], [17, 86], [17, 96], [18, 77], [18, 83], [18, 101], [18, 108], [19, 76], [19, 78], [19, 97], [19, 102], [20, 73], [20, 79], [20, 92], [20, 109], [21, 80], [21, 83], [21, 87], [21, 98], [22, 71], [22, 80], [22, 81], [22, 91], [23, 74], [23, 82], [23, 93], [23, 110], [24, 64], [24, 75], [24, 94], [24, 107], [25, 62], [25, 65], [25, 95], [25, 107], [26, 84], [26, 92], [26, 111], [26, 114], [27, 83], [27, 85], [27, 106], [27, 108], [28, 71], [28, 86], [28, 87], [28, 105], [29, 80], [29, 87], [29, 103], [29, 112], [30, 88], [30, 92], [30, 97], [30, 109], [31, 68], [31, 74], [31, 89], [31, 101], [32, 67], [32, 73], [32, 90], [32, 102], [33, 81], [33, 91], [33, 104], [33, 115], [34, 67], [34, 79], [34, 96], [34, 105], [35, 68], [35, 82], [35, 94], [35, 95], [36, 64], [36, 69], [36, 100], [36, 106], [37, 93], [37, 103], [37, 116], [37, 118], [38, 92], [38, 94], [38, 95], [38, 114], [39, 88], [39, 97], [39, 103], [39, 112], [40, 84], [40, 98], [40, 99], [40, 108], [41, 72], [41, 81], [41, 99], [41, 111], [42, 89], [42, 101], [42, 113], [42, 117], [43, 90], [43, 102], [43, 104], [43, 119], [44, 72], [44, 85], [44, 91], [44, 106], [45, 104], [45, 112], [45, 118], [45, 119], [46, 84], [46, 86], [46, 105], [46, 111], [47, 94], [47, 103], [47, 107], [47, 118], [48, 93], [48, 98], [48, 108], [48, 110], [49, 77], [49, 89], [49, 109], [49, 114], [50, 78], [50, 90], [50, 110], [50, 116], [51, 99], [51, 111], [51, 113], [51, 117], [52, 100], [52, 106], [52, 113], [52, 120], [53, 93], [53, 96], [53, 105], [53, 116], [54, 77], [54, 78], [54, 101], [54, 102], [55, 110], [55, 113], [55, 116], [55, 120], [56, 104], [56, 109], [56, 114], [56, 115], [57, 85], [57, 100], [57, 112], [57, 118], [58, 86], [58, 96], [58, 115], [58, 119], [59, 95], [59, 107], [59, 117], [59, 120], [60, 115], [60, 117], [60, 119], [60, 120]]);;
R:=P177Census(D);;Need(Size(R.F)=240);;
PrintTo("current_c4_descent/120_054.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_054 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
