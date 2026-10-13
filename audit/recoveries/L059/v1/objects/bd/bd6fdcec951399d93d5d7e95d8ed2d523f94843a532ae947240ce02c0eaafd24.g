Need:=function(ok) if not ok then Error("L059 cubic census invalid"); fi; end;;
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
D:=P177Graph("VT3_74_2",74,[1, 3, 4, 6, 7, 8, 10, 11, 12, 13, 16, 17, 18, 19, 23, 27, 31, 32, 34, 36, 37, 41, 42, 44, 45, 46, 50, 53, 54, 55, 56, 59, 60, 62, 63, 67, 69],[[1, 15], [1, 25], [1, 68], [2, 3], [2, 12], [2, 37], [3, 15], [3, 52], [4, 14], [4, 26], [4, 47], [5, 13], [5, 42], [5, 69], [6, 21], [6, 64], [6, 68], [7, 25], [7, 26], [7, 30], [8, 28], [8, 33], [8, 51], [9, 23], [9, 32], [9, 67], [10, 24], [10, 65], [10, 70], [11, 24], [11, 29], [11, 43], [12, 25], [12, 47], [13, 30], [13, 68], [14, 36], [14, 45], [15, 41], [16, 30], [16, 35], [16, 66], [17, 21], [17, 38], [17, 51], [18, 39], [18, 72], [18, 73], [19, 38], [19, 71], [19, 73], [20, 44], [20, 60], [20, 67], [21, 41], [22, 27], [22, 44], [22, 55], [23, 39], [23, 57], [24, 63], [26, 34], [27, 33], [27, 61], [28, 41], [28, 55], [29, 31], [29, 42], [31, 48], [31, 57], [32, 48], [32, 49], [33, 50], [34, 66], [34, 74], [35, 42], [35, 53], [36, 70], [36, 71], [37, 49], [37, 58], [38, 59], [39, 59], [40, 44], [40, 56], [40, 62], [43, 50], [43, 53], [45, 73], [45, 74], [46, 51], [46, 65], [46, 71], [47, 54], [48, 63], [49, 60], [50, 65], [52, 55], [52, 60], [53, 61], [54, 58], [54, 70], [56, 61], [56, 66], [57, 69], [58, 63], [59, 64], [62, 72], [62, 74], [64, 69], [67, 72]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_74_2.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_74_2 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
