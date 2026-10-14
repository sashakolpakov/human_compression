#############################################################################
##
#W  obsolete.gd          GAP 4 package CTblLib                  Thomas Breuer
##
##  This file contains declarations of global variables
##  that had been documented in earlier versions of the CTblLib package.
##


#############################################################################
##
#F  CharTableLibrary( <arglist> )
##
##  This function is available just for compatibility with GAP 3.
##
BindGlobal( "CharTableLibrary", function( arglist )
    return CallFuncList( CharacterTableFromLibrary, arglist );
end );


#############################################################################
##
#F  FirstNameCharTable( <tblname> )
#F  FileNameCharTable( <tblname> )
##
##  Add some harmless functions of the GAP 3 compatibility mode
##  that are related to the character table library.
##
BindGlobal( "FirstNameCharTable",
    function( name )
    name:= LibInfoCharacterTable( name );
    if name = fail then
      return false;
    else
      return name.firstName;
    fi;
    end );

BindGlobal( "FileNameCharTable",
    function( name )
    name:= LibInfoCharacterTable( name );
    if name = fail then
      return false;
    else
      return name.fileName;
    fi;
    end );


#############################################################################
##
#F  NotifyCharTable( <firstname>, <filename>, <othernames> )
#F  CharTableSpecialized( <gentbl>, <param> )
#F  AllCharTableNames( ... )
##
##  for compatibility with GAP 3
##
DeclareSynonym( "NotifyCharTable", NotifyCharacterTable );
DeclareSynonym( "CharTableSpecialized", CharacterTableSpecialized );
DeclareSynonym( "AllCharTableNames", AllCharacterTableNames );


#############################################################################
##
#F  CTblLibSetUnload( <bool> )
##
BindGlobal( "CTblLibSetUnload", function( bool )
    SetUserPreference( "CTblLib", "UnloadCTblLibFiles", bool );
    end );


#############################################################################
##
#V  FingerprintOfCharacterTableGlobals
#A  FingerprintOfCharacterTable( <tbl> )
##
##  This feature is now superseded by the supported attributes.
##
DeclareGlobalVariable( "FingerprintOfCharacterTableGlobals" );

InstallFlushableValue( FingerprintOfCharacterTableGlobals,
    [ [ "Size" ],
      [ "NrConjugacyClasses" ],
      [ "IsSimpleCharacterTable" ],
      [ "OrdersClassRepresentatives", "Collected" ],
      [ "SizesCentralizers", "Collected" ],
    ] );

DeclareAttribute( "FingerprintOfCharacterTable", IsOrdinaryTable );

InstallMethod( FingerprintOfCharacterTable,
    [ "IsOrdinaryTable" ],
    function( tbl )
    local result, list, val, name;

    result:= rec();

    for list in FingerprintOfCharacterTableGlobals do
      val:= tbl;
      for name in list do
        val:= ValueGlobal( name )( val );
      od;
      result.( String( list ) ):= val;
    od;

    return result;
    end );


#############################################################################
##
#E

