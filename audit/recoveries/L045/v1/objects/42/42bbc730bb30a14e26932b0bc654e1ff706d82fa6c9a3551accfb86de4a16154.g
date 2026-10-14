#############################################################################
##
#W  ctbltoct.g           GAP 4 package CTblLib                  Thomas Breuer
##
##  This file contains functions for collecting information about a
##  character table contained in the GAP Character Table Library,
##  and for turning this information into an overview string.
##
##  Functions for creating Browse overviews are in the file 'ctbltocb.g'.
##  Functions for creating HTML files are in 'ctbltoc/gap/htmltbl.g' (using
##  tools from the file 'gap/utlmrkup.g' of the AtlasRep package).
##
##  0. Some utilities for collecting information
##  1. Transform the info into a plain string.
##


#############################################################################
##
##  0. Some utilities for collecting information
##


#############################################################################
##
##  CTblLib.TableValue( <groupname>, <attrname> )
##
##  helper: access attribute values
##
CTblLib.TableValue:= function( groupname, attrname )
    local enum, attrs, attr, tbl;

    enum:= CTblLib.Data.IdEnumerator;
    if not groupname in enum.identifiers then
      enum:= CTblLib.Data.IdEnumeratorExt;
    fi;
    if groupname in enum.identifiers then
      attrs:= enum.attributes;
      if IsBound( attrs.( attrname ) ) then
        attr:= attrs.( attrname );
        return attr.attributeValue( attr, groupname );
      fi;
    fi;

    if attrname = "FusionsTo" then
      return Set( List( ComputedClassFusions( CharacterTable( groupname ) ),
                        r -> r.name ) );
    elif attrname = "Maxes" then
      tbl:= CharacterTable( groupname );
      if HasMaxes( tbl ) then
        return Maxes( tbl );
      else
        return fail;
      fi;
    elif IsBoundGlobal( attrname ) then
      # We assume that there is a (default) value.
      return ValueGlobal( attrname )( CharacterTable( groupname ) );
    else
      # We have no idea what to do.
      return fail;
    fi;
end;


#############################################################################
##
#F  CTblLib.CompareAsNumbersAndNonnumbers( <nam1>, <nam2> )
##
##  This is a copy of `BrowseData.CompareAsNumbersAndNonnumbers'.
##
CTblLib.CompareAsNumbersAndNonnumbers:= function( nam1, nam2 )
    local len1, len2, len, digit, comparenumber, i;

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


##############################################################################
##
#F  CTblLib.MaxesInfoTable( <groupname>, <zero> )
##
##  `CTblLib.MaxesInfoTable' returns a "datatable" record
##  with information about the available character tables of
##  maximal subgroups of the group <groupname>.
##  If the `Maxes' info for <groupname> is not available then the names of
##  the form `<groupname>M<i>' are considered.
##
CTblLib.MaxesInfoTable := function( groupname, zero )
    local maxes, size, matrix, title, i, maxname, maxsize;

    maxes:= CTblLib.TableValue( groupname, "Maxes" );
    size:= CTblLib.TableValue( groupname, "Size" );
    matrix:= [];

    if maxes = fail then
      # List those maxes that are known as such.
      title:= "Some maximal subgroups";
      for i in [ 1 .. 100 ] do
        maxname:= Concatenation( groupname, "M", String( i ) );
        maxname:= LibInfoCharacterTable( maxname );
        if maxname <> fail then
          maxname:= maxname.firstName;
          maxsize:= CTblLib.TableValue( maxname, "Size" );
          Add( matrix, [
                String( i ),
                String( maxsize ),
                String( size / maxsize ),
                rec( type:= "linkedtext",
                     display:= StructureDescriptionCharacterTableName(
                                   maxname ),
                     target:= [ "details page", [ maxname, 0 ] ] ),
                rec( type:= "linkedtext",
                     display:= maxname,
                     target:= [ "details page", [ maxname, 0 ] ] ) ] );
        fi;
      od;
    else
      # Loop over the maxes.
      title:= "Maximal subgroups";
      for maxname in maxes do
        maxsize:= CTblLib.TableValue( maxname, "Size" );
        Add( matrix, [ String( Length( matrix ) + 1 ),
                       String( maxsize ),
                       String( size / maxsize ),
                       rec( type:= "linkedtext",
                            display:= StructureDescriptionCharacterTableName(
                                          maxname ),
                            target:= [ "details page", [ maxname, 0 ] ] ),
                       rec( type:= "linkedtext",
                            display:= maxname,
                            target:= [ "details page", [ maxname, 0 ] ] ) ] );
      od;
    fi;

    if IsEmpty( matrix ) then
      return fail;
    fi;

    return rec( type:= "datatable",
                title:= title,
                header:= [ "", "Order", "Index", "Structure", "Name" ],
                matrix:= matrix,
                colalign:= [ "right", "right", "right", "left", "left" ] );
