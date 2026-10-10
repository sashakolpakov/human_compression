# Complete finite degree-two/four diagnostic only for beta=5, eps1=eps2=+1.
Check:=function(ok,msg) if not ok then Print("FAIL ",msg,"\n");QUIT_GAP(1);fi;end;;
SetInfoLevel(InfoWarning,0);;
Ffree:=FreeGroup("a","b","c");;a:=Ffree.1;;b:=Ffree.2;;c:=Ffree.3;;
mix:=function(A,B)
 local d,e1,e2,s;
 d:=DirectProduct(A.g,B.g);e1:=Embedding(d,1);e2:=Embedding(d,2);
 s:=List([1..3],i->Image(e1,A.s[i])*Image(e2,B.s[i]));
 return rec(g:=Group(s),s:=s);
end;;
q:=32;;eps1:=1;;eps2:=1;;
rels:=[a^8,b^q,c^8,(a*b)^2,(b*c)^2,(a*b*c)^2,b*a^2*(a^2*b^(1+eps1*q/4))^-1,c^2*b*(b^(1+eps2*q/4)*c^2)^-1];;
fp:=Ffree/rels;;iso:=IsomorphismPermGroup(fp);;
p:=rec(g:=Image(iso),s:=List(GeneratorsOfGroup(fp),x->Image(iso,x)));;
pm:=rec(g:=p.g,s:=[p.s[1]^-1,p.s[1]^2*p.s[2],p.s[3]]);;r:=mix(p,pm);;
mu:=GroupHomomorphismByImages(r.g,r.g,r.s,[r.s[1]^-1,r.s[1]^2*r.s[2],r.s[3]]);;
ag:=Group([mu]);;IsGroupOfAutomorphisms(ag);;
full:=SemidirectProduct(ag,r.g);;et:=Embedding(full,1);;er:=Embedding(full,2);;
s:=[Image(et,mu)];;for g in r.s do Add(s,s[Length(s)]*Image(er,g));od;
Print("FULL ",[Size(full),PClassPGroup(full)]," invol ",List(s,Order),"\n");
free:=FreeGroup("r0","r1","r2","r3");;fs:=GeneratorsOfGroup(free);;
aa:=fs[1]*fs[2];;bb:=fs[2]*fs[3];;cc:=fs[3]*fs[4];;
w1:=bb*aa^2*(aa^2*bb^(1+eps1*q/4))^-1;;
w2:=cc^2*bb*(bb^(1+eps2*q/4)*cc^2)^-1;;
rr:=[aa^8,bb^q,cc^8,w1*w2^-1,w1^2,Comm(w1,aa),Comm(w1,bb),Comm(w1,cc)];;
wr:=List(fs,g->g^2);;
for i in [1..4] do for j in [i+2..4] do Add(wr,Comm(fs[i],fs[j]));od;od;
rfp:=free/Concatenation(wr,rr);;
rmap:=GroupHomomorphismByImages(rfp,full,GeneratorsOfGroup(rfp),s);;
if rmap=fail or not IsSurjective(rmap) then Error("small presentation does not map onto R");fi;
rpq:=EpimorphismQuotientSystem(PQuotient(rfp,2,PClassPGroup(full)+1));;
Print("SMALL_PRESENTATION ",[Length(rr),Sum(List(rr,Length)),Size(Image(rpq)),Size(full)],"\n");
if Size(Image(rpq))<>Size(full) then Error("small presentation p quotient mismatch");fi;
cr:=Concatenation(List(rr,w->w^2),Concatenation(List(rr,w->List(fs,g->Comm(w,g)))));;
Append(cr,List(fs,g->g^2));;
for i in [1..4] do for j in [i+2..4] do if j<=4 then Add(cr,Comm(fs[i],fs[j]));fi;od;od;
cfp:=free/cr;;
Print("CENTRAL_RELS ",Length(cr),"\n");
peq:=EpimorphismQuotientSystem(PQuotient(cfp,2,PClassPGroup(full)+1));;cg:=Image(peq);;cs:=List(GeneratorsOfGroup(cfp),g->Image(peq,g));;
epi:=GroupHomomorphismByImages(cg,full,cs,s);;cl:=Kernel(epi);;
Check(IsSurjective(epi) and Size(cg)=131072 and Size(cl)=16 and IsAbelian(cl) and Exponent(cl)=2 and IsSubgroup(Centre(cg),cl),"central extension");
Print("CENTRAL_COVER ",[Size(cg),Size(cl),IsAbelian(cl),Exponent(cl),IsSubgroup(Centre(cg),cl)],"\n");
ip:=function(gs)
return Intersection(Group(gs{[1,2,3]}),Group(gs{[2,3,4]}))=Group(gs{[2,3]}) and Intersection(Group(gs{[1,2]}),Group(gs{[2,3]}))=Group([gs[2]]) and Intersection(Group(gs{[2,3]}),Group(gs{[3,4]}))=Group([gs[3]]);
end;;
Print("CENTRAL_IP ",ip(cs),"\n");
if Size(cl)<=1024 then
 en:=fail;;maxs:=MaximalSubgroups(cl);;good:=[];;ii:=0;;
 for n in maxs do
  en:=NaturalHomomorphismByNormalSubgroup(cg,n);;ns:=List(cs,g->Image(en,g));;
  if ip(ns) then Add(good,n);fi;
  ii:=ii+1;
 od;
 Check(Length(maxs)=15 and Length(good)=1,"unique double cover");
 Print("DOUBLE_COVERS ",[Length(maxs),Length(good)],"\n");
