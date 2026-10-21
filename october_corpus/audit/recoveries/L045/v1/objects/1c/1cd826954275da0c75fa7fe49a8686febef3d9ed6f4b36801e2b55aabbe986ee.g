#############################################################################
##
#W  atlasirr.g           GAP 4 package CTblLib                  Thomas Breuer
##
##  This file contains code for writing given irrational character values
##  in terms of the ``atomic irrationalities'' that are defined in the
##  ATLAS of Finite Groups.
##


#############################################################################
##
#F  CTblLib.DescriptionOfRootOfUnity( <root> )
##
##  Differences to the GAP library function 'DescriptionOfRootOfUnity':
##
##  - Return 'fail' if <root> is not a root of unity.
##  - Do not run into an error for example in the case of '-1-2*E(4)', or
##    into an infinite recursion, as for '-E(24)-E(24)^11+E(24)^17+E(24)^19'.
##
CTblLib.DescriptionOfRootOfUnity := function( root )
    local coeffs, n, sum, num, i, val, coeff, g, exp, cand, quot, groot;

    # Handle the trivial cases that 'root' is an integer.
    if root = 1 then
      return [ 1, 1 ];
    elif root = -1 then
      return [ 2, 1 ];
    elif IsRat( root ) then
      return fail;
    fi;

    # Compute the Zumbroich basis coefficients,
    # and number and sum of exponents with nonzero coefficient (mod 'n').
    coeffs:= ExtRepOfObj( root );
    n:= Length( coeffs );
    sum:= 0;
    num:= 0;
    for i in [ 1 .. n ] do
      val:= coeffs[i];
      if val <> 0 then
        sum:= sum + i;
        num:= num + 1;
        coeff:= val;
      fi;
    od;
    sum:= sum - num;

    # 'num' is equal to '1' if and only if 'root' or its negative
    # belongs to the basis.
    # (The coefficient is equal to '-1' if and only if either
    # 'n' is a multiple of $4$ or
    # 'n' is odd and 'root' is a primitive $2 'n'$-th root of unity.)
    if num = 1 then
      if coeff < 0 then
        if n mod 2 = 0 then
          sum:= sum + n/2;
        else
          sum:= 2*sum + n;
          n:= 2*n;
        fi;
      fi;
      if root = E(n)^sum then
        return [ n, sum mod n ];
      else
        return fail;
      fi;
    fi;

    # Let $N$ be 'n' if 'n' is even, and equal to $2 'n'$ otherwise.
    # The exponent is determined modulo $N / \gcd( N, 'num' )$.
    g:= GcdInt( n, num );

    if sum mod g <> 0 then
      return fail;
    fi;

    sum:= sum / num;

    if g = 1 then

      # If 'n' and 'num' are coprime then 'root' is identified up to its sign.
      exp:= sum mod n;
      cand:= E(n)^exp;
      if root <> cand then
        if root = - cand then
          exp:= 2*exp + n;
          n:= 2*n;
        else
          return fail;
        fi;
      fi;

    elif g = 2 then

      # 'n' is even, and again 'root' is determined up to its sign.
      exp:= sum mod ( n / 2 );
      cand:= E(n)^exp;
      if root <> cand then
        if root = - cand then
          exp:= exp + n / 2;
        else
          return fail;
        fi;
      fi;

    else

      # Divide off one of the candidates.
      # The quotient is a 'g'-th or $2 'g'$-th root of unity,
      # which can be identified by recursion.
      exp:= sum mod ( n / g );
      quot:= root * E(n)^(n-exp);
      if 2 * g mod Conductor( quot ) <> 0 then
        return fail;
      fi;
      groot:= CTblLib.DescriptionOfRootOfUnity( quot );
      if n mod 2 = 1 and groot[1] mod 2 = 0 then
        exp:= 2*exp;
        n:= 2*n;
      fi;
      exp:= exp + groot[2] * n / groot[1];
      if root <> E(n)^exp then
        return fail;
      fi;

    fi;

    # Return the result.
    return [ n, exp mod n ];
end;


#############################################################################
##
#F  CTblLib.DetectMultipleOfRootOfUnity( <cyc> )
##
##  The result is 'fail' if <cyc> is not a multiple of a root of unity,
##  and otherwise a string of the form "1", "-1", "i", "-i", "z<n>",
##  "z<n>*<k>", "-z<n>*<k>", "z<n>**", "-z<n>**",
##  for some positive integers <n> and <k>.
##
CTblLib.DetectMultipleOfRootOfUnity := function( cyc )
    local g, descr, n, ATLAS;

    if IsInt( cyc ) then
      return String( cyc );
    fi;

    g:= Gcd( ExtRepOfObj( cyc ) );
    descr:= CTblLib.DescriptionOfRootOfUnity( cyc / g );
    if descr = fail then
      return fail;
    elif descr[1] = 4 then
      if descr[2] = 3 then
        ATLAS:= "-";
      else
        ATLAS:= "";
      fi;
      if g <> 1 then
        Append( ATLAS, String( g ) );
      fi;
      Append( ATLAS, "i" );
      return ATLAS;
    else
      if descr[1] mod 4 = 2 then
        # Reduce to the conductor.
        n:= descr[1] / 2;
        descr:= [ n, ( descr[2] - n ) / 2 mod n ];
        g:= -g;
      elif descr[1] mod 4 = 0 then
        if descr[2] = descr[1] / 2 + 1 then
          # Prefer negative sign to conjugation,
          g:= -g;
          descr:= [ descr[1], 1 ];
        elif descr[2] = descr[1] / 2 - 1 then
          # Prefer complex conjugation.
          g:= -g;
          descr:= [ descr[1], descr[1] - 1 ];
        fi;
      fi;
      if g = 1 then
        ATLAS:= "z";
      elif g = -1 then
        ATLAS:= "-z";
      else
        ATLAS:= Concatenation( String( g ), "z" );
      fi;
      Append( ATLAS, String( descr[1] ) );
      if descr[2] = descr[1] - 1 then
        Append( ATLAS, "**" );
      elif descr[2] <> 1 then
        Append( ATLAS, "*" );
        Append( ATLAS, String( descr[2] ) );
      fi;
      return ATLAS;
    fi;
end;


