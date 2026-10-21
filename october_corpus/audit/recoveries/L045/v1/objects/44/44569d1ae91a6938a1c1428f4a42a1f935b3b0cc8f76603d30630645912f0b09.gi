#############################################################################
##
#W  brdbattrX.gi          GAP 4 package CTblLib                 Thomas Breuer
##
##  This file contains code from `lib/brdbattr.gd` in the Browse package,
##  and a few utilities from other files in Browse.
##


#############################################################################
##
##  Provide alternatives for some functions that are defined in `BrowseData`.
##
CTblLib.IsAttributeLine:=
    obj -> IsStringRep( obj ) or
           ( IsDenseList( obj ) and
             ForAll( obj, x -> IsStringRep( x ) or IsInt( x )
                                                or IsBool( x ) ) and
             ForAny( obj, x -> not IsStringRep( x ) ) );

CTblLib.IsBrowseTableCellData:= 
    obj -> CTblLib.IsAttributeLine( obj ) or
       ( IsDenseList( obj ) and ForAll( obj, CTblLib.IsAttributeLine ) ) or
       ( IsRecord( obj ) and IsBound( obj.rows ) and IsDenseList( obj.rows )
                         and ForAll( obj.rows, CTblLib.IsAttributeLine ) );

CTblLib.CompareAsNumbersAndNonnumbers:= function( nam1, nam2 )
    local len1, len2, len, digit, comparenumber, i;

    # Essentially the code does the following, just more efficiently.
    # return BrowseData.SplitStringIntoNumbersAndNonnumbers( nam1 ) <
    #        BrowseData.SplitStringIntoNumbersAndNonnumbers( nam2 );

    len1:= Length( nam1 );
    len2:= Length( nam2 );
    len:= len1;
    if len2 < len then
      len:= len2;
    fi;
    digit:= false;
    comparenumber:= 0;
    for i in [ 1 .. len ] do
      if nam1[i] in DIGITS then
        if nam2[i] in DIGITS then
          digit:= true;
          if comparenumber = 0 then
            # first digit of a number, or previous digits were equal
            if nam1[i] < nam2[i] then
              comparenumber:= 1;
            elif nam1[i] <> nam2[i] then
              comparenumber:= -1;
            fi;
          fi;
        else
          # if digit then the current number in `nam2' is shorter,
          # so `nam2' is smaller;
          # if not digit then a number starts in `nam1' but not in `nam2',
          # so `nam1' is smaller
          return not digit;
        fi;
      elif nam2[i] in DIGITS then
        # if digit then the current number in `nam1' is shorter,
        # so `nam1' is smaller;
        # if not digit then a number starts in `nam2' but not in `nam1',
        # so `nam2' is smaller
        return digit;
      else
        # both characters are non-digits
        if digit then
          # first evaluate the current numbers (which have the same length)
          if comparenumber = 1 then
            # nam1 is smaller
            return true;
          elif comparenumber = -1 then
            # nam2 is smaller
            return false;
          fi;
          digit:= false;
        fi;
        # now compare the non-digits
        if nam1[i] <> nam2[i] then
          return nam1[i] < nam2[i];
        fi;
      fi;
    od;

    if digit then
      # The suffix of the shorter string is a number.
      # If the longer string continues with a digit then it is larger,
      # otherwise the first digits of the number decide.
      if len < len1 and nam1[ len+1 ] in DIGITS then
        # nam2 is smaller
        return false;
      elif len < len2 and nam2[ len+1 ] in DIGITS then
        # nam1 is smaller
        return true;
      elif comparenumber = 1 then
        # nam1 is smaller
        return true;
      elif comparenumber = -1 then
        # nam2 is smaller
        return false;
      fi;
    fi;

    # Now the longer string is larger.
    return len1 < len2;
end;

CTblLib.CompareLenLex := function( val1, val2 )
  if   Length( val1 ) < Length( val2 ) then
    return true;
  elif Length( val2 ) < Length( val1 ) then
    return false;
  fi;
  return val1 < val2;
end;

