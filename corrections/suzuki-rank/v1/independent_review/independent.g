# Independent reconstruction with GAP's native finite fields and ovoid actions.
HCMain:=function()
 local fld,z,one,zero,theta,eta,lam,U,H,involution,J,ident,u,v0,b,h,v,a,c,w,
       K,ovoid,x,y,face1,face2,p1,p2,ab,bc,abc,orders,cyca,cycb,cycc,
       d1,d2,inK,inOther,check,decode,expected,normalizer,P,sx,bullet,
       e,vec,left,right,i,j,g,pp,phi;
 check:=function(ok,msg) if not ok then Error(msg);fi;end;
 fld:=GF(2^15);one:=One(fld);zero:=Zero(fld);theta:=256;
 z:=First(Elements(fld),t->t^15+t+one=zero);
 check(z<>fail and Order(z)=32767,"field root primitive");
 eta:=z^1057;lam:=z^11+z^7+z^6+z^4+z^3+z+one;
 check(Order(eta)=31 and eta^5+eta^3+eta^2+eta+one=zero,"eta");
 check(lam^32<>lam and lam^3+eta^12*lam^2+eta^11*lam+eta=zero,"lambda");
 ident:=IdentityMat(4,fld);J:=Reversed(ident);
 U:=function(x,y)
  return [[one,zero,zero,zero],[x,one,zero,zero],
   [x^(theta+1)+y,x^theta,one,zero],
   [x^(theta+2)+x*y+y^theta,y,x,one]];
 end;
 H:=t->DiagonalMat([t^(theta+1),t,t^-1,t^(-theta-1)]);
 involution:=function(x,y)
  local T;T:=U(x,y);return T^-1*J*U(zero,one)*J*T;
 end;
 u:=involution(eta^2,eta^3);v0:=involution(eta^5,eta^30);
 b:=H(eta);h:=H(lam);v:=h*v0*h^-1;a:=u*b^-1;c:=b^-1*v;w:=a*b*c;
 orders:=List([a,b,c,a*b,b*c,w],Order);check(orders=[31,31,25,2,2,2],"six orders");
 decode:=function(n)
  local ans,j;ans:=zero;j:=0;
  while n>0 do if n mod 2=1 then ans:=ans+z^j;fi;n:=QuoInt(n,2);j:=j+1;od;
  return ans;
 end;
 expected:=rec(
  u:=[[4671,4175,5401,1],[5156,1562,1830,5401],[845,5157,1562,4175],[1131,845,5156,4671]],
  v0:=[[5401,5401,4867,1],[4467,1563,1562,4867],[1131,5717,1563,5401],[624,1131,4467,5401]]);
 check(u=List(expected.u,row->List(row,decode)) and v0=List(expected.v0,row->List(row,decode)),"printed involutions");
 check(eta=decode(624) and lam=decode(2267),"printed field elements");
 for g in [u,v0,b,h,v,a,c,w] do check(TransposedMat(g)*J*g=J,"symplectic");od;
 pp:=[[1,2],[1,3],[2,4],[3,4]];
 phi:=function(g)
  return List(pp,I->List(pp,L->(g[I[1]][L[1]]*g[I[2]][L[2]]+g[I[1]][L[2]]*g[I[2]][L[1]])^128));
 end;
 for g in [u,v0,b,h,v,a,c,w] do check(phi(g)=g,"Suzuki equations");od;
 K:=Elements(GF(32));
 ovoid:=Set(List(Concatenation([[one,zero,zero,zero]],Concatenation(List(K,x->List(K,y->[x^(theta+2)+x*y+y^theta,y,x,one])))),x->OnLines(x,ident)));
 check(Length(ovoid)=1025,"ovoid size");
 face1:=Action(Group([u,b]),ovoid,OnLines);face2:=Action(Group([v0,b]),ovoid,OnLines);
 check(Size(face1)=32^2*(32^2+1)*31 and Size(face2)=Size(face1),"two face group orders");
 check(IsTransitive(face1,[1..1025]) and IsTransitive(face2,[1..1025]),"face transitivity");
 Print("NATIVE_FIELD_ORDERS ",orders,"\n");
 Print("OVOID_SIZE ",Length(ovoid)," FACE_ORDERS ",[Size(face1),Size(face2)],"\n");
 cyca:=List([0..30],j->a^j);cycb:=List([0..30],j->b^j);cycc:=List([0..24],j->c^j);
 check(Intersection(cyca,cycb)=[ident] and Intersection(cycb,cycc)=[ident],"cyclic intersections");
 d1:=Set(Concatenation(cyca,List(cyca,t->t*v)));d2:=Set(Concatenation(cycc,List(cycc,t->t*u)));
 check(Length(d1)=62 and Length(d2)=50 and Intersection(d1,d2)=Set([ident,w]),"dihedral groups");
 inK:=g->ForAll(g,row->ForAll(row,t->t^32=t));inOther:=g->inK(h^-1*g*h);
 check(Set(Filtered(d1,inK))=Set(cyca) and Set(Filtered(d1,inOther))=Set([ident,v]),"first dihedral intersections");
 check(Set(Filtered(d2,inK))=Set([ident,u]) and Set(Filtered(d2,inOther))=Set(cycc),"second dihedral intersections");
 Print("ALL_SMALL_PARABOLIC_INTERSECTIONS_PASS\n");
 normalizer:=List([[8572,0,0,0],[7848,11664,0,0],[30790,2579,18143,0],[24164,14648,27323,22280]],row->List(row,decode));
 check(phi(normalizer)=normalizer and TransposedMat(normalizer)*J*normalizer=J and normalizer^-1*w*normalizer=J,"normalizing conjugation");
 P:=PermutationMat((1,2)(3,4),4,fld);sx:=P*(normalizer^-1*a*normalizer)^-1*P^-1;
 check(sx=TransposedMat(sx) and sx*J*sx=J,"normalized symmetric source element");
 check(sx[1][4]*sx[2][4]+sx[1][2]*sx[4][4]=decode(28331),"source equation13 residual");
 bullet:=function(vv,ww)
  return List([[2,4],[1,2],[3,4],[1,3]],q->(vv[q[1]]*ww[q[2]]+vv[q[2]]*ww[q[1]])^128);
 end;
 for pp in [[1,2],[1,3],[2,4],[3,4]] do
  left:=bullet(List(sx,row->row[pp[1]]),List(sx,row->row[pp[2]]));
  vec:=bullet(ident[pp[1]],ident[pp[2]]);right:=List(sx,row->row*vec);
  check(left=right,"orthogonal pair condition");
 od;
 check(bullet(List(sx,row->row[1]),List(sx,row->row[4]))<>[zero,zero,zero,zero],"nonorthogonal source misuse");
 Print("SOURCE_COORDINATE_DIAGNOSTIC_PASS RESIDUAL_13 28331\n");
 Print("COMPLETE_INDEPENDENT_GAP_RECONSTRUCTION\n");
end;;
HCMain();QUIT;
