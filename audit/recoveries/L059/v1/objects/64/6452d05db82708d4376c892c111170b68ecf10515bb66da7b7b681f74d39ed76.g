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
D:=P177Graph("096_017",96,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48],[[1, 49], [1, 50], [1, 79], [1, 80], [2, 49], [2, 50], [2, 67], [2, 68], [3, 67], [3, 68], [3, 85], [3, 86], [4, 55], [4, 56], [4, 85], [4, 86], [5, 55], [5, 56], [5, 73], [5, 74], [6, 73], [6, 74], [6, 91], [6, 92], [7, 61], [7, 62], [7, 91], [7, 92], [8, 61], [8, 62], [8, 79], [8, 80], [9, 50], [9, 51], [9, 92], [9, 93], [10, 50], [10, 51], [10, 56], [10, 57], [11, 56], [11, 57], [11, 62], [11, 63], [12, 62], [12, 63], [12, 68], [12, 69], [13, 68], [13, 69], [13, 74], [13, 75], [14, 74], [14, 75], [14, 80], [14, 81], [15, 80], [15, 81], [15, 86], [15, 87], [16, 86], [16, 87], [16, 92], [16, 93], [17, 51], [17, 52], [17, 81], [17, 82], [18, 51], [18, 52], [18, 69], [18, 70], [19, 69], [19, 70], [19, 87], [19, 88], [20, 57], [20, 58], [20, 87], [20, 88], [21, 57], [21, 58], [21, 75], [21, 76], [22, 75], [22, 76], [22, 93], [22, 94], [23, 63], [23, 64], [23, 93], [23, 94], [24, 63], [24, 64], [24, 81], [24, 82], [25, 52], [25, 53], [25, 94], [25, 95], [26, 52], [26, 53], [26, 58], [26, 59], [27, 58], [27, 59], [27, 64], [27, 65], [28, 64], [28, 65], [28, 70], [28, 71], [29, 70], [29, 71], [29, 76], [29, 77], [30, 76], [30, 77], [30, 82], [30, 83], [31, 82], [31, 83], [31, 88], [31, 89], [32, 88], [32, 89], [32, 94], [32, 95], [33, 53], [33, 54], [33, 83], [33, 84], [34, 53], [34, 54], [34, 71], [34, 72], [35, 71], [35, 72], [35, 89], [35, 90], [36, 59], [36, 60], [36, 89], [36, 90], [37, 59], [37, 60], [37, 77], [37, 78], [38, 77], [38, 78], [38, 95], [38, 96], [39, 65], [39, 66], [39, 95], [39, 96], [40, 65], [40, 66], [40, 83], [40, 84], [41, 49], [41, 54], [41, 91], [41, 96], [42, 49], [42, 54], [42, 55], [42, 60], [43, 55], [43, 60], [43, 61], [43, 66], [44, 61], [44, 66], [44, 67], [44, 72], [45, 67], [45, 72], [45, 73], [45, 78], [46, 73], [46, 78], [46, 79], [46, 84], [47, 79], [47, 84], [47, 85], [47, 90], [48, 85], [48, 90], [48, 91], [48, 96]]);;
R:=P177Census(D);;Need(Size(R.F)=192);;
PrintTo("current_c4_descent/096_017.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 096_017 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