CTblLib.ReplacedEntry:= function( value, from, to )
    local pos;

    pos:= Position( from, value );
    if pos <> fail then
      value:= to[ pos ];
    fi;

    return value;
end;


#############################################################################
##
#F  DatabaseIdEnumeratorX( <arec> )
##
InstallGlobalFunction( DatabaseIdEnumeratorX, function( arec )
    local comps, entry;

    arec:= ShallowCopy( arec );

    # Check for the presence of the mandatory components.
    comps:= [ [ "identifiers", "list", IsList ],
              [ "entry", "function", IsFunction ],
            ];
    for entry in comps do
      if not IsBound( arec.( entry[1] ) )
         or not entry[3]( arec.( entry[1] ) ) then
        Error( "<arec>.", entry[1], " must be bound to a ", entry[2] );
      fi;
    od;

    # Set default values for the optional components.
    comps:= [ [ "attributes", "record", IsRecord, rec() ],
              [ "isUpToDate", "function", IsFunction, ReturnTrue ],
              [ "version", "object", IsObject, "" ],
              [ "update", "function", IsFunction, ReturnTrue ],
              [ "viewLabel", "table cell data object",
                CTblLib.IsBrowseTableCellData, "name" ],
              [ "viewValue", "function", IsFunction, String ],
              [ "viewSort", "function", IsFunction, \< ],
              [ "sortParameters", "list", IsList, [] ],
              [ "widthCol", "positive integer", IsPosInt ],
              [ "align", "string", IsString, "r" ],
              [ "categoryValue", "function", IsFunction ],
              [ "isSorted", "boolean", IsBool, false ],
            ];
    for entry in comps do
      if IsBound( arec.( entry[1] ) ) then
        if not entry[3]( arec.( entry[1] ) ) then
          Error( "<arec>.", entry[1], ", if bound, must be a ", entry[2] );
        fi;
      elif IsBound( entry[4] ) then
        arec.( entry[1] ):= entry[4];
      fi;
    od;
    if not IsBound( arec.categoryValue ) then
      arec.categoryValue:= arec.viewValue;
    fi;

    # Set the "self" attribute.
    DatabaseAttributeAddX( arec, rec(
        identifier:= "self",
        description:= "the identifiers themselves",
        type:= "values",
        data:= arec.identifiers,
        version:= arec.version,
        update:= function( a )
            a.data:= a.idenumerator.identifiers;
            return true;
          end,
        viewLabel:= arec.viewLabel,
        viewValue:= arec.viewValue,
        viewSort:= arec.viewSort,
        sortParameters:= arec.sortParameters,
        align:= arec.align,
        categoryValue:= arec.categoryValue,
      ) );
    if IsBound( arec.widthCol ) then
      arec.attributes.self.widthCol:= arec.widthCol;
    fi;

    return arec;
end );