#############################################################################
##
#F  CTblLib.DetectQuadraticIrrationality( <cyc> )
##
##  This function is similar to the GAP library function 'Quadratic',
##  but the aim is to compute only a string that describes <cyc>,
##  in the format used in the ATLAS of Finite Groups.
##  The main difference to the string computed by 'Quadratic' is that the
##  constant part appears in the end not in the beginning.
##  Besides that, multiples (not arbitrary linear combinations!) of 'b27',
##  'b45' etc. and their conjugates are written as that,
##  and 'z3' is preferred to 'b3'.
##
CTblLib.DetectQuadraticIrrationality := function( cyc )
    local q, ATLAS, sum, ATLAS2, m, k, pos;

    if IsInt( cyc ) then
      return String( cyc );
    fi;

    q:= Quadratic( cyc );
    if not IsRecord( q ) then
      return fail;
    fi;

    if q.d = 2 then
      # Only type 'b' can occur.
      if q.b = 1 then
        ATLAS:= "";
      elif q.b = -1 then
        ATLAS:= "-";
      else
        ATLAS:= ShallowCopy( String( q.b ) );
      fi;
      Append( ATLAS, "b" );
      Append( ATLAS, String( AbsInt( q.root ) ) );
      sum:= q.a + q.b;
      if sum < 0 then
        Append( ATLAS, String( sum / 2 ) );
      elif 0 < sum then
        Append( ATLAS, Concatenation( "+", String( sum / 2 ) ) );
      fi;
    else
      # Choose the shortest expression among types 'b', 'i', 'r'.
      if q.b = 1 then
        ATLAS:= "";
      elif q.b = -1 then
        ATLAS:= "-";
      else
        ATLAS:= ShallowCopy( String( q.b ) );
      fi;
      if 0 < q.root then
        Append( ATLAS, Concatenation( "r", String( q.root ) ) );
      else
        Append( ATLAS, "i" );
        if q.root <> -1 then
          Append( ATLAS, String( - q.root ) );
        fi;
      fi;

      if 0 < q.a then
        Append( ATLAS, "+" );
        Append( ATLAS, String( q.a ) );
      elif q.a < 0 then
        Append( ATLAS, String( q.a ) );
      fi;

      if ( q.root - 1 ) mod 4 = 0 then
        # In this case, also $b_{|'root'|}$ is possible.
        # Note that here the coefficients are never equal to $\pm 1$.
        ATLAS2:= Concatenation( String( 2 * q.b ),
                                "b", String( AbsInt( q.root ) ) );
        sum:= q.a + q.b;
        if 0 < sum then
          Append( ATLAS2, "+" );
          Append( ATLAS2, String( sum ) );
        elif sum < 0 then
          Append( ATLAS2, String( sum ) );
        fi;
        if Length( ATLAS2 ) < Length( ATLAS ) then
          ATLAS:= ATLAS2;
        fi;

      fi;

    fi;

    # Deal with non-squarefree radicands in the $b_N$ case
    # (only multiples of the atomic irrationality and its conjugate).
    # Let $k$, $m$, $n$ be integers such that $m$ and $n$ are odd
    # and $n$ is squarefree.
    # We have
    # $k b_{m^2 n} = k ( -1 + \sqrt{\pm m^2 n} ) / 2
    #              = - k / 2 + k m \sqrt{\pm n} / 2.
    # If this expression equals the given value
    # $( a \pm b \sqrt{\pm n} ) / d$
    # then $a/d = -k/2$ and $\pm b/d = k m/2$ hold.
    # That is, $k = -2a/d$ and $\pm m = -b/a$.
    # So the condition is that $b/a$ is an odd integer;
    # The sign of this integer determines whether $b_{m^2 n}$ or $b_{m^2 n}*$
    # occurs.
    if q.d = 2 or IsBound( ATLAS2 ) then
      if q.a <> 0 then
        m:= q.b / q.a;
        if IsInt( m ) and IsOddInt( m ) then
          k:= -2 * q.a / q.d;
          if k = 1 then
            ATLAS:= Concatenation( "b", String( m^2 * AbsInt( q.root ) ) );
          elif k = -1 then
            ATLAS:= Concatenation( "-b", String( m^2 * AbsInt( q.root ) ) );
          else
            ATLAS:= Concatenation( String( k ), "b",
                        String( m^2 * AbsInt( q.root ) ) );
          fi;
          if 0 < m then
            if q.root < 0 then
              Append( ATLAS, "**" );
            else
              Append( ATLAS, "*" );
            fi;
          fi;
        fi;
      fi;
    fi;

    # Deal with conductor 3 (prefer 'z3' to 'b3').
    if Conductor( cyc ) = 3 then
      pos:= PositionSublist( ATLAS, "b3" );
      if pos <> fail then
        pos:= pos + 2;
        if Length( ATLAS ) < pos or not IsDigitChar( ATLAS[ pos ] ) then
          ATLAS:= ReplacedString( ATLAS, "b3", "z3" );
        fi;
      fi;
    fi;

    return ATLAS;
end;


