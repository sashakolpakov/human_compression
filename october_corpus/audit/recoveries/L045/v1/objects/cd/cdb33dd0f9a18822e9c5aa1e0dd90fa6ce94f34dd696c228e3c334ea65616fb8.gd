#############################################################################
##
#W  brdbattrX.gd          GAP 4 package CTblLib                 Thomas Breuer
##
##  This file contains code from `lib/brdbattr.gd` in the Browse package.
##  (We need code independent of Browse because we want the functionality
##  of `AllCharacterTableNames` also if Browse is not available.)
##  This file contains the declarations for tools for database handling.
##  The GAP objects introduced for that are database id enumerators and
##  database attributes.
##


#############################################################################
##
#I  InfoDatabaseAttributeX
##
DeclareInfoClass( "InfoDatabaseAttributeX" );
#T unify in case Browse is available!


DeclareGlobalFunction( "DatabaseIdEnumeratorX" );
DeclareGlobalFunction( "DatabaseAttributeAddX" );
DeclareGlobalFunction( "DatabaseAttributeValueDefaultX" );
DeclareGlobalFunction( "DatabaseAttributeComputeX" );
DeclareGlobalFunction( "DatabaseIdEnumeratorUpdateX" );
DeclareGlobalFunction( "DatabaseAttributeLoadDataX" );
DeclareGlobalFunction( "DatabaseAttributeSetDataX" );
DeclareGlobalFunction( "DatabaseAttributeStringX" );


#############################################################################
##
#E

