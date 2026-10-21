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
D:=P177Graph("096_031",96,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48],[[1, 49], [1, 55], [1, 63], [1, 80], [2, 55], [2, 61], [2, 63], [2, 90], [3, 54], [3, 55], [3, 66], [3, 74], [4, 54], [4, 59], [4, 66], [4, 91], [5, 49], [5, 59], [5, 64], [5, 80], [6, 55], [6, 70], [6, 73], [6, 74], [7, 52], [7, 63], [7, 84], [7, 89], [8, 54], [8, 57], [8, 65], [8, 78], [9, 49], [9, 62], [9, 77], [9, 89], [10, 59], [10, 70], [10, 73], [10, 91], [11, 52], [11, 64], [11, 89], [11, 95], [12, 57], [12, 65], [12, 70], [12, 92], [13, 61], [13, 62], [13, 68], [13, 89], [14, 59], [14, 61], [14, 64], [14, 90], [15, 63], [15, 75], [15, 82], [15, 84], [16, 54], [16, 72], [16, 76], [16, 78], [17, 49], [17, 58], [17, 75], [17, 77], [18, 56], [18, 66], [18, 86], [18, 90], [19, 66], [19, 80], [19, 86], [19, 96], [20, 52], [20, 81], [20, 85], [20, 93], [21, 57], [21, 60], [21, 69], [21, 87], [22, 60], [22, 62], [22, 67], [22, 88], [23, 50], [23, 73], [23, 80], [23, 96], [24, 64], [24, 75], [24, 82], [24, 95], [25, 70], [25, 72], [25, 76], [25, 92], [26, 58], [26, 61], [26, 68], [26, 75], [27, 50], [27, 56], [27, 73], [27, 90], [28, 67], [28, 82], [28, 85], [28, 93], [29, 60], [29, 69], [29, 72], [29, 93], [30, 58], [30, 60], [30, 81], [30, 88], [31, 51], [31, 52], [31, 81], [31, 87], [32, 57], [32, 71], [32, 79], [32, 87], [33, 62], [33, 67], [33, 71], [33, 94], [34, 65], [34, 84], [34, 85], [34, 91], [35, 65], [35, 74], [35, 85], [35, 95], [36, 56], [36, 77], [36, 83], [36, 94], [37, 53], [37, 79], [37, 86], [37, 92], [38, 50], [38, 69], [38, 78], [38, 83], [39, 51], [39, 74], [39, 76], [39, 95], [40, 51], [40, 67], [40, 82], [40, 87], [41, 71], [41, 72], [41, 79], [41, 93], [42, 58], [42, 71], [42, 81], [42, 94], [43, 51], [43, 76], [43, 84], [43, 91], [44, 68], [44, 83], [44, 94], [44, 96], [45, 50], [45, 53], [45, 78], [45, 79], [46, 69], [46, 83], [46, 86], [46, 92], [47, 53], [47, 56], [47, 77], [47, 88], [48, 53], [48, 68], [48, 88], [48, 96]]);;
R:=P177Census(D);;Need(Size(R.F)=3072);;
PrintTo("current_c4_descent/096_031.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 096_031 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
