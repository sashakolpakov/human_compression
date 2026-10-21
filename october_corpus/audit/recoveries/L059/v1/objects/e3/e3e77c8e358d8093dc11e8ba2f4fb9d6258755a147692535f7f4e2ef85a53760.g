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
D:=P177Graph("064_009",64,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32],[[1, 33], [1, 34], [1, 53], [1, 54], [2, 33], [2, 34], [2, 45], [2, 46], [3, 45], [3, 46], [3, 57], [3, 58], [4, 37], [4, 38], [4, 57], [4, 58], [5, 37], [5, 38], [5, 49], [5, 50], [6, 49], [6, 50], [6, 61], [6, 62], [7, 41], [7, 42], [7, 61], [7, 62], [8, 41], [8, 42], [8, 53], [8, 54], [9, 34], [9, 35], [9, 62], [9, 63], [10, 34], [10, 35], [10, 38], [10, 39], [11, 38], [11, 39], [11, 42], [11, 43], [12, 42], [12, 43], [12, 46], [12, 47], [13, 46], [13, 47], [13, 50], [13, 51], [14, 50], [14, 51], [14, 54], [14, 55], [15, 54], [15, 55], [15, 58], [15, 59], [16, 58], [16, 59], [16, 62], [16, 63], [17, 35], [17, 36], [17, 55], [17, 56], [18, 35], [18, 36], [18, 47], [18, 48], [19, 47], [19, 48], [19, 59], [19, 60], [20, 39], [20, 40], [20, 59], [20, 60], [21, 39], [21, 40], [21, 51], [21, 52], [22, 51], [22, 52], [22, 63], [22, 64], [23, 43], [23, 44], [23, 63], [23, 64], [24, 43], [24, 44], [24, 55], [24, 56], [25, 33], [25, 36], [25, 61], [25, 64], [26, 33], [26, 36], [26, 37], [26, 40], [27, 37], [27, 40], [27, 41], [27, 44], [28, 41], [28, 44], [28, 45], [28, 48], [29, 45], [29, 48], [29, 49], [29, 52], [30, 49], [30, 52], [30, 53], [30, 56], [31, 53], [31, 56], [31, 57], [31, 60], [32, 57], [32, 60], [32, 61], [32, 64]]);;
R:=P177Census(D);;Need(Size(R.F)=128);;
PrintTo("current_c4_descent/064_009.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 064_009 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
