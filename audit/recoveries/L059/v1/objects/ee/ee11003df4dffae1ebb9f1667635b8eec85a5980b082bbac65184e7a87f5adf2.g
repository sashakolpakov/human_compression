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
D:=P177Graph("120_069",120,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60],[[1, 88], [1, 97], [1, 100], [1, 107], [2, 88], [2, 90], [2, 93], [2, 95], [3, 70], [3, 97], [3, 102], [3, 108], [4, 63], [4, 67], [4, 90], [4, 100], [5, 95], [5, 104], [5, 112], [5, 114], [6, 105], [6, 107], [6, 108], [6, 113], [7, 63], [7, 98], [7, 102], [7, 119], [8, 63], [8, 64], [8, 103], [8, 105], [9, 68], [9, 93], [9, 102], [9, 112], [10, 76], [10, 97], [10, 99], [10, 114], [11, 73], [11, 75], [11, 94], [11, 113], [12, 70], [12, 75], [12, 77], [12, 98], [13, 67], [13, 87], [13, 103], [13, 114], [14, 82], [14, 84], [14, 85], [14, 119], [15, 69], [15, 74], [15, 95], [15, 105], [16, 68], [16, 80], [16, 111], [16, 115], [17, 65], [17, 80], [17, 99], [17, 104], [18, 86], [18, 93], [18, 94], [18, 105], [19, 61], [19, 76], [19, 89], [19, 96], [20, 66], [20, 73], [20, 76], [20, 81], [21, 75], [21, 83], [21, 99], [21, 100], [22, 72], [22, 87], [22, 109], [22, 120], [23, 63], [23, 82], [23, 91], [23, 113], [24, 64], [24, 69], [24, 71], [24, 109], [25, 67], [25, 102], [25, 115], [25, 117], [26, 85], [26, 92], [26, 108], [26, 112], [27, 74], [27, 78], [27, 91], [27, 106], [28, 62], [28, 74], [28, 92], [28, 111], [29, 69], [29, 80], [29, 86], [29, 88], [30, 70], [30, 92], [30, 93], [30, 96], [31, 68], [31, 85], [31, 96], [31, 97], [32, 72], [32, 75], [32, 76], [32, 88], [33, 77], [33, 83], [33, 85], [33, 118], [34, 72], [34, 83], [34, 107], [34, 114], [35, 79], [35, 89], [35, 103], [35, 112], [36, 64], [36, 81], [36, 82], [36, 107], [37, 100], [37, 109], [37, 115], [37, 119], [38, 79], [38, 118], [38, 119], [38, 120], [39, 62], [39, 71], [39, 91], [39, 117], [40, 90], [40, 98], [40, 109], [40, 117], [41, 67], [41, 79], [41, 104], [41, 106], [42, 84], [42, 92], [42, 106], [42, 117], [43, 87], [43, 89], [43, 95], [43, 106], [44, 74], [44, 80], [44, 90], [44, 94], [45, 65], [45, 66], [45, 86], [45, 89], [46, 78], [46, 81], [46, 86], [46, 96], [47, 81], [47, 91], [47, 103], [47, 108], [48, 62], [48, 70], [48, 73], [48, 116], [49, 69], [49, 72], [49, 101], [49, 110], [50, 65], [50, 68], [50, 116], [50, 118], [51, 61], [51, 79], [51, 82], [51, 83], [52, 64], [52, 66], [52, 110], [52, 120], [53, 99], [53, 101], [53, 115], [53, 116], [54, 62], [54, 77], [54, 110], [54, 113], [55, 101], [55, 104], [55, 111], [55, 118], [56, 94], [56, 98], [56, 110], [56, 116], [57, 66], [57, 71], [57, 87], [57, 101], [58, 61], [58, 65], [58, 73], [58, 78], [59, 61], [59, 77], [59, 84], [59, 120], [60, 71], [60, 78], [60, 84], [60, 111]]);;
R:=P177Census(D);;Need(Size(R.F)=240);;
PrintTo("current_c4_descent/120_069.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_069 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
