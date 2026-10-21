# Independent GAP canonical-field verification. No author program is imported,
# and neither the ambient Suzuki group nor the 2132-element subgroup is listed.
CheckWitness := function()
 local F,o,zz,z,x,roots,decode,mat,M,r,id,U,h,w,theta,i,rows,got,row,
       d,p,lam,exponent,params,g,expected,a,b,c,j;
 F:=GF(2^15); o:=One(F); zz:=Zero(F); x:=Indeterminate(F);
 roots:=RootsOfPolynomial(F,x^15+x+o);
 if Length(roots)<>15 then Error("Polynomial roots"); fi;
 z:=roots[1];
 if Order(z)<>32767 then Error("Primitive field root"); fi;
 decode:=function(k)
  local v,j;
  v:=zz; j:=0;
  while k>0 do
   if k mod 2=1 then v:=v+z^j; fi;
   k:=QuoInt(k,2); j:=j+1;
  od;
  return v;
 end;
 mat:=flat->List([0..3],i->List([1..4],j->decode(flat[4*i+j])));
 id:=IdentityMat(4,F); theta:=256;
 U:=function(a,b)
  return [[o,zz,zz,zz],[a,o,zz,zz],[a^(theta+1)+b,a^theta,o,zz],
          [a^(theta+2)+a*b+b^theta,b,a,o]];
 end;
 h:=t->DiagonalMat([t^(theta+1),t,t^-1,t^(-theta-1)]);
 w:=NullMat(4,4,F); for i in [1..4] do w[i,5-i]:=o; od;
 M:=mat([1,1,1,0,0,0,1,1,0,1,1,1,1,0,0,0]);
 r:=mat([1,0,0,0,1,1,0,0,1,1,1,0,1,0,1,1]);
 if M^4+M+id<>NullMat(4,4,F) or Order(M)<>15 or Order(r)<>4
    or r<>U(o,zz) or M^r<>M^2 then Error("Binary matrix identities"); fi;
 rows:=[
  [3,13,5682,315,[893,0,5682,893,893],
   [892,5454,5454,5455,0,893,1,5454,5455,1,5683,1,1,0,5455,893]],
  [5,41,624,25575,[5992,4671,1131,5992,1831],
   [844,5992,1366,5993,4670,845,4671,1366,1367,4671,1563,1,4671,4670,1367,4467]]
 ];
 got:=[];
 for row in rows do
  d:=row[1];p:=row[2];lam:=decode(row[3]);exponent:=row[4];
  params:=List(row[5],decode); expected:=mat(row[6]);
  if lam^(2^d)<>lam or not ForAll(params,t->t^(2^d)=t)
     or exponent<>(2^(4*d)-1)/p then Error("Subfield data"); fi;
  g:=(M+lam*id)^exponent;
  if g<>expected or Order(g)<>p then Error("Literal matrix and order"); fi;
  if g<>U(params[1],params[2])*h(params[3])*w*U(params[4],params[5])
     then Error("Bruhat membership"); fi;
  Add(got,g);
  Print("FIXED_FIELD degree=",d," order=",p," scalar=",row[3],
        " exponent=",exponent," matrix_and_Bruhat=PASS\n");
 od;
 a:=got[1];b:=got[2];c:=a*b;
 if a*b<>b*a or Order(c)<>533 or c^r<>c^278 then Error("Combined torus"); fi;
 if a^r<>a^5 or b^r<>b^32 then Error("Individual torus actions"); fi;
 if not ForAll([a,b],g->g^2<>id) then Error("Odd orders"); fi;
 Print("FIELD_ROOTS 15 PRIMITIVE_ORDER 32767\n");
 Print("TORUS_ACTIONS 13:5 41:32 533:278\n");
 Print("PASS_INDEPENDENT_L114_WITNESS\n");
end;
CheckWitness();
QUIT_GAP(0);
