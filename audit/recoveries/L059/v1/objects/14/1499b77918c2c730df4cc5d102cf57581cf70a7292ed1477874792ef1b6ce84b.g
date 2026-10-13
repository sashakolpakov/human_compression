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
D:=P177Graph("108_022",108,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54],[[1, 55], [1, 56], [1, 57], [1, 59], [2, 55], [2, 58], [2, 60], [2, 63], [3, 56], [3, 61], [3, 64], [3, 68], [4, 57], [4, 62], [4, 65], [4, 69], [5, 58], [5, 61], [5, 70], [5, 75], [6, 59], [6, 66], [6, 71], [6, 76], [7, 60], [7, 67], [7, 72], [7, 77], [8, 62], [8, 66], [8, 78], [8, 84], [9, 63], [9, 73], [9, 79], [9, 85], [10, 64], [10, 74], [10, 80], [10, 86], [11, 65], [11, 74], [11, 81], [11, 86], [12, 67], [12, 73], [12, 74], [12, 82], [13, 68], [13, 82], [13, 87], [13, 93], [14, 69], [14, 83], [14, 88], [14, 94], [15, 70], [15, 78], [15, 89], [15, 95], [16, 67], [16, 71], [16, 77], [16, 90], [17, 72], [17, 78], [17, 81], [17, 95], [18, 67], [18, 74], [18, 83], [18, 91], [19, 75], [19, 84], [19, 96], [19, 102], [20, 76], [20, 91], [20, 97], [20, 103], [21, 77], [21, 92], [21, 94], [21, 98], [22, 62], [22, 69], [22, 79], [22, 99], [23, 80], [23, 84], [23, 90], [23, 102], [24, 70], [24, 72], [24, 81], [24, 89], [25, 62], [25, 78], [25, 92], [25, 100], [26, 85], [26, 100], [26, 101], [26, 103], [27, 86], [27, 100], [27, 103], [27, 104], [28, 85], [28, 86], [28, 101], [28, 104], [29, 66], [29, 76], [29, 87], [29, 105], [30, 58], [30, 63], [30, 88], [30, 106], [31, 82], [31, 89], [31, 93], [31, 99], [32, 75], [32, 80], [32, 90], [32, 96], [33, 64], [33, 65], [33, 80], [33, 81], [34, 66], [34, 84], [34, 92], [34, 100], [35, 58], [35, 70], [35, 101], [35, 107], [36, 92], [36, 93], [36, 94], [36, 107], [37, 91], [37, 95], [37, 103], [37, 106], [38, 77], [38, 93], [38, 98], [38, 107], [39, 76], [39, 95], [39, 97], [39, 106], [40, 73], [40, 85], [40, 96], [40, 105], [41, 61], [41, 68], [41, 97], [41, 108], [42, 56], [42, 59], [42, 98], [42, 104], [43, 68], [43, 87], [43, 89], [43, 99], [44, 60], [44, 71], [44, 72], [44, 90], [45, 73], [45, 82], [45, 83], [45, 91], [46, 61], [46, 75], [46, 101], [46, 107], [47, 56], [47, 64], [47, 97], [47, 108], [48, 83], [48, 94], [48, 102], [48, 108], [49, 69], [49, 88], [49, 102], [49, 108], [50, 55], [50, 57], [50, 98], [50, 104], [51, 63], [51, 79], [51, 96], [51, 105], [52, 57], [52, 65], [52, 79], [52, 99], [53, 55], [53, 60], [53, 88], [53, 106], [54, 59], [54, 71], [54, 87], [54, 105]]);;
R:=P177Census(D);;Need(Size(R.F)=216);;
PrintTo("current_c4_descent/108_022.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 108_022 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
