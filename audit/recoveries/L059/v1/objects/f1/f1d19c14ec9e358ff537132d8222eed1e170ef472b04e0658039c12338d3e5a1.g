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
D:=P177Graph("072_022",72,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36],[[1, 49], [1, 52], [1, 60], [1, 61], [2, 47], [2, 52], [2, 60], [2, 71], [3, 41], [3, 42], [3, 45], [3, 66], [4, 44], [4, 53], [4, 55], [4, 63], [5, 41], [5, 42], [5, 52], [5, 62], [6, 53], [6, 63], [6, 64], [6, 65], [7, 45], [7, 54], [7, 66], [7, 69], [8, 39], [8, 49], [8, 54], [8, 56], [9, 40], [9, 43], [9, 46], [9, 59], [10, 58], [10, 64], [10, 68], [10, 69], [11, 52], [11, 54], [11, 62], [11, 69], [12, 40], [12, 44], [12, 55], [12, 60], [13, 38], [13, 39], [13, 42], [13, 49], [14, 43], [14, 46], [14, 53], [14, 57], [15, 37], [15, 46], [15, 64], [15, 69], [16, 43], [16, 47], [16, 54], [16, 56], [17, 39], [17, 40], [17, 58], [17, 59], [18, 65], [18, 67], [18, 71], [18, 72], [19, 47], [19, 63], [19, 66], [19, 71], [20, 41], [20, 44], [20, 58], [20, 68], [21, 48], [21, 62], [21, 68], [21, 70], [22, 40], [22, 60], [22, 64], [22, 65], [23, 38], [23, 42], [23, 43], [23, 47], [24, 39], [24, 53], [24, 57], [24, 58], [25, 50], [25, 55], [25, 67], [25, 71], [26, 49], [26, 61], [26, 63], [26, 66], [27, 37], [27, 41], [27, 44], [27, 46], [28, 45], [28, 51], [28, 68], [28, 70], [29, 61], [29, 65], [29, 70], [29, 72], [30, 37], [30, 48], [30, 62], [30, 67], [31, 38], [31, 50], [31, 51], [31, 57], [32, 50], [32, 55], [32, 61], [32, 70], [33, 37], [33, 45], [33, 51], [33, 67], [34, 51], [34, 56], [34, 57], [34, 72], [35, 38], [35, 48], [35, 50], [35, 59], [36, 48], [36, 56], [36, 59], [36, 72]]);;
R:=P177Census(D);;Need(Size(R.F)=288);;
PrintTo("current_c4_descent/072_022.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 072_022 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
