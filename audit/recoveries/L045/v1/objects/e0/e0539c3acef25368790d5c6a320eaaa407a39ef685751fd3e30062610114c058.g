#############################################################################
##
#W  maketbl.g           GAP character table library             Thomas Breuer
##
##  This file contains the function 'CTblLib.RecomputeTOC', which produces
##  the files 'data/extinfo.json', 'data/firstnames.json',
##  'data/fusionsources.json', 'data/tom_tbl.json', 'data/othernames.json',
##  'data/version', 'data/attr*.json', 'data/grp_*.json' of the CTblLib
##  package of GAP 4, from the data files 'data/ct[go]*.tbl'.
##  (In earlier times, this task was done by the 'awk' script 'etc/maketbl',
##  and the computed data were written to the file 'data/ctprimar.tbl'.)
##
##  For the conventions about the contents of the table library files,
##  see '../gap4/ctadmin.gd'.
##
##  If a line has more than 78 characters or ends with a backslash,
##  a warning is printed.
##
##  The following calls to 'ARC' are used by this program.
##
##  ARC("<name>","maxes",<list>);
##      The string "<name>M<i>" is constructed as an admissible name for
##      the <i>-th entry of <list> (which may contain holes).
##
##  ARC("<name>","isSimple",<list>);
##      This is used just in order to check whether 'extInfo' is available
##      exactly for tables of simple groups.
##
##  ARC("<name>","extInfo",<list>);
##      For simple tables <name>, the info in <list> will be stored in
##      'LIBLIST.simpleInfo'.
##

LoadPackage( "CTblLib", false );

#T local function, eventually should be available in IO!
CTblLib.CurrentDateTimeString:= function( options )
    local name, str, out;

    name:= Filename( DirectoriesSystemPrograms(), "date" );
    if name = fail then
      return "unknown";
    fi;
    str:= "";
    out:= OutputTextString( str, true );
    Process( DirectoryCurrent(), name, InputTextNone(), out, options );
    CloseStream( out );
    Unbind( str[ Length( str ) ] );
    return str;
end;


ReplaceDataFileIfNecessary:= function( outstr, dir, outfile, from )
    local oldcontents, frompos1, frompos2, topos1, topos2, bakfile,
          diff, str, out;

    outfile:= Filename( dir[1], outfile );
    oldcontents:= StringFile( outfile );
    frompos1:= PositionSublist( oldcontents, from );
    frompos2:= PositionSublist( outstr, from );
    topos1:= Length( oldcontents );
    topos2:= Length( outstr );
    if frompos1 <> fail and frompos2 <> fail and
       oldcontents{ [ frompos1 .. topos1 ] }
       = outstr{ [ frompos2 .. topos2 ] } then
      Print( "#I  no update of '", outfile, "' is necessary\n" );
      return false;
    fi;

    # Save the old file.
    bakfile:= Concatenation( outfile, "~" );
    Exec( "mv", outfile, bakfile );

    # Create the new file (without trailing backslashes).
    FileString( outfile, outstr );

    # Print the differences between old and new version.
    diff:= Filename( DirectoriesSystemPrograms(), "diff" );
    str:= "";
    out:= OutputTextString( str, true );
    Process( DirectoryCurrent(), diff, InputTextNone(), out,
             [ bakfile, outfile ] );
    CloseStream( out );
    Print( "#I  differences for ", outfile, ":\n" );
    Print( str );
    return true;
end;


