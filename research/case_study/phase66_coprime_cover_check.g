# Exact integral word-certificate checker; no field sampling is used.
Check:=function(ok,msg) if not ok then Print("FAIL ",msg,"\n");QUIT_GAP(1);fi;end;;
SetInfoLevel(InfoWarning,0);;
Ffree:=FreeGroup("a","b","c");;a:=Ffree.1;;b:=Ffree.2;;c:=Ffree.3;;
mix:=function(A,B)
 local d,e1,e2,s;
 d:=DirectProduct(A.g,B.g);e1:=Embedding(d,1);e2:=Embedding(d,2);
 s:=List([1..3],i->Image(e1,A.s[i])*Image(e2,B.s[i]));
 return rec(g:=Group(s),s:=s);
end;;
terms:=[[-1, [2]], [-1, [3]], [2, [2, 3]], [3, [3, 4]], [-1, [2, 1, 2]], [-2, [2, 1, 3]], [-5, [2, 3, 4]], [2, [3, 2, 1]], [4, [3, 2, 4]], [-3, [3, 4, 3]], [2, [2, 1, 2, 3]], [1, [2, 1, 3, 2]], [4, [2, 1, 3, 4]], [-1, [2, 3, 2, 1]], [-2, [2, 3, 2, 3]], [-2, [2, 3, 2, 4]], [3, [2, 3, 4, 3]], [-1, [3, 2, 1, 2]], [-1, [3, 2, 1, 4]], [-2, [3, 2, 4, 3]], [-2, [3, 4, 3, 2]], [-1, [3, 4, 3, 4]], [-2, [2, 1, 2, 1, 2]], [-1, [2, 1, 2, 1, 3]], [-5, [2, 1, 2, 3, 4]], [-1, [2, 1, 3, 2, 1]], [3, [2, 1, 3, 2, 4]], [-3, [2, 1, 3, 4, 3]], [-1, [2, 3, 2, 3, 4]], [2, [2, 3, 2, 4, 3]], [2, [2, 3, 4, 3, 2]], [-1, [2, 3, 4, 3, 4]], [1, [3, 2, 1, 2, 4]], [-1, [3, 2, 1, 4, 3]], [3, [3, 4, 3, 2, 1]], [1, [3, 4, 3, 2, 4]], [2, [2, 1, 2, 1, 2, 3]], [1, [2, 1, 2, 1, 3, 2]], [1, [2, 1, 2, 1, 3, 4]], [-1, [2, 1, 2, 3, 2, 1]], [-2, [2, 1, 2, 3, 2, 4]], [2, [2, 1, 2, 3, 4, 3]], [-1, [2, 1, 3, 2, 1, 2]], [-1, [2, 1, 3, 2, 1, 4]], [-2, [2, 1, 3, 2, 4, 3]], [-1, [2, 1, 3, 4, 3, 2]], [3, [2, 3, 2, 1, 2, 1]], [1, [2, 3, 2, 3, 4, 3]], [-2, [2, 3, 2, 4, 3, 4]], [1, [2, 3, 4, 3, 2, 4]], [1, [3, 2, 1, 2, 3, 2]], [-1, [3, 2, 1, 3, 2, 3]], [-2, [3, 2, 4, 3, 2, 3]], [-2, [2, 1, 2, 1, 2, 3, 4]], [-2, [2, 1, 2, 1, 3, 2, 1]]];;
run:=function(beta,eps1,eps2)
 local q,rels,fp,iso,p,pm,r,mu,ag,full,et,er,s,g,med,iend,act,dim,zz,perms,bb4,normal4,field,ms,idmat,e0,v,d,total,term,w,j,constraints,mat,sp,zm,sm;
