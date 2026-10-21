Need:=function(ok) if not ok then Error("L059 cutoff probe invalid"); fi; end;;
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


D:=P177Graph("072_016",72,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36],[[1, 37], [1, 44], [1, 52], [1, 56], [2, 37], [2, 52], [2, 62], [2, 65], [3, 41], [3, 45], [3, 53], [3, 57], [4, 41], [4, 53], [4, 60], [4, 66], [5, 45], [5, 57], [5, 59], [5, 63], [6, 41], [6, 49], [6, 51], [6, 55], [7, 40], [7, 48], [7, 55], [7, 58], [8, 59], [8, 60], [8, 63], [8, 66], [9, 41], [9, 49], [9, 64], [9, 70], [10, 48], [10, 58], [10, 61], [10, 64], [11, 40], [11, 46], [11, 55], [11, 67], [12, 51], [12, 55], [12, 59], [12, 68], [13, 39], [13, 43], [13, 45], [13, 58], [14, 40], [14, 42], [14, 51], [14, 56], [15, 59], [15, 64], [15, 68], [15, 70], [16, 46], [16, 61], [16, 64], [16, 67], [17, 39], [17, 58], [17, 60], [17, 71], [18, 40], [18, 51], [18, 65], [18, 69], [19, 43], [19, 45], [19, 67], [19, 72], [20, 44], [20, 47], [20, 54], [20, 56], [21, 42], [21, 56], [21, 61], [21, 70], [22, 39], [22, 48], [22, 50], [22, 52], [23, 42], [23, 43], [23, 44], [23, 57], [24, 60], [24, 67], [24, 71], [24, 72], [25, 61], [25, 65], [25, 69], [25, 70], [26, 47], [26, 54], [26, 62], [26, 65], [27, 46], [27, 50], [27, 52], [27, 72], [28, 43], [28, 57], [28, 62], [28, 69], [29, 42], [29, 44], [29, 66], [29, 71], [30, 38], [30, 39], [30, 48], [30, 54], [31, 37], [31, 49], [31, 50], [31, 53], [32, 38], [32, 46], [32, 54], [32, 72], [33, 62], [33, 66], [33, 69], [33, 71], [34, 37], [34, 50], [34, 63], [34, 68], [35, 38], [35, 47], [35, 49], [35, 53], [36, 38], [36, 47], [36, 63], [36, 68]]);;
R:=P177Census(D);;
Need(Size(R.F)=4608);;
PrintTo("quartic_cutoff_probe/072_016.g","L059Result := ",R,";\n");
Print("L059_CUTOFF_COMPLETE 072_016 ",Length(R.witnesses),"\n");
QUIT;