#############################################################################
##
#F  CTblLib.RecomputeTOC( ["attributes"] )
##
##  - replaces the files 'data/extinfo.json', 'data/firstnames.json',
##    'data/fusionsources.json', 'data/othernames.json', 'data/tom_tbl.json',
##    and 'data/version' by updated versions if necessary,
##    according to the data files 'data/cto*.tbl' and 'data/ctg*.tbl',
##    saves backups of the old contents in files with suffix '~'
##
##  - updates the attributes listed in 'CTblLib.SupportedAttributes'
##    if necessary
##
##  If the optional argument '"attributes"' is given then the data files of
##  the attributes listed in
##  'CTblLib.Data.attributesRelevantForGroupInfoForCharacterTable',
##  except the attribute "indiv", are recomputed and replaced.
##
CTblLib.RecomputeTOC:= function( arg )
    local match, matchstart, matchend, app, amend, setnewname, dir, infiles,
          ordinfiles, modinfiles, clminfiles, firstnames, allnames,
          lowerposition, simplenames, extinfo, tbltom, fusions, currname,
          toolong, backslash, infile, lines, i, line, nam, tolo, spl, k,
          entry, l, map, known, datestr, update, outstr, list, currfile,
          pair, currlist, j, fussrc, outfile, save, idenum, attrnames, pairs,
          attrid, attrid2, order, attr, oldcontents, bakfile, diff, str, out;

    # Avoid reading data files more than once.
    SetUserPreference( "ctbllib", "UnloadCTblLibFiles", false );

    match:= function( str, substr )
      return PositionSublist( str, substr ) <> fail;
    end;

    matchstart:= function( str, prefix )
      return Length( prefix ) <= Length( str ) and
             str{ [ 1 .. Length( prefix ) ] } = prefix;
    end;

    matchend:= function( str, suffix )
      return Length( suffix ) <= Length( str ) and
             str{ [ 1 - Length( suffix ) .. 0 ] + Length( str ) } = suffix;
    end;

    app:= function( arg )
      local string;
      for string in arg do
        Append( outstr, string );
      od;
    end;

    amend:= function( line, prefix, toadd, suffix, indent )
      if Sum( List( [ line, prefix, toadd, suffix ], Length ) ) <= 77 then
        return Concatenation( line, prefix, toadd, suffix );
      else
        app( line, "\n" );
        return Concatenation( indent, prefix, toadd, suffix );
      fi;
    end;

    setnewname:= function( new, old )
      local known;

      known:= First( allnames, x -> new in x[2] );
      if known = fail then
        known:= First( allnames, x -> old = x[1] );
        if known = fail then
          Add( allnames, [ old, [ new ] ] );
        else
          AddSet( known[2], new );
        fi;
      elif old <> known[1] then
        Print( "#E  clash: name '", new, "' for tables '", old, "' and '",
               known[1], "'\n" );
      else