#############################################################################
##
#F  DatabaseAttributeAddX( <dbidenum>, <arec> )
##
InstallGlobalFunction( DatabaseAttributeAddX, function( dbidenum, arec )
    local comps, entry;

    # Check `dbidenum'.
    if not IsRecord( dbidenum ) or not IsBound( dbidenum.attributes )
                                or not IsRecord( dbidenum.attributes ) then
      Error( "<dbidenum> must be a database id enumerator" );
    elif IsBound( arec.identifier ) and
         IsBound( dbidenum.attributes.( arec.identifier ) ) then
      Error( "an attribute with identifier `", arec.identifier,
             "' is already bound in <dbidenum>" );
    fi;
    arec:= ShallowCopy( arec );
    arec.idenumerator:= dbidenum;

    # Check for the presence of the mandatory components.
    comps:= [ [ "identifier", "string", IsString ],
              [ "type", "string", IsString ],
            ];
    for entry in comps do
      if not IsBound( arec.( entry[1] ) )
         or not entry[3]( arec.( entry[1] ) ) then
        Error( "<arec>.", entry[1], " must be bound to a ", entry[2] );
      fi;
    od;

    # Do more tests.
    if not arec.type in [ "values", "pairs" ] then
      Error( "<arec>.type must be one of `\"values\"', `\"pairs\"'" );
    fi;

    # Set default values for the optional components.
    comps:= [ 
              [ "description", "string", IsString, "" ],
              [ "name", "string", IsString ],
              [ "datafile", "string", IsString ],
              [ "attributeValue", "function", IsFunction,
                DatabaseAttributeValueDefaultX ],
              [ "dataDefault", "object", IsObject, "" ],
              [ "eval", "function", IsFunction ],
              [ "neededAttributes", "list", IsList, [] ],
              [ "prepareAttributeComputation", "function", IsFunction,
                ReturnTrue ],
              [ "cleanupAfterAttributeComputation", "function", IsFunction,
                ReturnTrue ],
              [ "create", "function", IsFunction ],
              [ "string", "function", IsFunction,
     #          function( id, val ) return String( val ); end ],
                String ],
              [ "check", "function", IsFunction, ReturnTrue ],
              [ "viewLabel", "table cell data object",
                CTblLib.IsBrowseTableCellData ],
              [ "viewValue", "function", IsFunction, String ],
              [ "viewSort", "function", IsFunction, \< ],
              [ "sortParameters", "list", IsList, [] ],
              [ "widthCol", "positive integer", IsPosInt ],
              [ "align", "string", IsString, "r" ],
              [ "categoryValue", "function", IsFunction ],
            ];
    for entry in comps do
      if IsBound( arec.( entry[1] ) ) then
        if not entry[3]( arec.( entry[1] ) ) then
          Error( "<arec>.", entry[1], ", if bound, must be a ", entry[2] );
        fi;
      elif IsBound( entry[4] ) then
        arec.( entry[1] ):= entry[4];
      fi;
    od;

    # Do more tests.
    if IsBound( arec.data ) then
      if   arec.type = "values" and not IsList( arec.data ) then
        Error( "<arec>.type is \"values\", so <arec>.data must be a list" );
      elif arec.type = "pairs" and
        not ( IsRecord( arec.data ) and IsBound( arec.data.automatic ) and
                 IsBound( arec.data.nonautomatic ) ) then
        Error( "<arec>.type is \"pairs\", so <arec>.data must be a record ",
               "with the components `automatic' and `nonautomatic'" );
      fi;
    fi;
    if IsBound( arec.name ) then
      if not IsBoundGlobal( arec.name ) or
         not IsFunction( ValueGlobal( arec.name ) ) then
        Error( "<arec>.name must be the identifier of a global function" );
      fi;
    fi;
    if IsBound( arec.isSorted ) then
      if arec.type = "values" then
        Error( "<arec>.isSorted is valid only for <arec>.type = \"pairs\"" );
      elif not arec.isSorted in [ true, false ] then
        Error( "<arec>.isSorted must be `true' or `false'" );
      fi;
    elif arec.type = "pairs" then
      arec.isSorted:= false;
    fi;

    # Set default values for the optional components.
    if not IsBound( arec.create ) and IsBound( arec.name ) then
      arec.create:= function( attr, id )
        return ValueGlobal( arec.name )(
                 attr.idenumerator.entry( attr.idenumerator, id ) );
      end;
    fi;
    if not IsBound( arec.viewLabel ) then
      if IsBound( arec.name ) then
        arec.viewLabel:= arec.name;
      else
        arec.viewLabel:= arec.identifier;
      fi;
    fi;
    if not IsBound( arec.categoryValue ) then
      arec.categoryValue:= arec.viewValue;
    fi;
    if not IsBound( arec.version ) and not IsBound( arec.datafile ) then
      arec.version:= dbidenum.version;
    fi;

    dbidenum.attributes.( arec.identifier ):= arec;
#T update component for attributes!
#T (when can I set a default value?)
#T where do I just have to replace known values?
end );