fi;
alln:=AllSubgroups(cl);;goodall:=[];;
for n in alln do
 en:=NaturalHomomorphismByNormalSubgroup(cg,n);;ns:=List(cs,g->Image(en,g));;
 if ip(ns) then Add(goodall,n);fi;
od;
maxgood:=Filtered(goodall,n->not ForAny(goodall,j->n<>j and IsSubgroup(j,n)));;
Check(Length(alln)=67 and SortedList(List(goodall,Size))=[2,4,4,8] and List(maxgood,Size)=[8],"complete central interval");
Print("ALL_CENTRAL_QUOTIENTS ",[Length(alln),Length(goodall)]," max good kernel sizes ",List(maxgood,Size)," all good ",List(goodall,Size),"\n");

scalarCounts:=[];;
runscalar:=function(signs)
 local cr,w,i,cfp,peq,cg,cs,epi,cl,ls,c4,z,ims,tup,hom,n,ns,ng,en,seen,good,minimal,below,bmap,ker;
 cr:=Concatenation(wr,List(rr,w->w^4));
 for w in rr do for i in [1..4] do Add(cr,w^fs[i]*w^-signs[i]);od;od;
 for w in rr do for i in rr do Add(cr,Comm(w,i));od;od;
 cfp:=free/cr;
 peq:=EpimorphismQuotientSystem(PQuotient(cfp,2,PClassPGroup(full)+2));cg:=Image(peq);cs:=List(GeneratorsOfGroup(cfp),g->Image(peq,g));
 epi:=GroupHomomorphismByImages(cg,full,cs,s);cl:=Kernel(epi);
 Check(IsSurjective(epi) and IsAbelian(cl) and Exponent(cl)<=4,"scalar kernel");
 Check(ForAll(GeneratorsOfGroup(cl),g->ForAll([1..4],i->g^cs[i]=g^signs[i])),"scalar action");
 Print("SCALAR_C4 ",signs," ",[Size(cg),AbelianInvariants(cl)],"\n");
 ls:=IndependentGeneratorsOfAbelianGroup(cl);c4:=CyclicGroup(4);z:=MinimalGeneratingSet(c4)[1];
 ims:=List(ls,g->Filtered(Elements(c4),x->Order(x)<=Order(g)));
 seen:=[];good:=0;minimal:=0;
 for tup in Cartesian(ims) do
  if ForAny(tup,x->Order(x)=4) then
   hom:=GroupHomomorphismByImages(cl,c4,ls,tup);n:=Kernel(hom);
   if not n in seen then
    Add(seen,n);en:=NaturalHomomorphismByNormalSubgroup(cg,n);ns:=List(cs,g->Image(en,g));ng:=Image(en);
    if ip(ns) then
     good:=good+1;
     bmap:=GroupHomomorphismByImages(ng,full,ns,s);ker:=Kernel(bmap);
     below:=NaturalHomomorphismByNormalSubgroup(ng,Subgroup(ng,List(GeneratorsOfGroup(ker),g->g^2)));
     if not ip(List(ns,g->Image(below,g))) then
      minimal:=minimal+1;Print("NEW_MINIMAL_C4 ",signs," ",tup,"\n");
     fi;
    fi;
   fi;
  fi;
 od;
 Add(scalarCounts,[Length(seen),good,minimal]);
 Print("C4_QUOTIENTS ",signs," ",[Length(seen),good,minimal],"\n");