end;


##############################################################################
##
#F  CTblLib.SylowNormalizerInfoTable( <groupname>, <zero> )
##
##  `CTblLib.SylowNormalizerInfoTable' returns a "datatable" record
##  with information about the available character tables of
##  Sylow normalizers of the group <groupname>.
##
CTblLib.SylowNormalizerInfoTable := function( groupname, zero )
    local size, matrix, p, name, sylnosize;

    size:= CTblLib.TableValue( groupname, "Size" );
    matrix:= [];

    # Get the tables of the known Sylow normalizers.
    for p in PrimeDivisors( size ) do
      name:= LibInfoCharacterTable(
                 Concatenation( groupname, "N", String( p ) ) );
      if name <> fail then
        name:= name.firstName;
        sylnosize:= CTblLib.TableValue( name, "Size" );
        Add( matrix, [ String( p ),
                       String( sylnosize ),
                       String( size / sylnosize ),
                       rec( type:= "linkedtext",
                            display:= StructureDescriptionCharacterTableName(
                                          name ),
                            target:= [ "details page", [ name, 0 ] ] ),
                       rec( type:= "linkedtext",
                            display:= name,
                            target:= [ "details page", [ name, 0 ] ] ) ] );
      fi;
    od;

    if IsEmpty( matrix ) then
      return fail;
    fi;

    return rec( type:= "datatable",
                title:= "Stored Sylow p normalizers",
                header:= [ "p", "Order", "Index", "Structure", "Name" ],
                matrix:= matrix,
                colalign:= [ "right", "right", "right", "left", "left" ] );
end;


##############################################################################
##
#F  CTblLib.BrauerTableInfoTable( <groupname>, <zero> )
##
##  `CTblLib.BrauerTableInfoTable' returns a "datatable" record
##  with information about the available Brauer character tables of
##  the group <groupname>.
##
CTblLib.BrauerTableInfoTable:= function( groupname, zero )
    local size, matrix, t, p, modtbl;

    size:= CTblLib.TableValue( groupname, "Size" );
    matrix:= [];
    t:= CharacterTable( groupname );

    # Get the tables of the available Brauer tables.
    for p in PrimeDivisors( size ) do
      modtbl:= t mod p;
      if modtbl <> fail then
        Add( matrix, [
              String( p ),
              rec( type:= "linkedtext",
                   display:= "details",
                   target:= [ "details page", [ groupname, p ] ] ),
              rec( type:= "linkedtext",
                   display:= "show table",
                   target:= [ "show table", [ groupname, p ] ] ),
              rec( type:= "linkedtext",
                   display:= "show dec. matrix",
                   target:= [ "dec. matrix", [ groupname, p, 0 ] ] ) ] );
      fi;
    od;

    if IsEmpty( matrix ) then
      return fail;
    fi;

    return rec( type:= "datatable",
                title:= "Available Brauer tables",
                header:= [ "p", "", "", "" ],
                matrix:= matrix,
                colalign:= [ "right", "left", "left", "left" ] );
end;


