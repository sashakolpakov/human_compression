# Independently transcribed primary Theorem4.1 tests; finite examples supplement
# the uniform reviewed proof and are not used as an extrapolation in parameters.
Need254:=function(b,s) if not b then Print("PHASE254_REJECT ",s,"\n");QUIT_GAP(2);fi;end;;
Check254:=function(row)
 local ss,tt,dd,l1,l2,nn,F,a,b,c,h,k,rels,U,iso,G,r,I,subs,i,j,target,delmap;
 ss:=row[1];tt:=row[2];dd:=row[3];l1:=row[4];l2:=row[5];nn:=ss+tt+dd;
 F:=FreeGroup("r0","r1","r2");a:=F.1;b:=F.2;c:=F.3;h:=2^ss*l1;k:=2^tt*l2;
 rels:=[a^2,b^2,c^2,(a*b)^h,(b*c)^k,(a*c)^2,Comm((a*b)^4,c),Comm(a,(b*c)^4)];
 if dd mod 2=1 then Add(rels,Comm((a*b)^2,c)^(2^((dd-1)/2)));
 else Add(rels,Comm((a*b)^2,(b*c)^2)^(2^((dd-2)/2)));fi;
 U:=F/rels;iso:=IsomorphismPermGroup(U);G:=Image(iso);r:=List(GeneratorsOfGroup(U),x->Image(iso,x));
 Need254(Size(G)=2^nn*l1*l2 and Order(r[1]*r[2])=h and Order(r[2]*r[3])=k,"literal general odd-factor presentation");
 I:=Combinations([1..3]);subs:=List(I,J->Subgroup(G,r{J}));
 for i in [1..8] do for j in [1..8] do
  Need254(Intersection(subs[i],subs[j])=subs[Position(I,Intersection(I[i],I[j]))],"literal general presentation IP");
 od;od;
 for i in I do
  target:=List([1..3],j->One(G));for j in i do target[j]:=r[j];od;
  delmap:=GroupHomomorphismByImages(G,G,r,target);Need254(delmap<>fail,"all Boolean deletions of literal source presentation");
 od;
 Need254(IsSolvableGroup(G),"solvability");
 Print("P254_SOURCE41 ",row," order=",Size(G)," type=",[h,k]," IP64 deletions8 PASS\n");
end;;
for row in [[2,2,1,5,7],[2,3,2,3,1],[2,2,3,1,5],[3,3,1,5,3],[2,2,4,3,5],[2,2,1,9,3]] do Check254(row);od;
Print("PHASE254_PRESENTATIONS_PASS\n");
QUIT_GAP(0);
