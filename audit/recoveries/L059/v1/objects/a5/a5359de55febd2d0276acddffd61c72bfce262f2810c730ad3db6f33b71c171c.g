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
D:=P177Graph("072_021",72,[1, 3, 6, 7, 8, 11, 13, 15, 17, 20, 23, 25, 26, 28, 30, 33, 35, 36, 37, 40, 41, 45, 47, 49, 50, 53, 54, 56, 60, 62, 63, 65, 66, 68, 70, 72],[[1, 2], [1, 5], [1, 19], [1, 29], [2, 6], [2, 8], [2, 13], [3, 5], [3, 14], [3, 18], [3, 44], [4, 7], [4, 11], [4, 13], [4, 17], [5, 15], [5, 17], [6, 10], [6, 16], [6, 21], [7, 12], [7, 18], [7, 29], [8, 14], [8, 27], [8, 38], [9, 13], [9, 30], [9, 37], [9, 68], [10, 11], [10, 20], [10, 23], [11, 19], [11, 27], [12, 15], [12, 20], [12, 36], [13, 31], [14, 23], [14, 36], [15, 24], [15, 32], [16, 26], [16, 33], [16, 40], [17, 22], [17, 34], [18, 35], [18, 41], [19, 28], [19, 37], [20, 38], [20, 44], [21, 30], [21, 49], [21, 62], [22, 50], [22, 53], [22, 72], [23, 46], [23, 51], [24, 35], [24, 50], [24, 62], [25, 29], [25, 34], [25, 52], [25, 67], [26, 27], [26, 39], [26, 43], [27, 49], [28, 31], [28, 39], [28, 61], [29, 53], [30, 43], [30, 61], [31, 45], [31, 54], [32, 33], [32, 41], [32, 63], [33, 48], [33, 55], [34, 45], [34, 56], [35, 55], [35, 57], [36, 42], [36, 58], [37, 59], [37, 64], [38, 60], [38, 65], [39, 62], [39, 68], [40, 51], [40, 57], [40, 71], [41, 43], [41, 52], [42, 66], [42, 68], [42, 70], [43, 50], [44, 47], [44, 70], [45, 59], [45, 71], [46, 60], [46, 66], [46, 72], [47, 58], [47, 61], [47, 69], [48, 49], [48, 56], [48, 60], [49, 57], [50, 67], [51, 56], [51, 65], [52, 62], [52, 72], [53, 64], [53, 71], [54, 55], [54, 58], [54, 64], [55, 70], [56, 64], [57, 63], [58, 63], [59, 63], [59, 70], [60, 71], [61, 66], [65, 67], [65, 69], [66, 67], [68, 69], [69, 72]]);;
R:=P177Census(D);;Need(Size(R.F)=288);;
PrintTo("current_c4_descent/072_021.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 072_021 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