#############################################################################
##
#F  DatabaseAttributeValueDefaultX( <attr>, <id> )
##
InstallGlobalFunction( DatabaseAttributeValueDefaultX, function( attr, id )
    local pos, comp, result;

    # If the `data' component is not bound then initialize it.
    if not IsBound( attr.data ) then
      if IsBound( attr.datafile ) and IsReadableFile( attr.datafile ) then
        DatabaseAttributeLoadDataX( attr );
      else
        DatabaseAttributeComputeX( attr.idenumerator, attr.identifier );
      fi;
    fi;
    if not IsBound( attr.data ) then
      Error( "<attr>.data is still not bound" );
    fi;

    if attr.type = "values" then
      if attr.idenumerator.isSorted then
        pos:= PositionSet( attr.idenumerator.identifiers, id );
      else
        pos:= Position( attr.idenumerator.identifiers, id );
      fi;
      if pos <> fail then
        if IsBound( attr.data[ pos ] ) then
          result:= attr.data[ pos ];
        elif IsBound( attr.name ) then
          result:= attr.create( attr, id );
          attr.data[ pos ]:= result;
        else
          result:= attr.dataDefault;
        fi;
      fi;
    elif attr.isSorted then
      for comp in [ attr.data.automatic, attr.data.nonautomatic ] do
        pos:= PositionSorted( comp, [ id ] );
        if pos <= Length( comp ) and comp[ pos ][1] = id then
          result:= comp[ pos ][2];
          break;
        fi;
      od;
    else
      for comp in [ attr.data.automatic, attr.data.nonautomatic ] do
        pos:= First( [ 1 .. Length( comp ) ], i -> comp[i][1] = id );
        if  pos <> fail then
          result:= comp[ pos ][2];
          break;
        fi;
      od;
    fi;

    if not IsBound( result ) then
      if IsBound( attr.dataDefault ) then
        result:= attr.dataDefault;
      else
        Error( "no `dataDefault' entry" );
      fi;
    fi;

    if IsBound( attr.eval ) then
      result:= attr.eval( attr, result );
    fi;
    return result;
end );


#############################################################################
##
#F  DatabaseAttributeLoadDataX( <attr> )
##
InstallGlobalFunction( DatabaseAttributeLoadDataX, function( attr )
    local filename, data;

    if IsBound( attr.datafile ) and IsReadableFile( attr.datafile ) then
      filename:= attr.datafile;
      if EndsWith( filename, ".json" ) then
        # evaluate the JSON text;
        # note that Browse does not force that a JSON parser is available
        if IsBound( AGR ) and IsBound( AGR.GapObjectOfJsonText ) then
          data:= ValueGlobal( "AGR" ).GapObjectOfJsonText(
                                          StringFile( filename ) );
          if data.status = false then
            Error( "the file '", filename,
                   "' does not contain a valid JSON text" );
          fi;
          data:= data.value;
        elif IsBound( JsonStringToGap ) then
          data:= ValueGlobal( "JsonStringToGap" )( StringFile( filename ) );
        else
          Error( "cannot evaluate the JSON format file '", filename, "'" );
        fi;
        # consistency check
        if EvalString( data.idenum ) <> attr.idenumerator then
          Error( "file '", filename,
                 "' contains data for the id enumerator '", data.idenum,
                 "', not for the one of the attribute <attr>" );
        elif data.attrid <> attr.identifier then
          Error( "file '", filename,
                 "' contains data for the attribute '", data.attrid,
                 "' not '", attr.identifier, "'" );
        fi;
        if data.version <> attr.idenumerator.version then
          Info( InfoWarning, 1,
                "versions of attribute '", data.attrid,
                "' and of id enumerator '", data.idenum,
                "' are not compatible" );
        fi;
        # set the data
        DatabaseAttributeSetDataX( attr.idenumerator, attr.identifier,
            data.version,
            rec( automatic:= data.automatic,
                 nonautomatic:= data.nonautomatic ) );
      else
        # just read the file
        Read( attr.datafile );
      fi;
    fi;
end );


