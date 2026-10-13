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
D:=P177Graph("096_015",96,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48],[[1, 49], [1, 50], [1, 77], [1, 78], [2, 49], [2, 50], [2, 69], [2, 70], [3, 69], [3, 70], [3, 89], [3, 90], [4, 61], [4, 62], [4, 89], [4, 90], [5, 61], [5, 62], [5, 81], [5, 82], [6, 53], [6, 54], [6, 81], [6, 82], [7, 53], [7, 54], [7, 73], [7, 74], [8, 73], [8, 74], [8, 93], [8, 94], [9, 65], [9, 66], [9, 93], [9, 94], [10, 65], [10, 66], [10, 85], [10, 86], [11, 57], [11, 58], [11, 85], [11, 86], [12, 57], [12, 58], [12, 77], [12, 78], [13, 50], [13, 51], [13, 94], [13, 95], [14, 50], [14, 51], [14, 54], [14, 55], [15, 54], [15, 55], [15, 58], [15, 59], [16, 58], [16, 59], [16, 62], [16, 63], [17, 62], [17, 63], [17, 66], [17, 67], [18, 66], [18, 67], [18, 70], [18, 71], [19, 70], [19, 71], [19, 74], [19, 75], [20, 74], [20, 75], [20, 78], [20, 79], [21, 78], [21, 79], [21, 82], [21, 83], [22, 82], [22, 83], [22, 86], [22, 87], [23, 86], [23, 87], [23, 90], [23, 91], [24, 90], [24, 91], [24, 94], [24, 95], [25, 51], [25, 52], [25, 79], [25, 80], [26, 51], [26, 52], [26, 71], [26, 72], [27, 71], [27, 72], [27, 91], [27, 92], [28, 63], [28, 64], [28, 91], [28, 92], [29, 63], [29, 64], [29, 83], [29, 84], [30, 55], [30, 56], [30, 83], [30, 84], [31, 55], [31, 56], [31, 75], [31, 76], [32, 75], [32, 76], [32, 95], [32, 96], [33, 67], [33, 68], [33, 95], [33, 96], [34, 67], [34, 68], [34, 87], [34, 88], [35, 59], [35, 60], [35, 87], [35, 88], [36, 59], [36, 60], [36, 79], [36, 80], [37, 49], [37, 52], [37, 93], [37, 96], [38, 49], [38, 52], [38, 53], [38, 56], [39, 53], [39, 56], [39, 57], [39, 60], [40, 57], [40, 60], [40, 61], [40, 64], [41, 61], [41, 64], [41, 65], [41, 68], [42, 65], [42, 68], [42, 69], [42, 72], [43, 69], [43, 72], [43, 73], [43, 76], [44, 73], [44, 76], [44, 77], [44, 80], [45, 77], [45, 80], [45, 81], [45, 84], [46, 81], [46, 84], [46, 85], [46, 88], [47, 85], [47, 88], [47, 89], [47, 92], [48, 89], [48, 92], [48, 93], [48, 96]]);;
R:=P177Census(D);;Need(Size(R.F)=192);;
PrintTo("current_c4_descent/096_015.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 096_015 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