#############################################################################
##
#F  CTblLib.DetectNonquadraticIrrationality( <cyc> )
##
##  If the conductor $n$, say, of <cyc> is squarefree then the basis of the
##  $n$-th cyclotomic field that consists of all primitive $n$-th roots of
##  unity is optimal for writing <cyc> in terms of those atomic ATLAS
##  irrationalities that arise as orbit sums of primitive $n$-th roots of
##  unity under subgroups of the Galois group $G$ of the $n$-th cyclotomic
##  field.
##  We can list the possible atomic irrationalities involved,
##  by computing the stabilizer of <cyc> in $G$.
##
CTblLib.DetectNonquadraticIrrationality:= function( cyc )
    local n, facts, res, stab, orb, conj, i, img, pos, staborder, coeffs,
          cand, candpos, candval, result, contrib, test, min, max, gcds,
          mingcd, filt, part1, part2, pair, lastcoeff, result2, orders,
          irratname1, irratname2, len, letters, gen, irratname, irrat, basis,
          basisnames, n0, coeffs0, constant, coll, mult, v, u, basis2, f, sf,
          vec, name, isnonreal, first;

    n:= Conductor( cyc );
    facts:= FactorsInt( n );
    res:= PrimeResidues( n );
    stab:= [];
    orb:= [ 1 ];
    conj:= [ cyc ];
    for i in res do
      img:= GaloisCyc( cyc, i );
      pos:= Position( conj, img );
      if pos = fail then
        Add( conj, img );
        orb[ Length( conj ) ]:= i;
      elif pos = 1 then
        Add( stab, i );
      fi;
    od;

    staborder:= Length( stab );
    if staborder = 1 then
      # Compute the coefficients w.r.t. the basis that consists
      # of roots of unity.
      coeffs:= CoeffsCyc( cyc, n );
      cand:= List( [ 0 .. n-1 ], i -> CoeffsCyc( E(n)^i, n ) );
      candpos:= [];
      candval:= List( cand, x -> 1 );
      for i in [ 1 .. Length( cand ) ] do
        pos:= Positions( cand[i], 1 );
        if pos = [] then
          candval[i]:= -1;
          pos:= Positions( cand[i], -1 );
        fi;
        candpos[i]:= [ i-1, pos, candval[i] ];
      od;
      SortParallel( List( candpos, x -> - Length( x[2] ) ), candpos );

      # Successively subtract a root that contributes most.
      result:= 0 * [ 0 .. n-1 ];
      contrib:= [];
      while not IsZero( coeffs ) do
        for i in [ 1 .. Length( candpos ) ] do
          test:= coeffs{ candpos[i][2] };
          min:= Minimum( test );
          if min > 0 then
            min:= min * candpos[i][3];
            Add( contrib, [ candpos[i][1], min ] );
            coeffs:= coeffs - min * cand[ candpos[i][1] + 1 ];
            break;
          else
            max:= Maximum( test );
            if max < 0 then
              max:= max * candpos[i][3];
              Add( contrib, [ candpos[i][1], max ] );
              coeffs:= coeffs - max * cand[ candpos[i][1] + 1 ];
              break;
            fi;
          fi;
        od;
      od;
      Sort( contrib );
      if contrib[1][1] = 0 then
        contrib:= Concatenation( contrib{ [ 2 .. Length( contrib ) ] },
                                 [ contrib[1] ] );
      fi;
      gcds:= List( contrib, x -> GcdInt( x[1], n ) );
      mingcd:= Minimum( gcds );
      filt:= contrib{ Positions( gcds, mingcd ) };

      if mingcd <> 1 then
        # Reduction, rewrite everything from n to n/mingcd.
        part1:= Sum( List( filt, x -> x[2] * E(n)^x[1] ), 0 );
        part2:= cyc - part1;    # is sure nonzero
        part1:= CTblLib.CharacterTableDisplayStringEntry( part1, fail );
        part2:= CTblLib.CharacterTableDisplayStringEntry( part2, fail );
        if part2[1] <> '-' and part1 <> "" then
          return Concatenation( part1, "+", part2 );
        else
          return Concatenation( part1, part2 );
        fi;
      fi;

      # Primitive 'n'-th roots are involved.
      pair:= filt[1];
      if n mod 4 = 0 then
        if pair[1] = n/2 - 1 then
          pair:= [ n-1, -pair[2] ];
        elif pair[1] = n/2 + 1 then
          pair:= [ 1, -pair[2] ];
        fi;
      fi;
      if pair[2] = 1 then
        result:= "z";
      elif pair[2] = -1 then
        result:= "-z";
      else
        result:= Concatenation( String( pair[2] ), "z" );
      fi;
      Append( result, String( n ) );
      if pair[1] = n-1 then
        Append( result, "**" );
      elif pair[1] <> 1 then
        Append( result, "*" );
        Append( result, String( pair[1] ) );
      fi;
      lastcoeff:= pair[2];
      for pair in filt{ [ 2 .. Length( filt ) ] }  do
        if pair[1] = 0 then
          if pair[2] > 0 then
            Add( result, '+' );
          else
            Append( result, String( pair[2] ) );
          fi;
        else
          if pair[2] <> lastcoeff then
            lastcoeff:= pair[2];
            if pair[2] = 1 then
              Add( result, '+' );
            elif pair[2] = -1 then
              Add( result, '-' );
            else
              if 0 < pair[2] then
                Add( result, '+' );
              fi;
              Append( result, String( pair[2] ) );
            fi;
          fi;
          Append( result, "&" );
          Append( result, String( pair[1] ) );
        fi;
      od;
      if filt = contrib then
        return result;
      else
        result2:= CTblLib.CharacterTableDisplayStringEntry(
                      cyc - AtlasIrrationality( result ), fail );
        if result2[1] = '-' then
          return Concatenation( result, result2 );
        else
          return Concatenation( result, "+", result2 );
        fi;
      fi;
    fi;

    # Now we know that 'cyc' lies in a proper subfield.
    # ATLAS irrationalities are defined for cyclic stabilizers of order
    # at most 8 or for the case that 'n' is prime and the quotient of
    # 'n-1' by the order of the stabilizer is at most 8.

    if not ( IsPrimeInt( n ) and ( n-1 ) <= 8 * staborder ) then
      # If the stabilizer is not cyclic of order at most 8
      # then switch to an appropriate subgroup.
      orders:= List( stab, x -> OrderMod( x, n ) );
      if not staborder in orders then
        staborder:= Maximum( orders );
      fi;
    fi;

    # Find an appropriate atomic irrationality.
    # Prefer c13 to w13, e31 to u31, c19 to u19,
    # but prefer y7 to c7, y11 to e11, y13 to f13, y17 to h17.
    irratname1:= fail;
    irratname2:= fail;
    if IsPrimeInt( n ) and ( n-1 ) <= 8 * staborder then
      # One of the irrationalities $b_n, \ldots, h_n$.
      len:= ( n - 1 ) / staborder;
      if len <= 8 then
        letters:= [ "", "b", "c", "d", "e", "f", "g", "h" ];
        irratname1:= letters[ len ];
      fi;
    fi;
    if staborder <= 8 then
      # One of the irrationalities $s_n, \ldots, y_n$, perhaps with dashes.
      letters:= [ "z", "y", "x", "w", "v", "u", "t", "s" ];
      irratname2:= ShallowCopy( letters[ staborder ] );
      if not IsBound( orders ) then
        orders:= List( stab, x -> OrderMod( x, n ) );
      fi;
      gen:= stab{ Positions( orders, staborder ) };
      gen:= Set( [ gen[1], gen[ Length( gen ) ] ] );
      i:= 1;
      repeat
        if i in gen then
          break;
        elif OrderMod( i, n ) = staborder then
          Add( irratname2, '\'' );
        fi;
        if n - i in gen then
          break;
        elif OrderMod( n - i, n ) = staborder then
          Add( irratname2, '\'' );
        fi;
        i:= i + 1;
      until false;
      irratname2:= ReplacedString( irratname2, "''", "\"" );
    fi;
    if irratname1 = fail then
      if irratname2 = fail then
        # We have no good idea.
        irratname:= "z";
      else
        irratname:= irratname2;
      fi;
    elif irratname2 = fail then
      irratname:= irratname1;
    else
      if irratname2 = "y" then
        irratname:= irratname2;
      else
        irratname:= irratname1;
      fi;
    fi;
    irratname:= Concatenation( irratname, String( n ) );

    # Compute the conjugates of the atomic irrationality.
    # (In general they are not linearly independent.)
    irrat:= AtlasIrrationality( irratname );
    basis:= [ irrat ];
    basisnames:= [ 1 ];
    for i in res do
      conj:= GaloisCyc( irrat, i );
      if not conj in basis then
        Add( basis, conj );
        Add( basisnames, i );
      fi;
    od;

    # Reduce the nonzero coefficients by subtracting an integer from 'cyc'.
    coeffs:= ExtRepOfObj( cyc );
    if Length( facts ) <> Length( Set( facts ) ) then
      # Let n0 denote the odd squarefree part of the conductor.
      # If the coefficients of the n0-th roots of unity are all the same
      # then this is the constant to extract.
      n0:= Product( Set( facts ) );
      if n0 mod 2 = 0 then
        n0:= n0 / 2;
      fi;
      coeffs0:= 0 * [ 1 .. n0 ];
      coeffs0{ PrimeResidues( n0 ) + 1 }:= coeffs{
          PrimeResidues( n0 ) * ( n / n0 ) + 1 };
      constant:= CycList( coeffs0 );
    else
      # 'n' is squarefree (and odd).
      # Shift by a constant such that zero is the coefficient with the
      # maximal multiplicity.
      # If all coefficients have the same multiplicity then shift
      # such that zero occurs as the coefficient of the last basis vector.
      coll:= Collected( coeffs{ res } );
      mult:= List( coll, x -> x[2] );
      max:= Maximum( mult );
      if ForAll( coll, pair -> pair[2] = max ) then
        constant:= coeffs[ basisnames[ Length( basisnames ) ] + 1 ];
      else
        # If possible then choose the constant such that the coefficient
        # of 'E(n)' becomes nonzero.
        pos:= Positions( mult, max );
        if Length( pos ) = 1 then
          # There is no choice.
          constant:= coll[ pos[1] ][1];
        elif coeffs[2] = coll[ pos[1] ][1] then
          constant:= coll[ pos[2] ][1];
        else
          constant:= coll[ pos[1] ][1];
        fi;
      fi;
      if Length( Factors( n ) ) mod 2 = 1 then
        constant:= - constant;
      fi;
    fi;
    cyc:= cyc - constant;
    coeffs:= ExtRepOfObj( cyc );

    # Try to compute the coefficients w.r.t. the conjugates.
    v:= VectorSpace( Rationals, basis );
    if Dimension( v ) = Length( basis ) then
      basis2:= basis;
      basis:= BasisNC( v, basis );
    else
      u:= TrivialSubspace( v );
      basis2:= [];
      for i in [ 1 .. Length( basis ) ] do
        cand:= basis[i];
        if cand in u then
          Unbind( basisnames[i] );
        else
          Add( basis2, cand );
          u:= Subspace( v, basis2 );
        fi;
      od;
      basisnames:= Compacted( basisnames );
      basis:= BasisNC( v, basis2 );
    fi;
    coeffs:= Coefficients( basis, cyc );
    if coeffs = fail then
      # The irrationality is not in the linear span of the conjugates
      # of the chosen atomic irrationality.
      # We extend the given basis by roots of unity in smaller
      # cyclotomic fields, and split the irrationality accordingly.
      # Then we recurse.
      f:= Field( Rationals, basis2 );
      u:= v;
      for sf in Difference( Subfields( f ), [ f ] ) do
        for vec in Basis( sf ) do
          if not vec in u then
            Add( basis2, vec );
            u:= Subspace( f, basis2 );

