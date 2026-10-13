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


D:=P177Graph("072_017",72,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36],[[1, 41], [1, 47], [1, 52], [1, 53], [2, 41], [2, 52], [2, 60], [2, 64], [3, 43], [3, 48], [3, 55], [3, 56], [4, 43], [4, 55], [4, 61], [4, 66], [5, 48], [5, 56], [5, 59], [5, 63], [6, 43], [6, 45], [6, 57], [6, 68], [7, 42], [7, 51], [7, 57], [7, 58], [8, 59], [8, 61], [8, 63], [8, 66], [9, 43], [9, 67], [9, 68], [9, 69], [10, 51], [10, 58], [10, 62], [10, 67], [11, 42], [11, 49], [11, 57], [11, 65], [12, 44], [12, 45], [12, 57], [12, 59], [13, 37], [13, 48], [13, 58], [13, 71], [14, 40], [14, 42], [14, 53], [14, 69], [15, 48], [15, 65], [15, 71], [15, 72], [16, 44], [16, 59], [16, 67], [16, 69], [17, 49], [17, 62], [17, 65], [17, 67], [18, 37], [18, 39], [18, 58], [18, 61], [19, 42], [19, 64], [19, 69], [19, 70], [20, 39], [20, 61], [20, 65], [20, 72], [21, 47], [21, 50], [21, 53], [21, 54], [22, 40], [22, 45], [22, 53], [22, 62], [23, 38], [23, 51], [23, 52], [23, 72], [24, 47], [24, 66], [24, 70], [24, 71], [25, 39], [25, 47], [25, 56], [25, 70], [26, 46], [26, 51], [26, 54], [26, 72], [27, 45], [27, 62], [27, 64], [27, 70], [28, 50], [28, 54], [28, 60], [28, 64], [29, 37], [29, 38], [29, 49], [29, 52], [30, 40], [30, 60], [30, 66], [30, 71], [31, 39], [31, 40], [31, 56], [31, 60], [32, 37], [32, 46], [32, 49], [32, 54], [33, 41], [33, 44], [33, 46], [33, 55], [34, 38], [34, 44], [34, 50], [34, 55], [35, 41], [35, 46], [35, 63], [35, 68], [36, 38], [36, 50], [36, 63], [36, 68]]);;
R:=P177Census(D);;
Need(Size(R.F)=4608);;
PrintTo("quartic_cutoff_probe/072_017.g","L059Result := ",R,";\n");
Print("L059_CUTOFF_COMPLETE 072_017 ",Length(R.witnesses),"\n");
QUIT;