##############################################################################
##
#F  CTblLib.AtlasRepInfoLink( <groupname>, <zero> )
##
##  `CTblLib.AtlasRepInfoLink' returns a "linkedtext" record if the package
##  `AtlasRep' is available and provides representations of <groupname>;
##  the purpose is to allow one to navigate to the AtlasRep overview.
##
CTblLib.AtlasRepInfoLink:= function( groupname, zero )
    local func, n;

    if not IsBoundGlobal( "AllAtlasGeneratingSetInfos" ) then
      return fail;
    fi;
    func:= ValueGlobal( "AllAtlasGeneratingSetInfos" );
    n:= Length( CallFuncList( func, [ groupname ] ) );
    if n = 0 then
      return fail;
    fi;

    return rec( type:= "linkedtext",
                title:= "Atlas representations",
                display:= Concatenation( String( n ), " available" ),
                target:= [ "AtlasRep overview", [ groupname ] ] );
end;


##############################################################################
##
#F  CTblLib.GroupInfoList( <groupname>, <zero> )
##
##  `CTblLib.GroupInfoList' returns a "datalist" record
##  with information about the known group constructions of
##  the group <groupname>.
##
CTblLib.GroupInfoList:= function( groupname, zero )
    local grps, i, factors, genericnam, genericfun, entry, pos, info;

    grps:= ShallowCopy( GroupInfoForCharacterTable( groupname ) );
    for i in [ 1 .. Length( grps ) ] do
      if grps[i][1] = "DirectProductByNames" then
        factors:= [];
        genericnam:= [ "Cyclic", "Alternating", "Symmetric", "Dihedral" ];
        genericfun:= [ "C", "A", "S", "D" ];
        for entry in grps[i][2] do
          if Length( entry ) = 1 then
            Add( factors, entry[1] );
          elif Length( entry ) = 2 and IsPosInt( entry[2] ) then
            pos:= Position( genericnam, entry[1] );
            if pos = fail then
              Add( factors, fail );
            else
              Add( factors,
                   Concatenation( genericfun[ pos ], String( entry[2] ) ) );
            fi;
          else
            Add( factors, fail );
          fi;
        od;
        if fail in factors then
          Unbind( grps[i] );
        else
          grps[i]:= [ "DirectProduct", factors ];
        fi;
      elif grps[i][1] = "Aut" then
        info:= CTblLib.GroupInfoList( grps[i][2][1], 0 );
        if info = fail or Length( info.list ) = 0 then
          Unbind( grps[i] );
        else
          grps[i]:= [ "AutomorphismGroup",
                      Concatenation( "  ", info.list[1], "  " ) ];
        fi;
      fi;
    od;

    if IsEmpty( grps ) then
      return fail;
    fi;

    grps:= Compacted( grps );
    Sort( grps );  # sort here in order to get increasing degrees etc.
    grps:= List( grps, x -> [ x[1], String( x[2] ) ] );
    grps:= List( grps, x -> Concatenation( x[1], "(",
               x[2]{ [ 2 .. Length( x[2] )-1 ] }, ")" ) );

    return rec( type:= "datalist",
                title:= "Group constructions in GAP",
                list:= grps,
                colalign:= [ "left" ] );
end;


##############################################################################
##
#F  CTblLib.FromFusionsInfoList( <groupname>, <zero> )
##
##  `CTblLib.FromFusionsInfoList' returns a "datalist" record
##  with information about the known class fusions
##  from the character table of the group <groupname> to other tables.
##
CTblLib.FromFusionsInfoList:= function( groupname, zero )
    local fusions, list, name;

    # Get the fusion info.
    fusions:= CTblLib.TableValue( groupname, "FusionsTo" );
    if IsEmpty( fusions ) then
      return fail;
    fi;

    fusions:= ShallowCopy( fusions );
    Sort( fusions, CTblLib.CompareAsNumbersAndNonnumbers );
    list:= [];

    # Loop over the fusions.
    for name in fusions do
      Add( list, rec( type:= "linkedtext",
                      display:= name,
                      target:= [ "details page", [ name, 0 ] ] ) );
    od;

    return rec( type:= "datalist",
                title:= "Stored class fusions from this table",
                list:= list );
