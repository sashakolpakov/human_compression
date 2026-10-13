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
D:=P177Graph("072_005",72,[1, 3, 5, 7, 9, 11, 14, 16, 18, 20, 22, 24, 25, 27, 29, 31, 33, 35, 38, 40, 42, 44, 46, 48, 49, 51, 53, 55, 57, 59, 62, 64, 66, 68, 70, 72],[[1, 2], [1, 12], [1, 13], [1, 67], [2, 3], [2, 14], [2, 68], [3, 4], [3, 15], [3, 69], [4, 5], [4, 16], [4, 70], [5, 6], [5, 17], [5, 71], [6, 7], [6, 18], [6, 72], [7, 8], [7, 19], [7, 61], [8, 9], [8, 20], [8, 62], [9, 10], [9, 21], [9, 63], [10, 11], [10, 22], [10, 64], [11, 12], [11, 23], [11, 65], [12, 24], [12, 66], [13, 14], [13, 24], [13, 25], [14, 15], [14, 26], [15, 16], [15, 27], [16, 17], [16, 28], [17, 18], [17, 29], [18, 19], [18, 30], [19, 20], [19, 31], [20, 21], [20, 32], [21, 22], [21, 33], [22, 23], [22, 34], [23, 24], [23, 35], [24, 36], [25, 26], [25, 36], [25, 37], [26, 27], [26, 38], [27, 28], [27, 39], [28, 29], [28, 40], [29, 30], [29, 41], [30, 31], [30, 42], [31, 32], [31, 43], [32, 33], [32, 44], [33, 34], [33, 45], [34, 35], [34, 46], [35, 36], [35, 47], [36, 48], [37, 38], [37, 48], [37, 49], [38, 39], [38, 50], [39, 40], [39, 51], [40, 41], [40, 52], [41, 42], [41, 53], [42, 43], [42, 54], [43, 44], [43, 55], [44, 45], [44, 56], [45, 46], [45, 57], [46, 47], [46, 58], [47, 48], [47, 59], [48, 60], [49, 50], [49, 60], [49, 61], [50, 51], [50, 62], [51, 52], [51, 63], [52, 53], [52, 64], [53, 54], [53, 65], [54, 55], [54, 66], [55, 56], [55, 67], [56, 57], [56, 68], [57, 58], [57, 69], [58, 59], [58, 70], [59, 60], [59, 71], [60, 72], [61, 62], [61, 72], [62, 63], [63, 64], [64, 65], [65, 66], [66, 67], [67, 68], [68, 69], [69, 70], [70, 71], [71, 72]]);;
R:=P177Census(D);;Need(Size(R.F)=576);;
PrintTo("current_c4_descent/072_005.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 072_005 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
