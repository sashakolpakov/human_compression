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
D:=P177Graph("110_007",110,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55],[[1, 67], [1, 83], [1, 86], [1, 107], [2, 63], [2, 64], [2, 107], [2, 110], [3, 70], [3, 72], [3, 103], [3, 110], [4, 59], [4, 71], [4, 103], [4, 105], [5, 67], [5, 81], [5, 96], [5, 105], [6, 58], [6, 69], [6, 84], [6, 100], [7, 59], [7, 82], [7, 100], [7, 101], [8, 59], [8, 75], [8, 76], [8, 92], [9, 60], [9, 68], [9, 76], [9, 110], [10, 68], [10, 69], [10, 96], [10, 97], [11, 70], [11, 78], [11, 91], [11, 108], [12, 60], [12, 70], [12, 87], [12, 95], [13, 60], [13, 98], [13, 102], [13, 107], [14, 59], [14, 90], [14, 102], [14, 104], [15, 90], [15, 97], [15, 99], [15, 108], [16, 61], [16, 75], [16, 105], [16, 106], [17, 64], [17, 75], [17, 89], [17, 104], [18, 73], [18, 93], [18, 100], [18, 104], [19, 60], [19, 73], [19, 77], [19, 86], [20, 79], [20, 86], [20, 99], [20, 106], [21, 63], [21, 68], [21, 98], [21, 109], [22, 67], [22, 77], [22, 82], [22, 98], [23, 56], [23, 66], [23, 70], [23, 77], [24, 66], [24, 84], [24, 88], [24, 104], [25, 62], [25, 63], [25, 79], [25, 84], [26, 83], [26, 90], [26, 93], [26, 101], [27, 69], [27, 87], [27, 88], [27, 93], [28, 75], [28, 80], [28, 81], [28, 88], [29, 77], [29, 78], [29, 81], [29, 85], [30, 62], [30, 78], [30, 101], [30, 103], [31, 56], [31, 58], [31, 86], [31, 95], [32, 56], [32, 85], [32, 89], [32, 108], [33, 85], [33, 94], [33, 96], [33, 98], [34, 57], [34, 61], [34, 88], [34, 96], [35, 61], [35, 76], [35, 95], [35, 103], [36, 64], [36, 80], [36, 84], [36, 91], [37, 57], [37, 67], [37, 80], [37, 106], [38, 57], [38, 72], [38, 93], [38, 97], [39, 65], [39, 85], [39, 97], [39, 109], [40, 64], [40, 76], [40, 102], [40, 109], [41, 78], [41, 82], [41, 94], [41, 105], [42, 63], [42, 65], [42, 69], [42, 94], [43, 56], [43, 65], [43, 92], [43, 99], [44, 57], [44, 74], [44, 83], [44, 99], [45, 73], [45, 82], [45, 83], [45, 102], [46, 61], [46, 68], [46, 72], [46, 87], [47, 72], [47, 74], [47, 101], [47, 108], [48, 74], [48, 79], [48, 80], [48, 107], [49, 58], [49, 65], [49, 71], [49, 79], [50, 58], [50, 66], [50, 73], [50, 87], [51, 89], [51, 90], [51, 92], [51, 109], [52, 71], [52, 92], [52, 95], [52, 106], [53, 62], [53, 71], [53, 94], [53, 100], [54, 62], [54, 74], [54, 91], [54, 110], [55, 66], [55, 81], [55, 89], [55, 91]]);;
R:=P177Census(D);;Need(Size(R.F)=1320);;
PrintTo("current_c4_descent/110_007.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 110_007 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