#T Omit this warning if the first name of the table is <nam>M<n>?
        Print( "#E  name '", new, "' defined twice for table '", old, "'\n" );
      fi;
    end;

    # input files
    dir:= DirectoriesPackageLibrary( "ctbllib", "data" );
    infiles:= SortedList( DirectoryContents( Filename( dir, "" ) ) );
    ordinfiles:= Filtered( infiles,
                     f -> matchstart( f, "cto" ) and matchend( f, ".tbl" ) );
    modinfiles:= Filtered( infiles,
                     f -> matchstart( f, "ctb" ) and matchend( f, ".tbl" ) );
    clminfiles:= Filtered( infiles,
                     f -> matchstart( f, "clm" ) and matchend( f, ".tbl" ) );

    # Initialize the lists of names.
    firstnames:= [];
    allnames:= [];
    lowerposition:= [];
    simplenames:= [];
    extinfo:= [];
    tbltom:= [];
    fusions:= [];
    currname:= "(unbound)";
    toolong:= rec();
    backslash:= rec();

    # Loop over the input files.
    for infile in ordinfiles do
      lines:= SplitString( StringFile( Filename( dir, infile ) ), "\n" );
      i:= 1;
      while i <= Length( lines ) do

        line:= lines[i];

        # Check for lines with more than 78 characters.
        if 78 < Length( line ) then
          if not IsBound( toolong.( infile ) ) then
            toolong.( infile ):= [ line ];
          else
            Add( toolong.( infile ), line );
          fi;
        fi;

        # Collect lines with trailing backslashes.
        if matchend( line, "\\" ) then
          if not IsBound( backslash.( infile ) ) then
            backslash.( infile ):= [ line ];
          else
            Add( backslash.( infile ), line );
          fi;
        fi;

        # Store the first names and the corresponding file names.
        if matchstart( line, "MOT" ) then
          nam:= SplitString( line, "\"" )[2];
          currname:= nam;
          tolo:= LowercaseString( nam );
          if tolo in lowerposition then
            Print( "#E  double name ", tolo, " (ignored in ", infile, ")\n" );
          else
            Add( firstnames, [ nam, infile ] );
            AddSet( lowerposition, tolo );
          fi;
        fi;

        # Store the other names of the tables.
        if matchstart( line, "ALN(" ) then
          spl:= SplitString( line, "\"" );
          nam:= spl[2];
          if spl[3] <> ",[" then
            Print( "#E  ALN call for '", nam, "': corrupted syntax\n" );
          fi;
          if nam <> currname then
            Print( "#E  ALN call for '", nam, "' under '", currname, "'\n" );
          fi;
          for k in [ 4 .. Length( spl ) ] do
            if spl[k] <> "" and spl[k] <> "," and spl[k] <> "]);" then
              setnewname( LowercaseString( spl[k] ), nam );
            fi;
          od;

          # Scan until the assignment is complete.
          while spl[ Length( spl ) ] <> "]);" do
            i:= i + 1;
            line:= lines[i];
            spl:= SplitString( line, "\"" );
            for entry in spl do
              if entry <> "" and entry <> "," and entry <> "]);" then
                setnewname( LowercaseString( entry ), nam );
              fi;
            od;
          od;
        fi;

        if matchstart( line, "ARC(" ) then
          spl:= SplitString( line, "\"" );
          if spl[2] <> currname then
            Print( "#E  ARC call for '", spl[2], "' under '", currname, "'\n" );
          fi;
        fi;

        # Store the extension info for simple groups.
        if matchstart( line, "ARC(" ) and match( line, "\"isSimple\"" ) then
          spl:= SplitString( line, "\"" );
          if spl[5] = ",true);" then
            Add( simplenames, spl[2] );
          fi;
        fi;
        if matchstart( line, "ARC(" ) and match( line, "\"extInfo\"" ) then
          Add( extinfo, SplitString( line, "\"" ){ [ 6, 2, 8 ] } );
        fi;

        # Create the names defined by 'maxes' components.
        if matchstart( line, "ARC(" ) and match( line, "\"maxes\"" ) then
          spl:= SplitString( line, "\"" );
          nam:= LowercaseString( spl[2] );
          l:= Number( spl[5], x -> x = ',' );
          for k in [ 6 .. Length( spl ) ] do
            entry:= spl[k];
            if ',' in entry and ForAll( entry, x -> x = ',' ) then
              l:= l + Number( entry, x -> x = ',' );
            elif not ';' in entry then
              tolo:= Concatenation( nam, "m", String( l ) );
              if tolo <> LowercaseString( entry ) then
                setnewname( tolo, entry );
              fi;
            fi;
          od;

          # Scan until the assignment is complete.
          while not ';' in spl[ Length( spl ) ] do
            i:= i + 1;
            line:= lines[i];
            spl:= SplitString( line, "\"" );
            for entry in spl do
              if ',' in entry and ForAll( entry, x -> x = ',' ) then
                l:= l + Number( entry, x -> x = ',' );
              elif entry <> "" and not ';' in entry then
                tolo:= Concatenation( nam, "m", String( l ) );
                if tolo <> LowercaseString( entry ) then
                  setnewname( tolo, entry );
                fi;
              fi;
            od;
          od;
        fi;

        # Store the info needed for the map to the names of tables of marks.
        if matchstart( line, "ARC(" ) and match( line, "\"tomfusion\"" ) then
          spl:= SplitString( line, "\"" );
          Add( tbltom, [ spl[6], spl[2] ] );
        fi;

        # Store the source and destination of fusions (just for checks).
        if matchstart( line, "ALF(" ) then
          spl:= SplitString( line, "\"" );
          if spl[2] <> currname then
            Print( "#E  ALF call for '", spl[2], "' under '", currname, "'\n" );
          fi;
          map:= spl[5];
          if map[ Length( map ) ] in ";[" then
            # The complete assignment fits in one line.
            map:= map{ [ 2 .. Length( map ) - 2 ] };
          else
            # There are more than one line to scan.
            map:= map{ [ 2 .. Length( map ) ] };
            i:= i + 1;
            line:= lines[i];
            while not line[ Length( line ) ] in ";[" do
              Append( map, "\n  " );
              Append( map, line );
              i:= i + 1;
              line:= lines[i];
            od;
            Append( map, "\n  " );
            Append( map, line{ [ 1 .. Length( line ) - 2 ] } );
          fi;
          known:= Filtered( fusions, x -> x[1] = spl[2] and x[2] = spl[4] );
          if ForAny( known, x -> x[3] = map ) then
            Print( "#E  ", infile, ": remove duplicate fusion ",
                   spl[2], " -> ", spl[4], "\n" );
          elif not IsEmpty( known ) then
            Print( "#E  ", infile, ": several fusions ",
                   spl[2], " -> ", spl[4], "?\n" );
            Add( fusions, [ spl[2], spl[4], map ] );
          else
            Add( fusions, [ spl[2], spl[4], map ] );
          fi;
        fi;

        i:= i + 1;
      od;
    od;

    # Print the warnings about the files.
    for infile in RecNames( toolong ) do
      Print( "#E  ", Length( toolong.( infile ) ),
             " too long line(s) in ", infile, ", first is\n",
             toolong.( infile )[1], "\n" );
    od;
    for infile in RecNames( backslash ) do
      Print( "#E  ", Length( backslash.( infile ) ),
             " trailing backslash(es) in ", infile, ", first is\n",
             backslash.( infile )[1], "\n" );
    od;

    # Check whether for the Brauer tables in the file 'ctb<id>.tbl',
    # the ordinary tables are in 'cto<id>.tbl'.
    for infile in modinfiles do
      for line in SplitString( StringFile( Filename( dir, infile ) ), "\n" ) do
        if matchstart( line, "MBT(" ) then
          spl:= SplitString( line, "\"" );
          if not [ spl[2], ReplacedString( infile, "ctb", "cto" ) ]
                 in firstnames then
            Print( "#E  for ", spl[2], ", a modular table is in ", infile,
                   "\n" );
          fi;
        fi;
      od;
    od;

    datestr:= CTblLib.CurrentDateTimeString( [ "-u", "+%d-%b-%Y, %T UTC" ] );
    update:= false;

    # Print info about the table identifiers per file.
    outstr:= Concatenation(
         "[\n[\n\"Version ", datestr, ". \",\n",
         "\"This file contains a list of length two, \",\n",
         "\"this description at pos. 1 \",\n",
         "\"and at pos. 2 the lexicographically sorted list of those \",\n",
         "\"pairs [<filename>, <ids>] where <ids> is the list of \",\n",
         "\"the identifiers of those tables which are stored in the file\",\n",
         "\"'data/<filename>.tbl' of GAP's CTblLib package.\"",
         "\n],\n[\n" );
    list:= [];
    currfile:= "";
    for pair in firstnames do
      if pair[2] <> currfile then
        currfile:= pair[2];
        currlist:= [];
        Add( list,
             [ currfile{ [ 1 .. Position( currfile, '.' )-1 ] }, currlist ] );
      fi;
      Add( currlist, pair[1] );
    od;
    Append( outstr,
            JoinStringsWithSeparator( List( list,
                x -> ReplacedString( String( x ), " ", "" ) ), ",\n" ) );
    Append( outstr, "\n]\n]\n" );
    update:= ReplaceDataFileIfNecessary( outstr, dir, "firstnames.json", "UTC" )
             or update;

    # Check whether the names that occur in fusions are valid.
    firstnames:= List( firstnames, x -> x[1] );
    for pair in fusions do
      if not pair[1] in firstnames then
        Print( "#E  fusion source '", pair[1], "' not valid first name\n" );
      fi;
      if not pair[2] in firstnames then
        Print( "#E  fusion destination '", pair[2],
               "' not valid first name\n" );
      fi;
    od;

    # Check whether the admissible names point to valid first names.
    for pair in allnames do
      if not pair[1] in firstnames then
        Print( "#E  no table \"", pair[1], "\"\n" );
      fi;
    od;

    # Print info about the tables of simple groups, their Schur multipliers
    # and outer automorphism groups to the file 'extinfo.json' if necessary.
    outstr:= Concatenation(
         "[\n[\n\"Version ", datestr, ". \",\n",
         "\"This file contains a list of length two, \",\n",
         "\"this description at pos. 1 \",\n",
         "\"and at pos. 2 the list of those triples [<mult>, <simp>, <out>] \",\n",
         "\"where <simp> is the identifier of the character table of a simple group \",\n",
         "\"in GAP's CTblLib package, \",\n",
         "\"and <mult> and <out> are strings that describe the structures of \",\n",
         "\"the Schur multiplier and of the outer automorphism group of this group.\"",
         "\n],\n[\n" );
    list:= [];
    for entry in extinfo do
      if entry[2] in simplenames then
        Add( list, Concatenation( "[\"", entry[1], "\",\"", entry[2],
                                  "\",\"", entry[3], "\"]" ) );
      else
        Print( "#E  extInfo for nonsimple table ", entry[2], "?\n" );
      fi;
    od;
    Append( outstr, JoinStringsWithSeparator( list, ",\n" ) );
    Append( outstr, "\n]\n]\n" );
    ReplaceDataFileIfNecessary( outstr, dir, "extinfo.json", "UTC" );

    # Print the map from character table identifiers to identifiers of
    # tables of marks to the file 'tom_tbl.json' if necessary.
    outstr:= Concatenation(
         "[\n[\n\"Version ", datestr, ". \",\n",
         "\"This file contains a list of length three, \",\n",
         "\"this description at pos. 1, \",\n",
         "\"the identifiers of tables of marks from GAP's TomLib package at pos. 2\",\n",
         "\"and the corresponding identifiers of character tables \",\n",
         "\"from GAP's CTblLib package at pos. 3.\"" );

    for i in [ 1, 2 ] do
      app( "\n],\n[\n" );
      line:= "";
      for j in [ 1 .. Length( tbltom )-1 ] do
        pair:= tbltom[j];
        line:= amend( line, "\"", LowercaseString( pair[i] ), "\",", "" );
      od;
      line:= amend( line, "\"",
                    LowercaseString( tbltom[ Length( tbltom ) ][i] ),
                    "\"", "" );
      app( line );
    od;
    app( "\n]\n]\n" );
    update:= ReplaceDataFileIfNecessary( outstr, dir, "tom_tbl.json", "UTC" )
             or update;

    # Print the json file with the list of fusion sources.
    outstr:= Concatenation(
         "[\n[\n\"Version ", datestr, ". \",\n",
         "\"This file contains a list of length two, \",\n",
         "\"this description at pos. 1 \",\n",
         "\"and at pos. 2 the lexicographically sorted list of those \",\n",
         "\"pairs [<id>, <ids>] where <ids> is the nonempty list of \",\n",
         "\"the identifiers of those tables for which a class fusion \",\n",
         "\"to the table with identifier <id> is part of \",\n",
         "\"GAP's CTblLib package.\"\n],\n[\n" );
    list:= [];
    for nam in Set( firstnames ) do
      fussrc:= List( Filtered( fusions, pair -> pair[2] = nam ), l -> l[1] );
      if Length( fussrc ) > 0 then
        Add( list, Concatenation( "[\"", nam, "\",[\"",
          JoinStringsWithSeparator( fussrc, "\",\"" ), "\"]]" ) );
      fi;
    od;
    Append( outstr, JoinStringsWithSeparator( list, ",\n" ) );
    Append( outstr, "\n]\n]\n" );
    update:= ReplaceDataFileIfNecessary( outstr, dir, "fusionsources.json", "UTC" )
             or update;

    # Print the json file with the list of admissible names (lowercase).
    outstr:= Concatenation(
         "[\n[\n\"Version ", datestr, ". \",\n",
         "\"This file contains a list of length two, \",\n",
         "\"this description at pos. 1 \",\n",
         "\"and at pos. 2 the lexicographically sorted list of those \",\n",
         "\"lists [<id>, <nam1>, <nam2>, ...] where <id> is an identifier \",\n",
         "\"of an ordinary table in GAP's CTblLib package \",\n",
         "\"for which <nam1>, <nam2>, ... are other admissible names, \",\n",
         "\"normalized to lower case.\"\n],\n[\n" );
    list:= [];
    for nam in Set( firstnames ) do
      l:= First( allnames, x -> x[1] = nam );
      if l <> fail then
        Add( list, Concatenation( "[\"",
                       JoinStringsWithSeparator( Concatenation( [ nam ], l[2] ),
                           "\",\"" ), "\"]" ) );
      fi;
    od;
    Append( outstr, JoinStringsWithSeparator( list, ",\n" ) );
    Append( outstr, "\n]\n]\n" );
    ReplaceDataFileIfNecessary( outstr, dir, "othernames.json", "UTC" );

    # Update the version string if necessary.
    # We take the highest version among those from 'firstnames.json',
    # 'fusionsources.json', 'tom_tbl.json';
    # this version must then coincide with the one of the 'attr_*.json' and
    # 'grp_*.json' files.
    if update then
      ReplaceDataFileIfNecessary( datestr, dir, "version", "" );
    fi;

    # Check whether the data files can be read into GAP.
    outfile:= Filename( DirectoryHome(),
                        "gap/3.5/bin/gap-ibm-i386-linux-gcc2" );
