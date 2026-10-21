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
D:=P177Graph("072_004",72,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71],[[1, 26], [1, 48], [1, 50], [1, 72], [2, 25], [2, 27], [2, 49], [2, 51], [3, 26], [3, 28], [3, 50], [3, 52], [4, 27], [4, 29], [4, 51], [4, 53], [5, 28], [5, 30], [5, 52], [5, 54], [6, 29], [6, 31], [6, 53], [6, 55], [7, 30], [7, 32], [7, 54], [7, 56], [8, 31], [8, 33], [8, 55], [8, 57], [9, 32], [9, 34], [9, 56], [9, 58], [10, 33], [10, 35], [10, 57], [10, 59], [11, 34], [11, 36], [11, 58], [11, 60], [12, 35], [12, 37], [12, 59], [12, 61], [13, 36], [13, 38], [13, 60], [13, 62], [14, 37], [14, 39], [14, 61], [14, 63], [15, 38], [15, 40], [15, 62], [15, 64], [16, 39], [16, 41], [16, 63], [16, 65], [17, 40], [17, 42], [17, 64], [17, 66], [18, 41], [18, 43], [18, 65], [18, 67], [19, 42], [19, 44], [19, 66], [19, 68], [20, 43], [20, 45], [20, 67], [20, 69], [21, 44], [21, 46], [21, 68], [21, 70], [22, 45], [22, 47], [22, 69], [22, 71], [23, 46], [23, 48], [23, 70], [23, 72], [24, 25], [24, 47], [24, 49], [24, 71], [25, 50], [25, 72], [26, 49], [26, 51], [27, 50], [27, 52], [28, 51], [28, 53], [29, 52], [29, 54], [30, 53], [30, 55], [31, 54], [31, 56], [32, 55], [32, 57], [33, 56], [33, 58], [34, 57], [34, 59], [35, 58], [35, 60], [36, 59], [36, 61], [37, 60], [37, 62], [38, 61], [38, 63], [39, 62], [39, 64], [40, 63], [40, 65], [41, 64], [41, 66], [42, 65], [42, 67], [43, 66], [43, 68], [44, 67], [44, 69], [45, 68], [45, 70], [46, 69], [46, 71], [47, 70], [47, 72], [48, 49], [48, 71]]);;
R:=P177Census(D);;Need(Size(R.F)=288);;
PrintTo("current_c4_descent/072_004.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 072_004 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
