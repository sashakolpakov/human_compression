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
D:=P177Graph("072_019",72,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54],[[1, 19], [1, 34], [1, 56], [1, 72], [2, 20], [2, 35], [2, 57], [2, 70], [3, 21], [3, 36], [3, 55], [3, 71], [4, 19], [4, 22], [4, 57], [4, 59], [5, 20], [5, 23], [5, 55], [5, 60], [6, 21], [6, 24], [6, 56], [6, 58], [7, 22], [7, 25], [7, 60], [7, 62], [8, 23], [8, 26], [8, 58], [8, 63], [9, 24], [9, 27], [9, 59], [9, 61], [10, 25], [10, 28], [10, 63], [10, 65], [11, 26], [11, 29], [11, 61], [11, 66], [12, 27], [12, 30], [12, 62], [12, 64], [13, 28], [13, 31], [13, 66], [13, 68], [14, 29], [14, 32], [14, 64], [14, 69], [15, 30], [15, 33], [15, 65], [15, 67], [16, 31], [16, 34], [16, 69], [16, 71], [17, 32], [17, 35], [17, 67], [17, 72], [18, 33], [18, 36], [18, 68], [18, 70], [19, 38], [19, 42], [20, 39], [20, 40], [21, 37], [21, 41], [22, 41], [22, 45], [23, 42], [23, 43], [24, 40], [24, 44], [25, 44], [25, 48], [26, 45], [26, 46], [27, 43], [27, 47], [28, 47], [28, 51], [29, 48], [29, 49], [30, 46], [30, 50], [31, 50], [31, 54], [32, 51], [32, 52], [33, 49], [33, 53], [34, 39], [34, 53], [35, 37], [35, 54], [36, 38], [36, 52], [37, 60], [37, 68], [38, 58], [38, 69], [39, 59], [39, 67], [40, 63], [40, 71], [41, 61], [41, 72], [42, 62], [42, 70], [43, 56], [43, 66], [44, 57], [44, 64], [45, 55], [45, 65], [46, 59], [46, 69], [47, 60], [47, 67], [48, 58], [48, 68], [49, 62], [49, 72], [50, 63], [50, 70], [51, 61], [51, 71], [52, 57], [52, 65], [53, 55], [53, 66], [54, 56], [54, 64]]);;
R:=P177Census(D);;Need(Size(R.F)=144);;
PrintTo("current_c4_descent/072_019.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 072_019 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
