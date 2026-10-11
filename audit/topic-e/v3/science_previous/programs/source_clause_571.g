# Validation of the explicit type (3,5,3) correction at p=571; not a finite proof premise.
Need:=function(b,m) if not b then Error(m);fi;end;
ProjectivePerm:=function(M,F)
 local pts,n,im,v,w,pos;
 pts:=Elements(F);n:=Length(pts);im:=[];
 for pos in [1..n+1] do
  if pos<=n then v:=[pts[pos],One(F)];else v:=[One(F),Zero(F)];fi;
  w:=v*M;
  if IsZero(w[2]) then Add(im,n+1);else Add(im,Position(pts,w[1]/w[2]));fi;
 od;return PermList(im);
end;

Check571:=function()
 local p,F,o,z,root,bval,w,y,x,A,B,C,J,r,ss,sols,pr,ends,whole,tr,disc,sq,matched,mat;
 p:=571;F:=GF(p);o:=One(F);z:=Zero(F);J:=[[z,o],[-o,z]];matched:=0;
 for root in Filtered(Elements(F),v->v^2=5*o) do
  bval:=(-o+root)/2;
  sols:=[];
  for w in Elements(F) do
   y:=First(Elements(F),v->v^2+bval*v+w^2-w+o=z);
   if y<>fail and 2*y+bval<>z then Add(sols,[w,y]);break;fi;
  od;
  Need(Length(sols)=1,"A5 seed");w:=sols[1][1];y:=sols[1][2];x:=y+bval;
  A:=[[w,x],[y,o-w]];B:=A^-1*J;
  for ss in Elements(F) do
   r:=(y-(o-2*w)*ss)/(2*y+bval);C:=[[r,ss],[ss,o-r]];
   if DeterminantMat(C)<>o then continue;fi;
   pr:=List([A,B,C],M->ProjectivePerm(M,F));ends:=[Group(pr{[1,2]}),Group(pr{[2,3]})];whole:=Group(pr);
   Need(List(pr,Order)=[3,5,3],"type");Need(Order(pr[1]*pr[2])=2 and Order(pr[2]*pr[3])=2 and Order(Product(pr))=2,"rotation relations");
   Need(List(ends,Size)=[60,60] and Size(Intersection(ends[1],ends[2]))=5,"A5 ends and exact IP");
   Need(Size(whole)=p*(p^2-1)/2,"whole PSL571 order");
   tr:=TraceMat(A*C)-TraceMat(A)*TraceMat(C)/2;Need(tr<>z,"nonzero reversal obstruction");
   Print("PSL571 ",rec(matrices:=List([A,B,C],M->List(M,row->List(row,Int))),order:=Size(whole),local_orders:=List(ends,Size),intersection:=Size(Intersection(ends[1],ends[2])),trace_obstruction:=Int(tr)),"\n");matched:=matched+1;
  od;
 od;
 Need(matched=2,"two [3,5,3] extensions");Print("PSL571_PASS\n");
end;
Check571();QUIT;
