#############################################################################
##
#W  init.g               GAP 4 package CTblLib                  Thomas Breuer
##

if IsBound( GAPInfo ) then

  # Read the declaration part.
  ReadPackage( "ctbllib", "gap4/ctadmin.gd" );
  ReadPackage( "ctbllib", "gap4/construc.gd" );
  ReadPackage( "ctbllib", "gap4/ctblothe.gd" );

  # Read functions concerning Deligne-Lusztig names.
  ReadPackage( "ctbllib", "dlnames/dlnames.gd" );

  # Read obsolete variable names if this happens also in the GAP library.
  if UserPreference( "gap", "ReadObsolete" ) <> false then
    ReadPackage( "ctbllib", "gap4/obsolete.gd" );
  fi;

  # Read support for database attributes
  # (independent of the corresponding functions from Browse).
  ReadPackage( "ctbllib", "gap4/brdbattrX.gd" );
  ReadPackage( "ctbllib", "gap4/brdbattrX.gi" );

else

  # GAP 3.4.4
  ReadPkg( "ctbllib", "gap3/ctadmin" );

fi;

#############################################################################
##
#E