#T o.k.?
    if outfile <> fail and IsExecutableFile( outfile ) then

      Print( "#I  check loading all data files with GAP 3.5\n" );

      # Call GAP without library functions, and check that the table files
      # 'clm*', 'ctb*', and 'cto*' can be read and do contain only admissible
      # function calls.
      # All functions in the list given below
      # are defined in the 'ctadmin' file.
      outstr:= "";
      app( "LIBTABLE:=\n",
           "rec( LOADSTATUS:= rec(), clmelab:= [], clmexsp:= [] );;\n",
           "GALOIS:= ( x -> x );;\n",
           "TENSOR:= ( x -> x );;\n",
           "ALF:= function( arg ); end;;\n",
           "ACM:= function( arg ); end;;\n",
           "ARC:= function( arg ); end;;\n",
           "ALN:= function( arg ); end;;\n",
           "MBT:= function( arg ); end;;\n",
           "MOT:= function( arg ); end;;\n" );
      for infile in Concatenation( clminfiles, ordinfiles, modinfiles ) do
        app( "READ(\"", Filename( dir, infile ), "\");\n" );
      od;

      FileString( "maketbl.checkin", outstr );
      Exec( Concatenation( outfile, " -b -l ~ ",
                "< maketbl.checkin > maketbl.checkout" ) );
      Exec( "sed -e '1d;/^gap> true$/d;/^gap> $/d' < maketbl.checkout" );
      RemoveFile( "maketbl.checkin" );
      RemoveFile( "maketbl.checkout" );

    fi;

    # Load the updated table of contents.
    save:= LIBLIST.PrivateBrauerTables;
    RereadPackage( "ctbllib", "gap4/ctprimar.g" );
    for nam in RecNames( LIBTABLE.LOADSTATUS ) do
      Unbind( LIBTABLE.LOADSTATUS.( nam ) );
    od;
    LIBLIST.PrivateBrauerTables:= save;

    # Update the supported attributes if necessary.
    # (Always recomputing ALL attributes would be too expensive.
    # We must exclude 'KnowsSomeGroupInfo' because of its needed attributes.)
    if Length( arg ) = 1 and arg[1] = "attributes" or update then
      if LoadPackage( "Browse" ) <> true then
        Print( "#E  cannot load 'Browse', ",
               "attribute computations impossible\n" );
        return;
      fi;

      idenum:= CTblLib.Data.IdEnumerator;

      DatabaseIdEnumeratorUpdate( idenum );

      attrnames:= Filtered( RecNames( idenum.attributes ),
                      nam -> IsBound( idenum.attributes.( nam ).name ) and
                             idenum.attributes.( nam ).name in
                                 CTblLib.SupportedAttributes and
                             nam <> "KnowsSomeGroupInfo" );

      if Length( arg ) = 1 and arg[1] = "attributes" then
        if LoadPackage( "mfer" ) <> true then
          Print( "#E  cannot load 'mfer', ",
                 "attribute 'atlas' will be incomplete\n" );
        fi;
        if LoadPackage( "ctblocks" ) <> true then
          Print( "#E  cannot load 'ctblocks', ",
                 "attribute 'atlas' will be incomplete\n" );
        fi;
        Append( attrnames,
            CTblLib.Data.attributesRelevantForGroupInfoForCharacterTable );
        Add( attrnames, "KnowsSomeGroupInfo" );
      fi;

      # Add also the needed attributes to the list.
      # ('DatabaseAttributeCompute' would automatically update them,
      # but we want to print the differences.)
      pairs:= [];
      for attrid in attrnames do
        attr:= idenum.attributes.( attrid );
        for attrid2 in attr.neededAttributes do
          Add( pairs, [ attrid2, attrid ] );
        od;
      od;
      order:= LinearOrderByPartialWeakOrder( pairs, [] );
      order:= Concatenation( order.cycles );
      attrnames:= Concatenation( order, Difference( attrnames, order ) );
      attrnames:= Filtered( attrnames, x -> x <> "indiv" );

      SetInfoLevel( InfoDatabaseAttribute, 1 );

      for attrid in attrnames do
        attr:= idenum.attributes.( attrid );
        if IsBound( attr.datafile ) then
          # We want to recompute the values also if the version number
          # has not changed.
          # Note that the character table part of the data may be unchanged,
          # but some data in AtlasRep may have become newly available.
          DatabaseAttributeCompute( idenum, attr.identifier, "automatic" );
          outstr:= DatabaseAttributeString( idenum,
                       "CTblLib.Data.IdEnumerator", attr.identifier, "JSON" );

          # Compare the file with the current contents.
          outfile:= attr.datafile;
          oldcontents:= StringFile( outfile );
          if oldcontents = fail then
            oldcontents:= "";
          fi;
          if oldcontents = outstr then
            Print( "#I  no update necessary for attribute ", attrid, "\n" );
          else
            # Save the old file.
            bakfile:= Concatenation( outfile, "~" );
            if IsExistingFile( outfile ) then
              Exec( "mv", outfile, bakfile );
            fi;

            # Create the new file (without trailing backslashes).
            FileString( outfile, outstr );

            # Print the differences between old and new version.
            if IsExistingFile( bakfile ) then
              diff:= Filename( DirectoriesSystemPrograms(), "diff" );
              str:= "";
              out:= OutputTextString( str, true );
              Process( DirectoryCurrent(), diff, InputTextNone(), out,
                       [ bakfile, outfile ] );
              CloseStream( out );
              if not IsEmpty( str ) then
                Print( "#I  differences for ", outfile, ":\n" );
                Print( str );
              fi;
            fi;
          fi;
        fi;
      od;
    fi;

end;


#############################################################################
##
#E