#############################################################################
##
#F  DatabaseAttributeSetDataX( <dbidenum>, <attridentifier>, <version>,
#F                             <data> )
##
InstallGlobalFunction( DatabaseAttributeSetDataX,
    function( dbidenum, attridentifier, version, data )
    local attr;

    if   not IsRecord( dbidenum ) or not IsBound( dbidenum.attributes )
                                or not IsRecord( dbidenum.attributes ) then
      Error( "usage: DatabaseAttributeSetData( <dbidenum>, ",
             "<attridentifier>,\n <version>, <data> )" );
    elif not IsBound( dbidenum.attributes.( attridentifier ) ) then
      Error( "<dbidenum> has no attribute `", attridentifier, "'" );
    fi;
    attr:= dbidenum.attributes.( attridentifier );
    if not ( ( attr.type = "values" and IsList( data ) ) or
             ( attr.type = "pairs" and IsRecord( data ) ) ) then
      Error( "<data> does not fit to the type of <attr>" );
    fi;
    if attr.type = "pairs" then
      if attr.isSorted = true and
         ( not IsSSortedList( data.automatic ) or
           not IsSSortedList( data.nonautomatic ) ) then
        Error( "the data lists are not strictly sorted" );
      fi;
      if not IsEmpty( Intersection( List( data.automatic, x -> x[1] ),
                          List( data.nonautomatic, x -> x[1] ) ) ) then
#T provide an NC variant that skips the tests?
        Error( "automatic and nonautomatic data are not disjoint" );
      fi;
      attr.data:= data;
    else
      if Length( dbidenum.identifiers ) < Length( data ) then
        Error( "automatic and nonautomatic data are not disjoint" );
      fi;
      attr.data:= data;
    fi;
    attr.version:= version;
#T What shall happen if the version does not fit to dbidenum?
end );


#############################################################################
##
#F  DatabaseIdEnumeratorUpdateX( <dbidenum> )
##
InstallGlobalFunction( DatabaseIdEnumeratorUpdateX, function( dbidenum )
    local name, attr;

    if dbidenum.update( dbidenum ) <> true then
      Info( InfoDatabaseAttributeX, 1,
            "DatabaseIdEnumeratorUpdateX: <dbidenum>.update returned ",
            "'false'" );
      return false;
    fi;

#T do this in the order prescribed by neededAttributes!
    for name in RecNames( dbidenum.attributes ) do
      attr:= dbidenum.attributes.( name );
      if not IsBound( attr.version ) then
        DatabaseAttributeLoadDataX( attr );
        if not IsBound( attr.version ) then
          Error( "<attr>.version still not bound" );
        fi;
      fi;
      if attr.version <> dbidenum.version then
        if IsBound( attr.update ) and attr.update( attr ) = true then
          attr.version:= dbidenum.version;
        else
          Info( InfoDatabaseAttributeX, 1,
                "DatabaseIdEnumeratorUpdateX: <attr>.update for attribute '",
                name, "' returned 'false'" );
          return false;
        fi;
      fi;
    od;

    return true;
end );


