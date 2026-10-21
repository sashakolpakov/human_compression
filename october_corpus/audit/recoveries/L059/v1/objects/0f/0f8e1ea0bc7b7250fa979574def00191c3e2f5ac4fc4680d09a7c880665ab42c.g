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
D:=P177Graph("120_067",120,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60],[[1, 73], [1, 105], [1, 114], [1, 117], [2, 63], [2, 100], [2, 105], [2, 119], [3, 90], [3, 91], [3, 109], [3, 114], [4, 64], [4, 85], [4, 100], [4, 104], [5, 65], [5, 87], [5, 91], [5, 119], [6, 71], [6, 78], [6, 91], [6, 111], [7, 64], [7, 65], [7, 68], [7, 107], [8, 90], [8, 97], [8, 100], [8, 102], [9, 89], [9, 104], [9, 106], [9, 109], [10, 66], [10, 77], [10, 91], [10, 104], [11, 62], [11, 78], [11, 102], [11, 103], [12, 68], [12, 81], [12, 83], [12, 120], [13, 65], [13, 82], [13, 103], [13, 118], [14, 63], [14, 71], [14, 93], [14, 115], [15, 65], [15, 74], [15, 80], [15, 89], [16, 71], [16, 86], [16, 92], [16, 100], [17, 71], [17, 87], [17, 89], [17, 112], [18, 62], [18, 66], [18, 95], [18, 101], [19, 75], [19, 76], [19, 96], [19, 103], [20, 74], [20, 83], [20, 96], [20, 117], [21, 61], [21, 68], [21, 102], [21, 112], [22, 68], [22, 88], [22, 101], [22, 109], [23, 93], [23, 97], [23, 104], [23, 118], [24, 72], [24, 93], [24, 99], [24, 102], [25, 67], [25, 81], [25, 90], [25, 106], [26, 72], [26, 79], [26, 85], [26, 118], [27, 72], [27, 77], [27, 81], [27, 89], [28, 92], [28, 98], [28, 107], [28, 110], [29, 87], [29, 94], [29, 101], [29, 113], [30, 70], [30, 76], [30, 95], [30, 97], [31, 73], [31, 76], [31, 99], [31, 120], [32, 66], [32, 69], [32, 82], [32, 120], [33, 63], [33, 94], [33, 98], [33, 103], [34, 69], [34, 74], [34, 84], [34, 94], [35, 62], [35, 107], [35, 112], [35, 118], [36, 75], [36, 79], [36, 115], [36, 119], [37, 67], [37, 74], [37, 78], [37, 119], [38, 67], [38, 80], [38, 111], [38, 112], [39, 75], [39, 80], [39, 86], [39, 93], [40, 85], [40, 108], [40, 116], [40, 120], [41, 88], [41, 97], [41, 98], [41, 108], [42, 77], [42, 86], [42, 108], [42, 113], [43, 83], [43, 84], [43, 87], [43, 110], [44, 61], [44, 63], [44, 76], [44, 110], [45, 61], [45, 92], [45, 96], [45, 116], [46, 101], [46, 110], [46, 111], [46, 117], [47, 70], [47, 88], [47, 99], [47, 116], [48, 70], [48, 86], [48, 106], [48, 117], [49, 62], [49, 69], [49, 81], [49, 88], [50, 64], [50, 79], [50, 90], [50, 99], [51, 66], [51, 67], [51, 72], [51, 114], [52, 69], [52, 96], [52, 111], [52, 113], [53, 75], [53, 94], [53, 107], [53, 116], [54, 84], [54, 105], [54, 106], [54, 108], [55, 82], [55, 83], [55, 95], [55, 109], [56, 73], [56, 85], [56, 95], [56, 98], [57, 73], [57, 77], [57, 84], [57, 115], [58, 61], [58, 64], [58, 78], [58, 82], [59, 79], [59, 80], [59, 92], [59, 105], [60, 70], [60, 113], [60, 114], [60, 115]]);;
R:=P177Census(D);;Need(Size(R.F)=240);;
PrintTo("current_c4_descent/120_067.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_067 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
