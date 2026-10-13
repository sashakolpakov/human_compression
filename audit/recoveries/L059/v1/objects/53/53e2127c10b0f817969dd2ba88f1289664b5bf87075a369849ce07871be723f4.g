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
D:=P177Graph("096_016",96,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48],[[1, 49], [1, 50], [1, 61], [1, 62], [2, 49], [2, 50], [2, 89], [2, 90], [3, 85], [3, 86], [3, 89], [3, 90], [4, 73], [4, 74], [4, 85], [4, 86], [5, 69], [5, 70], [5, 73], [5, 74], [6, 57], [6, 58], [6, 69], [6, 70], [7, 53], [7, 54], [7, 57], [7, 58], [8, 53], [8, 54], [8, 93], [8, 94], [9, 81], [9, 82], [9, 93], [9, 94], [10, 77], [10, 78], [10, 81], [10, 82], [11, 65], [11, 66], [11, 77], [11, 78], [12, 61], [12, 62], [12, 65], [12, 66], [13, 50], [13, 51], [13, 94], [13, 95], [14, 50], [14, 51], [14, 58], [14, 59], [15, 58], [15, 59], [15, 66], [15, 67], [16, 66], [16, 67], [16, 74], [16, 75], [17, 74], [17, 75], [17, 82], [17, 83], [18, 82], [18, 83], [18, 90], [18, 91], [19, 54], [19, 55], [19, 90], [19, 91], [20, 54], [20, 55], [20, 62], [20, 63], [21, 62], [21, 63], [21, 70], [21, 71], [22, 70], [22, 71], [22, 78], [22, 79], [23, 78], [23, 79], [23, 86], [23, 87], [24, 86], [24, 87], [24, 94], [24, 95], [25, 51], [25, 52], [25, 63], [25, 64], [26, 51], [26, 52], [26, 91], [26, 92], [27, 87], [27, 88], [27, 91], [27, 92], [28, 75], [28, 76], [28, 87], [28, 88], [29, 71], [29, 72], [29, 75], [29, 76], [30, 59], [30, 60], [30, 71], [30, 72], [31, 55], [31, 56], [31, 59], [31, 60], [32, 55], [32, 56], [32, 95], [32, 96], [33, 83], [33, 84], [33, 95], [33, 96], [34, 79], [34, 80], [34, 83], [34, 84], [35, 67], [35, 68], [35, 79], [35, 80], [36, 63], [36, 64], [36, 67], [36, 68], [37, 49], [37, 56], [37, 92], [37, 93], [38, 49], [38, 56], [38, 57], [38, 64], [39, 57], [39, 64], [39, 65], [39, 72], [40, 65], [40, 72], [40, 73], [40, 80], [41, 73], [41, 80], [41, 81], [41, 88], [42, 81], [42, 88], [42, 89], [42, 96], [43, 52], [43, 53], [43, 89], [43, 96], [44, 52], [44, 53], [44, 60], [44, 61], [45, 60], [45, 61], [45, 68], [45, 69], [46, 68], [46, 69], [46, 76], [46, 77], [47, 76], [47, 77], [47, 84], [47, 85], [48, 84], [48, 85], [48, 92], [48, 93]]);;
R:=P177Census(D);;Need(Size(R.F)=192);;
PrintTo("current_c4_descent/096_016.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 096_016 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
