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
D:=P177Graph("VT3_72_23",72,[1, 2, 3, 4, 5, 6, 10, 14, 16, 17, 19, 21, 28, 29, 30, 31, 32, 33, 34, 36, 37, 38, 44, 45, 48, 52, 54, 56, 59, 62, 65, 66, 67, 68, 71, 72],[[1, 27], [1, 42], [1, 70], [2, 18], [2, 22], [2, 60], [3, 42], [3, 51], [3, 61], [4, 23], [4, 26], [4, 60], [5, 22], [5, 63], [5, 70], [6, 50], [6, 58], [6, 63], [7, 32], [7, 33], [7, 37], [8, 10], [8, 52], [8, 68], [9, 14], [9, 31], [9, 45], [10, 53], [10, 64], [11, 34], [11, 37], [11, 62], [12, 16], [12, 19], [12, 72], [13, 36], [13, 65], [13, 72], [14, 46], [14, 50], [15, 45], [15, 59], [15, 67], [16, 43], [16, 49], [17, 20], [17, 27], [17, 40], [18, 66], [18, 68], [19, 39], [19, 55], [20, 62], [20, 67], [21, 22], [21, 57], [21, 58], [23, 56], [23, 68], [24, 31], [24, 52], [24, 71], [25, 36], [25, 52], [25, 56], [26, 28], [26, 30], [27, 34], [28, 40], [28, 47], [29, 40], [29, 60], [29, 70], [30, 39], [30, 69], [31, 64], [32, 35], [32, 53], [33, 49], [33, 57], [34, 61], [35, 59], [35, 62], [36, 51], [37, 43], [38, 49], [38, 55], [38, 58], [39, 44], [41, 44], [41, 45], [41, 48], [42, 54], [43, 65], [44, 47], [46, 54], [46, 71], [47, 67], [48, 50], [48, 55], [51, 71], [53, 66], [54, 63], [56, 69], [57, 66], [59, 64], [61, 65], [69, 72]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_72_23.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_72_23 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