#T not true:
#T f may be too small!

          fi;
        od;
      od;
      basis:= BasisNC( f, basis2 );
      coeffs:= Coefficients( basis, cyc );
      if coeffs = fail then
        Error( "cannot identify irrational value <cyc>" );
      fi;

      part1:= coeffs{ [ 1 .. Length( basisnames ) ] }
              * basis2{ [ 1 .. Length( basisnames ) ] };
      part2:= cyc - part1;    # is sure nonzero
      part1:= CTblLib.CharacterTableDisplayStringEntry( part1, fail );
      part2:= CTblLib.CharacterTableDisplayStringEntry( part2, fail );
      if part2[1] <> '-' and part1 <> "" then
        return Concatenation( part1, "+", part2 );
      else
        return Concatenation( part1, part2 );
      fi;
    fi;

    # Compute the ATLAS description.
    name:= "";
    isnonreal:= ( cyc <> GaloisCyc( cyc, -1 ) );
    first:= true;
    for i in [ 1 .. Length( coeffs ) ] do
      if coeffs[i] <> 0 then
        if coeffs[i] > 0 and name <> "" then
          Add( name, '+' );
        fi;
        if coeffs[i] = -1 then
          Append( name, "-" );
        elif coeffs[i] <> 1 then
          Append( name, String( coeffs[i] ) );
        fi;
        if first then
          Append( name, irratname );
          first:= false;
          if i <> 1 then
            if isnonreal and GaloisCyc( basis[1], -1 ) = basis[i] then
              # Prefer ** if applicable.
              Append( name, "**" );
            else
              Append( name, "*" );
              Append( name, String( basisnames[i] ) );
            fi;
          fi;
        else
          Add( name, '&' );
          Append( name, String( basisnames[i] ) );
        fi;
      fi;
    od;
    if constant <> 0 then
      if IsInt( constant ) then
        if constant > 0 then
          Add( name, '+' );
        fi;
        Append( name, String( constant ) );
      else
        Append( name, CTblLib.DetectNonquadraticIrrationality( constant ) );
      fi;
    fi;

    return name;
end;


