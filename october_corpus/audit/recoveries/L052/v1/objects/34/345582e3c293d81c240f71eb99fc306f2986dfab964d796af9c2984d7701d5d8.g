SizeScreen([100000,100000]);;
Need:=function(b,msg) if not b then Error(msg);fi;end;;
Meet:=function(m,n,r)return Sum(Filtered([0..r-1],i->QuoInt(m,2^i) mod 2=1 and QuoInt(n,2^i) mod 2=1),i->2^i);end;;
Subsets:=function(rr)
 local G,r;
 G:=Group(rr);r:=Length(rr);
 return List([0..2^r-1],m->Group(rr{Filtered([1..r],i->QuoInt(m,2^(i-1)) mod 2=1)},One(G)));
end;;
IP:=function(rr)
 local r,ss,m,n;
 r:=Length(rr);ss:=Subsets(rr);
 for m in [0..2^r-1] do for n in [0..2^r-1] do Need(Intersection(ss[m+1],ss[n+1])=ss[Meet(m,n,r)+1],"IP");od;od;
 return List(ss,Size);
end;;
F:=FreeGroup("a","b","c");;a:=F.1;;b:=F.2;;c:=F.3;;
P:=F/[a^2,b^2,c^2,(a*b*c)^2,(a*b)^3,(b*c)^3];;
iso:=IsomorphismPermGroup(P);;Need(iso<>fail and IsBijective(iso),"fp exact");;
r44:=List(GeneratorsOfGroup(P),g->Image(iso,g));;
r45:=[(1,2)(3,4),(2,6)(3,5),(1,4)(2,3),(1,4)(3,5)];;
r63:=[(3,6)(4,7)(5,9)(8,10)(11,12),(2,4)(3,6)(5,10)(8,12)(9,11),(1,2)(3,5)(4,7)(6,9)(8,11)(10,12),(1,3)(2,5)(4,8)(7,11)(10,12)];;
G:=fail;;N:=0;;rr:=[];;rank:=0;;aa:=[];;sm:=fail;;w:=();;
for data in [["4.4",r44],["4.5",r45],["6.3",r63]] do
 rr:=data[2];;G:=Group(rr);;rank:=Length(rr);;N:=LargestMovedPoint(G);;
 Print("EXAMPLE ",data[1],"\nORDER ",Size(G),"\nIP ",IP(rr),"\nGENERATORS ",List(rr,g->List([1..N],i->i^g)),"\n");;
 if data[1]="4.5" then Need(G=AlternatingGroup(6),"A6 identity");fi;
 if data[1]="6.3" then
  aa:=Concatenation([One(G)],List(rr{[2..4]},r->rr[1]*r));;rot:=Group(aa);;Need(rot=G,"rotation=G");;
  ss:=List([0..15],m->Group(List(Combinations(Filtered([1..4],i->QuoInt(m,2^(i-1)) mod 2=1),2),ij->aa[ij[1]]^-1*aa[ij[2]]),One(G)));;
  inter:=Intersection(ss[8],ss[15]);;sm:=ss[7];;Need(Size(inter)>Size(sm),"IC+ failure");;
  w:=First(Elements(inter),g->not g in sm);;
  Print("ROTATION_ORDER ",Size(rot),"\nICPLUS_ORDERS ",List(ss,Size),"\nFAILURE ",[Size(inter),Size(sm)],"\nWITNESS ",List([1..N],i->i^w),"\n");;
 else
  pars:=List([1..rank],i->Group(rr{Difference([1..rank],[i])}));;
  cosets:=List(pars,H->RightCosets(G,H));;
  edges:=[];;
  for i in [1..rank] do for j in [i+1..rank] do if j<=rank then
   for h in [1..Length(cosets[i])] do for k in [1..Length(cosets[j])] do
    if Intersection(Elements(cosets[i][h]),Elements(cosets[j][k]))<>[] then Add(edges,[i,h,j,k]);fi;
   od;od;
  fi;od;od;
  Print("PARABOLIC_ORDERS ",List(pars,Size),"\nCOS_COUNTS ",List(cosets,Length),"\nEDGES ",edges,"\n");;
 fi;
od;
Print("PASS_EXAMPLES\n");;QUIT;
