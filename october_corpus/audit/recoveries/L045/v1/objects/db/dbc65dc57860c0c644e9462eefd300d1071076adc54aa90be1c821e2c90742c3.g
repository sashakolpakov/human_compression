
##  Provide the function 'OrthogonalDiscriminants' that is used by the
##  the GAP library's 'Display' method for character tables
##  if it is available.
##
##  It evaluates the Orthogonal Discriminants from the database,
##  which are contained in the file 'data/odresults.json' of CTblLib.
##  (This is just code for fetching values and reducing them
##  to characteristics coprime to the group order;
##  it does not require the package for computing ODs,
##  and it cannot apply the criteria for these computations.)

if not IsBound( OrthogonalDiscriminants ) then

CTblLib.OD_data:= AGR.GapObjectOfJsonText( StringFile(
                    Filename( DirectoriesPackageLibrary( "ctbllib", "data" ),
                              "odresults.json" ) ) ).value;;

DeclareAttribute( "OrthogonalDiscriminants", IsCharacterTable );

# Install the method with lower rank than the method from the OD package,
# in order to give that method precedence if it will be loaded later.
InstallMethod( OrthogonalDiscriminants,
    [ "IsCharacterTable" ], -1,
    function( tbl )
    local p, ordtbl, name, result, data, facttbl, pos, simpname, r, reduce,
          ind, irr, i, map, entry, OD0, chi, val, d, q, perf, deg;

    p:= UnderlyingCharacteristic( tbl );
    if p = 0 then
      ordtbl:= tbl;
    else
      ordtbl:= OrdinaryCharacterTable( tbl );
    fi;
    name:= Identifier( ordtbl );

    result:= [];
    data:= fail;
    facttbl:= fail;
    pos:= Position( name, '.' );
#T this makes sense only for almost simple groups!
    if pos = fail then
      simpname:= name;
    else
      simpname:= name{ [ 1 .. pos-1 ] };
    fi;
    if IsBound( CTblLib.OD_data.( simpname ) ) then
      data:= CTblLib.OD_data.( simpname );
      if IsBound( data.( name ) ) then
        data:= data.( name );
      fi;
    else
      # Perhaps we know the ODs for a factor group.
      for r in ComputedClassFusions( ordtbl ) do
        if 1 < Length( ClassPositionsOfKernel( r.map ) ) then
          name:= r.name;
          pos:= Position( name, '.' );
          if pos = fail then
            simpname:= name;
          else
            simpname:= name{ [ 1 .. pos-1 ] };
          fi;
          if IsBound( CTblLib.OD_data.( simpname ) ) then
            data:= CTblLib.OD_data.( simpname );
            if IsBound( data.( name ) ) then
              data:= data.( name );
            fi;
            facttbl:= CharacterTable( name );
            if p <> 0 then
              facttbl:= facttbl mod p;
            fi;
            if facttbl <> fail then
              break;
            fi;
          fi;
        fi; 
      od;
    fi;

    if IsRecord( data ) and IsBound( data.( p ) ) then
      # We have the 'p'-modular values (perhaps incomplete).
      reduce:= false;
      data:= data.( p );
    elif data = fail or Size( tbl ) mod p = 0 then
      # We do not know the 'p'-modular values for 'name'.
      # Compute the positions of orthogonal irreducibles of even degree.
      # (If some indicators are not known then we regard them as orthogonal.)
      ind:= Indicator( tbl, 2 );
      irr:= Irr( tbl );
      for i in [ 1 .. Length( ind ) ] do
        if irr[ i, 1 ] mod 2 = 0 and not ind[i] in [ -1, 0 ] then
          result[i]:= "?";
        fi;
      od;
      return result;
    else
      # We know the values for 'p' iff we know them for '0'.
      reduce:= true;
      data:= data.( 0 );
    fi;

    if facttbl = fail then
      map:= [ 1 .. NrConjugacyClasses( tbl ) ];
    else
      map:= List( RestrictedClassFunctions( Irr( facttbl ), tbl ),
                  x -> Position( Irr( tbl ), x ) );
    fi;

    for entry in data do
      if ( not reduce ) or entry[4] = "?" then
        result[ map[ entry[2] ] ]:= entry[4];
      elif p = 2 then
        # This should not happen,
        # 2 divides the orders of the groups that belong to the database.
        result[ map[ entry[2] ] ]:= "?";
      else
        # 'p' does not divide the group order,
        # we reduce the value from characteristic 0.
        # (Note that the character fields of the ordinary and the
        # Brauer character are equal.)
        OD0:= AtlasIrrationality( entry[4] );
        chi:= Irr( tbl )[ entry[2] ];
        val:= FrobeniusCharacterValue( OD0, p );
#T with the OD package, we can do better ...

        # If we get 'fail' then either the Conway polynomial in question
        # is not available or the conductor of 'OD0' is divisible by 'p'.
        # If 'val' is zero then we cannot use it.
        if val = fail or IsZero( val ) then
          result[ map[ entry[2] ] ]:= "?";
        else
          # Compute whether 'val' is a square in the character field.
          d:= DegreeFFE( val );
          q:= SizeOfFieldOfDefinition( chi, p );
          if IsEvenInt( Length( Factors( q ) ) / d ) or
             IsEvenInt( (q-1) / Order( val ) ) then
            result[ map[ entry[2] ] ]:= "O+";
          else
            result[ map[ entry[2] ] ]:= "O-";
          fi;
        fi;
      fi;
    od;

    if facttbl <> fail then
      # Add values not coming from the factor.
#T here only for 2.G;
#T if we want also 3.G.2 and 4.G.2 and 6.G.2 and 12.G.2
#T then use ad hoc arguments: K = F[root];
#T if 4 divides the degree of chi then OD = 1,
#T otherwise OD = -n where K = F[sqrt(c)].
#T (but what are the exact conditions where this holds?)
      ind:= Indicator( tbl, 2 );
      irr:= Irr( tbl );
      if p = 0 then
        perf:= IsPerfect( tbl );
      else
        perf:= IsPerfect( OrdinaryCharacterTable( tbl ) );
      fi;
      for i in [ 1 .. Length( ind ) ] do
        deg:= irr[ i, 1 ];
        if deg mod 2 = 0 and not ind[i] in [ -1, 0 ]
           and not IsBound( result[i] ) then
          if perf and Size( tbl ) / Size( facttbl ) = 2 and p <> 2 then
            # faithful character of a perfect central extension 2.G,
            # the image of the spinor norm is trivial
            if deg mod 4 = 0 then
              if p = 0 then
                result[i]:= "1";
              else
                result[i]:= "O+";
              fi;
            else
              if p = 0 then
                result[i]:= "-1";
              else
                result[i]:= "?";
              fi;
            fi;
          else
            result[i]:= "?";
          fi;
        fi;
      od;
    fi;

    return result;
    end );

fi;

