LogTo("research/leemans/phase2_edge_inflation_check.log");;

# Exact affine square-grid group, retaining the orientation as well as the
# translation coordinate. Ordinary action on a 2-by-2 grid would lose signs.
GridSeed := function(n)
  local aa,bb,cc,mmul,mact,mats,m,ns,j,idx,a,diamond,vmod,degree,
        encode,gens,gg,tr,images,u,v,w,mt,im;
  aa:=[[-1,0],[0,1]]; bb:=[[0,1],[1,0]]; cc:=[[1,0],[0,-1]];
  mmul:=function(x,y) return x*y; end;
  mats:=[IdentityMat(2)];
  j:=1;
  while j<=Length(mats) do
    for m in [aa,bb] do
      ns:=m*mats[j];
      if not ns in mats then Add(mats,ns); fi;
    od;
    j:=j+1;
  od;
  diamond:=IsEvenInt(n);
  if diamond then a:=2^((n-4)/2); vmod:=2*a;
  else a:=2^((n-3)/2); vmod:=a; fi;
  degree:=8*a*vmod;
  encode:=function(t,M)
    local x,y;
    x:=t[1] mod a;
    if diamond then y:=(t[2]-t[1]) mod vmod;
    else y:=t[2] mod vmod; fi;
    return 8*(x*vmod+y)+Position(mats,M);
  end;
  gens:=[];
  for idx in [1..3] do
    gg:=[aa,bb,cc][idx];
    if idx=3 then tr:=[0,1]; else tr:=[0,0]; fi;
    images:=[];
    for u in [0..a-1] do
      for v in [0..vmod-1] do
        if diamond then w:=[u,u+v]; else w:=[u,v]; fi;
        for mt in mats do
          im:=gg*w+tr;
          Add(images,encode(im,gg*mt));
        od;
      od;
    od;
    Add(gens,PermList(images));
  od;
  return rec(group:=Group(gens),gens:=gens,n:=n);
end;

IPCheck := function(gens)
  local r,sets,subs,I,J;
  r:=Length(gens); sets:=Combinations([1..r]);
  subs:=List(sets,I->Group(Concatenation([()],gens{I})));
  for I in [1..Length(sets)] do
    for J in [I..Length(sets)] do
      if Intersection(subs[I],subs[J]) <>
        subs[Position(sets,Intersection(sets[I],sets[J]))] then
        Error("IP failure");
      fi;
    od;
  od;
  return true;
end;

RankThreeHelly := function(gens)
  local h0,h1,h2,lhs,rhs;
  h0:=Group(gens{[2,3]}); h1:=Group(gens{[1,3]});
  h2:=Group(gens{[1,2]});
  lhs:=Set(Concatenation(List(Elements(Intersection(h0,h1)),
    x->List(Elements(Intersection(h0,h2)),y->x*y))));
  rhs:=Filtered(Elements(h0),x->ForAny(Elements(h1),y->y^-1*x in h2));
  return lhs=Set(rhs);
end;

# Inflate the selected pairs. Omitted pairs retain their orders in B.
Inflate := function(seed,edges)
  local factors,edge,di,u,v,j,m,prod,emb,gens,i,x,fidx;
  factors:=[seed.group];
  for edge in edges do
    m:=edge[3];
    u:=PermList(List([0..m-1],j->((-j) mod m)+1));
    v:=PermList(List([0..m-1],j->((1-j) mod m)+1));
    Add(factors,Group(u,v));
    Add(edge,u); Add(edge,v);
  od;
  prod:=CallFuncList(DirectProduct,factors);
  emb:=List([1..Length(factors)],j->Embedding(prod,j));
  gens:=[];
  for i in [1..Length(seed.gens)] do
    x:=Image(emb[1],seed.gens[i]);
    for fidx in [1..Length(edges)] do
      edge:=edges[fidx];
      if i=edge[1] then x:=x*Image(emb[fidx+1],edge[4]);
      elif i=edge[2] then x:=x*Image(emb[fidx+1],edge[5]); fi;
    od;
    Add(gens,x);
  od;
  return rec(group:=Group(gens),gens:=gens);
end;