end;


##############################################################################
##
#F  CTblLib.NamesOfFusionSourcesInfoList( <groupname>, <zero> )
##
##  `CTblLib.NamesOfFusionSourcesInfoList' returns a "datalist" record
##  with information about the known class fusions
##  from other character tables to that of the group <groupname>.
##
CTblLib.NamesOfFusionSourcesInfoList:= function( groupname, zero )
    local fusions, list, name;

    # Get the fusion info.
    fusions:= CTblLib.TableValue( groupname, "NamesOfFusionSources" );
    if IsEmpty( fusions ) then
      return fail;
    fi;

    fusions:= ShallowCopy( fusions );
    Sort( fusions, CTblLib.CompareAsNumbersAndNonnumbers );
    list:= [];

    # Loop over the fusions.
    for name in fusions do
      Add( list, rec( type:= "linkedtext",
                      display:= name,
                      target:= [ "details page", [ name, 0 ] ] ) );
    od;
    return rec( type:= "datalist",
                title:= "Stored class fusions to this table",
                list:= list );
end;


##############################################################################
##
#F  CTblLib.BlocksInfoTable( <groupname>, <p> )
##
##  `CTblLib.BlocksInfoTable' returns a "datatable" record
##  with information about the <p>-blocks of the group <groupname>.
##
CTblLib.BlocksInfoTable:= function( groupname, p )
    local matrix, t, modtbl, info, i, row;

    matrix:= [];
    t:= CharacterTable( groupname );
    modtbl:= t mod p;
    if modtbl = fail then
#T we could show the numbers of ordinary/Brauer characters per block
      return fail;
    fi;

    info:= BlocksInfo( modtbl );

    for i in [ 1 .. Length( info ) ] do
      row:= [ String( i ), String( info[i].defect ) ];
      if info[i].defect = 0 then
        row[3]:= Concatenation( "chi_", String( info[i].ordchars[1] ),
                                ", phi_", String( info[i].modchars[1] ) );
      else
        row[3]:= rec( type:= "linkedtext",
                      display:= Concatenation(
                        String( Length( info[i].ordchars ) ), " x ",
                        String( Length( info[i].modchars ) ) ),
                      target:= [ "dec. matrix", [ groupname, p, i ] ] );
      fi;
      Add( matrix, row );
    od;

    return rec( title:= "p-blocks",
                type:= "datatable",
                header:= [ "nr", "defect", "matrix" ],
                matrix:= matrix,
                colalign:= [ "right", "right", "left" ] );
end;


