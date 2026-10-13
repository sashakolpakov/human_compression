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
D:=P177Graph("096_019",96,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48],[[1, 54], [1, 60], [1, 63], [1, 75], [2, 54], [2, 60], [2, 81], [2, 93], [3, 51], [3, 57], [3, 72], [3, 78], [4, 51], [4, 57], [4, 88], [4, 95], [5, 63], [5, 75], [5, 88], [5, 94], [6, 52], [6, 59], [6, 74], [6, 80], [7, 62], [7, 64], [7, 69], [7, 76], [8, 53], [8, 58], [8, 73], [8, 79], [9, 52], [9, 59], [9, 90], [9, 94], [10, 62], [10, 64], [10, 85], [10, 92], [11, 73], [11, 79], [11, 87], [11, 93], [12, 72], [12, 80], [12, 81], [12, 93], [13, 72], [13, 78], [13, 85], [13, 91], [14, 55], [14, 67], [14, 71], [14, 77], [15, 49], [15, 50], [15, 82], [15, 84], [16, 53], [16, 58], [16, 89], [16, 96], [17, 55], [17, 67], [17, 86], [17, 91], [18, 81], [18, 82], [18, 83], [18, 84], [19, 65], [19, 69], [19, 76], [19, 96], [20, 70], [20, 75], [20, 89], [20, 96], [21, 69], [21, 77], [21, 88], [21, 95], [22, 49], [22, 58], [22, 88], [22, 94], [23, 74], [23, 80], [23, 86], [23, 92], [24, 49], [24, 50], [24, 65], [24, 68], [25, 56], [25, 61], [25, 66], [25, 70], [26, 68], [26, 71], [26, 77], [26, 89], [27, 63], [27, 65], [27, 66], [27, 68], [28, 66], [28, 70], [28, 90], [28, 95], [29, 79], [29, 82], [29, 85], [29, 92], [30, 54], [30, 61], [30, 85], [30, 91], [31, 71], [31, 76], [31, 90], [31, 94], [32, 55], [32, 62], [32, 87], [32, 93], [33, 49], [33, 58], [33, 72], [33, 80], [34, 56], [34, 61], [34, 83], [34, 87], [35, 73], [35, 84], [35, 86], [35, 91], [36, 74], [36, 78], [36, 83], [36, 87], [37, 56], [37, 60], [37, 86], [37, 92], [38, 51], [38, 59], [38, 65], [38, 96], [39, 54], [39, 61], [39, 69], [39, 77], [40, 64], [40, 67], [40, 81], [40, 83], [41, 55], [41, 62], [41, 70], [41, 75], [42, 52], [42, 57], [42, 68], [42, 89], [43, 50], [43, 53], [43, 90], [43, 95], [44, 56], [44, 60], [44, 71], [44, 76], [45, 51], [45, 59], [45, 79], [45, 82], [46, 63], [46, 64], [46, 66], [46, 67], [47, 52], [47, 57], [47, 73], [47, 84], [48, 50], [48, 53], [48, 74], [48, 78]]);;
R:=P177Census(D);;Need(Size(R.F)=768);;
PrintTo("current_c4_descent/096_019.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 096_019 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