#############################################################################
##
#V  CTblLib.IrrationalityMapping
##
##  Note that all attempts to convert an irrational character value from an
##  ATLAS table to a description in terms of atomic ATLAS irrationalities
##  can yield only some heuristics, with various exceptions.
##
##  - Multiples of roots of unity are not always shown as such.
##    For example, '-z3' is shown as 'z3**+1'.
##  - There is in general no unique notation for quadratic irrationalities.
##    For example, '-b27**' occurs in the table of U6(2).3 and is equal to
##    '3z3+2', which occurs in the table of 3.U6(2).3.
##  - Several atomic irrationalities can describe the same value.
##    For example, 'd13' equals 'x13' and 'f19' equals 'x19', all four
##    expressions occur in the ATLAS.
##  - The relative description of Galois conjugates is not uniform.
##    For example, both 'y7*3' and 'y7*4' occur in the ATLAS.
##
##  What follows is the list of exceptions for the heuristics that is given
##  by 'CTblLib.CharacterTableDisplayStringEntry'.
##
CTblLib.IrrationalityMapping := [
  # multiples of roots of unity
  [ "-z3", "z3**+1", "L3(4)" ],
  [ "z3**", "-z3-1", "3.L3(7).3", "U3(11)", "3.U3(5).3" ],
  [ "-z3**", "z3+1", "3.L3(7).3", "U3(11)", "3.U3(5).3" ],
  [ "2z3**", "-i3-1", "3.U3(5).3" ],
  [ "2z3**", "-2z3-2", "U3(11)" ],
  [ "-2z3**", "i3+1", "3.L3(7).3" ],
  [ "-2z3**", "2z3+2", "U3(11)" ],
  [ "4z3", "2i3-2", "3.Suz" ],
  [ "-4z3", "-2i3+2", "3.Suz" ],
  [ "4z3**", "-2i3-2", "3.Suz" ],
  [ "-4z3**", "2i3+2", "3.Suz" ],
  [ "8z3", "4i3-4", "3.Suz", "6.Suz" ],
  [ "-8z3", "-4i3+4", "3.Suz", "6.Suz" ],
  [ "8z3**", "-4i3-4", "3.Suz", "6.Suz" ],
  [ "-8z3**", "4i3+4", "3.Suz", "6.Suz" ],

  # other quadratic irrationalities of type b<n>
  # with not squarefree <n>
  [ "-b27**", "3z3+2", "U6(2)" ],
  [ "3b27**", "-9z3-6", "U6(2)" ],
  [ "-3b27**", "9z3+6", "U6(2)" ],
  [ "-4b27**", "6i3+2", "U6(2)" ],
  [ "-6b27", "-9i3+3", "S6(3)", "2.S6(3)" ],
  [ "-20b27", "-30i3+10", "S6(3)", "2.S6(3)" ],
  [ "-20b27**", "30i3+10", "S6(3)", "2.S6(3)" ],
  [ "-6b27**", "9i3+3", "S6(3)", "2.S6(3)" ],
  [ "270b27", "405i3-135", "S6(3)", "2.S6(3)" ],
  [ "-270b27", "-405i3+135", "S6(3)" ],
  [ "270b27**", "-405i3-135", "S6(3)", "2.S6(3)" ],
  [ "-270b27**", "405i3+135", "S6(3)" ],
  [ "-495b27**", "1485z3+990", "O10-(2)", "S6(3)" ],
  [ "-495b27", "-1485z3-495", "O10-(2)", "S6(3)" ],
  [ "b45", "3b5+1", "U3(9)" ],
  [ "b45*", "-3b5-2", "U3(9)" ],
  [ "-b45", "-3b5-1", "O8-(2)", "ON" ],
  [ "-b45*", "2+3b5", "A14" ],
  [ "-b45*", "3b5+2", "O8-(2)", "ON", "O8-(3)" ],
  [ "2b45", "3r5-1", "O8-(3)" ],
  [ "-2b45", "-3r5+1", "2.J2", "O8-(3)", "S4(5)" ],
  [ "2b45*", "-3r5-1", "O8-(3)" ],
  [ "-2b45*", "3r5+1", "2.J2", "O8-(3)", "S4(5)" ],
  [ "b63", "3b7+1", "O10+(2)" ],
  [ "b63**", "-3b7-2", "O10+(2)" ],
  [ "b75", "5z3+2", "G2(5)", "O10-(2)", "2.S6(3)", "U6(2)" ],
  [ "b75**", "-5z3-3", "G2(5)", "O10-(2)", "2.S6(3)", "U6(2)" ],
  [ "-b75", "-5z3-2", "O10-(2)" ],
  [ "-b75**", "5z3+3", "O10-(2)" ],
  [ "2b75", "5i3-1", "O10-(2)", "U6(2)" ],
  [ "2b75**", "-5i3-1", "O10-(2)", "U6(2)" ],
  [ "3b75", "15z3+6", "U6(2)" ],
  [ "3b75**", "-15z3-9", "U6(2)" ],
  [ "4b75**", "-10i3-2", "U6(2)" ],
  [ "5b75", "25z3+10", "O10-(2)" ],
  [ "5b75**", "-25z3-15", "O10-(2)" ],
  [ "-5b75", "-25z3-10", "S6(3)" ],
  [ "-5b75**", "25z3+15", "S6(3)" ],
  [ "-12b75", "-30i3+6", "O10-(2)", "S6(3)" ],
  [ "-12b75**", "30i3+6", "O10-(2)", "S6(3)" ],
  [ "b125", "5b5+2", "2.S4(5)" ],
  [ "b125*", "5b5*+2", "2.S4(5)" ],
  [ "-b125", "5b5*+3", "HN", "S4(5)" ],
  [ "-b125*", "5b5+3", "HN", "S4(5)" ],
  [ "-5b125", "25b5*+15", "HN", "S4(5)" ],
  [ "-5b125*", "25b5+15", "HN", "S4(5)" ],
  [ "5b125", "25b5+10", "2.S4(5)" ],
  [ "5b125*", "25b5*+10", "2.S4(5)" ],
  [ "-b135**", "3b15+2", "O10+(2)" ],
  [ "-b135", "-3b15-1", "O10+(2)" ],
  [ "3b135", "9b15+3", "O10+(2)" ],
  [ "b147", "7z3+3", "U5(2)", "U6(2)" ],
  [ "b147**", "-7z3-4", "U5(2)", "U6(2)" ],
  [ "10b147", "35i3-5", "U6(2)" ],
  [ "10b147**", "-35i3-5", "U6(2)" ],
  [ "b243", "9z3+4", "S6(3)" ],
  [ "-b243", "-9z3-4", "2.S6(3)" ],
  [ "b243**", "-9z3-5", "S6(3)" ],
  [ "-b243**", "9z3+5", "2.S6(3)" ],
  [ "2b243**", "-9i3-1", "U6(2)" ],
  [ "-6b243", "-27i3+3", "U5(2)" ],
  [ "-6b243**", "27i3+3", "U5(2)" ],
  [ "30b243", "135i3-15", "2.S6(3)" ],
  [ "-30b243", "-135i3+15", "S6(3)" ],
  [ "-30b243**", "135i3+15", "S6(3)" ],
  [ "30b243**", "-135i3-15", "2.S6(3)" ],
  [ "-55b243", "-495z3-220", "O10-(2)" ],
  [ "-55b243**", "495z3+275", "O10-(2)" ],
  [ "81b243", "729z3+324", "S6(3)" ],
  [ "81b243**", "-729z3-405", "S6(3)" ],
  [ "-81b243", "-729z3-324", "2.S6(3)" ],
  [ "-81b243**", "729z3+405", "2.S6(3)" ],
  [ "b363", "11z3+5", "O10-(2)" ],
  [ "b363**", "-11z3-6", "O10-(2)" ],
  [ "-2b363", "-11i3+1", "O10-(2)" ],
  [ "-2b363**", "11i3+1", "O10-(2)" ],
  [ "-6b363", "-33i3+3", "O10-(2)" ],
  [ "-6b363**", "33i3+3", "O10-(2)" ],
  [ "b507", "13z3+6", "O10-(2)", "U6(2)" ],
  [ "b507**", "-13z3-7", "O10-(2)", "U6(2)" ],
  [ "b675", "15z3+7", "O10-(2)", "2.S6(3)" ],
  [ "b675**", "-15z3-8", "O10-(2)", "2.S6(3)" ],
  [ "-b675", "-15z3-7", "S6(3)" ],
  [ "-b675**", "15z3+8", "S6(3)" ],

  # other quadratic irrationalities
  [ "z3+2", "-z3**+1", "3_1.U4(3)", "6_1.U4(3)", "12_1.U4(3)" ],
  [ "15r5+18", "-30b5*+3", "2.S4(5)" ],
  [ "i3-10", "2z3-9", "S6(3)", "2.S6(3)" ],
  [ "i3+10", "-2z3**+9", "2.S6(3)" ],
  [ "2i3+10", "-4z3**+8", "2.S6(3)" ],
  [ "-i3+10", "-2z3+9", "S6(3)", "2.S6(3)" ],
  [ "3z3+11", "-3z3**+8", "S6(3)" ], # force the partner to be shown
  [ "9z3+14", "-9z3**+5", "S6(3)" ], # force the partner to be shown
  [ "27z3+21", "-27z3**-6", "S6(3)", "2.S6(3)" ], # force the partner to be shown
  [ "21z3+19", "-21z3**-2", "2.S6(3)" ], # force the partner to be shown
  [ "55z3+60", "-55z3**+5", "2.S6(3)" ], # force the partner to be shown
  [ "13i3+17", "-26z3**+4", "2.S6(3)" ], # force the partner to be shown
  [ "15i3+17", "-30z3**+2", "2.S6(3)" ], # force the partner to be shown
  [ "3i3+11", "-6z3**+8", "2.S6(3)" ], # force the partner to be shown
  [ "288i3+208", "-576z3**-80", "S6(3)", "2.S6(3)" ], # force the partner to be shown
  [ "270i3+234", "-540z3**-36", "S6(3)" ], # force the partner to be shown
  [ "135z3+150", "-135z3**+15", "S6(3)" ], # force the partner to be shown
  [ "45i3+50", "-90z3**+5", "S6(3)" ], # force the partner to be shown
  [ "30z3+5", "15i3-10", "U5(2)" ],
  [ "-60z3-6", "-30i3+24", "U6(2)" ],
  [ "2r5-1", "4b5+1", "S4(4)" ],
  [ "2i2", "i8", "2.A13" ],
  [ "-2i2", "-i8", "2.A13" ],
  [ "3z3+10", "-3z3**+7", "U5(2)" ],  # force the partner to be shown
  [ "9z3+18", "-9z3**+9", "O10-(2)" ], # force the partner to be shown
  [ "15z3+11", "-15z3**-4", "O10-(2)" ], # force the partner to be shown
  [ "15z3+23", "-15z3**+8", "2.S6(3)" ], # force the partner to be shown

  # non-quadratic irrationalities
  [ "d13-&4", "k13", "2.S6(3).2" ],
  [ "u\"52", "k'52", "2.O7(3).2" ],
  [ "u\"\"56", "k56", "ON.2" ],
  [ "-u\"\"56", "-k56", "2.O7(3).2" ],
  [ "y13-&5", "l13", "2.S4(5).2" ],
  [ "d13", "x13", "L3(9)", "L3(9).2_2" ],
  [ "f19", "x19", "L3(7)", "L3(7).3", "3.L3(7)" ],
  [ "-f19", "-x19", "U3(8)" ],
  [ "m5+&3", "m5&3", "2.HS.2" ],
  [ "2y7+&3", "2y7+&4", "3D4(2)" ],
  [ "6y7-3&3", "6y7-3&4", "3D4(2)" ],
  [ "8y7+3&3", "8y7+3&4", "3D4(2)" ],
  [ "y7+3&3", "y7+3&4", "3D4(2)" ],
  [ "y7-&3", "y7-&4", "3D4(2)" ],
  [ "2y9+&2", "y9-&4", "3D4(2)", "J3" ],
  [ "y16", "-y16*7", "L2(31)" ], # force another conjugate
# [ "y16*3", "y16*13", "2.A6.2_2" ],  # does not help ...
  [ "y'16", "m16", "L2(49)", "L2(81)", "L3(7)", "L3(7).3", "3.L3(7)", "3.L3(7).3", "U3(9)" ],
  [ "y'20", "m20", "L3(9)", "U3(11)", "U3(11).3", "3.U3(11)", "3.U3(11).3" ],
  [ "y\"\"40", "m'40", "U3(11)", "U3(11).3", "3.U3(11)", "3.U3(11).3" ],
  [ "y\"63*13", "y\"63*22", "U3(8)" ],
  [ "-y\"63-&13", "y\"63*43", "U3(8)" ],
  [ "z5&3", "z5+z5*3", "U3(4)" ],  # force another conjugate
  [ "3z5+4&3", "3z5+4z5*3", "U3(4)" ],  # force another conjugate
  [ "z9*2-&8", "-z9**+&2", "U3(8)" ],
  [ "-z9*2+&8", "z9**-&2", "U3(8)" ],
  [ "-z9*5+&8", "z9**-&5", "R(27)", "U3(8)" ],
  [ "-7z9*2+&8", "z9**-7&2", "U3(8)" ],
  [ "-7z9*5+&8", "z9**-7&5", "U3(8)" ],
  [ "-z9+&4", "z9*4-&1", "U3(8)" ],
  [ "-7z9+&4", "z9*4-7&1", "U3(8)" ],
  [ "-z9*4+&7", "z9*7-&4", "U3(8)" ],
  [ "-7z9+&7", "z9*7-7&1", "U3(8)" ],
  [ "-7z9*4+&7", "z9*7-7&4", "U3(8)" ],
  [ "-7z9+7&7", "7z9*7-7&1", "U3(8)" ],
  [ "z12-2&5-z3", "3z12-2i-z3", "U3(11)" ],
  [ "-z12+2&5-z3", "-3z12+2i-z3", "U3(11)" ],
  [ "10z12-20i+10z3**", "5r3-15i-5i3-5", "U3(11)" ],
  [ "-10z12+20i+10z3**", "-5r3+15i-5i3-5", "U3(11)" ],
];


