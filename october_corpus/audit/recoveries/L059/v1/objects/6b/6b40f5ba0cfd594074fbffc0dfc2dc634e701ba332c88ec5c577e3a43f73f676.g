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
D:=P177Graph("064_015",64,[1, 3, 5, 8, 9, 11, 12, 13, 14, 16, 24, 26, 27, 28, 29, 30, 32, 34, 35, 36, 41, 43, 47, 48, 53, 54, 55, 56, 57, 58, 63, 64],[[1, 2], [1, 4], [1, 19], [1, 22], [2, 5], [2, 8], [2, 28], [3, 6], [3, 7], [3, 10], [3, 18], [4, 9], [4, 14], [4, 36], [5, 10], [5, 15], [5, 39], [6, 11], [6, 16], [6, 32], [7, 12], [7, 13], [7, 27], [8, 17], [8, 23], [8, 46], [9, 17], [9, 18], [9, 40], [10, 24], [10, 48], [11, 19], [11, 20], [11, 37], [12, 20], [12, 25], [12, 42], [13, 21], [13, 22], [13, 38], [14, 15], [14, 31], [14, 51], [15, 26], [15, 32], [16, 21], [16, 33], [16, 50], [17, 26], [17, 27], [18, 34], [18, 54], [19, 35], [19, 53], [20, 28], [20, 29], [21, 29], [21, 36], [22, 30], [22, 47], [23, 24], [23, 41], [23, 57], [24, 37], [24, 42], [25, 30], [25, 43], [25, 56], [26, 37], [26, 38], [27, 44], [27, 60], [28, 45], [28, 59], [29, 39], [29, 40], [30, 40], [30, 46], [31, 34], [31, 41], [31, 58], [32, 49], [32, 62], [33, 35], [33, 43], [33, 55], [34, 38], [34, 50], [35, 39], [35, 51], [36, 52], [36, 61], [37, 47], [38, 53], [39, 54], [40, 48], [41, 44], [41, 49], [42, 55], [42, 64], [43, 45], [43, 52], [44, 47], [44, 56], [45, 48], [45, 57], [46, 58], [46, 63], [47, 59], [48, 60], [49, 53], [49, 55], [50, 56], [50, 64], [51, 57], [51, 63], [52, 54], [52, 58], [53, 61], [54, 62], [55, 59], [56, 61], [57, 62], [58, 60], [59, 63], [60, 64], [61, 63], [62, 64]]);;
R:=P177Census(D);;Need(Size(R.F)=1536);;
PrintTo("current_c4_descent/064_015.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 064_015 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
