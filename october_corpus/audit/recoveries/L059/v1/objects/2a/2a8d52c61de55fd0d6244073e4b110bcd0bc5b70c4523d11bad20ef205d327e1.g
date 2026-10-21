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
D:=P177Graph("064_014",64,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32],[[1, 33], [1, 38], [1, 47], [1, 58], [2, 36], [2, 38], [2, 47], [2, 48], [3, 35], [3, 40], [3, 50], [3, 51], [4, 33], [4, 40], [4, 53], [4, 58], [5, 35], [5, 38], [5, 51], [5, 60], [6, 39], [6, 52], [6, 53], [6, 64], [7, 37], [7, 40], [7, 50], [7, 54], [8, 41], [8, 46], [8, 54], [8, 59], [9, 42], [9, 45], [9, 48], [9, 55], [10, 36], [10, 40], [10, 48], [10, 53], [11, 39], [11, 41], [11, 47], [11, 52], [12, 37], [12, 38], [12, 54], [12, 60], [13, 41], [13, 45], [13, 51], [13, 59], [14, 42], [14, 46], [14, 55], [14, 58], [15, 34], [15, 53], [15, 56], [15, 64], [16, 37], [16, 52], [16, 55], [16, 62], [17, 36], [17, 44], [17, 49], [17, 59], [18, 46], [18, 54], [18, 63], [18, 64], [19, 43], [19, 45], [19, 48], [19, 61], [20, 34], [20, 42], [20, 57], [20, 60], [21, 34], [21, 43], [21, 50], [21, 57], [22, 34], [22, 41], [22, 47], [22, 56], [23, 35], [23, 55], [23, 56], [23, 62], [24, 33], [24, 44], [24, 57], [24, 59], [25, 45], [25, 51], [25, 63], [25, 64], [26, 43], [26, 46], [26, 58], [26, 61], [27, 39], [27, 42], [27, 49], [27, 60], [28, 37], [28, 44], [28, 52], [28, 61], [29, 36], [29, 49], [29, 62], [29, 63], [30, 35], [30, 44], [30, 56], [30, 61], [31, 39], [31, 43], [31, 49], [31, 50], [32, 33], [32, 57], [32, 62], [32, 63]]);;
R:=P177Census(D);;Need(Size(R.F)=128);;
PrintTo("current_c4_descent/064_014.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 064_014 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