#############################################################################
##
#F  CTblLib.StringOfAtlasIrrationality( <cyc> )
##
##  <#GAPDoc Label="CTblLib.StringOfAtlasIrrationality">
##  <ManSection>
##  <Func Name="CTblLib.StringOfAtlasIrrationality" Arg='cyc'/>
##
##  <Returns>
##  a string that describes the cyclotomic integer <A>cyc</A>.
##  </Returns>
##
##  <Description>
##  This function is intended for expressing the cyclotomic integer
##  <A>cyc</A> as a linear combination of so-called
##  <Q>atomic &ATLAS; irrationalities</Q>
##  (see <Cite Key="CCN85" Where="p. xxvii"/>), with integer coefficients.
##  <P/>
##  Often there is no <Q>optimal</Q> expression of that kind for <A>cyc</A>,
##  and this function uses certain heuristics for finding a not too bad
##  expression.
##  Concerning the character tables in the &ATLAS; of Finite Groups
##  <Cite Key="CCN85"/>, an explicit mapping between the values which are
##  computed by this function and the descriptions that are shown in the book
##  is available, see <C>CTblLib.IrrationalityMapping</C>.
##  Such a mapping is not yet available for the character tables from the
##  &ATLAS; of Brauer Characters <Cite Key="JLPW95"/>,
##  <E>this function is only experimental</E> for these tables,
##  it is likely to be changed in the future.
##  <P/>
##  <Ref Func="CTblLib.StringOfAtlasIrrationality"/> is used by
##  <Ref Func="BrowseAtlasTable"/>.
##  <P/>
##  <Example><![CDATA[
##  gap> values:= List( [ "e31", "y'24+3", "r2+i", "r2+i2" ],
##  >                   AtlasIrrationality );;
##  gap> List( values, CTblLib.StringOfAtlasIrrationality );
##  [ "e31", "y'24+3", "z8-&3+i", "2z8" ]
##  ]]></Example>
##  <P/>
##  The implementation uses the following heuristics for computing
##  a description of the cyclotomic integer <A>cyc</A>
##  with conductor <M>N</M>, say.
##  <P/>
##  <List>
##    <Item>
##      If <M>N</M> is not squarefree the let <M>N_0</M> be
##      the squarefree part of <M>N</M>,
##      split <A>cyc</A> into the sum of its odd squarefree part and its
##      non-squarefree part, and consider the two values separately;
##      note that the odd squarefree part is well-defined by the fact that
##      the basis of the <M>N</M>-th cyclotomic field given by
##      <Ref Func="ZumbroichBase" BookName="ref"/> contains all primitive
##      <M>N_0</M>-th roots of unity.
##      Also note that except for quadratic irrationalities (where <M>N</M>
##      is squarefree), all roots of unity that are involved in the
##      representation of atomic irrationalities
##      w.&nbsp;r.&nbsp;t.&nbsp;this basis have the same multiplicative
##      order.
##    </Item>
##    <Item>
##      If <A>cyc</A> is a multiple of a root of unity then write it as such,
##      i. e., as a string involving <M>z_N</M>.
##    </Item>
##    <Item>
##      Otherwise, if <A>cyc</A> lies in a quadratic number field
##      then write it as a linear combination of an integer.
##      Usually the string involves <M>r_N</M>, <M>i_N</M>, or <M>b_N</M>,
##      but also multiples of <M>b_M</M> may occur, where <M>M</M> is a
##      &ndash;not squarefree&ndash; multiple of <M>N</M>.
##    </Item>
##    <Item>
##      Otherwise, find a large cyclic subgroup of the stabilizer of
##      <A>cyc</A> inside the Galois group over the Rationals
##      &ndash;this subgroup defines an atomic irrationality&ndash;
##      and express <A>cyc</A> as a linear combination of the orbit sums.
##      In the worst case, there is no nontrivial stabilizer, and we find
##      only a description as a sum of roots of unity.
##    </Item>
##  </List>
##  <P/>
##  There is of course a lot of space for improvements.
##  For example, one could use the Bosma basis representation
##  (see <Ref Func="BosmaBase"/>) of <A>cyc</A> for splitting the value
##  into a sum of values from strictly smaller cyclotomic fields,
##  which would be useful at least if their conductors are coprime.
##  Note that the Bosma basis of the <M>N</M>-th cyclotomic field
##  has the property that it is a union of bases for the cyclotomic fields
##  with conductor dividing <M>N</M>.
##  Thus one can easily find out that <M>\sqrt{{5}} + \sqrt{{7}}</M> can
##  be written as a sum of two values in terms of <M>5</M>-th and <M>7</M>-th
##  roots of unity.
##  In non-coprime situations, this argument fails.
##  For example, one can still detect that <M>\sqrt{{15}} + \sqrt{{21}}</M>
##  involves only <M>15</M>-th and <M>21</M>-th roots of unity,
##  but it is not obvious how to split the value into the two parts.
##  </Description>
##  </ManSection>
##  <#/GAPDoc>
##
CTblLib.StringOfAtlasIrrationality:= function( cyc )
    local res, pos, n, n0, cycsqfr, cycrest, coeffs, coeffs2, resrest,
          ressqfr, entry, b, bnames, res2, i;

    # Handle trivial cases.
    if IsInt( cyc ) then
      return String( cyc );
    elif not IsCycInt( cyc ) then
      return "?";
    fi;

    # Split 'cyc' into the sum of its odd squarefree part 'cycsqfr'
    # and the rest 'cycrest'.
    n:= Conductor( cyc );
    n0:= Product( PrimeDivisors( n ) );
    if n0 mod 2 = 0 then
      n0:= n0 / 2;
    fi;
    if n0 = n then
      cycsqfr:= cyc;
      cycrest:= 0;
    else
      coeffs:= CoeffsCyc( cyc, n );
      res:= PrimeResidues( n0 ) * ( n / n0 ) + 1;
      coeffs2:= coeffs * 0;
      coeffs2{ res }:= coeffs{ res };
      cycsqfr:= CycList( coeffs2 );
      cycrest:= cyc - cycsqfr;
    fi;

    # Find a string for the non-squarefree part.
    if cycrest = 0 then
      resrest:= "";
    else
      # With highest priority, detect multiples of roots of unity.
      resrest:= CTblLib.DetectMultipleOfRootOfUnity( cycrest );
      if resrest = fail then
        # Compute a best expression for quadratic irrationalities.
        resrest:= CTblLib.DetectQuadraticIrrationality( cycrest );
        if resrest = fail then
          # Detect other irrationalities.
          resrest:= CTblLib.DetectNonquadraticIrrationality( cycrest );
        fi;
      fi;
    fi;

    # Find a string for the squarefree part.
    if cycsqfr = 0 then
      ressqfr:= "";
    else
      # With highest priority, detect multiples of roots of unity.
      ressqfr:= CTblLib.DetectMultipleOfRootOfUnity( cycsqfr );
      if ressqfr = fail then
        # Compute a best expression for quadratic irrationalities.
        ressqfr:= CTblLib.DetectQuadraticIrrationality( cycsqfr );
        if ressqfr = fail then
          # Detect other irrationalities.
          ressqfr:= CTblLib.DetectNonquadraticIrrationality( cycsqfr );
        fi;
      fi;

      # The two parts will be concatenated, insert a '+' sign if needed.
      if ressqfr[1] <> '-' and resrest <> "" then
        ressqfr:= Concatenation( "+", ressqfr );
      fi;
    fi;

    # Put the two parts together.
    res:= Concatenation( resrest, ressqfr );

    # Find an alternative description in some special cases.
    coeffs:= fail;
    if n = 5 then
      b:= Basis( CF( 5 ), [ EM(5), GaloisCyc( EM(5), 3 ), E(5)^3, 1 ] );
      bnames:= [ "m5", "m5*3", "z5*3", "1" ];
      coeffs:= Coefficients( b, cyc );
      if coeffs[1] <> 0 then
        bnames[2]:= "&3";
      fi;
    elif n = 12 then
      b:= Basis( CF( 12 ), [ E(12), E(4), E(3), E(3)^2 ] );
      bnames:= [ "z12", "i", "z3", "z3**" ];
      coeffs:= Coefficients( b, cyc );
      if coeffs[3] = coeffs[4] then
        coeffs[3]:= - coeffs[3];
        Unbind( coeffs[4] );
        bnames[3]:= "1";
      fi;
    fi;
    if coeffs <> fail and ForAll( coeffs, IsInt ) then
      # Combine the strings for the basis elements.
      if coeffs[1] = 0 then
        res2:= "";
      elif coeffs[1] = 1 then
        res2:= bnames[1];
      elif coeffs[1] = -1 then
        res2:= Concatenation( "-", bnames[1] );
      else
        res2:= Concatenation( String( coeffs[1] ), bnames[1] );
      fi;
      for i in [ 2 .. Length( coeffs ) ] do
        if coeffs[i] > 0 then
          if res2 <> "" then
            Append( res2, "+" );
          fi;
          if bnames[i] = "1" then
            Append( res2, String( coeffs[i] ) );
          elif coeffs[i] <> 1 then
            Append( res2, String( coeffs[i] ) );
            Append( res2, String( bnames[i] ) );
          else
            Append( res2, String( bnames[i] ) );
          fi;
        elif coeffs[i] < 0 then
          if bnames[i] = "1" then
            Append( res2, String( coeffs[i] ) );
          elif coeffs[i] <> -1 then
            Append( res2, String( coeffs[i] ) );
            Append( res2, String( bnames[i] ) );
          else
            Append( res2, "-" );
            Append( res2, String( bnames[i] ) );
          fi;
        fi;
      od;

      # If the alternative description is shorter then take it.
      if Length( res2 ) < Length( res ) then
        res:= res2;
      fi;
    fi;

    return res;
