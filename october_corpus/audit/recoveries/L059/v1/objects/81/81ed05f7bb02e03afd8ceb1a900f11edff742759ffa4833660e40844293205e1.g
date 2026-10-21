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
D:=P177Graph("096_048",96,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48],[[1, 49], [1, 50], [1, 67], [1, 68], [2, 49], [2, 50], [2, 61], [2, 62], [3, 55], [3, 56], [3, 61], [3, 62], [4, 55], [4, 56], [4, 67], [4, 68], [5, 73], [5, 74], [5, 91], [5, 92], [6, 73], [6, 74], [6, 85], [6, 86], [7, 79], [7, 80], [7, 85], [7, 86], [8, 79], [8, 80], [8, 91], [8, 92], [9, 76], [9, 77], [9, 94], [9, 95], [10, 76], [10, 77], [10, 88], [10, 89], [11, 82], [11, 83], [11, 88], [11, 89], [12, 82], [12, 83], [12, 94], [12, 95], [13, 52], [13, 53], [13, 70], [13, 71], [14, 52], [14, 53], [14, 64], [14, 65], [15, 58], [15, 59], [15, 64], [15, 65], [16, 58], [16, 59], [16, 70], [16, 71], [17, 50], [17, 51], [17, 95], [17, 96], [18, 50], [18, 51], [18, 89], [18, 90], [19, 56], [19, 57], [19, 89], [19, 90], [20, 56], [20, 57], [20, 95], [20, 96], [21, 62], [21, 63], [21, 83], [21, 84], [22, 62], [22, 63], [22, 77], [22, 78], [23, 68], [23, 69], [23, 77], [23, 78], [24, 68], [24, 69], [24, 83], [24, 84], [25, 65], [25, 66], [25, 80], [25, 81], [26, 65], [26, 66], [26, 74], [26, 75], [27, 71], [27, 72], [27, 74], [27, 75], [28, 71], [28, 72], [28, 80], [28, 81], [29, 53], [29, 54], [29, 92], [29, 93], [30, 53], [30, 54], [30, 86], [30, 87], [31, 59], [31, 60], [31, 86], [31, 87], [32, 59], [32, 60], [32, 92], [32, 93], [33, 66], [33, 67], [33, 85], [33, 96], [34, 66], [34, 67], [34, 90], [34, 91], [35, 61], [35, 72], [35, 90], [35, 91], [36, 61], [36, 72], [36, 85], [36, 96], [37, 51], [37, 52], [37, 81], [37, 82], [38, 51], [38, 52], [38, 75], [38, 76], [39, 57], [39, 58], [39, 75], [39, 76], [40, 57], [40, 58], [40, 81], [40, 82], [41, 54], [41, 55], [41, 73], [41, 84], [42, 54], [42, 55], [42, 78], [42, 79], [43, 49], [43, 60], [43, 78], [43, 79], [44, 49], [44, 60], [44, 73], [44, 84], [45, 63], [45, 64], [45, 93], [45, 94], [46, 63], [46, 64], [46, 87], [46, 88], [47, 69], [47, 70], [47, 87], [47, 88], [48, 69], [48, 70], [48, 93], [48, 94]]);;
R:=P177Census(D);;Need(Size(R.F)=768);;
PrintTo("current_c4_descent/096_048.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 096_048 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
