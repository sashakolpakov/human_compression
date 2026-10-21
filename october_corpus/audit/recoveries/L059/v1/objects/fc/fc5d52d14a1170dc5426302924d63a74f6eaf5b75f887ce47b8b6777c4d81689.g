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
D:=P177Graph("096_046",96,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48],[[1, 49], [1, 50], [1, 79], [1, 80], [2, 49], [2, 50], [2, 73], [2, 74], [3, 55], [3, 56], [3, 73], [3, 74], [4, 55], [4, 56], [4, 79], [4, 80], [5, 50], [5, 51], [5, 91], [5, 92], [6, 50], [6, 51], [6, 85], [6, 86], [7, 56], [7, 57], [7, 85], [7, 86], [8, 56], [8, 57], [8, 91], [8, 92], [9, 51], [9, 52], [9, 67], [9, 68], [10, 51], [10, 52], [10, 61], [10, 62], [11, 57], [11, 58], [11, 61], [11, 62], [12, 57], [12, 58], [12, 67], [12, 68], [13, 52], [13, 53], [13, 82], [13, 83], [14, 52], [14, 53], [14, 76], [14, 77], [15, 58], [15, 59], [15, 76], [15, 77], [16, 58], [16, 59], [16, 82], [16, 83], [17, 53], [17, 54], [17, 88], [17, 89], [18, 53], [18, 54], [18, 94], [18, 95], [19, 59], [19, 60], [19, 94], [19, 95], [20, 59], [20, 60], [20, 88], [20, 89], [21, 54], [21, 55], [21, 64], [21, 65], [22, 54], [22, 55], [22, 70], [22, 71], [23, 49], [23, 60], [23, 70], [23, 71], [24, 49], [24, 60], [24, 64], [24, 65], [25, 63], [25, 64], [25, 92], [25, 93], [26, 63], [26, 64], [26, 86], [26, 87], [27, 69], [27, 70], [27, 86], [27, 87], [28, 69], [28, 70], [28, 92], [28, 93], [29, 62], [29, 63], [29, 80], [29, 81], [30, 62], [30, 63], [30, 74], [30, 75], [31, 68], [31, 69], [31, 74], [31, 75], [32, 68], [32, 69], [32, 80], [32, 81], [33, 75], [33, 76], [33, 90], [33, 91], [34, 75], [34, 76], [34, 85], [34, 96], [35, 81], [35, 82], [35, 85], [35, 96], [36, 81], [36, 82], [36, 90], [36, 91], [37, 61], [37, 72], [37, 89], [37, 90], [38, 61], [38, 72], [38, 95], [38, 96], [39, 66], [39, 67], [39, 95], [39, 96], [40, 66], [40, 67], [40, 89], [40, 90], [41, 71], [41, 72], [41, 83], [41, 84], [42, 71], [42, 72], [42, 77], [42, 78], [43, 65], [43, 66], [43, 77], [43, 78], [44, 65], [44, 66], [44, 83], [44, 84], [45, 78], [45, 79], [45, 87], [45, 88], [46, 78], [46, 79], [46, 93], [46, 94], [47, 73], [47, 84], [47, 93], [47, 94], [48, 73], [48, 84], [48, 87], [48, 88]]);;
R:=P177Census(D);;Need(Size(R.F)=768);;
PrintTo("current_c4_descent/096_046.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 096_046 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