end;


#############################################################################
##
#F  CTblLib.CharacterTableDisplayStringEntry( <cyc>, <data> )
#F  CTblLib.CharacterTableDisplayStringEntryData( <tbl> )
#F  CTblLib.CharacterTableDisplayLegend( <data> )
##
##  These functions are variants of the default functions
##  'CharacterTableDisplayStringEntryDefault',
##  'CharacterTableDisplayStringEntryDataDefault',
##  'CharacterTableDisplayLegendDefault'.
##
##  We use <data> for caching results,
##  otherwise delegate the work to 'CTblLib.StringOfAtlasIrrationality'.
##
CTblLib.CharacterTableDisplayStringEntry:= function( cyc, data )
    local res, pos, entry;

    # Perhaps the cyc has appeared already.
    res:= fail;
    if IsRecord( data ) and IsBound( data.irrstack ) then
      pos:= Position( data.irrstack, cyc );
      if pos <> fail then
        res:= data.irrnames[ pos ];
      fi;
    fi;

    if res = fail then
      res:= CTblLib.StringOfAtlasIrrationality( cyc );
    fi;

    # Replace the automatically computed string by the string that
    # appears in the ATLAS (if applicable).
    if IsRecord( data ) and IsBound( data.name ) then
      for entry in CTblLib.IrrationalityMapping do
        if entry[1] = res and
           data.name in entry{ [ 3 .. Length( entry ) ] } then
          res:= entry[2];
          break;
        fi;
      od;

      # Extend the cache if applicable.
      if IsBound( data.irrstack ) then
        Add( data.irrstack, cyc );
        Add( data.irrnames, res );
      fi;
    fi;

    # Return the computed value.
    return res;
