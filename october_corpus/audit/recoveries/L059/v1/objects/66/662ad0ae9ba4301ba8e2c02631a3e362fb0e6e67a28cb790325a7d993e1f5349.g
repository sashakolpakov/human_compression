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
D:=P177Graph("064_010",64,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32],[[1, 33], [1, 34], [1, 45], [1, 46], [2, 33], [2, 34], [2, 57], [2, 58], [3, 53], [3, 54], [3, 57], [3, 58], [4, 41], [4, 42], [4, 53], [4, 54], [5, 37], [5, 38], [5, 41], [5, 42], [6, 37], [6, 38], [6, 61], [6, 62], [7, 49], [7, 50], [7, 61], [7, 62], [8, 45], [8, 46], [8, 49], [8, 50], [9, 34], [9, 35], [9, 62], [9, 63], [10, 34], [10, 35], [10, 42], [10, 43], [11, 42], [11, 43], [11, 50], [11, 51], [12, 50], [12, 51], [12, 58], [12, 59], [13, 38], [13, 39], [13, 58], [13, 59], [14, 38], [14, 39], [14, 46], [14, 47], [15, 46], [15, 47], [15, 54], [15, 55], [16, 54], [16, 55], [16, 62], [16, 63], [17, 35], [17, 36], [17, 47], [17, 48], [18, 35], [18, 36], [18, 59], [18, 60], [19, 55], [19, 56], [19, 59], [19, 60], [20, 43], [20, 44], [20, 55], [20, 56], [21, 39], [21, 40], [21, 43], [21, 44], [22, 39], [22, 40], [22, 63], [22, 64], [23, 51], [23, 52], [23, 63], [23, 64], [24, 47], [24, 48], [24, 51], [24, 52], [25, 33], [25, 40], [25, 60], [25, 61], [26, 33], [26, 40], [26, 41], [26, 48], [27, 41], [27, 48], [27, 49], [27, 56], [28, 49], [28, 56], [28, 57], [28, 64], [29, 36], [29, 37], [29, 57], [29, 64], [30, 36], [30, 37], [30, 44], [30, 45], [31, 44], [31, 45], [31, 52], [31, 53], [32, 52], [32, 53], [32, 60], [32, 61]]);;
R:=P177Census(D);;Need(Size(R.F)=256);;
PrintTo("current_c4_descent/064_010.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 064_010 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
