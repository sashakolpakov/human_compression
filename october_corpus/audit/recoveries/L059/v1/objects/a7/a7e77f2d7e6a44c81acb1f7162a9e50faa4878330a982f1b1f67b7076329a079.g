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
D:=P177Graph("072_025",72,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36],[[1, 37], [1, 38], [1, 55], [1, 56], [2, 37], [2, 38], [2, 49], [2, 50], [3, 43], [3, 44], [3, 49], [3, 50], [4, 43], [4, 44], [4, 55], [4, 56], [5, 41], [5, 42], [5, 59], [5, 60], [6, 41], [6, 42], [6, 53], [6, 54], [7, 47], [7, 48], [7, 53], [7, 54], [8, 47], [8, 48], [8, 59], [8, 60], [9, 39], [9, 40], [9, 57], [9, 58], [10, 39], [10, 40], [10, 51], [10, 52], [11, 45], [11, 46], [11, 51], [11, 52], [12, 45], [12, 46], [12, 57], [12, 58], [13, 40], [13, 41], [13, 67], [13, 68], [14, 40], [14, 41], [14, 61], [14, 62], [15, 46], [15, 47], [15, 61], [15, 62], [16, 46], [16, 47], [16, 67], [16, 68], [17, 38], [17, 39], [17, 71], [17, 72], [18, 38], [18, 39], [18, 65], [18, 66], [19, 44], [19, 45], [19, 65], [19, 66], [20, 44], [20, 45], [20, 71], [20, 72], [21, 42], [21, 43], [21, 69], [21, 70], [22, 42], [22, 43], [22, 63], [22, 64], [23, 37], [23, 48], [23, 63], [23, 64], [24, 37], [24, 48], [24, 69], [24, 70], [25, 52], [25, 53], [25, 70], [25, 71], [26, 52], [26, 53], [26, 64], [26, 65], [27, 58], [27, 59], [27, 64], [27, 65], [28, 58], [28, 59], [28, 70], [28, 71], [29, 50], [29, 51], [29, 68], [29, 69], [30, 50], [30, 51], [30, 62], [30, 63], [31, 56], [31, 57], [31, 62], [31, 63], [32, 56], [32, 57], [32, 68], [32, 69], [33, 54], [33, 55], [33, 61], [33, 72], [34, 54], [34, 55], [34, 66], [34, 67], [35, 49], [35, 60], [35, 66], [35, 67], [36, 49], [36, 60], [36, 61], [36, 72]]);;
R:=P177Census(D);;Need(Size(R.F)=288);;
PrintTo("current_c4_descent/072_025.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 072_025 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