#############################################################################
##
#F  DatabaseAttributeComputeX( <dbidenum>, <attridentifier>[, <what>] )
##
InstallGlobalFunction( DatabaseAttributeComputeX, function( arg )
    local idenum, attridentifier, what, attr, attrid, attr2, i, new,
          oldnonautomatic, oldautomatic, automatic, newautomatic, id;

    idenum:= arg[1];
    attridentifier:= arg[2];
    what:= "automatic";
    if Length( arg ) = 3 and arg[3] in [ "all", "automatic", "new" ] then
      what:= arg[3];
    fi;

    if not IsRecord( idenum ) or
       not IsBound( idenum.attributes ) or
       not IsRecord( idenum.attributes ) or
       not IsString( attridentifier ) or
       not IsBound( idenum.attributes.( attridentifier ) ) then
      Info( InfoDatabaseAttributeX, 1,
            "<idenum> has no component <attridentifier>" );
      return false;
    fi;
    attr:= idenum.attributes.( attridentifier );

    if not IsBound( attr.create ) then
      Info( InfoDatabaseAttributeX, 1,
            "<attr> has no component <create>" );
      return false;
    fi;

    # Update the needed attributes if necessary.
    for attrid in attr.neededAttributes do
      attr2:= idenum.attributes.( attrid );
      if not IsBound( attr2.version ) and not IsBound( attr2.data ) and
         IsBound( attr2.datafile ) and IsReadableFile( attr2.datafile ) then
        DatabaseAttributeLoadDataX( attr2 );
      fi;
      if not IsBound( attr2.version ) or attr2.version <> idenum.version then
        Info( InfoDatabaseAttributeX, 1,
              "DatabaseAttributeCompute for attribute ", attridentifier,
              ":\n#I  compute needed attribute ", attrid );
        DatabaseAttributeComputeX( idenum, attrid, what );
      fi;
    od;

    attr.prepareAttributeComputation( attr );

    if attr.type = "values" then
      if what = "automatic" then
        what:= "all";
      fi;
      if not IsBound( attr.data ) then
        # Fetch the known values; if necessary then initialize.
        if IsBound( attr.datafile ) and IsReadableFile( attr.datafile ) then
          DatabaseAttributeLoadDataX( attr );
        else
          attr.data:= [];
        fi;
      fi;

      Info( InfoDatabaseAttributeX, 1,
            "DatabaseAttributeCompute: start for attribute ",
            attridentifier );

      for i in [ 1 .. Length( idenum.identifiers ) ] do
        if ( not IsBound( attr.data[i] ) ) or ( what <> "new" ) then
          new:= attr.create( attr, idenum.identifiers[i] );
          if IsBound( attr.data[i] ) then
            if IsBound( attr.dataDefault ) and new = attr.dataDefault then
              Info( InfoDatabaseAttributeX, 2,
                    "difference in recompute for ", idenum.identifiers[i],
                     ":\n#E  deleting entry\n", attr.data[i] );
              Unbind( attr.data[i] );
            elif new <> attr.data[i] then
              Info( InfoDatabaseAttributeX, 2,
                    "difference in recompute for ", idenum.identifiers[i],
                     ":\n#E  replacing entry\n#E  ", attr.data[i],
                     "\n#E  by\n#E  ", new );
              attr.data[i]:= new;
            fi;
          elif not IsBound( attr.dataDefault ) or new <> attr.dataDefault then
            Info( InfoDatabaseAttributeX, 2,
                  "recompute: new entry for ", idenum.identifiers[i],
                  ":\n#I  ", new );
            attr.data[i]:= new;
          fi;
        fi;
      od;

      Info( InfoDatabaseAttributeX, 1,
            "DatabaseAttributeCompute: done for attribute ",
            attridentifier );

      attr.version:= idenum.version;
    else
      if not IsBound( attr.data ) then
        # Fetch the known values; if necessary then initialize.
        if IsBound( attr.datafile ) and IsReadableFile( attr.datafile ) then
          DatabaseAttributeLoadDataX( attr );
        else
          attr.data:= rec( automatic:= [], nonautomatic:= [] );
        fi;
      fi;
      oldnonautomatic:= List( attr.data.nonautomatic, x -> x[1] );
      oldautomatic:= List( attr.data.automatic, x -> x[1] );
      automatic:= [];
      newautomatic:= [];

      Info( InfoDatabaseAttributeX, 1,
            "DatabaseAttributeCompute: start for attribute ",
            attridentifier );

      for id in idenum.identifiers do
        if not ( ( what in [ "automatic", "new" ] and id in oldnonautomatic ) or
           ( what = "new" and id in oldautomatic ) ) then
          new:= attr.create( attr, id );
          if new <> attr.dataDefault then
            Add( automatic, [ id, new ] );

            # Handle the case that a nonautomatic value becomes automatic.
            if what = "all" and id in oldnonautomatic then
              Info( InfoDatabaseAttributeX, 2,
                    "recompute: formerly nonautomatic value for ", id,
                    "#I  is now automatic" );
              Add( newautomatic, id );
            fi;
          fi;
        fi;
      od;
      attr.data.automatic:= automatic;
      if newautomatic <> [] then
        attr.data.nonautomatic:= Filtered( attr.data.nonautomatic,
            pair -> not pair[1] in newautomatic );
      fi;

      Info( InfoDatabaseAttributeX, 1,
            "DatabaseAttributeCompute: done for attribute ",
            attridentifier );

      attr.version:= idenum.version;
    fi;

    attr.cleanupAfterAttributeComputation( attr );

    return true;
end );


