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
D:=P177Graph("072_008",72,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60],[[1, 13], [1, 24], [1, 64], [1, 69], [2, 13], [2, 14], [2, 65], [2, 70], [3, 14], [3, 15], [3, 66], [3, 71], [4, 15], [4, 16], [4, 67], [4, 72], [5, 16], [5, 17], [5, 61], [5, 68], [6, 17], [6, 18], [6, 62], [6, 69], [7, 18], [7, 19], [7, 63], [7, 70], [8, 19], [8, 20], [8, 64], [8, 71], [9, 20], [9, 21], [9, 65], [9, 72], [10, 21], [10, 22], [10, 61], [10, 66], [11, 22], [11, 23], [11, 62], [11, 67], [12, 23], [12, 24], [12, 63], [12, 68], [13, 29], [13, 34], [14, 30], [14, 35], [15, 31], [15, 36], [16, 25], [16, 32], [17, 26], [17, 33], [18, 27], [18, 34], [19, 28], [19, 35], [20, 29], [20, 36], [21, 25], [21, 30], [22, 26], [22, 31], [23, 27], [23, 32], [24, 28], [24, 33], [25, 37], [25, 48], [26, 37], [26, 38], [27, 38], [27, 39], [28, 39], [28, 40], [29, 40], [29, 41], [30, 41], [30, 42], [31, 42], [31, 43], [32, 43], [32, 44], [33, 44], [33, 45], [34, 45], [34, 46], [35, 46], [35, 47], [36, 47], [36, 48], [37, 53], [37, 58], [38, 54], [38, 59], [39, 55], [39, 60], [40, 49], [40, 56], [41, 50], [41, 57], [42, 51], [42, 58], [43, 52], [43, 59], [44, 53], [44, 60], [45, 49], [45, 54], [46, 50], [46, 55], [47, 51], [47, 56], [48, 52], [48, 57], [49, 61], [49, 72], [50, 61], [50, 62], [51, 62], [51, 63], [52, 63], [52, 64], [53, 64], [53, 65], [54, 65], [54, 66], [55, 66], [55, 67], [56, 67], [56, 68], [57, 68], [57, 69], [58, 69], [58, 70], [59, 70], [59, 71], [60, 71], [60, 72]]);;
R:=P177Census(D);;Need(Size(R.F)=576);;
PrintTo("current_c4_descent/072_008.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 072_008 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
