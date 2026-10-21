# Exact finite cross-check of the separately proved uniform obstruction.
Check:=function(ok,msg) if not ok then Print("FAIL ",msg,"\n");QUIT_GAP(1);fi;end;;
SetInfoLevel(InfoWarning,0);;
Ffree:=FreeGroup("a","b","c");;a:=Ffree.1;;b:=Ffree.2;;c:=Ffree.3;;
mix:=function(A,B)
 local d,e1,e2,s;
 d:=DirectProduct(A.g,B.g);e1:=Embedding(d,1);e2:=Embedding(d,2);
 s:=List([1..3],i->Image(e1,A.s[i])*Image(e2,B.s[i]));
 return rec(g:=Group(s),s:=s);
end;;
extension:=function(f,s)
 local mu,ag,t,e0,e1,ts,iso;
 mu:=GroupHomomorphismByImages(f,f,s,[s[1]^-1,s[1]^2*s[2]]);
 if mu=fail or not IsBijective(mu) then Error("mirror failed");fi;
 ag:=Group([mu]);if not IsGroupOfAutomorphisms(ag) then Error("not autos");fi;
 t:=SemidirectProduct(ag,f);e0:=Embedding(t,1);e1:=Embedding(t,2);
 ts:=[Image(e1,s[1]),Image(e1,s[2])];
 Add(ts,Image(e0,mu)*ts[1]*ts[2]);
 iso:=IsomorphismPermGroup(t);
 return rec(g:=Image(iso),s:=List(ts,x->Image(iso,x)));
end;;


coextension:=function(v,s)
 local mu,ag,t,e0,e1,ts,iso;
 mu:=GroupHomomorphismByImages(v,v,s,[s[1]^-1,s[1]^2*s[2]]);
 if mu=fail or not IsBijective(mu) then Error("vertex mirror failed");fi;
 ag:=Group([mu]);if not IsGroupOfAutomorphisms(ag) then Error("not autos");fi;
 t:=SemidirectProduct(ag,v);e0:=Embedding(t,1);e1:=Embedding(t,2);
 ts:=[Image(e0,mu),Image(e1,s[1]),Image(e1,s[2])];
 iso:=IsomorphismPermGroup(t);
 return rec(g:=Image(iso),s:=List(ts,x->Image(iso,x)));
end;;
shrink:=function(q,r)
 local e,k,n,f;
 e:=GroupHomomorphismByImages(q.g,r.g,q.s,r.s);k:=Kernel(e);
 n:=Subgroup(q.g,List(GeneratorsOfGroup(k),x->x^2));
 f:=NaturalHomomorphismByNormalSubgroup(q.g,n);
 return rec(g:=Image(f),s:=List(q.s,x->Image(f,x)));
