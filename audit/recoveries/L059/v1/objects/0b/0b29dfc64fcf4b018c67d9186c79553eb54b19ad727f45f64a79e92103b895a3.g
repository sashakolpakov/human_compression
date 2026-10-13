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
D:=P177Graph("080_016",80,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40],[[1, 53], [1, 55], [1, 57], [1, 60], [2, 53], [2, 55], [2, 74], [2, 78], [3, 49], [3, 54], [3, 56], [3, 58], [4, 57], [4, 60], [4, 63], [4, 64], [5, 49], [5, 54], [5, 71], [5, 76], [6, 41], [6, 43], [6, 52], [6, 62], [7, 44], [7, 51], [7, 67], [7, 69], [8, 42], [8, 47], [8, 74], [8, 78], [9, 47], [9, 56], [9, 58], [9, 66], [10, 63], [10, 64], [10, 73], [10, 77], [11, 41], [11, 62], [11, 79], [11, 80], [12, 44], [12, 50], [12, 51], [12, 59], [13, 45], [13, 48], [13, 65], [13, 70], [14, 66], [14, 70], [14, 72], [14, 73], [15, 42], [15, 43], [15, 52], [15, 68], [16, 42], [16, 68], [16, 71], [16, 72], [17, 64], [17, 67], [17, 71], [17, 76], [18, 67], [18, 69], [18, 74], [18, 80], [19, 42], [19, 44], [19, 47], [19, 48], [20, 47], [20, 66], [20, 75], [20, 79], [21, 41], [21, 54], [21, 73], [21, 77], [22, 50], [22, 59], [22, 72], [22, 73], [23, 45], [23, 46], [23, 48], [23, 61], [24, 68], [24, 69], [24, 75], [24, 77], [25, 63], [25, 65], [25, 79], [25, 80], [26, 65], [26, 70], [26, 76], [26, 78], [27, 51], [27, 56], [27, 63], [27, 65], [28, 59], [28, 62], [28, 76], [28, 78], [29, 52], [29, 57], [29, 66], [29, 70], [30, 55], [30, 61], [30, 71], [30, 72], [31, 43], [31, 45], [31, 64], [31, 67], [32, 46], [32, 49], [32, 74], [32, 80], [33, 41], [33, 44], [33, 48], [33, 54], [34, 50], [34, 53], [34, 75], [34, 79], [35, 46], [35, 61], [35, 75], [35, 77], [36, 58], [36, 60], [36, 68], [36, 69], [37, 58], [37, 59], [37, 60], [37, 62], [38, 43], [38, 45], [38, 50], [38, 53], [39, 51], [39, 55], [39, 56], [39, 61], [40, 46], [40, 49], [40, 52], [40, 57]]);;
R:=P177Census(D);;Need(Size(R.F)=160);;
PrintTo("current_c4_descent/080_016.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 080_016 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
