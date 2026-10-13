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
D:=P177Graph("080_015",80,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40],[[1, 49], [1, 59], [1, 64], [1, 69], [2, 41], [2, 42], [2, 49], [2, 59], [3, 45], [3, 50], [3, 67], [3, 70], [4, 45], [4, 50], [4, 71], [4, 76], [5, 50], [5, 60], [5, 64], [5, 69], [6, 52], [6, 60], [6, 73], [6, 77], [7, 46], [7, 53], [7, 63], [7, 66], [8, 42], [8, 43], [8, 55], [8, 68], [9, 52], [9, 60], [9, 63], [9, 80], [10, 46], [10, 53], [10, 72], [10, 77], [11, 42], [11, 53], [11, 58], [11, 68], [12, 41], [12, 42], [12, 50], [12, 60], [13, 46], [13, 49], [13, 67], [13, 70], [14, 41], [14, 44], [14, 47], [14, 74], [15, 48], [15, 51], [15, 76], [15, 79], [16, 54], [16, 56], [16, 75], [16, 80], [17, 43], [17, 55], [17, 64], [17, 75], [18, 58], [18, 62], [18, 65], [18, 71], [19, 41], [19, 48], [19, 54], [19, 74], [20, 48], [20, 51], [20, 67], [20, 78], [21, 44], [21, 57], [21, 75], [21, 80], [22, 53], [22, 58], [22, 64], [22, 75], [23, 55], [23, 61], [23, 65], [23, 71], [24, 46], [24, 49], [24, 71], [24, 76], [25, 51], [25, 59], [25, 73], [25, 77], [26, 43], [26, 45], [26, 63], [26, 66], [27, 44], [27, 47], [27, 65], [27, 69], [28, 54], [28, 56], [28, 68], [28, 73], [29, 58], [29, 62], [29, 70], [29, 74], [30, 57], [30, 61], [30, 72], [30, 78], [31, 48], [31, 54], [31, 65], [31, 69], [32, 47], [32, 52], [32, 76], [32, 79], [33, 44], [33, 57], [33, 68], [33, 73], [34, 55], [34, 61], [34, 70], [34, 74], [35, 51], [35, 59], [35, 63], [35, 80], [36, 56], [36, 62], [36, 72], [36, 78], [37, 43], [37, 45], [37, 72], [37, 77], [38, 57], [38, 61], [38, 66], [38, 79], [39, 47], [39, 52], [39, 67], [39, 78], [40, 56], [40, 62], [40, 66], [40, 79]]);;
R:=P177Census(D);;Need(Size(R.F)=160);;
PrintTo("current_c4_descent/080_015.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 080_015 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
