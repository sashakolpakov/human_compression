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
D:=P177Graph("072_015",72,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36],[[1, 37], [1, 42], [1, 52], [1, 53], [2, 37], [2, 52], [2, 61], [2, 66], [3, 43], [3, 44], [3, 54], [3, 55], [4, 37], [4, 39], [4, 50], [4, 57], [5, 43], [5, 45], [5, 55], [5, 67], [6, 37], [6, 50], [6, 51], [6, 55], [7, 44], [7, 46], [7, 54], [7, 57], [8, 59], [8, 62], [8, 63], [8, 65], [9, 42], [9, 48], [9, 53], [9, 56], [10, 38], [10, 47], [10, 63], [10, 68], [11, 45], [11, 50], [11, 52], [11, 72], [12, 38], [12, 43], [12, 51], [12, 58], [13, 46], [13, 57], [13, 59], [13, 63], [14, 42], [14, 49], [14, 63], [14, 68], [15, 50], [15, 52], [15, 59], [15, 68], [16, 43], [16, 49], [16, 51], [16, 53], [17, 45], [17, 62], [17, 65], [17, 67], [18, 47], [18, 48], [18, 56], [18, 58], [19, 38], [19, 47], [19, 67], [19, 72], [20, 60], [20, 61], [20, 64], [20, 66], [21, 41], [21, 54], [21, 61], [21, 71], [22, 39], [22, 40], [22, 48], [22, 57], [23, 59], [23, 64], [23, 68], [23, 70], [24, 62], [24, 66], [24, 69], [24, 71], [25, 38], [25, 39], [25, 46], [25, 58], [26, 47], [26, 58], [26, 60], [26, 64], [27, 61], [27, 67], [27, 71], [27, 72], [28, 41], [28, 44], [28, 64], [28, 70], [29, 39], [29, 46], [29, 66], [29, 71], [30, 51], [30, 55], [30, 60], [30, 70], [31, 41], [31, 42], [31, 49], [31, 54], [32, 40], [32, 48], [32, 65], [32, 69], [33, 49], [33, 53], [33, 62], [33, 69], [34, 40], [34, 45], [34, 56], [34, 72], [35, 60], [35, 65], [35, 69], [35, 70], [36, 40], [36, 41], [36, 44], [36, 56]]);;
R:=P177Census(D);;Need(Size(R.F)=144);;
PrintTo("current_c4_descent/072_015.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 072_015 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
