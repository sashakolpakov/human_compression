# Independent reviewer control.  No author program or saved field is imported.
# GAP's finite fields and K-vector coordinates replace the author's polynomial
# arithmetic and additive-space partition algorithm.
CheckIndependent := function(n)
    local F,K,z,r,basis,V,bs,one,zero,kl,points,v,p,normalize,lift,
          images,w,j,perm,cycles,fixed,theta,U,h,i,a,b,c,e,t,
          laws,torus,UK,B,T,QT,gens,subfieldfixed,affine,hom,qreport;
    F:=GF(2^n); K:=GF(8); z:=PrimitiveElement(F); r:=n/3;
    one:=One(F); zero:=Zero(F); kl:=AsList(K);
    bs:=List([0..r-1],i->z^i);
    V:=VectorSpace(K,bs); basis:=Basis(V,bs);
    if Dimension(V)<>r then Error("K dimension"); fi;
    normalize:=function(x)
        local k;
        k:=PositionProperty(x,y->y<>zero);
        if k=fail then Error("Zero projective vector"); fi;
        return x/x[k];
    end;
    points:=Filtered(Tuples(kl,r-1),x->
        PositionProperty(x,y->y<>zero)<>fail and
        x[PositionProperty(x,y->y<>zero)]=one);
    Sort(points);
    lift:=x->Sum([1..r-1],i->x[i]*z^i);
    images:=[];
    for v in points do
        w:=Coefficients(basis,lift(v)^2);
        Remove(w,1);
        p:=normalize(w);
        j:=PositionSorted(points,p);
        if j>Length(points) or points[j]<>p then Error("Projective image"); fi;
        Add(images,j);
    od;
    perm:=PermList(images);
    if perm=fail or not IsOne(perm^n) then Error("Frobenius permutation"); fi;
    cycles:=Collected(List(Cycles(perm,[1..Length(points)]),Length));
    fixed:=List([0..n-1],i->Number([1..Length(points)],j->j^(perm^i)=j));
    if n=9 then
        if Length(points)<>9 or cycles<>[[9,1]] or fixed<>Concatenation([9],List([1..8],i->0)) then Error("q512 count"); fi;
    elif n=15 then
        if Length(points)<>585 or cycles<>[[5,3],[15,38]] or fixed<>[585,0,0,0,0,15,0,0,0,0,15,0,0,0,0] then Error("q32768 count"); fi;
    else Error("Unexpected field"); fi;
    theta:=2^((n+1)/2);
    U:=function(a,b)
        return [[one,zero,zero,zero],[a,one,zero,zero],
          [a^(theta+1)+b,a^theta,one,zero],
          [a^(theta+2)+a*b+b^theta,b,a,one]];
    end;
    h:=t->DiagonalMat([t^(theta+1),t,t^-1,t^(-theta-1)]);
    laws:=0; torus:=0;
    for i in [1..128] do
        a:=z^i; b:=z^(i+3); c:=z^(2*i+7); e:=z^(3*i+1);
        if U(a,b)*U(c,e)<>U(a+c,b+e+a*c^theta) then Error("Root multiplication"); fi;
        laws:=laws+1;
        t:=z^(i+2);
        if U(a,b)^h(t)<>U(t^theta*a,t^(theta+2)*b) then Error("Torus conjugation"); fi;
        torus:=torus+1;
    od;
    if Set(List(Filtered(kl,x->x<>zero),t->t^(theta+2)))<>Set(Filtered(kl,x->x<>zero)) then Error("Full scalar image"); fi;
    if not ForAll(kl,a->a^theta=a^4) then Error("Subfield Suzuki exponent"); fi;
    qreport:=rec(n:=n, q:=2^n, quotientDimension:=r-1,
       projectivePoints:=Length(points),cycles:=cycles,fixed:=fixed,
       orbits:=Sum(fixed)/n,rootLaws:=laws,torusLaws:=torus);
    # A small actual matrix action, never an ambient Suzuki enumeration.
    if n=9 then
        UK:=Group(List(Cartesian(kl,kl),ab->U(ab[1],ab[2])));
        B:=ClosureGroup(UK,h(PrimitiveElement(K)));
        QT:=ClosureGroup(B,U(zero,z));
        if Size(UK)<>64 or IsAbelian(UK) or Size(B)<>448 or Size(QT)<>3584 then Error("Actual matrix groups"); fi;
        subfieldfixed:=Filtered(Elements(QT),m->ForAll(m,row->ForAll(row,x->x^8=x)));
        if Length(subfieldfixed)<>448 or Group(subfieldfixed)<>B then Error("Actual field intersection"); fi;
        hom:=ActionHomomorphism(QT,RightCosets(QT,B),OnRight);
        affine:=Image(hom);
        if Size(affine)<>56 or not IsTransitive(affine,[1..8]) or not IsTransitive(Stabilizer(affine,1),[2..8]) then Error("Actual local double transitivity"); fi;
        qreport.matrixOrders:=[Size(UK),Size(B),Size(QT),Size(affine)];
        qreport.subfieldIntersection:=Length(subfieldfixed);
    fi;
    Print("INDEPENDENT_FIELD ",qreport,"\n");
end;
CheckIndependent(9);
CheckIndependent(15);
Print("PASS_INDEPENDENT_L115_FIELDS_AND_MATRICES\n");
QUIT_GAP(0);