#############################################################################
##
#F  DatabaseAttributeStringX( <idenum>, <idenumname>, <attridentifier>
#F                            [, <format>] )
##
InstallGlobalFunction( DatabaseAttributeStringX,
    function( idenum, idenumname, attridentifier, format... )
    local attr, str, strfun, txt, comp, entry;

    if not IsBound( idenum.attributes.( attridentifier ) ) then
      Error( "<idenum> has no component <attridentifier>" );
    elif Length( format ) = 0 then
      format:= "GAP";
    elif format[1] in [ "GAP", "JSON" ] then
      format:= format[1];
    else
      Error( "<format>, if given, must be \"GAP\" or \"JSON\"" );
    fi;

    attr:= idenum.attributes.( attridentifier );
    if not IsBound( attr.data ) then
      if IsBound( attr.datafile ) and IsReadableFile( attr.datafile ) then
        DatabaseAttributeLoadDataX( attr );
      else
        DatabaseAttributeComputeX( idenum, attridentifier );
      fi;
    fi;

    if attr.type = "values" then
      Error( "the attribute <attr> must have the type \"pairs\"" );
    elif IsBound( attr.string ) then
      strfun:= attr.string;
    else
      strfun:= String;
    fi;

    if format = "GAP" then
      str:= Concatenation( "DatabaseAttributeSetData( ", idenumname, ", \"",
                attridentifier, "\",\n" );
      if IsString( attr.version ) then
        Append( str, Concatenation( "\"", attr.version, "\"," ) );
      else
        Append( str, Concatenation( String( attr.version ), "," ) );
      fi;
      Append( str, "rec(\nautomatic:=[\n" );
      txt:= "],\nnonautomatic:=[\n";
      for comp in [ attr.data.automatic, attr.data.nonautomatic ] do
        for entry in comp do
          if entry[2] <> attr.dataDefault then
            Append( str, strfun( entry ) );
          fi;
        od;
        Append( str, txt );
        txt:= "]));\n";
      od;
    else
      # Json format:
      # - version
      str:= "{\n\"version\": ";
      if IsString( attr.version ) then
        Append( str, Concatenation( "\"", attr.version, "\",\n" ) );
      else
        Append( str, Concatenation( String( attr.version ), ",\n" ) );
      fi;

      # - ID enumerator:
      Append( str, Concatenation( "\"idenum\": \"", idenumname, "\",\n" ) );

      # - attribute identifier:
      Append( str, Concatenation( "\"attrid\": \"", attridentifier, "\",\n" ) );

      # - automatically computed data:
      Append( str, "\"automatic\": [\n" );
      for entry in attr.data.automatic do
        if entry[2] <> attr.dataDefault then
          Append( str, strfun( entry ) );
        fi;
      od;
      if not IsEmpty( attr.data.automatic ) then
        Unbind( str[ Length( str ) ] );  # no newline
        Unbind( str[ Length( str ) ] );  # no final comma allowed
        Append( str, "\n" );
      fi;

      # - other data:
      Append( str, "],\n\"nonautomatic\": [\n" );
      for entry in attr.data.nonautomatic do
        if entry[2] <> attr.dataDefault then
          Append( str, strfun( entry ) );
        fi;
      od;
      if not IsEmpty( attr.data.nonautomatic ) then
        Unbind( str[ Length( str ) ] );  # no newline
        Unbind( str[ Length( str ) ] );  # no final comma allowed
        Append( str, "\n" );
      fi;
      Append( str, "]\n}\n" );
    fi;

    return str;
end );


#############################################################################
##
#E

