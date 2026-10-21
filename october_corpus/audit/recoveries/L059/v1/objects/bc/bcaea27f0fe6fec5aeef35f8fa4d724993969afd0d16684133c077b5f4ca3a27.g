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
D:=P177Graph("104_009",104,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52],[[1, 59], [1, 69], [1, 73], [1, 99], [2, 59], [2, 73], [2, 96], [2, 102], [3, 54], [3, 61], [3, 63], [3, 100], [4, 54], [4, 61], [4, 97], [4, 101], [5, 53], [5, 54], [5, 69], [5, 99], [6, 53], [6, 83], [6, 92], [6, 93], [7, 60], [7, 62], [7, 67], [7, 104], [8, 55], [8, 65], [8, 75], [8, 96], [9, 53], [9, 64], [9, 74], [9, 83], [10, 60], [10, 62], [10, 89], [10, 103], [11, 65], [11, 71], [11, 77], [11, 96], [12, 53], [12, 54], [12, 96], [12, 102], [13, 59], [13, 62], [13, 63], [13, 100], [14, 82], [14, 85], [14, 98], [14, 102], [15, 80], [15, 81], [15, 90], [15, 94], [16, 56], [16, 57], [16, 66], [16, 68], [17, 86], [17, 87], [17, 89], [17, 91], [18, 55], [18, 69], [18, 75], [18, 91], [19, 72], [19, 76], [19, 77], [19, 97], [20, 78], [20, 84], [20, 98], [20, 102], [21, 68], [21, 76], [21, 80], [21, 81], [22, 56], [22, 57], [22, 90], [22, 98], [23, 80], [23, 88], [23, 89], [23, 91], [24, 69], [24, 71], [24, 77], [24, 91], [25, 75], [25, 76], [25, 79], [25, 97], [26, 59], [26, 62], [26, 97], [26, 101], [27, 73], [27, 81], [27, 92], [27, 93], [28, 56], [28, 61], [28, 67], [28, 104], [29, 66], [29, 82], [29, 85], [29, 99], [30, 78], [30, 88], [30, 95], [30, 101], [31, 58], [31, 70], [31, 71], [31, 74], [32, 65], [32, 67], [32, 86], [32, 87], [33, 63], [33, 72], [33, 77], [33, 94], [34, 64], [34, 79], [34, 84], [34, 103], [35, 66], [35, 78], [35, 84], [35, 99], [36, 85], [36, 87], [36, 95], [36, 101], [37, 58], [37, 60], [37, 66], [37, 68], [38, 58], [38, 71], [38, 93], [38, 95], [39, 65], [39, 67], [39, 80], [39, 88], [40, 83], [40, 86], [40, 90], [40, 94], [41, 63], [41, 75], [41, 79], [41, 94], [42, 64], [42, 73], [42, 74], [42, 81], [43, 64], [43, 72], [43, 82], [43, 103], [44, 56], [44, 61], [44, 89], [44, 103], [45, 70], [45, 78], [45, 88], [45, 100], [46, 79], [46, 84], [46, 92], [46, 104], [47, 55], [47, 57], [47, 70], [47, 74], [48, 70], [48, 85], [48, 87], [48, 100], [49, 58], [49, 60], [49, 90], [49, 98], [50, 68], [50, 76], [50, 83], [50, 86], [51, 72], [51, 82], [51, 92], [51, 104], [52, 55], [52, 57], [52, 93], [52, 95]]);;
R:=P177Census(D);;Need(Size(R.F)=208);;
PrintTo("current_c4_descent/104_009.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 104_009 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
