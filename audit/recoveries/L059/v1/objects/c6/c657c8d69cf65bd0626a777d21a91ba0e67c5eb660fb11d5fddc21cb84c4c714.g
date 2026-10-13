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
D:=P177Graph("072_026",72,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36],[[1, 38], [1, 42], [1, 56], [1, 66], [2, 44], [2, 50], [2, 58], [2, 60], [3, 39], [3, 59], [3, 61], [3, 67], [4, 38], [4, 40], [4, 61], [4, 69], [5, 48], [5, 58], [5, 66], [5, 72], [6, 44], [6, 55], [6, 57], [6, 59], [7, 42], [7, 50], [7, 57], [7, 69], [8, 39], [8, 40], [8, 48], [8, 60], [9, 55], [9, 56], [9, 67], [9, 72], [10, 38], [10, 42], [10, 46], [10, 71], [11, 37], [11, 58], [11, 60], [11, 71], [12, 37], [12, 46], [12, 59], [12, 67], [13, 38], [13, 43], [13, 53], [13, 69], [14, 43], [14, 48], [14, 51], [14, 58], [15, 51], [15, 53], [15, 55], [15, 59], [16, 42], [16, 52], [16, 64], [16, 69], [17, 48], [17, 60], [17, 64], [17, 68], [18, 52], [18, 55], [18, 67], [18, 68], [19, 46], [19, 54], [19, 63], [19, 71], [20, 37], [20, 45], [20, 70], [20, 71], [21, 37], [21, 46], [21, 47], [21, 49], [22, 41], [22, 43], [22, 53], [22, 70], [23, 43], [23, 49], [23, 51], [23, 65], [24, 51], [24, 53], [24, 54], [24, 62], [25, 47], [25, 52], [25, 64], [25, 65], [26, 62], [26, 63], [26, 64], [26, 68], [27, 41], [27, 45], [27, 52], [27, 68], [28, 54], [28, 56], [28, 63], [28, 66], [29, 44], [29, 45], [29, 50], [29, 70], [30, 39], [30, 47], [30, 49], [30, 61], [31, 40], [31, 41], [31, 61], [31, 70], [32, 49], [32, 65], [32, 66], [32, 72], [33, 44], [33, 54], [33, 57], [33, 62], [34, 47], [34, 50], [34, 57], [34, 65], [35, 39], [35, 40], [35, 62], [35, 63], [36, 41], [36, 45], [36, 56], [36, 72]]);;
R:=P177Census(D);;Need(Size(R.F)=144);;
PrintTo("current_c4_descent/072_026.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 072_026 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
