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
D:=P177Graph("084_009",84,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],[[1, 50], [1, 58], [1, 66], [1, 71], [2, 50], [2, 51], [2, 58], [2, 68], [3, 43], [3, 55], [3, 63], [3, 69], [4, 47], [4, 64], [4, 66], [4, 71], [5, 51], [5, 55], [5, 63], [5, 72], [6, 54], [6, 56], [6, 61], [6, 73], [7, 49], [7, 52], [7, 63], [7, 84], [8, 53], [8, 60], [8, 65], [8, 67], [9, 51], [9, 65], [9, 67], [9, 68], [10, 43], [10, 47], [10, 57], [10, 69], [11, 51], [11, 61], [11, 72], [11, 73], [12, 49], [12, 63], [12, 66], [12, 80], [13, 47], [13, 54], [13, 56], [13, 57], [14, 45], [14, 54], [14, 59], [14, 81], [15, 44], [15, 73], [15, 76], [15, 79], [16, 45], [16, 56], [16, 77], [16, 82], [17, 44], [17, 67], [17, 76], [17, 83], [18, 47], [18, 53], [18, 60], [18, 64], [19, 52], [19, 65], [19, 83], [19, 84], [20, 59], [20, 66], [20, 80], [20, 81], [21, 71], [21, 73], [21, 79], [21, 80], [22, 45], [22, 56], [22, 58], [22, 62], [23, 67], [23, 69], [23, 70], [23, 83], [24, 45], [24, 54], [24, 65], [24, 83], [25, 48], [25, 69], [25, 70], [25, 82], [26, 49], [26, 55], [26, 76], [26, 78], [27, 48], [27, 71], [27, 80], [27, 82], [28, 44], [28, 74], [28, 78], [28, 81], [29, 43], [29, 59], [29, 70], [29, 74], [30, 50], [30, 52], [30, 62], [30, 75], [31, 44], [31, 57], [31, 64], [31, 78], [32, 46], [32, 59], [32, 60], [32, 74], [33, 52], [33, 61], [33, 75], [33, 79], [34, 46], [34, 53], [34, 77], [34, 82], [35, 58], [35, 62], [35, 76], [35, 78], [36, 68], [36, 72], [36, 74], [36, 81], [37, 43], [37, 50], [37, 62], [37, 70], [38, 57], [38, 64], [38, 75], [38, 84], [39, 46], [39, 60], [39, 61], [39, 79], [40, 46], [40, 49], [40, 53], [40, 55], [41, 48], [41, 75], [41, 77], [41, 84], [42, 48], [42, 68], [42, 72], [42, 77]]);;
R:=P177Census(D);;Need(Size(R.F)=336);;
PrintTo("current_c4_descent/084_009.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 084_009 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