##############################################################################
##
#V  CTblLib.OrdinaryTableInfo
#V  CTblLib.BrauerTableInfo
##
##  `CTblLib.OrdinaryTableInfo' is a list of functions that describe the
##  parts of information shown by `BrowseCTblLibInfo' and
##  `StringCTblLibInfo'.
#T and also by the HTML file generator `HTMLCreateGroupInfoFile'
##
CTblLib.OrdinaryTableInfo:= [

    # The group order shall be displayed as number and in factored form.
    function( groupname, zero )
      return rec( title:= "Group order",
                  type:= "factored order",
                  value:= CTblLib.TableValue( groupname, "Size" ) );
    end,

    # The number of classes shall be displayed.
    function( groupname, zero )
      return rec( title:= "Number of classes",
                  type:= "string",
                  value:= String( CTblLib.TableValue( groupname,
                                      "NrConjugacyClasses" ) ) );
    end,

    # The `InfoText' value shall be displayed.
    function( groupname, zero )
      return rec( title:= "InfoText value",
                  type:= "string",
                  value:= CTblLib.TableValue( groupname, "InfoText" ) );
    end,

    # Display the name of the main table of this table.
    function( groupname, zero )
      local name;
      name:= CTblLib.TableValue( groupname, "IdentifierOfMainTable" );
      if name = fail then
        return fail;
      fi;
      return rec( title:= "Main table",
                  type:= "linkedtext",
                  display:= name,
                  target:= [ "details page", [ name, 0 ] ] );
    end,

    # Display the names of duplicates of this table.
    function( groupname, zero )
      local names;
      names:= CTblLib.TableValue( groupname, "IdentifiersOfDuplicateTables" );
      if Length( names ) = 0 then
        return fail;
      fi;
      names:= List( names,
                    nam -> rec( type:= "linkedtext",
                                display:= nam,
                                target:= [ "details page", [ nam, 0 ] ] ) );
      return rec( type:= "datalist",
                  title:= "Duplicates",
                  list:= names );
    end,

    # Display info about maximal subgroups if available.
    CTblLib.MaxesInfoTable,

    # Display info about Sylow normalizers if available.
    CTblLib.SylowNormalizerInfoTable,

    # Display the available Brauer tables.
    CTblLib.BrauerTableInfoTable,

    # Display the link to AtlasRep if available.
    CTblLib.AtlasRepInfoLink,

    # Display the GroupInfo values.
    CTblLib.GroupInfoList,

    # The fusions on this table shall be mentioned.
    CTblLib.FromFusionsInfoList,

    # The fusions to this table shall be mentioned.
    CTblLib.NamesOfFusionSourcesInfoList,

    ];


CTblLib.BrauerTableInfo:= [

    # The group order shall be displayed as number and in factored form.
    function( groupname, p )
      return rec( title:= "Group order",
                  type:= "factored order",
                  value:= CTblLib.TableValue( groupname, "Size" ) );
    end,

    # The number of p-regular classes shall be displayed.
    function( groupname, p )
      local t;

      t:= CharacterTable( groupname );
      return rec( title:= "Number of p-regular classes",
                  type:= "string",
                  value:= Concatenation( String( Length(
                              Filtered( OrdersClassRepresentatives( t ),
                                        x -> x mod p <> 0 ) ) ),
                              " out of ",
                              String( NrConjugacyClasses( t ) ) ) );
    end,

    # Information about p-blocks shall be displayed.
    CTblLib.BlocksInfoTable,

    ];


#############################################################################
##
##  1. Transform the info into a plain string.
##


##############################################################################
##
#F  StringStandardTable( <obj> )
##
StringStandardTable:= function( obj )
    local width, colwidths, row, j, totalwidth, hlines, hlinem, hlinee,
          str, left, mid, right, n, res, header, matrix, frow;

    width:= function( entry )
      if IsString( entry ) then
        return Length( entry );
      else
        return Length( entry.display );
      fi;
    end;

    # Compute column widths.
    if IsBound( obj.header ) then
      colwidths:= List( obj.header, width );
    else
      colwidths:= ListWithIdenticalEntries( Length( obj.matrix[1] ), 0 );
    fi;
    for row in obj.matrix do
      for j in [ 1 .. Length( row ) ] do
        colwidths[j]:= Maximum( colwidths[j], width( row[j] ) );
      od;
    od;
    totalwidth:= Sum( colwidths, 0 ) + 4 + 3 * ( Length( colwidths ) - 1 );
    n:= Length( colwidths );
    if not CTblLib.ShowOnlyASCII() then
      mid:= List( colwidths, i -> RepeatedUTF8String( "─", i ) );
      hlines:= Concatenation( "┌─",
                   JoinStringsWithSeparator( mid, "─┬─" ), "─┐" );
      hlinem:= Concatenation( "├─",
                   JoinStringsWithSeparator( mid, "─┼─" ), "─┤" );
      hlinee:= Concatenation( "└─",
                   JoinStringsWithSeparator( mid, "─┴─" ), "─┘" );
      left:= "│ ";
      mid:= " │ ";
      right:= " │";
    else
      hlines:= RepeatedString( '-', totalwidth );
      hlinem:= hlines;
      hlinee:= hlines;
      left:= "| ";
      mid:= " | ";
      right:= " |";
    fi;
    for j in [ 1 .. n ] do
      if obj.colalign[j] = "left" then
        colwidths[j]:= -colwidths[j];
      fi;
    od;

    res:= [ hlines ];

    if IsBound( obj.header ) then
      header:= List( [ 1 .. n ],
                     i -> String( CTblLib.StringRender( obj.header[i] ),
                                  colwidths[i] ) );
      Add( res, Concatenation( left,
                    JoinStringsWithSeparator( header, mid ), right ) );
      Add( res, hlinem );
    fi;

    for row in obj.matrix do
      frow:= List( [ 1 .. n ],
                   i -> String( CTblLib.StringRender( row[i] ),
                                colwidths[i] ) );
      Add( res, Concatenation( left,
                    JoinStringsWithSeparator( frow, mid ), right ) );
    od;
    Add( res, hlinee );

    return res;
