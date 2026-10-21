# Deterministic exact witnesses for the exhaustive prime-sieve exception list.
# Core GAP finite fields only; no group recognition, random search or database.
SizeScreen([4096,100000]);;
Check := function(condition,label)
 if not condition then Print("FAIL: ",label,"\n");QUIT_GAP(1);fi;
end;;
cases := [5, 13, 17, 25, 29, 37, 41, 49, 53, 61, 73, 89, 97, 101, 109, 113, 121, 125, 137, 149, 157, 169, 173, 181, 193, 197, 229, 233, 241, 257, 269, 277, 281, 289, 293, 313, 317, 337, 349, 353, 361, 373, 389, 397, 401, 409, 421, 433, 449, 457, 461, 509, 521, 529, 541, 557, 569, 593, 601, 613, 617, 625, 641, 653, 661, 673, 677, 701, 709, 733, 757, 761, 769, 773, 797, 809, 821, 829, 841, 853, 857, 877, 881, 929, 937, 941, 953, 961, 977, 997, 1009, 1013, 1021, 1033, 1049, 1061, 1069, 1093, 1097, 1109, 1117, 1129, 1181, 1201, 1217, 1229, 1249, 1277, 1289, 1297, 1301, 1321, 1361, 1369, 1373, 1381, 1409, 1429, 1481, 1489, 1549, 1553, 1597, 1601, 1609, 1613, 1621, 1637, 1669, 1681, 1693, 1709, 1721, 1741, 1777, 1789, 1801, 1849, 1861, 1877, 1889, 1901, 1913, 1933, 1949, 1973, 2029, 2053, 2069, 2081, 2089, 2113, 2129, 2141, 2161, 2197, 2209, 2213, 2221, 2237, 2269, 2281, 2293, 2297, 2309, 2333, 2341, 2357, 2377, 2381, 2389, 2393, 2417, 2437, 2441, 2477, 2521, 2549, 2609, 2617, 2621, 2633, 2677, 2689, 2729, 2741, 2749, 2789, 2801, 2809, 2837, 2857, 2861, 2897, 2909, 2953, 2969, 3001, 3037, 3041, 3049, 3061, 3089, 3109, 3121, 3169, 3181, 3209, 3221, 3229, 3301, 3329, 3361, 3389, 3433, 3449, 3457, 3461, 3469, 3481, 3529, 3541, 3581, 3613, 3697, 3701, 3709, 3721, 3761, 3769, 3821, 3877, 3881, 3989, 4001, 4049, 4093, 4129, 4157, 4201, 4217, 4229, 4241, 4289, 4409, 4421, 4481, 4489, 4549, 4561, 4621, 4649, 4729, 4789, 4817, 4861, 4889, 4957, 4969, 5041, 5081, 5209, 5237, 5281, 5329, 5333, 5381, 5501, 5521, 5641, 5657, 5669, 5741, 5821, 5849, 5881, 5981, 6029, 6089, 6221, 6229, 6257, 6269, 6301, 6329, 6397, 6421, 6449, 6469, 6553, 6577, 6581, 6689, 6709, 6733, 6761, 6833, 6841, 6869, 6889, 6917, 7069, 7129, 7229, 7237, 7253, 7309, 7321, 7349, 7369, 7481, 7489, 7541, 7549, 7561, 7589, 7669, 7741, 7789, 7829, 7853, 7921, 8009, 8093, 8161, 8269, 8329, 8429, 8501, 8513, 8581, 8609, 8669, 8681, 8689, 8741, 8761, 8821, 8849, 8861, 8929, 8969, 9029, 9041, 9049, 9109, 9241, 9281, 9349, 9421, 9461, 9521, 9661, 9689, 9829, 9941, 10009, 10141, 10429, 10529, 10709, 10781, 10789, 10949, 11549, 11593, 11621, 11969, 12409, 12781, 13109, 13397, 13441, 13469, 14029, 14281, 14321, 14629, 14741, 15289, 15401, 15541, 15581, 15641, 15809, 16301, 16421, 16729, 16829, 17029, 17341, 17389, 17401, 17669, 17681, 18061, 18089, 20021, 20201, 20749, 20929, 22441, 22541, 23561, 23869, 43889];;
Run := function(q)
 local p,degree,field,generator,basis,coeffs,delta,d,x,y,g,D,z,mu,t,tp,k,ii,
       a,sign,found,r1,r2,T,I4,H,barT,order,primes,poly,recdata,started;
 started:=Runtime();
 p:=Set(FactorsInt(q))[1];degree:=Length(FactorsInt(q));
 Check(p^degree=q,"prime-power input");
 field:=GF(q^2);generator:=Z(q^2);
 basis:=Basis(field,List([0..2*degree-1],j->generator^j));
 coeffs:=v->List(Coefficients(basis,v),IntFFE);
 poly:=List(CoefficientsOfUnivariatePolynomial(MinimalPolynomial(GF(p),generator)),IntFFE);
 delta:=generator^((q+1)/2); d:=delta^2;
 Check(delta^q=-delta and d^q=d,"quadratic tower");
 found:=false;x:=Zero(field);y:=Zero(field);
 if q=5 then
   k:=generator^3;order:=26;found:=true;
 else
   for a in [0..q-2] do
     x:=Z(q)^a;g:=d*x^2;
     if Order(g)<>q-1 then continue;fi;
     D:=g^2-g+One(field);
     z:=RootFFE(q,D,2);
     if z=fail then continue;fi;
     for sign in [1,-1] do
       y:=(One(field)-g+sign*z)/(d*x);
       mu:=(delta*y-One(field))/(delta*y+One(field));
       if Order(mu^2)=(q+1)/2 then
         t:=delta*x-(delta*x)^-1;tp:=mu-mu^-1;k:=-t-tp;
         Check(t*tp=2*One(field),"pair relation");
         Check(d*x*y^2+2*d*x^2*y-x-2*y=Zero(field),"elliptic curve");
         found:=true;break;
       fi;
     od;
     if found then break;fi;
   od;
   order:=q^2-1;
 fi;
 Check(found,"exception witness found");
 Check(k<>Zero(field) and k^q=-k,"nonzero trace-zero k");
 Check(Size(Field([k^2]))=q,"full square field");
 ii:=Z(q)^((q-1)/4);
 r1:=[[1,0,0,0],[0,0,0,1],[0,0,-1,0],[0,1,0,0]]*One(field);
 r2:=[[0,ii,0,0],[ii,0,0,0],[0,0,k,ii-k],[0,0,ii+k,-k]];
 T:=r1*r2;I4:=IdentityMat(4,field);
 Check(T^order=I4 or (q=5 and T^order=-I4),"matrix exponent modulo center");
 primes:=Set(FactorsInt(order));
 for a in primes do
   Check(T^(order/a)<>I4 and T^(order/a)<>-I4,"exact projective order");
 od;
 H:=DiagonalMat([1,-1,1,-1]*One(field));
 barT:=List(T,row->List(row,v->v^q));
 Check(T*H*TransposedMat(barT)=H and DeterminantMat(T)=One(field),"special unitarity");
 recdata:=[q,p,degree,order,poly,coeffs(delta),coeffs(x),coeffs(y),coeffs(k),coeffs(ii)];
 Print("WITNESS ",recdata,"\n");
 Print("PASS q=",q," runtime_ms=",Runtime()-started,"\n");
end;;
Print("GAP version: ",GAPInfo.Version,"\n");
for q in cases do Run(q);od;
Print("ALL PASS: ",Length(cases)," exhaustive finite-field witnesses.\n");
QUIT;
