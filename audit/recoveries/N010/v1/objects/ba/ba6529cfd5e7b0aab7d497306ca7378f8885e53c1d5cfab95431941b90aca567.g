SizeScreen([100000,100000]);;
Need:=function(b,msg) if not b then Print("FAIL ",msg,"\n");QUIT_GAP(1);fi;end;;
CheckCase:=function(st,expected)
 local f,u,v,w,rels,g,iso,h,a,locals,edges,j,refl,eval,k,bad,localf,localg,li,lp,refwords,rows;
 f:=FreeGroup("u","v","w");u:=f.1;v:=f.2;w:=f.3;
 rels:=[u^4,v^4,w^4,(u*v)^2,(v*w)^2,(u*v*w)^2,(u^-1*v)^st[1]*(u*v^-1)^st[2],(v^-1*w)*(v*w^-1)^3];
 g:=f/rels;iso:=IsomorphismPermGroup(g);Need(iso<>fail,"fp permutation isomorphism");Need(IsBijective(iso),"actual fp isomorphism bijective");h:=Image(iso);a:=List(GeneratorsOfGroup(g),x->Image(iso,x));Need(Size(h)=expected,"full fp order");
 Need(ForAll(rels,r->MappedWord(r,[u,v,w],a)=One(h)),"literal relations");
 locals:=[Group(a{[1,2]}),Group(a{[2,3]})];Need(List(locals,Size)=[40,40],"local orders");Need(List(a,Order)=[4,4,4],"type444");
 Need(Size(Intersection(Group(a[1]),Group(a[2])))=1,"first cyclic intersection");Need(Size(Intersection(Group(a[2]),Group(a[3])))=1,"last cyclic intersection");Need(Intersection(locals[1],locals[2])=Group(a[2]),"actual end intersection");
 refl:=[a[1]^-1,a[1]^2*a[2],a[3]];bad:=Filtered([1..Length(rels)],i->MappedWord(rels[i],[u,v,w],refl)<>One(h));Need(Length(bad)>0,"reflection relator fails");
 for k in [st,[1,3]] do
   localf:=FreeGroup("p","q");localg:=localf/[localf.1^4,localf.2^4,(localf.1*localf.2)^2,(localf.1^-1*localf.2)^k[1]*(localf.1*localf.2^-1)^k[2]];
   li:=IsomorphismPermGroup(localg);Need(li<>fail and IsBijective(li),"local fp iso");Need(Size(Image(li))=40,"exact local fp order");
 od;
 rows:=List(a,p->List([1..LargestMovedPoint(h)],i->i^p));
 Print("CASE ",st," ORDER ",Size(h)," DEGREE ",LargestMovedPoint(h)," ORDERS ",List(a,Order)," LOCALS ",List(locals,Size)," END ",Size(Intersection(locals[1],locals[2]))," REFLECTION_FAILS ",bad,"\n");
 Print("GENERATORS ",rows,"\n");
end;;
CheckCase([1,3],2000);;CheckCase([3,1],960);;
Print("PASS_TWO_ORIENTED_AMALGAMATIONS\n");
QUIT_GAP(0);