end;


##############################################################################
##
#F  CTblLib.StringRender( <obj> )
##
CTblLib.StringRender:= function( obj )
    local len, list, str, pos, i, entry, lentry;

    if IsString( obj ) then
      return obj;
    elif not ( IsRecord( obj ) and IsBound( obj.type ) ) then
      Error( "<obj> must be a string or a record with the component `type'" );
    fi;

    if   obj.type = "string" then
      return obj.value;
    elif obj.type = "linkedtext" then
      # Ignore the link information.
      return obj.display;
    elif obj.type = "datalist" then
      # Break the list into lines.
      # (In each line, add at least one entry, then fill up.
      # Note that `FormatParagraph' would be allowed to add line breaks
      # inside entries.)
      len:= SizeScreen()[1] - 5;
      list:= [];
      str:= Concatenation( CTblLib.StringRender( obj.list[1] ), "," );
      pos:= Length( str );
      for i in [ 2 .. Length( obj.list ) ] do
        entry:= CTblLib.StringRender( obj.list[i] );
        lentry:= Length( entry ) + 2;
        if pos + lentry > len then
          Add( list, str );
          str:= "";
          pos:= 0;
        fi;
        if pos <> 0 then
          Append( str, " " );
          pos:= pos + 1;
        fi;
        Append( str, entry );
        Append( str, "," );
        pos:= pos + lentry - 1;
      od;
      Unbind( str[ pos ] );
      Add( list, str );

      return list;
    elif obj.type = "datatable" then
      return StringStandardTable( obj );
    elif obj.type = "factored order" then
      return Concatenation( String( obj.value ), " = ",
                 StringPP( obj.value ) );
    else
      Error( "unknown type `", obj.type, "'" );
    fi;
end;


