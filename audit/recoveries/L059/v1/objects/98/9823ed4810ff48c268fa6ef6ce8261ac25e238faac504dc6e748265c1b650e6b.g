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
D:=P177Graph("120_062",120,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60],[[1, 73], [1, 90], [1, 106], [1, 117], [2, 64], [2, 72], [2, 101], [2, 116], [3, 83], [3, 91], [3, 98], [3, 108], [4, 68], [4, 82], [4, 93], [4, 99], [5, 75], [5, 96], [5, 110], [5, 113], [6, 64], [6, 92], [6, 100], [6, 113], [7, 67], [7, 73], [7, 76], [7, 83], [8, 93], [8, 95], [8, 116], [8, 118], [9, 71], [9, 89], [9, 98], [9, 110], [10, 82], [10, 102], [10, 106], [10, 107], [11, 71], [11, 88], [11, 95], [11, 103], [12, 66], [12, 86], [12, 89], [12, 107], [13, 70], [13, 87], [13, 100], [13, 102], [14, 65], [14, 76], [14, 92], [14, 104], [15, 67], [15, 69], [15, 85], [15, 118], [16, 66], [16, 69], [16, 109], [16, 115], [17, 70], [17, 97], [17, 103], [17, 105], [18, 63], [18, 81], [18, 86], [18, 104], [19, 84], [19, 85], [19, 87], [19, 114], [20, 65], [20, 74], [20, 88], [20, 94], [21, 81], [21, 84], [21, 111], [21, 120], [22, 62], [22, 94], [22, 112], [22, 114], [23, 61], [23, 74], [23, 78], [23, 109], [24, 77], [24, 79], [24, 105], [24, 115], [25, 63], [25, 80], [25, 97], [25, 119], [26, 62], [26, 68], [26, 80], [26, 108], [27, 78], [27, 96], [27, 99], [27, 120], [28, 75], [28, 79], [28, 90], [28, 112], [29, 61], [29, 101], [29, 117], [29, 119], [30, 72], [30, 77], [30, 91], [30, 111], [31, 74], [31, 89], [31, 105], [31, 118], [32, 63], [32, 71], [32, 102], [32, 115], [33, 84], [33, 92], [33, 97], [33, 107], [34, 67], [34, 81], [34, 94], [34, 100], [35, 76], [35, 95], [35, 109], [35, 114], [36, 63], [36, 91], [36, 99], [36, 114], [37, 68], [37, 74], [37, 75], [37, 84], [38, 94], [38, 96], [38, 115], [38, 117], [39, 72], [39, 90], [39, 97], [39, 109], [40, 81], [40, 101], [40, 105], [40, 108], [41, 72], [41, 87], [41, 96], [41, 104], [42, 65], [42, 85], [42, 90], [42, 108], [43, 69], [43, 88], [43, 99], [43, 101], [44, 66], [44, 75], [44, 91], [44, 103], [45, 68], [45, 70], [45, 86], [45, 117], [46, 65], [46, 70], [46, 110], [46, 116], [47, 69], [47, 98], [47, 104], [47, 106], [48, 64], [48, 82], [48, 85], [48, 103], [49, 83], [49, 86], [49, 88], [49, 113], [50, 66], [50, 73], [50, 87], [50, 93], [51, 82], [51, 83], [51, 112], [51, 119], [52, 61], [52, 93], [52, 111], [52, 113], [53, 62], [53, 73], [53, 77], [53, 110], [54, 78], [54, 80], [54, 106], [54, 116], [55, 64], [55, 79], [55, 98], [55, 120], [56, 61], [56, 67], [56, 79], [56, 107], [57, 77], [57, 95], [57, 100], [57, 119], [58, 76], [58, 80], [58, 89], [58, 111], [59, 62], [59, 102], [59, 118], [59, 120], [60, 71], [60, 78], [60, 92], [60, 112]]);;
R:=P177Census(D);;Need(Size(R.F)=1440);;
PrintTo("current_c4_descent/120_062.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_062 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
