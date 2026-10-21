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
D:=P177Graph("080_021",80,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40],[[1, 41], [1, 42], [1, 65], [1, 66], [2, 41], [2, 42], [2, 57], [2, 58], [3, 57], [3, 58], [3, 73], [3, 74], [4, 49], [4, 50], [4, 73], [4, 74], [5, 49], [5, 50], [5, 65], [5, 66], [6, 42], [6, 43], [6, 74], [6, 75], [7, 42], [7, 43], [7, 50], [7, 51], [8, 50], [8, 51], [8, 58], [8, 59], [9, 58], [9, 59], [9, 66], [9, 67], [10, 66], [10, 67], [10, 74], [10, 75], [11, 43], [11, 44], [11, 67], [11, 68], [12, 43], [12, 44], [12, 59], [12, 60], [13, 59], [13, 60], [13, 75], [13, 76], [14, 51], [14, 52], [14, 75], [14, 76], [15, 51], [15, 52], [15, 67], [15, 68], [16, 44], [16, 45], [16, 76], [16, 77], [17, 44], [17, 45], [17, 52], [17, 53], [18, 52], [18, 53], [18, 60], [18, 61], [19, 60], [19, 61], [19, 68], [19, 69], [20, 68], [20, 69], [20, 76], [20, 77], [21, 45], [21, 46], [21, 69], [21, 70], [22, 45], [22, 46], [22, 61], [22, 62], [23, 61], [23, 62], [23, 77], [23, 78], [24, 53], [24, 54], [24, 77], [24, 78], [25, 53], [25, 54], [25, 69], [25, 70], [26, 46], [26, 47], [26, 78], [26, 79], [27, 46], [27, 47], [27, 54], [27, 55], [28, 54], [28, 55], [28, 62], [28, 63], [29, 62], [29, 63], [29, 70], [29, 71], [30, 70], [30, 71], [30, 78], [30, 79], [31, 47], [31, 48], [31, 71], [31, 72], [32, 47], [32, 48], [32, 63], [32, 64], [33, 63], [33, 64], [33, 79], [33, 80], [34, 55], [34, 56], [34, 79], [34, 80], [35, 55], [35, 56], [35, 71], [35, 72], [36, 41], [36, 48], [36, 73], [36, 80], [37, 41], [37, 48], [37, 49], [37, 56], [38, 49], [38, 56], [38, 57], [38, 64], [39, 57], [39, 64], [39, 65], [39, 72], [40, 65], [40, 72], [40, 73], [40, 80]]);;
R:=P177Census(D);;Need(Size(R.F)=160);;
PrintTo("current_c4_descent/080_021.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 080_021 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
