# GAP 4: direct finite-field diagnostics only, no group enumeration.
# Each example independently checks every defining field condition and
# the four-by-four middle matrix order, including the nonscalar half-power.
Check := function(b, label)
    if not b then Error(Concatenation("FAIL: ", label)); fi;
end;;

RunDiagnostics := function()
local e,q,field,subfield,delta,n,count,first,a,x,lam,mu,t,tp,k,ii,r1,r2,T,I4,eigenvalues,H,conjugate;
for e in [1..4] do
    q := 9^e;;
    field := GF(q^2);;
    subfield := GF(q);;
    delta := Z(q^2)^((q+1)/2);;
    Check(delta^q=-delta, "trace-zero delta");
    n := (q+1)/2;;
    # Deterministic increasing powers of the canonical primitive element.
    count := 0;; first := fail;;
    for a in [0..q-2] do
        x := Z(q)^a;;
        lam := delta*x;;
        mu := (lam-One(field))/(lam+One(field));;
        if Order(lam^2)=q-1 and Order(mu^2)=n then
            count := count+1;
            if first=fail then first:=a; fi;
        fi;
    od;
    Check(first<>fail, "parameter exists in diagnostic field");
    lam := delta*Z(q)^first;;
    mu := (lam-One(field))/(lam+One(field));;
    t := lam-lam^-1;; tp := mu-mu^-1;; k := -t-tp;;
    Check(t*tp=2*One(field), "Cayley characteristic-three identity");
    Check(k<>Zero(field) and k^q=-k, "nonzero trace-zero k");
    Check(Size(Field([k^2]))=q, "full square field");
    ii := Z(q)^((q-1)/4);;
    r1 := [[1,0,0,0],[0,0,0,1],[0,0,-1,0],[0,1,0,0]]*One(field);;
    r2 := [[0,ii,0,0],[ii,0,0,0],
           [0,0,k,ii-k],[0,0,ii+k,-k]];;
    T := r1*r2;; I4 := IdentityMat(4,field);;
    Check(Order(T)=q^2-1, "matrix order");
    Check(T^((q^2-1)/2)<>I4 and T^((q^2-1)/2)<>-I4,
          "half-power nonscalar");
    eigenvalues := [lam,-lam^-1,mu,-mu^-1];;
    Check(Length(Set(eigenvalues))=4, "four distinct eigenvalues");
    Check(ForAll(eigenvalues,z->DeterminantMat(T-z*I4)=Zero(field)),
          "all asserted eigenvalues");
    H := DiagonalMat([1,-1,1,-1]*One(field));;
    conjugate := List(T,row->List(row,z->z^q));;
    Check(T*H*TransposedMat(conjugate)=H and DeterminantMat(T)=One(field),
          "middle special-unitary matrix");
    Print("PASS e=",e," q=",q," count=",count," first_x_power=",first,
          " k_power=",LogFFE(k,Z(q^2))," order=",Order(T),
          " square_field=",Size(Field([k^2])),"\n");
od;
Print("PASS: four diagnostic fields, all nonzero x counted, all matrix/field checks.\n");
end;;
Print("GAP version: ",GAPInfo.Version,"\n");
RunDiagnostics();
QUIT;
