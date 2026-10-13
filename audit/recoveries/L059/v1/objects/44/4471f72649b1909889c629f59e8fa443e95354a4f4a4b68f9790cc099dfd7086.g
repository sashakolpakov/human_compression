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
D:=P177Graph("072_027",72,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36],[[1, 48], [1, 49], [1, 51], [1, 68], [2, 43], [2, 44], [2, 49], [2, 60], [3, 40], [3, 43], [3, 54], [3, 68], [4, 44], [4, 45], [4, 53], [4, 56], [5, 42], [5, 45], [5, 54], [5, 71], [6, 42], [6, 48], [6, 56], [6, 57], [7, 39], [7, 40], [7, 69], [7, 71], [8, 39], [8, 50], [8, 51], [8, 57], [9, 50], [9, 53], [9, 60], [9, 69], [10, 39], [10, 47], [10, 56], [10, 65], [11, 45], [11, 46], [11, 50], [11, 64], [12, 41], [12, 42], [12, 55], [12, 69], [13, 46], [13, 49], [13, 67], [13, 69], [14, 39], [14, 43], [14, 55], [14, 58], [15, 50], [15, 63], [15, 65], [15, 68], [16, 41], [16, 45], [16, 58], [16, 68], [17, 42], [17, 47], [17, 49], [17, 63], [18, 43], [18, 56], [18, 64], [18, 67], [19, 52], [19, 55], [19, 64], [19, 72], [20, 41], [20, 61], [20, 65], [20, 66], [21, 37], [21, 46], [21, 47], [21, 62], [22, 55], [22, 59], [22, 62], [22, 63], [23, 65], [23, 67], [23, 70], [23, 72], [24, 38], [24, 46], [24, 58], [24, 61], [25, 38], [25, 63], [25, 64], [25, 66], [26, 37], [26, 41], [26, 59], [26, 67], [27, 47], [27, 52], [27, 58], [27, 70], [28, 38], [28, 54], [28, 59], [28, 60], [29, 40], [29, 48], [29, 59], [29, 70], [30, 38], [30, 44], [30, 51], [30, 70], [31, 52], [31, 54], [31, 57], [31, 66], [32, 37], [32, 48], [32, 53], [32, 66], [33, 37], [33, 44], [33, 52], [33, 71], [34, 57], [34, 60], [34, 62], [34, 72], [35, 40], [35, 53], [35, 61], [35, 72], [36, 51], [36, 61], [36, 62], [36, 71]]);;
R:=P177Census(D);;Need(Size(R.F)=144);;
PrintTo("current_c4_descent/072_027.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 072_027 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
