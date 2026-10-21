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
D:=P177Graph("108_023",108,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54],[[1, 55], [1, 56], [1, 57], [1, 59], [2, 55], [2, 58], [2, 60], [2, 63], [3, 56], [3, 61], [3, 64], [3, 68], [4, 57], [4, 60], [4, 62], [4, 69], [5, 58], [5, 65], [5, 70], [5, 76], [6, 59], [6, 64], [6, 66], [6, 77], [7, 57], [7, 60], [7, 67], [7, 78], [8, 61], [8, 71], [8, 79], [8, 87], [9, 62], [9, 72], [9, 80], [9, 88], [10, 63], [10, 70], [10, 73], [10, 89], [11, 59], [11, 64], [11, 74], [11, 84], [12, 55], [12, 60], [12, 75], [12, 90], [13, 65], [13, 71], [13, 91], [13, 101], [14, 66], [14, 81], [14, 92], [14, 102], [15, 67], [15, 82], [15, 93], [15, 103], [16, 68], [16, 79], [16, 83], [16, 96], [17, 69], [17, 73], [17, 80], [17, 104], [18, 63], [18, 70], [18, 74], [18, 84], [19, 56], [19, 64], [19, 85], [19, 97], [20, 55], [20, 57], [20, 86], [20, 100], [21, 72], [21, 81], [21, 94], [21, 105], [22, 73], [22, 94], [22, 102], [22, 104], [23, 74], [23, 95], [23, 100], [23, 106], [24, 75], [24, 82], [24, 99], [24, 107], [25, 76], [25, 83], [25, 91], [25, 96], [26, 77], [26, 83], [26, 92], [26, 108], [27, 66], [27, 78], [27, 92], [27, 93], [28, 67], [28, 68], [28, 78], [28, 79], [29, 69], [29, 80], [29, 85], [29, 97], [30, 58], [30, 70], [30, 97], [30, 98], [31, 56], [31, 59], [31, 99], [31, 103], [32, 81], [32, 82], [32, 94], [32, 99], [33, 83], [33, 88], [33, 105], [33, 108], [34, 73], [34, 87], [34, 89], [34, 101], [35, 84], [35, 90], [35, 106], [35, 107], [36, 85], [36, 86], [36, 95], [36, 98], [37, 72], [37, 86], [37, 95], [37, 105], [38, 89], [38, 96], [38, 104], [38, 108], [39, 62], [39, 80], [39, 84], [39, 106], [40, 61], [40, 79], [40, 90], [40, 107], [41, 62], [41, 69], [41, 76], [41, 91], [42, 75], [42, 77], [42, 90], [42, 92], [43, 78], [43, 93], [43, 97], [43, 98], [44, 58], [44, 63], [44, 88], [44, 105], [45, 71], [45, 82], [45, 101], [45, 103], [46, 96], [46, 99], [46, 103], [46, 108], [47, 66], [47, 77], [47, 87], [47, 101], [48, 75], [48, 85], [48, 98], [48, 107], [49, 65], [49, 91], [49, 95], [49, 100], [50, 67], [50, 74], [50, 93], [50, 106], [51, 86], [51, 89], [51, 100], [51, 104], [52, 61], [52, 68], [52, 94], [52, 102], [53, 71], [53, 72], [53, 87], [53, 88], [54, 65], [54, 76], [54, 81], [54, 102]]);;
R:=P177Census(D);;Need(Size(R.F)=216);;
PrintTo("current_c4_descent/108_023.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 108_023 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
