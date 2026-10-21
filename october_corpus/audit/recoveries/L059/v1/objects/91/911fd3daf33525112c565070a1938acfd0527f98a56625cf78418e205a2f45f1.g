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
D:=P177Graph("120_050",120,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60],[[1, 61], [1, 62], [1, 63], [1, 65], [2, 61], [2, 64], [2, 66], [2, 69], [3, 62], [3, 67], [3, 70], [3, 73], [4, 63], [4, 66], [4, 68], [4, 74], [5, 64], [5, 67], [5, 75], [5, 79], [6, 65], [6, 70], [6, 71], [6, 80], [7, 63], [7, 66], [7, 72], [7, 81], [8, 68], [8, 71], [8, 82], [8, 87], [9, 69], [9, 75], [9, 76], [9, 88], [10, 65], [10, 70], [10, 77], [10, 81], [11, 61], [11, 66], [11, 78], [11, 89], [12, 72], [12, 76], [12, 77], [12, 83], [13, 73], [13, 79], [13, 83], [13, 88], [14, 74], [14, 82], [14, 84], [14, 95], [15, 69], [15, 74], [15, 75], [15, 82], [16, 62], [16, 70], [16, 85], [16, 89], [17, 61], [17, 63], [17, 86], [17, 94], [18, 78], [18, 84], [18, 85], [18, 90], [19, 73], [19, 79], [19, 80], [19, 87], [20, 80], [20, 87], [20, 90], [20, 95], [21, 77], [21, 81], [21, 91], [21, 102], [22, 64], [22, 75], [22, 92], [22, 94], [23, 62], [23, 65], [23, 93], [23, 101], [24, 86], [24, 91], [24, 92], [24, 96], [25, 83], [25, 88], [25, 96], [25, 102], [26, 72], [26, 81], [26, 97], [26, 109], [27, 85], [27, 89], [27, 98], [27, 110], [28, 67], [28, 79], [28, 99], [28, 101], [29, 68], [29, 82], [29, 86], [29, 92], [30, 64], [30, 69], [30, 100], [30, 108], [31, 93], [31, 97], [31, 99], [31, 103], [32, 92], [32, 94], [32, 98], [32, 104], [33, 76], [33, 88], [33, 103], [33, 109], [34, 90], [34, 95], [34, 104], [34, 110], [35, 68], [35, 74], [35, 105], [35, 114], [36, 78], [36, 89], [36, 106], [36, 115], [37, 67], [37, 73], [37, 107], [37, 108], [38, 71], [38, 87], [38, 93], [38, 99], [39, 72], [39, 77], [39, 78], [39, 85], [40, 100], [40, 105], [40, 107], [40, 111], [41, 99], [41, 101], [41, 106], [41, 112], [42, 71], [42, 80], [42, 111], [42, 114], [43, 84], [43, 95], [43, 112], [43, 115], [44, 96], [44, 102], [44, 104], [44, 110], [45, 86], [45, 94], [45, 113], [45, 118], [46, 76], [46, 83], [46, 100], [46, 107], [47, 107], [47, 108], [47, 113], [47, 116], [48, 91], [48, 102], [48, 116], [48, 118], [49, 103], [49, 109], [49, 112], [49, 115], [50, 93], [50, 101], [50, 117], [50, 120], [51, 84], [51, 90], [51, 105], [51, 111], [52, 100], [52, 108], [52, 117], [52, 119], [53, 111], [53, 114], [53, 116], [53, 118], [54, 97], [54, 109], [54, 119], [54, 120], [55, 98], [55, 110], [55, 113], [55, 116], [56, 91], [56, 96], [56, 97], [56, 103], [57, 105], [57, 114], [57, 119], [57, 120], [58, 106], [58, 115], [58, 117], [58, 119], [59, 98], [59, 104], [59, 106], [59, 112], [60, 113], [60, 117], [60, 118], [60, 120]]);;
R:=P177Census(D);;Need(Size(R.F)=240);;
PrintTo("current_c4_descent/120_050.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_050 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
