# Acquired frame inverse, for permutations already known to belong to saved G.
F004MatrixCertificateReference:=CertifiesFullEnd;;
F004MatrixPoints:=fail;;F004MatrixBasisIndices:=fail;;F004MatrixFrameIndex:=fail;;
F004MatrixBasis:=fail;;F004MatrixBasisInverse:=fail;;F004MatrixFrameCoefficients:=fail;;
F004InitializeMatrixFrame:=function(path,indices,frameIndex,coefficients)
 local raw,marker,pos,body,ints,F;
 raw:=StringFile(path);marker:="\"points\":";
 pos:=PositionSublist(raw,marker);
 if pos=fail or PositionSublist(raw,marker,pos+1)<>fail or
    raw{[Length(raw)-2..Length(raw)]}<>"]}\n" then Error("exact unique final points array");fi;
 body:=raw{[pos+Length(marker)..Length(raw)-2]};
 if ForAny(body,c->not c in "0123456789,[] \n\r\t") then Error("numeric-list literal only");fi;
 ints:=EvalString(body);
 if not IsList(ints) or not IsDenseList(ints) or Length(ints)<>177156 or
    ForAny(ints,v->not IsList(v) or not IsDenseList(v) or Length(v)<>7 or
      ForAny(v,x->not IsInt(x) or x<0 or x>10)) then Error("exact indexed GF11 points");fi;
 F:=GF(11);F004MatrixPoints:=List(ints,v->List(v,x->x*One(F)));
 if Length(indices)<>7 or Length(Set(indices))<>7 or
    ForAny(indices,i->not IsInt(i) or i<1 or i>177156) or
    not IsInt(frameIndex) or frameIndex<1 or frameIndex>177156 or frameIndex in indices or
    Length(coefficients)<>7 or ForAny(coefficients,x->not IsInt(x) or x<1 or x>10) then
  Error("exact acquired frame metadata");fi;
 F004MatrixBasisIndices:=ShallowCopy(indices);F004MatrixFrameIndex:=frameIndex;
 F004MatrixBasis:=F004MatrixPoints{indices};
 if RankMat(F004MatrixBasis)<>7 then Error("independent actual basis");fi;
 F004MatrixBasisInverse:=Inverse(F004MatrixBasis);
 F004MatrixFrameCoefficients:=List(coefficients,x->x*One(F));
 if F004MatrixFrameCoefficients*F004MatrixBasis<>F004MatrixPoints[frameIndex] then
  Error("actual eighth line coordinates");fi;
end;;
F004MatrixLiftKnown:=function(p)
 local U,d,raw,result;
 U:=List(F004MatrixBasisIndices,i->F004MatrixPoints[i^p]);
 if RankMat(U)<>7 then Error("known-member image basis");fi;
 d:=F004MatrixPoints[F004MatrixFrameIndex^p]*Inverse(U);
 if ForAny(d,x->x=Zero(GF(11))) then Error("known-member frame coefficients");fi;
 raw:=F004MatrixBasisInverse*DiagonalMat(List([1..7],i->d[i]/F004MatrixFrameCoefficients[i]))*U;
 result:=DeterminantMat(raw)^(-3)*raw;
 if DeterminantMat(result)<>One(GF(11)) or
    ForAny(F004MatrixBasisIndices,i->OnLines(F004MatrixPoints[i],result)<>F004MatrixPoints[i^p]) or
    OnLines(F004MatrixPoints[F004MatrixFrameIndex],result)<>F004MatrixPoints[F004MatrixFrameIndex^p] then
  Error("exact known-member frame lift");fi;
 return result;
end;;

F004CertifiesFullEndMatrix:=function(t)
 local a,b,letters,state,word,last,i,k,o,hasFirst,hasSecond,primes;
 if modelName<>"G2_11" then return F004MatrixCertificateReference(t);fi;
 if Length(t)<>3 then Error("exact three-mark end interface");fi;
 t:=List(t,F004MatrixLiftKnown);
 if modelName="G2_7" then primes:=[19,43];
 elif modelName="G2_8" then primes:=[73,19];
 elif modelName="G2_9" then primes:=[13,73];
 elif modelName="G2_11" then primes:=[19,37];
 else return false;fi;
 a:=t[1]*t[2];b:=t[2]*t[3];letters:=[a,a^-1,b,b^-1];
 state:=17;word:=IdentityMat(7,GF(11));last:=0;hasFirst:=false;hasSecond:=false;
 for i in [1..160] do
  state:=(1103515245*state+12345) mod 2147483648;k:=1+((QuoInt(state,65536)) mod 4);
  if (last=1 and k=2) or (last=2 and k=1) or (last=3 and k=4) or (last=4 and k=3) then k:=((k+1) mod 4)+1;fi;
  word:=word*letters[k];last:=k;
  if i mod 4=0 then
   o:=Order(word);certificateTests:=certificateTests+1;
   if o mod primes[1]=0 then hasFirst:=true;fi;
   if o mod primes[2]=0 then hasSecond:=true;fi;
   if hasFirst and hasSecond then certifiedFullEnds:=certifiedFullEnds+1;return true;fi;
  fi;
 od;
 return false;
end;;