RunChecks := function()
  local n,B,i,j,pair,images,hom,expected,H,params,s,t,l,delta,
        q,edges,r,ab,dp,e1,e2,gens,ks,types,k,seed,rel;
  for n in [5..9] do
    B:=GridSeed(n);
    if Size(B.group)<>2^n then Error("Grid seed order"); fi;
    IPCheck(B.gens);
    if not RankThreeHelly(B.gens) then Error("Grid seed Helly"); fi;
    for pair in Combinations([1..3],2) do
      images:=List([1..3],i->());
      for i in pair do images[i]:=B.gens[i]; od;
      hom:=GroupHomomorphismByImages(B.group,Group(B.gens{pair}),B.gens,images);
      if hom=fail then Error("Missing pair retraction"); fi;
    od;
    Print("GRID n=",n," order=",Size(B.group)," IP=true Helly=true retractions=true\n");
  od;

  for params in [[2,2,1,0],[3,2,1,0],[2,3,2,0],[3,3,2,1],
                  [2,2,2,2],[3,2,3,2],[2,2,1,4]] do
    s:=params[1];t:=params[2];l:=params[3];delta:=params[4];
    B:=GridSeed(delta+5);
    edges:=[];
    if s>2 then Add(edges,[1,2,2^s]); fi;
    if t>2 then Add(edges,[2,3,2^t]); fi;
    if l>1 then Add(edges,[1,3,2^l]); fi;
    H:=Inflate(B,edges);
    expected:=2^(s+t+l+delta);
    if Size(H.group)<>expected then Error("Hypertope order"); fi;
    types:=[Order(H.gens[1]*H.gens[2]),Order(H.gens[2]*H.gens[3]),
            Order(H.gens[1]*H.gens[3])];
    if types<>[2^s,2^t,2^l] then Error("Hypertope types"); fi;
    IPCheck(H.gens);
    if not RankThreeHelly(H.gens) then Error("Hypertope Helly"); fi;
    gens:=H.gens;
    if Comm((gens[1]*gens[2])^4,gens[3])<>() or
       Comm(gens[1],(gens[2]*gens[3])^4)<>() or
       Comm((gens[1]*gens[3])^2,gens[2])<>() then
      Error("Source edge-power presentation relators");
    fi;
    if IsEvenInt(delta) then
      rel:=Comm((gens[1]*gens[2])^2,gens[3])^(2^(delta/2));
    else
      rel:=Comm((gens[1]*gens[2])^2,(gens[2]*gens[3])^2)^(2^((delta-1)/2));
    fi;
    if rel<>() then Error("Source lattice presentation relator"); fi;
    Print("HYPER params=",params," order=",Size(H.group)," type=",types,
          " IP=true Helly=true source_relators=true\n");
  od;

  for params in [[[2,2,2],0],[[3,2,3],1],[[2,2,2,2],0],[[2,3,2,2],1]] do
    ks:=params[1];delta:=params[2];r:=Length(ks)+1;
    B:=GridSeed(delta+5);
    ab:=ElementaryAbelianGroup(IsPermGroup,2^(r-3));
    dp:=DirectProduct(ab,B.group);e1:=Embedding(dp,1);e2:=Embedding(dp,2);
    gens:=Concatenation(List(GeneratorsOfGroup(ab),x->Image(e1,x)),
                        List(B.gens,x->Image(e2,x)));
    seed:=rec(group:=dp,gens:=gens);
    edges:=[];
    for i in [1..r-1] do
      q:=Order(gens[i]*gens[i+1]);
      if 2^ks[i]>q then Add(edges,[i,i+1,2^ks[i]]); fi;
    od;
    H:=Inflate(seed,edges); expected:=2^(Sum(ks)+1+delta);
    if Size(H.group)<>expected then Error("Higher rank order"); fi;
    types:=List([1..r-1],i->Order(H.gens[i]*H.gens[i+1]));
    if types<>List(ks,k->2^k) then Error("Higher rank types"); fi;
    IPCheck(H.gens);
    for pair in Combinations([1..r],2) do
      if pair[2]-pair[1]>1 and Order(H.gens[pair[1]]*H.gens[pair[2]])<>2 then
        Error("String failure");
      fi;
    od;
    Print("POLY rank=",r," exponents=",ks," excess=",delta,
          " order=",Size(H.group)," IP=true string=true\n");
  od;
  for r in [3,4] do
    ab:=ElementaryAbelianGroup(IsPermGroup,2^r);
    seed:=rec(group:=ab,gens:=GeneratorsOfGroup(ab));
    edges:=List(Combinations([1..r],2),e->[e[1],e[2],4]);
    H:=Inflate(seed,edges);
    expected:=2^(r+Binomial(r,2));
    if Size(H.group)<>expected then Error("Complete even diagram order"); fi;
    IPCheck(H.gens);
    if r=3 and not RankThreeHelly(H.gens) then Error("Complete diagram Helly"); fi;
    Print("CUBE complete_rank=",r," every_pair_order=4 order=",Size(H.group),
          " IP=true\n");
  od;
  Print("ALL EDGE-INFLATION CHECKS PASS\n");
end;

RunChecks();
LogTo();
QUIT;
