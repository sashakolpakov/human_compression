#############################################################################
##
#W  read.g               GAP 4 package CTblLib                  Thomas Breuer
##

# Notify functions concerning Deligne-Lusztig names.
DeclareAutoreadableVariables( "ctbllib", "dlnames/dllib.g",
    [ "DeltigLibUnipotentCharacters", "DeltigLibGetRecord" ] );

# Read the implementation part.
ReadPackage( "ctbllib", "gap4/ctadmin.gi" );
ReadPackage( "ctbllib", "gap4/construc.gi" );
ReadPackage( "ctbllib", "gap4/ctblothe.gi" );
ReadPackage( "ctbllib", "gap4/test.g" );

# Read functions concerning Deligne-Lusztig names.
ReadPackage( "ctbllib", "dlnames/dlnames.gi" );

# Initialize database attributes
# and Browse overviews of tables, irrationalities, and differences of data.
ReadPackage( "ctbllib", "gap4/ctbltoct.g" );
CTblLib.Data.IdEnumerator:= rec( attributes:= rec(), identifiers:= [] );
CTblLib.Data.IdEnumeratorExt:= rec( attributes:= rec(), identifiers:= [] );
CTblLib.Data.attributesRelevantForGroupInfoForCharacterTable:= [];
CTblLib.SpinSymNames:= [];

# Use the code in CTblLib to build an id enumerator, independent of Browse.
ReadPackage( "ctbllib", "gap4/ctdbattr.g" );

# Load ATLAS related stuff.
ReadPackage( "ctbllib", "gap4/od.g" );
ReadPackage( "ctbllib", "gap4/atlasstr.g" );
ReadPackage( "ctbllib", "gap4/atlasirr.g" );


#############################################################################
##
#E

