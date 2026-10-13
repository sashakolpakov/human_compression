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
D:=P177Graph("100_010",100,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50],[[1, 51], [1, 52], [1, 53], [1, 54], [2, 51], [2, 55], [2, 56], [2, 57], [3, 52], [3, 55], [3, 58], [3, 59], [4, 53], [4, 56], [4, 58], [4, 60], [5, 54], [5, 57], [5, 59], [5, 60], [6, 61], [6, 62], [6, 63], [6, 64], [7, 61], [7, 65], [7, 66], [7, 67], [8, 62], [8, 65], [8, 68], [8, 69], [9, 63], [9, 66], [9, 68], [9, 70], [10, 64], [10, 67], [10, 69], [10, 70], [11, 71], [11, 72], [11, 73], [11, 74], [12, 71], [12, 75], [12, 76], [12, 77], [13, 72], [13, 75], [13, 78], [13, 79], [14, 73], [14, 76], [14, 78], [14, 80], [15, 74], [15, 77], [15, 79], [15, 80], [16, 81], [16, 82], [16, 83], [16, 84], [17, 81], [17, 85], [17, 86], [17, 87], [18, 82], [18, 85], [18, 88], [18, 89], [19, 83], [19, 86], [19, 88], [19, 90], [20, 84], [20, 87], [20, 89], [20, 90], [21, 91], [21, 92], [21, 93], [21, 94], [22, 91], [22, 95], [22, 96], [22, 97], [23, 92], [23, 95], [23, 98], [23, 99], [24, 93], [24, 96], [24, 98], [24, 100], [25, 94], [25, 97], [25, 99], [25, 100], [26, 61], [26, 72], [26, 83], [26, 94], [27, 57], [27, 61], [27, 85], [27, 96], [28, 58], [28, 69], [28, 72], [28, 85], [29, 58], [29, 80], [29, 83], [29, 96], [30, 57], [30, 69], [30, 80], [30, 94], [31, 51], [31, 62], [31, 73], [31, 84], [32, 51], [32, 75], [32, 86], [32, 97], [33, 59], [33, 62], [33, 75], [33, 98], [34, 70], [34, 73], [34, 86], [34, 98], [35, 59], [35, 70], [35, 84], [35, 97], [36, 52], [36, 63], [36, 74], [36, 91], [37, 65], [37, 76], [37, 87], [37, 91], [38, 52], [38, 65], [38, 88], [38, 99], [39, 60], [39, 63], [39, 76], [39, 88], [40, 60], [40, 74], [40, 87], [40, 99], [41, 53], [41, 64], [41, 81], [41, 92], [42, 55], [42, 66], [42, 77], [42, 81], [43, 55], [43, 78], [43, 89], [43, 92], [44, 53], [44, 66], [44, 78], [44, 100], [45, 64], [45, 77], [45, 89], [45, 100], [46, 54], [46, 71], [46, 82], [46, 93], [47, 56], [47, 67], [47, 71], [47, 95], [48, 68], [48, 79], [48, 82], [48, 95], [49, 56], [49, 68], [49, 90], [49, 93], [50, 54], [50, 67], [50, 79], [50, 90]]);;
R:=P177Census(D);;Need(Size(R.F)=400);;
PrintTo("current_c4_descent/100_010.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 100_010 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