##############################################################################
##
#F  DisplayCTblLibInfo( <tbl> )
#F  DisplayCTblLibInfo( <name>[, <p>] )
#F  StringCTblLibInfo( <tbl> )
#F  StringCTblLibInfo( <name>[, <p>] )
##
##  <#GAPDoc Label="DisplayCTblLibInfo">
##  <ManSection>
##  <Func Name="DisplayCTblLibInfo" Arg='tbl' Label="for a character table"/>
##  <Func Name="DisplayCTblLibInfo" Arg='name[, p]' Label="for a name"/>
##  <Func Name="StringCTblLibInfo" Arg='tbl' Label="for a character table"/>
##  <Func Name="StringCTblLibInfo" Arg='name[, p]' Label="for a name"/>
##
##  <Description>
##  When <Ref Func="DisplayCTblLibInfo" Label="for a character table"/>
##  is called with an ordinary or modular character table <A>tbl</A> then
##  an overview of the information available for this character table
##  is shown via the function that is given by the user preference
##  <Ref Subsect="subsect:displayfunction"/>.
##  When <Ref Func="DisplayCTblLibInfo" Label="for a name"/>
##  is called with a string <A>name</A> that is an admissible name for
##  an ordinary character table then the overview for this character table
##  is shown.
##  If a prime integer <A>p</A> is entered in addition to <A>name</A> then
##  information about the <A>p</A>-modular character table is shown instead.
##  <P/>
##  An interactive variant of
##  <Ref Func="DisplayCTblLibInfo" Label="for a name"/> is
##  <Ref Func="BrowseCTblLibInfo"/>.
##  <P/>
##  The string that is shown by
##  <Ref Func="DisplayCTblLibInfo" Label="for a name"/> can be computed using
##  <Ref Func="StringCTblLibInfo" Label="for a name"/>,
##  with the same arguments.
##  <P/>
##  <Example><![CDATA[
##  gap> StringCTblLibInfo( CharacterTable( "A5" ) );;
##  gap> StringCTblLibInfo( CharacterTable( "A5" ) mod 2 );;
##  gap> StringCTblLibInfo( "A5" );;
##  gap> StringCTblLibInfo( "A5", 2 );;
##  ]]></Example>
##  </Description>
##  </ManSection>
##  <#/GAPDoc>
##
BindGlobal( "StringCTblLibInfo", function( groupname, p... )
    local name, title, attr, str, info, fun, val, str2;

    if Length( p ) = 0 and IsCharacterTable( groupname ) then
      p:= UnderlyingCharacteristic( groupname );
      groupname:= Identifier( groupname );
      if p <> 0 then
        name:= PartsBrauerTableName( groupname );
        if name <> fail then
          groupname:= name.ordname;
        fi;
      fi;
    elif Length( p ) = 0 and IsString( groupname ) then
      p:= 0;
    elif Length( p ) = 1 and IsString( groupname ) and IsPosInt( p[1] ) then
      p:= p[1];
    else
      Error( "usage: StringCTblLibInfo( <tbl> ) or\n",
             "  StringCTblLibInfo( <name>[, <p>] )" );
    fi;

    name:= LibInfoCharacterTable( groupname );
    if name = fail then
      return "";
    fi;
    groupname:= name.firstName;

    # Construct the information about `groupname'.
    title:= Concatenation( "Character Table info for ", groupname );
    if p <> 0 then
      Append( title, Concatenation( " mod ", String( p ) ) );
    fi;

    # header line
    attr:= IsBound( TextAttr ) and IsRecord( TextAttr );
    if attr then
      str:= ShallowCopy( TextAttr.underscore );
    else
      str:= "";
    fi;
    Append( str, title );
    if attr then
      Append( str, TextAttr.reset );
    fi;
    Append( str, "\n\n" );

    if p = 0 then
      info:= CTblLib.OrdinaryTableInfo;
    else
      info:= CTblLib.BrauerTableInfo;
    fi;

    for fun in info do
      val:= fun( groupname, p );
      if val <> fail then
        if attr then
          Append( str, TextAttr.bold );
        fi;
        Append( str, val.title );
        Append( str, ":" );
        if attr then
          Append( str, TextAttr.reset );
        fi;
        Append( str, "\n  " );
        str2:= CTblLib.StringRender( val );
        if IsString( str2 ) then
          str2:= ReplacedString( str2, "\n", "\n  " );
        else
          str2:= JoinStringsWithSeparator( str2, "\n  " );
        fi;
        Append( str, str2 );
        Append( str, "\n\n" );
      fi;
    od;

    return str;
end );


BindGlobal( "DisplayCTblLibInfo", function( arg )
    local str, width, fun;

    str:= CallFuncList( StringCTblLibInfo, arg );
    if str <> "" then
      width:= SizeScreen()[1] - 2;
      if CTblLib.ShowOnlyASCII() then
        str:= List( SplitString( str, "\n" ),
                l -> InitialSubstringUTF8String( l, width, "*" ) );
      else
        str:= List( SplitString( str, "\n" ),
                l -> InitialSubstringUTF8String( l, width, "⋯" ) );
      fi;

      fun:= EvalString( UserPreference( "AtlasRep", "DisplayFunction" ) );
      fun( JoinStringsWithSeparator( str, "\n" ) );
    fi;
end );


#############################################################################
##
#E