end;;
scalarCounts:=[];;
for signs in Tuples([-1,1],4) do runscalar(signs);od;
Check(scalarCounts=[[0,0,0],[24,0,0],[0,0,0],[8,2,0],[0,0,0],[8,2,0],[0,0,0],[8,4,0],[24,0,0],[8,0,0],[8,2,0],[0,0,0],[8,2,0],[0,0,0],[8,4,0],[0,0,0]],"complete cyclic-four counts");

unipotentCounts:=[];;
rununipotent:=function(bits)
 local cr,w,i,pivot,v,cfp,peq,cg,cs,epi,cl,maxs,ns2,m,n,seen,good,minimal,en,ns,ng,bmap,ker,kn,nn,below;
 pivot:=Position(bits,1);
 cr:=Concatenation(wr,List(rr,w->w^2));
 for w in rr do
  v:=Comm(w,fs[pivot]);
  for i in [1..4] do Add(cr,Comm(w,fs[i])*v^-bits[i]);Add(cr,Comm(v,fs[i]));od;
  Add(cr,v^2);
 od;
 for w in rr do for i in rr do Add(cr,Comm(w,i));od;od;
 cfp:=free/cr;
 peq:=EpimorphismQuotientSystem(PQuotient(cfp,2,PClassPGroup(full)+2));cg:=Image(peq);cs:=List(GeneratorsOfGroup(cfp),g->Image(peq,g));
 epi:=GroupHomomorphismByImages(cg,full,cs,s);cl:=Kernel(epi);
 Check(IsSurjective(epi) and IsAbelian(cl) and Exponent(cl)=2,"unipotent kernel");
 Print("UNIPOTENT_V4 ",bits," ",[Size(cg),Size(cl)],"\n");
 Check(Size(cl)<=256,"complete enumeration size bound");
 seen:=[];good:=0;minimal:=0;
 for m in MaximalSubgroups(cl) do for n in MaximalSubgroups(m) do
  if not n in seen and IsNormal(cg,n) then
   Add(seen,n);en:=NaturalHomomorphismByNormalSubgroup(cg,n);ns:=List(cs,g->Image(en,g));ng:=Image(en);
   bmap:=GroupHomomorphismByImages(ng,full,ns,s);ker:=Kernel(bmap);
   if not IsSubgroup(Centre(ng),ker) and ip(ns) then
    good:=good+1;kn:=Filtered(MaximalSubgroups(ker),nn->IsNormal(ng,nn));
    if Length(kn)<>1 then Error("noncentral V4 has wrong normal line count");fi;
    below:=NaturalHomomorphismByNormalSubgroup(ng,kn[1]);
    if not ip(List(ns,g->Image(below,g))) then minimal:=minimal+1;Print("NEW_MINIMAL_V4 ",bits,"\n");fi;
   fi;
  fi;
 od;od;
 Add(unipotentCounts,[Length(seen),good,minimal]);
 Print("V4_QUOTIENTS ",bits," ",[Length(seen),good,minimal],"\n");
end;;
unipotentCounts:=[];;
for bits in Filtered(Tuples([0,1],4),b->1 in b) do rununipotent(bits);od;
Check(unipotentCounts=[[35,0,0],[43,2,0],[35,0,0],[43,2,0],[35,0,0],[43,0,0],[35,0,0],[35,0,0],[43,3,0],[35,0,0],[43,2,0],[35,0,0],[43,2,0],[35,0,0],[43,0,0]],"complete noncentral V4 counts");

Print("PASS COMPLETE_DEGREE_2_4 beta=5 eps=1,1\n");
QUIT_GAP(0);
