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
D:=P177Graph("096_020",96,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48],[[1, 54], [1, 60], [1, 63], [1, 75], [2, 54], [2, 60], [2, 83], [2, 87], [3, 51], [3, 57], [3, 72], [3, 78], [4, 51], [4, 57], [4, 90], [4, 94], [5, 63], [5, 75], [5, 88], [5, 94], [6, 53], [6, 59], [6, 73], [6, 80], [7, 53], [7, 59], [7, 88], [7, 95], [8, 62], [8, 64], [8, 69], [8, 77], [9, 52], [9, 58], [9, 74], [9, 79], [10, 62], [10, 64], [10, 86], [10, 91], [11, 74], [11, 79], [11, 87], [11, 93], [12, 73], [12, 78], [12, 83], [12, 87], [13, 72], [13, 78], [13, 85], [13, 91], [14, 56], [14, 67], [14, 70], [14, 76], [15, 49], [15, 50], [15, 82], [15, 84], [16, 56], [16, 67], [16, 85], [16, 92], [17, 81], [17, 82], [17, 83], [17, 84], [18, 49], [18, 50], [18, 89], [18, 96], [19, 52], [19, 58], [19, 65], [19, 68], [20, 65], [20, 69], [20, 77], [20, 96], [21, 71], [21, 75], [21, 89], [21, 96], [22, 70], [22, 77], [22, 90], [22, 94], [23, 49], [23, 58], [23, 88], [23, 94], [24, 73], [24, 80], [24, 86], [24, 92], [25, 69], [25, 76], [25, 88], [25, 95], [26, 55], [26, 61], [26, 66], [26, 71], [27, 68], [27, 70], [27, 76], [27, 89], [28, 63], [28, 65], [28, 66], [28, 68], [29, 66], [29, 71], [29, 90], [29, 95], [30, 55], [30, 61], [30, 81], [30, 93], [31, 74], [31, 84], [31, 86], [31, 91], [32, 72], [32, 80], [32, 81], [32, 93], [33, 54], [33, 61], [33, 85], [33, 91], [34, 56], [34, 62], [34, 87], [34, 93], [35, 50], [35, 52], [35, 73], [35, 78], [36, 79], [36, 82], [36, 85], [36, 92], [37, 64], [37, 67], [37, 81], [37, 83], [38, 55], [38, 60], [38, 86], [38, 92], [39, 51], [39, 59], [39, 65], [39, 96], [40, 50], [40, 52], [40, 90], [40, 95], [41, 54], [41, 61], [41, 69], [41, 76], [42, 56], [42, 62], [42, 71], [42, 75], [43, 55], [43, 60], [43, 70], [43, 77], [44, 49], [44, 58], [44, 72], [44, 80], [45, 53], [45, 57], [45, 68], [45, 89], [46, 63], [46, 64], [46, 66], [46, 67], [47, 53], [47, 57], [47, 74], [47, 84], [48, 51], [48, 59], [48, 79], [48, 82]]);;
R:=P177Census(D);;Need(Size(R.F)=768);;
PrintTo("current_c4_descent/096_020.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 096_020 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
