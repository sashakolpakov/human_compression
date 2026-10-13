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
D:=P177Graph("080_025",80,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40],[[1, 41], [1, 42], [1, 71], [1, 72], [2, 41], [2, 42], [2, 61], [2, 62], [3, 51], [3, 52], [3, 61], [3, 62], [4, 51], [4, 52], [4, 71], [4, 72], [5, 42], [5, 43], [5, 74], [5, 75], [6, 42], [6, 43], [6, 64], [6, 65], [7, 52], [7, 53], [7, 64], [7, 65], [8, 52], [8, 53], [8, 74], [8, 75], [9, 49], [9, 50], [9, 75], [9, 76], [10, 49], [10, 50], [10, 65], [10, 66], [11, 59], [11, 60], [11, 65], [11, 66], [12, 59], [12, 60], [12, 75], [12, 76], [13, 48], [13, 49], [13, 72], [13, 73], [14, 48], [14, 49], [14, 62], [14, 63], [15, 58], [15, 59], [15, 62], [15, 63], [16, 58], [16, 59], [16, 72], [16, 73], [17, 45], [17, 46], [17, 73], [17, 74], [18, 45], [18, 46], [18, 63], [18, 64], [19, 55], [19, 56], [19, 63], [19, 64], [20, 55], [20, 56], [20, 73], [20, 74], [21, 46], [21, 47], [21, 76], [21, 77], [22, 46], [22, 47], [22, 66], [22, 67], [23, 56], [23, 57], [23, 66], [23, 67], [24, 56], [24, 57], [24, 76], [24, 77], [25, 47], [25, 48], [25, 79], [25, 80], [26, 47], [26, 48], [26, 69], [26, 70], [27, 57], [27, 58], [27, 69], [27, 70], [28, 57], [28, 58], [28, 79], [28, 80], [29, 44], [29, 45], [29, 61], [29, 80], [30, 44], [30, 45], [30, 70], [30, 71], [31, 54], [31, 55], [31, 70], [31, 71], [32, 54], [32, 55], [32, 61], [32, 80], [33, 43], [33, 44], [33, 77], [33, 78], [34, 43], [34, 44], [34, 67], [34, 68], [35, 53], [35, 54], [35, 67], [35, 68], [36, 53], [36, 54], [36, 77], [36, 78], [37, 50], [37, 51], [37, 78], [37, 79], [38, 50], [38, 51], [38, 68], [38, 69], [39, 41], [39, 60], [39, 68], [39, 69], [40, 41], [40, 60], [40, 78], [40, 79]]);;
R:=P177Census(D);;Need(Size(R.F)=160);;
PrintTo("current_c4_descent/080_025.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 080_025 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