end;;
run:=function(beta,eps1,eps2)
 local q,rels,fp,iso,p,pm,r,t,td,qq,qqd,q0,q0d,h,e,l,k1,k2,yy,zz,w,sub,i,mu,ends,ip,kk,df,hr,lr,n,qn,qnmarks,good,rv1,rv2,x,u,y;
 q:=2^beta;
 rels:=[a^8,b^q,c^8,(a*b)^2,(b*c)^2,(a*b*c)^2,b*a^2*(a^2*b^(1+eps1*q/4))^-1,c^2*b*(b^(1+eps2*q/4)*c^2)^-1];
 fp:=Ffree/rels;iso:=IsomorphismPermGroup(fp);
 p:=rec(g:=Image(iso),s:=List(GeneratorsOfGroup(fp),x->Image(iso,x)));
 pm:=rec(g:=p.g,s:=[p.s[1]^-1,p.s[1]^2*p.s[2],p.s[3]]);r:=mix(p,pm);
 t:=extension(Group(r.s{[1,2]}),r.s{[1,2]});td:=coextension(Group(r.s{[2,3]}),r.s{[2,3]});
 qq:=mix(r,t);qqd:=mix(r,td);q0:=shrink(qq,r);q0d:=shrink(qqd,r);h:=mix(q0,q0d);
 Check(List([p,r,t,qq,q0,q0d,h],x->Size(x.g))=[64*q,128*q,32*q,512*q,256*q,256*q,256*q],"orders and same reduced cover");
 x:=p.s[2]^(q/4);u:=p.s[1]^2;y:=p.s[3]^2;
 Check(x^p.s[1]=x^-1 and x^p.s[3]=x^-1 and u^p.s[2]=u*x^-eps1 and y^p.s[2]=y*x^eps2 and y^p.s[1]=y^-1*x^eps2,"coordinate identities");
 rv1:=q0.s[2]*q0.s[1]^2*(q0.s[1]^2*q0.s[2]^(1+eps1*q/4))^-1;
 rv2:=q0.s[3]^2*q0.s[2]*(q0.s[2]^(1+eps2*q/4)*q0.s[3]^2)^-1;
 Check(Order(rv1)=2 and Order(rv2)=2 and Size(Group([rv1,rv2]))=4 and ForAll(q0.s,g->Comm(rv1,g)=One(q0.g) and Comm(rv2,g)=One(q0.g)),"independent central relators in S");
 Print("PARAM ",[beta,eps1,eps2]," orders P,R,T,Qraw,Q0,Q0d,H ",List([p,r,t,qq,q0,q0d,h],x->Size(x.g)),"\n");
 for i in [r,qq,qqd,q0,q0d,h] do
 e:=GroupHomomorphismByImages(i.g,r.g,i.s,r.s);l:=Kernel(e);
 ends:=[Group(i.s{[1,2]}),Group(i.s{[2,3]})];
 ip:=Intersection(ends[1],ends[2])=Group([i.s[2]]);
 mu:=GroupHomomorphismByImages(i.g,i.g,i.s,[i.s[1]^-1,i.s[1]^2*i.s[2],i.s[3]]);
 Check(mu<>fail and IsBijective(mu),"mirror");
 if i=r then Check(not ip,"R is nonpolytopal");else Check(ip,"cover IP");fi;
 if i=q0 or i=q0d or i=h then Check(Size(l)=2 and ForAll(ends,g->Size(Intersection(g,l))=1),"locally injective double cover");fi;
 Print("ROW ",[Size(i.g),Size(l),StructureDescription(l),IsSubgroup(Centre(i.g),l),List(ends,g->Size(Intersection(g,l))),ip,mu<>fail],"\n");
 od;
 e:=GroupHomomorphismByImages(h.g,r.g,h.s,r.s);l:=Kernel(e);
 sub:=AllSubgroups(l);
 Print("Lsub ",List(sub,n->[Size(n),IsNormal(h.g,n)]),"\n");
 hr:=mix(qq,qqd);e:=GroupHomomorphismByImages(hr.g,r.g,hr.s,r.s);lr:=Kernel(e);
 Check(Size(hr.g)=1024*q and Size(lr)=8 and AbelianInvariants(lr)=[2,4],"raw shared kernel");
 Check(Intersection(Group(hr.s{[1,2]}),Group(hr.s{[2,3]}))=Group([hr.s[2]]),"shared cover IP");
 Print("RAW_H ",[Size(hr.g),StructureDescription(lr),Intersection(Group(hr.s{[1,2]}),Group(hr.s{[2,3]}))=Group([hr.s[2]])],"\n");
 mu:=GroupHomomorphismByImages(hr.g,hr.g,hr.s,[hr.s[1]^-1,hr.s[1]^2*hr.s[2],hr.s[3]]);
 good:=[];
 for n in AllSubgroups(lr) do
  if IsNormal(hr.g,n) and Image(mu,n)=n then
   qn:=NaturalHomomorphismByNormalSubgroup(hr.g,n);qnmarks:=List(hr.s,g->Image(qn,g));
   ip:=Intersection(Group(qnmarks{[1,2]}),Group(qnmarks{[2,3]}))=Group([qnmarks[2]]);
   Print("RAW_NORMAL ",[Size(n),StructureDescription(n),ip],"\n");
   if ip then Add(good,n);fi;
  fi;
 od;
 Check(List(Filtered(good,n->not ForAny(good,j->n<>j and IsSubgroup(j,n))),Size)=[4],"unique maximal admissible raw shared kernel");
 Print("RAW_MAXIMAL_GOOD ",List(Filtered(good,n->not ForAny(good,j->n<>j and IsSubgroup(j,n))),Size),"\n");
 yy:=r.s[3]^2;zz:=Comm(yy,r.s[2]);w:=NormalClosure(r.g,Group([yy]));
 Check(Size(w)=16 and AbelianInvariants(w)=[4,4] and Size(Intersection(w,Group(r.s{[1,2]})))=4 and Order(zz)=4 and zz^2=r.s[2]^(q/2),"normal closure");
 Print("W ",[Size(w),StructureDescription(w),Size(Intersection(w,Group(r.s{[1,2]}))),Order(zz)]," Z2=Bhalf ",zz^2=r.s[2]^(q/2),"\n");
 df:=GroupHomomorphismByImages(r.g,r.g,r.s,List(Reversed(r.s),x->x^-1));
 Print("Rdual ",df<>fail,"\n");
end;;
for beta in [5,6] do for eps1 in [-1,1] do for eps2 in [-1,1] do run(beta,eps1,eps2);od;od;od;
Print("PASS UNIFORM_DIAGNOSTICS 8\n");

QUIT_GAP(0);