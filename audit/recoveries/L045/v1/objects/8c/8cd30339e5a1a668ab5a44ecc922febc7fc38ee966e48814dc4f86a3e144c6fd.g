#############################################################################
##
#W  ctprimar.g                  GAP table library               Thomas Breuer
##
##  Reading this file loads the data of the GAP character table library.
##


#############################################################################
##
##  Read the relevant data files that were produced by
##  'CTblLib.RecomputeTOC()'.
##
CallFuncList( function()
  local dir, file, str, evl, i, l, len, nam;

  dir:= DirectoriesPackageLibrary( "ctbllib", "data" );

  file:= Filename( dir[1], "firstnames.json" );
  str:= StringFile( file );
  if str = fail then
    Error( "the data file '", file, "' is not available" );
  fi;
  evl:= EvalString( str )[2];
  LIBLIST.files:= [];
  LIBLIST.filenames:= [];
  LIBLIST.firstnames:= [];
  for i in [ 1 .. Length( evl ) ] do
    l:= evl[i];
    Add( LIBLIST.files, l[1] );
    Append( LIBLIST.filenames,
            ListWithIdenticalEntries( Length( l[2] ), i ) );
    Append( LIBLIST.firstnames, l[2] );
  od;
  MakeImmutable( LIBLIST.files );
  MakeImmutable( LIBLIST.filenames );
  MakeImmutable( LIBLIST.firstnames );
  LIBLIST.firstnames_orig:= LIBLIST.firstnames;

  file:= Filename( dir[1], "othernames.json" );
  str:= StringFile( file );
  if str = fail then
    Error( "the data file '", file, "' is not available" );
  fi;
  evl:= MakeImmutable( EvalString( str )[2] );
  if not IsSSortedList( evl ) then
    Error( "the list in '", file, "' is assumed to be sorted" );
  fi;
  len:= Length( evl );
  LIBLIST.allnames:= [];
  LIBLIST.position:= [];
  for i in [ 1 .. Length( LIBLIST.firstnames ) ] do
    nam:= LIBLIST.firstnames[i];
    Add( LIBLIST.allnames, LowercaseString( nam ) );
    Add( LIBLIST.position, i );
    l:= PositionSorted( evl, [ nam ] );
    if l <= len and evl[l][1] = nam then
      l:= evl[l];
      Append( LIBLIST.allnames, l{ [ 2 .. Length( l ) ] } );
      Append( LIBLIST.position, ListWithIdenticalEntries( Length( l ) - 1, i ) );
    fi;
  od;
  SortParallel( LIBLIST.allnames, LIBLIST.position );

  file:= Filename( dir[1], "fusionsources.json" );
  str:= StringFile( file );
  if str = fail then
    Error( "the data file '", file, "' is not available" );
  fi;
  LIBLIST.fusionsource:= List( LIBLIST.firstnames, x -> [] );
  for l in EvalString( str )[2] do
    LIBLIST.fusionsource[ Position( LIBLIST.firstnames, l[1] ) ]:= l[2];
  od;
  MakeImmutable( LIBLIST.fusionsource );

  file:= Filename( dir[1], "extinfo.json" );
  str:= StringFile( file );
  if str = fail then
    Error( "the data file '", file, "' is not available" );
  fi;
  LIBLIST.simpleInfo:= MakeImmutable( EvalString( str )[2] );

  # Add the info about sporadic simple groups.
  LIBLIST.sporadicSimple := MakeImmutable( [
  "M11", "M12", "J1", "M22", "J2", "M23", "HS", "J3",
  "M24", "McL", "He", "Ru", "Suz", "ON", "Co3", "Co2",
  "Fi22", "HN", "Ly", "Th", "Fi23", "Co1", "J4", "F3+",
  "B", "M" ] );

  # Add the info about generic tables.
  file:= Filename( dir[1], "ctgeneri.tbl" );
  str:= StringFile( file );
  if str = fail then
    Error( "the data file '", file, "' is not available" );
  fi;
  LIBLIST.GENERIC:= rec( allnames:= [], firstnames:= [] );
  for l in Filtered( SplitString( str, "\n" ),
                     x -> StartsWith( x, "LIBTABLE" ) and
                          PositionSublist( x, "(\"" ) <> fail ) do
    nam:= SplitString( l, "\"" )[2];
    Add( LIBLIST.GENERIC.allnames, LowercaseString( nam ) );
    Add( LIBLIST.GENERIC.firstnames, nam );
  od;

  # Prepare for 'NotifyBrauerTables'.
  LIBLIST.PrivateBrauerTables:= [ [], [] ];

  # Set the version.
  file:= Filename( dir[1], "version" );
  str:= StringFile( file );
  if str = fail then
    Error( "the data file '", file, "' is not available" );
  fi;
  LIBLIST.lastupdated:= Chomp( str );
end, [] );


#############################################################################
##
#E