end;

CTblLib.CharacterTableDisplayStringEntryData:=
    CharacterTableDisplayStringEntryDataDefault;

CTblLib.CharacterTableDisplayLegend:= function( data )
    local i;

    # Keep only the unidentified irrationalities.
    for i in [ 1 .. Length( data.irrnames ) ] do
      if not ForAny( data.irrnames[i], IsUpperAlphaChar ) then
        Unbind( data.irrnames[i] );
        Unbind( data.irrstack[i] );
      fi;
    od;

    data.irrnames:= Compacted( data.irrnames );
    data.irrstack:= Compacted( data.irrstack );

    return CharacterTableDisplayLegendDefault( data );
end;


#############################################################################
##
#F  CTblLib.RelativeIrrationalities( <vals>, <info> )
##
##  We assume that all entries in <vals> are algebraically conjugate
##  cyclotomic integers,
##  and that <info> is a record that describes the context where <vals>
##  occurs.
##  At least the components 'name' and 'cache' of <info> are bound;
##  they are used for caching values that have already been met.
##  The component 'characteristic' of <info>, if present, denotes the
##  underlying characteristic of the character table in which <vals> occur.
##
##  The code duplicates part of the code for computing power maps for
##  Cambridge format tables, in order to choose the same Galois conjugations
##  '*k' in the blocks of irrationalities as in the power maps.
##
##  The function calls 'CTblLib.CharacterTableDisplayStringEntry',
##  which uses 'CTblLib.IrrationalityMapping'.
##
CTblLib.RelativeIrrationalities:= function( vals, info )
    local copyvals, perm, pos, strings, lens, min, cand, val,
          complexconjugate, isnonreal, i, n, residues, resorders, stabilizer,
          inverse;

    # Cache strings once they are computed.
    # Note that caching does not only reduce the efforts (think of large
    # blocks of irrationalities) but also gives preference to already used
    # values (which is not obvious in cases '2y7+&4' vs. 'y7+2&2' (3D4(2)).
    copyvals:= ShallowCopy( vals );
    perm:= Sortex( copyvals );
    pos:= Position( info.cache.lists, copyvals );
    if pos = fail then
      # We have to work.
#T use info.characteristic!
      strings:= List( vals,
                  x -> CTblLib.CharacterTableDisplayStringEntry( x, info ) );
      if Length( vals ) <> 1 then
        # We have to choose one explicit expression, and relative values
        # for the others.
        # We choose among the expressions of minimal length;
        # if there is one without '&' then we take the first such entry,
        # otherwise we take the first shortest entry.
        lens:= List( strings, Length );
        min:= Minimum( lens );
        cand:= strings{ Positions( lens, min ) };
        val:= First( cand, x -> not '&' in x );
        if val = fail then
          val:= cand[1];
        fi;
        pos:= Position( strings, val );
        val:= vals[ pos ];
        complexconjugate:= GaloisCyc( val, -1 );
        isnonreal:= ( val <> complexconjugate );

        if Quadratic( val ) <> fail then
          # Write '*' or '**' if the letter 'b' is involved,
          # otherwise keep the absolute names.
          if not ( 'i' in strings[ pos ] or 'r' in strings[ pos ] ) then
            for i in [ 1 .. Length( vals ) ] do
              if vals[i] <> val then
                if vals[i] = complexconjugate then
                  strings[i]:= "**";
                else
                  strings[i]:= "*";
                fi;
              fi;
            od;
          fi;
        else
          # The values are non-quadratic.
          # Compute suitable '*k' or '**k' values.
          n:= Conductor( val );
          for i in [ 1 .. Length( vals ) ] do
            if i <> pos then
              if vals[i] = val then
                # Avoid '*1'.
                strings[i]:= strings[ pos ];
              elif isnonreal and vals[i] = complexconjugate then
                # Prefer '**' to '*k'.
                strings[i]:= "**";
              else
                # Find a suitable '*k' of smallest possible mult. order.
                # (For 'y9' type irrationalities, use '*2' and '*4'.)
                residues:= PrimeResidues( n );
                if not ( n = 9 and Length( vals ) = 3  ) then
                  resorders:= List( residues, x -> OrderMod( x, n ) );
                  SortParallel( resorders, residues );
                fi;
                stabilizer:= Filtered( residues,
                                       x -> GaloisCyc( val, x ) = val );
                min:= First( residues, x -> GaloisCyc( val, x ) = vals[i] );
                min:= First( residues,
                             x -> ( x / min ) mod n in stabilizer );
                strings[i]:= min;
              fi;
            fi;
          od;

          if isnonreal then
            # Adjust s. t. pairs of complex conjugates appear as '*k', '**k',
            # except if the string of '**k' is longer than that of '*(n-k)'.
            inverse:= [];
            for i in [ 1 .. Length( vals ) ] do
              if not IsBound( inverse[i] ) then
                complexconjugate:= GaloisCyc( vals[i], -1 );
                pos:= Position( vals, complexconjugate );
                while pos <> fail and IsBound( inverse[ pos ] ) do
                  pos:= Position( vals, complexconjugate, pos );
                od;
                inverse[i]:= pos;
                if pos <> fail then
                  inverse[ pos ]:= i;
                fi;
              fi;
            od;

            for i in [ 1 .. Length( inverse ) ] do
              if inverse[i] <> fail then
                if i < inverse[i] and IsInt( strings[i] ) then
                  if strings[i] < strings[ inverse[i] ] then
                    if Length( String( strings[i] ) ) + 1
                       <= Length( String( strings[ inverse[i] ] ) ) then
                      strings[ inverse[i] ]:= - strings[i];
                    elif Length( String( n - strings[i] ) )
                         <= Length( String( strings[ inverse[i] ] ) ) then
                      strings[ inverse[i] ]:= n - strings[i];
                    fi;
                  else
                    if Length( String( strings[ inverse[i] ] ) ) + 1
                       <= Length( String( strings[i] ) ) then
                      strings[i]:= - strings[ inverse[i] ];
                    elif Length( String( n - strings[ inverse[i] ] ) )
                         <= Length( String( strings[i] ) ) then
                      strings[i]:= n - strings[ inverse[i] ];
                    fi;
                  fi;
                fi;
              fi;
            od;

          fi;

          # Create the final relative names.
          for i in [ 1 .. Length( strings ) ] do
            if IsInt( strings[i] ) then
              if strings[i] > 0 then
                strings[i]:= Concatenation( "*", String( strings[i] ) );
              else
                strings[i]:= Concatenation( "**", String( - strings[i] ) );
              fi;
            fi;
          od;
        fi;
      fi;

      Add( info.cache.lists, copyvals );
      Add( info.cache.strings, Permuted( strings, perm ) );
      pos:= Length( info.cache.strings );
    fi;

    return Permuted( info.cache.strings[ pos ], perm^-1 );
end;


#############################################################################
##
#E