q:=2^beta;;
rels:=[a^8,b^q,c^8,(a*b)^2,(b*c)^2,(a*b*c)^2,b*a^2*(a^2*b^(1+eps1*q/4))^-1,c^2*b*(b^(1+eps2*q/4)*c^2)^-1];;
fp:=Ffree/rels;;iso:=IsomorphismPermGroup(fp);;
p:=rec(g:=Image(iso),s:=List(GeneratorsOfGroup(fp),x->Image(iso,x)));;
pm:=rec(g:=p.g,s:=[p.s[1]^-1,p.s[1]^2*p.s[2],p.s[3]]);;r:=mix(p,pm);;
mu:=GroupHomomorphismByImages(r.g,r.g,r.s,[r.s[1]^-1,r.s[1]^2*r.s[2],r.s[3]]);;
ag:=Group([mu]);;IsGroupOfAutomorphisms(ag);;
full:=SemidirectProduct(ag,r.g);;et:=Embedding(full,1);;er:=Embedding(full,2);;
s:=[Image(et,mu)];;for g in r.s do Add(s,s[Length(s)]*Image(er,g));od;
Print("FULL ",[Size(full),PClassPGroup(full)]," invol ",List(s,Order),"\n");


 Check(Size(p.g)=64*q and Size(full)=256*q,"source and full R orders");
 bb4:=Image(er,r.s[2]^4);normal4:=Group([bb4]);
 Check(Size(normal4)=q/4 and IsNormal(full,normal4),"normal B4");
 Check(bb4^s[1]=bb4^(1+q/8) and bb4^s[2]=bb4^-1 and bb4^s[3]=bb4^-1 and bb4^s[4]=bb4^(1+q/8),"reflection action on B4");
 med:=Group(s{[2,3]});iend:=Intersection(Group(s{[1,2,3]}),Group(s{[2,3,4]}));
 zz:=Image(er,Comm(r.s[3]^2,r.s[2]));
 Check(Size(med)=2*q and Size(iend)=4*q and Group(Concatenation(GeneratorsOfGroup(med),[zz]))=iend and ForAll(GeneratorsOfGroup(med),g->Comm(g,zz)=One(full)),"central index2 end defect");
 act:=ActionHomomorphism(full,RightCosets(full,med),OnRight);dim:=Index(full,med);perms:=List(s,g->Image(act,g));
 Check(dim=128 and Size(Image(act))=1024 and Kernel(act)=normal4,"fixed marked coset quotient");
 field:=Rationals;ms:=List(perms,g->PermutationMat(g,dim,field));idmat:=IdentityMat(dim,field);
 e0:=List([1..dim],i->0);e0[1]:=1;
 Check(ForAll([2,3],i->e0*ms[i]=e0),"identity medial coset");
 v:=e0*(idmat-ms[4])*(idmat-ms[1]);zm:=PermutationMat(Image(act,zz),dim,field);d:=e0*(zm-idmat);
 total:=List([1..dim],i->0);
 for term in terms do
  Check(IsInt(term[1]),"integer coefficient");w:=v;
  for j in term[2] do w:=Permuted(w,perms[j]);od;
  total:=total+term[1]*w;
 od;
 Check(total=2*d and d<>Zero(d),"literal integral orbit identity");
 if beta=5 and eps1=1 and eps2=1 then
  constraints:=[ms[2]-idmat,ms[3]-idmat,(idmat-ms[4])*(idmat-ms[1])];
  mat:=List([1..dim],i->Concatenation(List(constraints,m->m[i])));
  sp:=NullspaceMat(mat);sm:=SmithNormalFormIntegerMat(mat);
  Check(Length(sp)=7 and ForAll(sp,w->w*(zm-idmat)=Zero(w)),"rational nullspace diagnostic");
  Check(Collected(List([1..dim],i->sm[i][i]))=[[0,7],[1,120],[2,1]],"Smith diagnostic");
  Print("SMITH_PASS 0^7 1^120 2^1\n");
 fi;
 Print("INTEGRAL_PASS ",[beta,eps1,eps2]," terms ",Length(terms)," full ",Size(full)," quotient ",Size(Image(act)),"\n");
end;;
for beta in [5,6] do for eps1 in [-1,1] do for eps2 in [-1,1] do run(beta,eps1,eps2);od;od;od;
Print("GAP_VERSION ",GAPInfo.Version,"\n");
Print("PASS COPRIME_INTEGRAL_CERTIFICATE 8\n");
QUIT_GAP(0);
