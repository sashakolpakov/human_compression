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
D:=P177Graph("064_012",64,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32],[[1, 35], [1, 48], [1, 49], [1, 59], [2, 33], [2, 35], [2, 49], [2, 62], [3, 35], [3, 42], [3, 54], [3, 58], [4, 38], [4, 48], [4, 55], [4, 59], [5, 35], [5, 43], [5, 51], [5, 54], [6, 39], [6, 41], [6, 49], [6, 57], [7, 44], [7, 48], [7, 53], [7, 60], [8, 33], [8, 36], [8, 52], [8, 62], [9, 36], [9, 42], [9, 55], [9, 58], [10, 39], [10, 45], [10, 49], [10, 50], [11, 37], [11, 48], [11, 53], [11, 63], [12, 40], [12, 46], [12, 56], [12, 59], [13, 39], [13, 40], [13, 53], [13, 54], [14, 33], [14, 46], [14, 47], [14, 56], [15, 42], [15, 44], [15, 56], [15, 57], [16, 38], [16, 47], [16, 55], [16, 61], [17, 38], [17, 43], [17, 51], [17, 52], [18, 38], [18, 41], [18, 52], [18, 57], [19, 44], [19, 60], [19, 61], [19, 62], [20, 34], [20, 40], [20, 59], [20, 64], [21, 39], [21, 47], [21, 54], [21, 61], [22, 33], [22, 37], [22, 47], [22, 63], [23, 42], [23, 57], [23, 63], [23, 64], [24, 41], [24, 46], [24, 58], [24, 60], [25, 34], [25, 61], [25, 62], [25, 64], [26, 45], [26, 46], [26, 51], [26, 60], [27, 34], [27, 37], [27, 41], [27, 58], [28, 43], [28, 44], [28, 50], [28, 56], [29, 36], [29, 40], [29, 52], [29, 53], [30, 36], [30, 45], [30, 50], [30, 55], [31, 45], [31, 51], [31, 63], [31, 64], [32, 34], [32, 37], [32, 43], [32, 50]]);;
R:=P177Census(D);;Need(Size(R.F)=2048);;
PrintTo("current_c4_descent/064_012.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 064_012 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
