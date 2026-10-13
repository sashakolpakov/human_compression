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


D:=P177Graph("070_004",70,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35],[[1, 40], [1, 58], [1, 61], [1, 65], [2, 44], [2, 48], [2, 60], [2, 66], [3, 45], [3, 49], [3, 53], [3, 54], [4, 42], [4, 47], [4, 50], [4, 53], [5, 36], [5, 66], [5, 68], [5, 69], [6, 49], [6, 55], [6, 62], [6, 67], [7, 39], [7, 48], [7, 58], [7, 62], [8, 45], [8, 56], [8, 60], [8, 62], [9, 37], [9, 64], [9, 67], [9, 70], [10, 38], [10, 43], [10, 69], [10, 70], [11, 48], [11, 52], [11, 55], [11, 69], [12, 39], [12, 56], [12, 63], [12, 66], [13, 37], [13, 42], [13, 46], [13, 54], [14, 38], [14, 41], [14, 57], [14, 66], [15, 39], [15, 59], [15, 67], [15, 69], [16, 54], [16, 59], [16, 63], [16, 68], [17, 46], [17, 56], [17, 57], [17, 64], [18, 38], [18, 39], [18, 64], [18, 65], [19, 38], [19, 48], [19, 51], [19, 61], [20, 41], [20, 46], [20, 63], [20, 65], [21, 43], [21, 47], [21, 52], [21, 61], [22, 49], [22, 52], [22, 58], [22, 59], [23, 36], [23, 42], [23, 57], [23, 70], [24, 50], [24, 51], [24, 57], [24, 60], [25, 37], [25, 43], [25, 59], [25, 65], [26, 36], [26, 54], [26, 56], [26, 67], [27, 41], [27, 42], [27, 43], [27, 68], [28, 47], [28, 51], [28, 55], [28, 70], [29, 44], [29, 52], [29, 53], [29, 68], [30, 36], [30, 53], [30, 55], [30, 60], [31, 37], [31, 40], [31, 47], [31, 49], [32, 41], [32, 44], [32, 50], [32, 61], [33, 40], [33, 51], [33, 62], [33, 64], [34, 40], [34, 45], [34, 46], [34, 50], [35, 44], [35, 45], [35, 58], [35, 63]]);;
R:=P177Census(D);;
Need(Size(R.F)=10080);;
PrintTo("quartic_cutoff_probe/070_004.g","L059Result := ",R,";\n");
Print("L059_CUTOFF_COMPLETE 070_004 ",Length(R.witnesses),"\n");
QUIT;
