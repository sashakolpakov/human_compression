#############################################################################
##
##  This file is read as soon as the GAP library of tables of marks
##  is available.
##  Afterwards the information about identifiers of the tables is stored in
##  'LIBLIST.TOM_TBL_INFO',
##  and methods for 'FusionCharTableTom' and 'CharacterTable' (for a table of
##  marks from the library) are installed.
##
##  The file also provides the mapping between
##  the GAP Character Table Library and the
##  GAP Library of Tables of Marks,
##  via the "tom" attribute of 'CTblLib.Data.IdEnumerator'.
##

CallFuncList( function()
  local dir, file, str, evl;

  dir:= DirectoriesPackageLibrary( "ctbllib", "data" );
  file:= Filename( dir[1], "tom_tbl.json" );
  str:= StringFile( file );
  if str = fail then
    Error( "the data file '", file, "' is not available" );
  fi;
  evl:= MakeImmutable( EvalString( str ) );
  LIBLIST.TOM_TBL_INFO_VERSION:= evl[1];
  LIBLIST.TOM_TBL_INFO:= evl{ [ 2, 3 ] };
  end, [] );


#############################################################################
##
#M  FusionCharTableTom( <tbl>, <tom> )  . . . . . . . . . . .  element fusion
##
##  <#GAPDoc Label="FusionCharTableTom">
##  <ManSection>
##  <Meth Name="FusionCharTableTom" Arg="tbl, tom"/>
##
##  <Description>
##  Let <A>tbl</A> be an ordinary character table from the
##  &GAP; Character Table Library
##  with the attribute <Ref Attr="FusionToTom"/>,
##  and let <A>tom</A> be the table of marks from the &GAP; package
##  <Package>TomLib</Package> that corresponds to <A>tbl</A>.
##  In this case,
##  a method for <Ref Oper="FusionCharTableTom" BookName="ref"/>
##  is available that returns the fusion from <A>tbl</A> to <A>tom</A> that
##  is given by the <Ref Attr="FusionToTom"/> value of <A>tbl</A>.
##  <P/>
##  <Example>
##  gap> tbl:= CharacterTable( "A5" );
##  CharacterTable( "A5" )
##  gap> tom:= TableOfMarks( "A5" );
##  TableOfMarks( "A5" )
##  gap> FusionCharTableTom( tbl, tom );
##  [ 1, 2, 3, 5, 5 ]
##  </Example>
##  </Description>
##  </ManSection>
##  <#/GAPDoc>
##
InstallMethod( FusionCharTableTom,
    [ "IsOrdinaryTable and IsLibraryCharacterTableRep and HasFusionToTom",
      "IsTableOfMarks and IsLibTomRep" ],
    function( tbl, tom )
    local fus;

    fus:= FusionToTom( tbl );
    if fus.name <> Identifier( tom ) then
      TryNextMethod();
    fi;
    fus:= fus.map;
    if HasPermutationTom( tom ) then
      fus:= OnTuples( fus, PermutationTom( tom ) );
    fi;
    if HasClassPermutation( tbl ) then
      fus:= Permuted( fus, ClassPermutation( tbl ) );
    fi;

    return fus;
    end );


#############################################################################
##
#M  CharacterTable( <tom> ) . . . . . . . . . . . . . .  for a table of marks
##
##  If <tom> is a library table of marks then we check whether there is a
##  corresponding character table in the library.
##  If there is no such character table but <tom> stores an underlying group
##  then we delegate to this group.
##  Otherwise we return `fail'.
##
##  <#GAPDoc Label="CharacterTable_for_tom">
##  <ManSection>
##  <Meth Name="CharacterTable" Arg="tom" Label="for a table of marks"/>
##
##  <Description>
##  For a table of marks <A>tom</A>, this method for
##  <Ref Oper="CharacterTable" Label="for a group" BookName="ref"/>
##  returns the character table corresponding to <A>tom</A>.
##  <P/>
##  If <A>tom</A> comes from the <Package>TomLib</Package>
##  package, the character table comes from the
##  &GAP; Character Table Library.
##  Otherwise, if <A>tom</A> stores an
##  <Ref Func="UnderlyingGroup" BookName="ref"/> value then
##  the task is delegated to a
##  <Ref Oper="CharacterTable" Label="for a group" BookName="ref"/> method
##  for this group,
##  and if no underlying group is available then <K>fail</K> is returned.
##  <P/>
##  <Example>
##  gap> CharacterTable( TableOfMarks( "A5" ) );
##  CharacterTable( "A5" )
##  </Example>
##  </Description>
##  </ManSection>
##  <#/GAPDoc>
##
InstallOtherMethod( CharacterTable,
    [ "IsTableOfMarks" ],
    function( tom )
    local pos;

    if IsLibTomRep( tom ) then
      pos:= Position( LIBLIST.TOM_TBL_INFO[1],
                      LowercaseString( Identifier( tom ) ) );
      if pos <> fail then
        return CharacterTable( LIBLIST.TOM_TBL_INFO[2][ pos ] );
      fi;
    elif HasUnderlyingGroup( tom ) then
      return CharacterTable( UnderlyingGroup( tom ) );
    fi;
    return fail;
    end );


#############################################################################
##
#V  CTblLib.Data.IdEnumerator.attributes.tom
##
Add( CTblLib.Data.attributesRelevantForGroupInfoForCharacterTable, "tom" );

DatabaseAttributeAddX( CTblLib.Data.IdEnumerator, rec(
  identifier:= "tom",
  description:= "mapping between CTblLib and GAP's library of tables of marks",
  type:= "pairs",
  datafile:= Filename( DirectoriesPackageLibrary( "ctbllib", "data" )[1],
                       "grp_tom.json" ),
  dataDefault:= [],
  isSorted:= true,
  attributeValue:= function( attr, id )
    local pos, main, name, names;

    pos:= Position( LIBLIST.TOM_TBL_INFO[2], LowercaseString( id ) );
    if pos = fail then
      main:= attr.idenumerator.attributes.IdentifierOfMainTable;
      name:= main.attributeValue( main, id );
      if name <> fail then
        pos:= Position( LIBLIST.TOM_TBL_INFO[2], LowercaseString( name ) );
      fi;
    fi;
    if pos <> fail then
      name:= LIBLIST.TOM_TBL_INFO[1][ pos ];
      names:= NamesLibTom( name );
      if names <> fail and not IsEmpty( names ) then
        name:= names[1];
      fi;
      return Concatenation( [ [ "GroupForTom", [ name ] ] ],
                 DatabaseAttributeValueDefaultX( attr, id ) );
    else
      return DatabaseAttributeValueDefaultX( attr, id );
    fi;
    end,
  eval:= function( attr, l )
    return List( l, val -> [ "GroupForTom", val ] );
    end,
  reverseEval:= function( attr, info )
    local pos, data, entry;

    if info[1] = "GroupForTom" then
      if Length( info[2] ) = 1 then
        pos:= Position( LIBLIST.TOM_TBL_INFO[1],
                        LowercaseString( info[2][1] ) );
        if pos <> fail then
          return LIBLIST.TOM_TBL_INFO[2][ pos ];
        fi;
      else
        if not IsBound( attr.data )  then
          Read( attr.datafile );
        fi;
        for data in [ attr.data.automatic, attr.data.nonautomatic ] do
          for entry in data do
            if info[2] in entry[2] then
              return entry[1];
            fi;
          od;
        od;
      fi;
    fi;
    return fail;
    end,
  neededAttributes:= [ "IsDuplicateTable", "IdentifiersOfDuplicateTables" ],
  prepareAttributeComputation:= function( attr )
    local i;

    CTblLib.Data.prepare( attr );
    CTblLib.Data.invposition:= InverseMap( LIBLIST.position );
    for i in [ 1 .. Length( CTblLib.Data.invposition ) ] do
      if IsInt( CTblLib.Data.invposition[i] ) then
        CTblLib.Data.invposition[i]:= [ CTblLib.Data.invposition[i] ];
      fi;
    od;
    CTblLib.Data.attrvalues_tom:= rec();
    end,
  cleanupAfterAttributeComputation:= function( attr )
    Unbind( CTblLib.Data.invposition );
    Unbind( CTblLib.Data.attrvalues_tom );
    CTblLib.Data.cleanup( attr );
    end,
  create:= function( attr, id )
    local main, mainid, subgroupfits, dupl, names, result, name, tbl, r,
          super, tom, mx, pos, i, orders;

    # For duplicate tables, take (and cache) the result for the main table.
    main:= attr.idenumerator.attributes.IdentifierOfMainTable;
    mainid:= main.attributeValue( main, id );
    if mainid <> fail then
      id:= mainid;
    fi;
    if IsBound( CTblLib.Data.attrvalues_tom ) and
       IsBound( CTblLib.Data.attrvalues_tom.( id ) ) then
      return CTblLib.Data.attrvalues_tom.( id );
    fi;

    # Now we know that we have to work.
    subgroupfits:= function( tom, poss, tbl )
      return First( poss,
           function( i )
             local G;
             G:= RepresentativeTom( tom, i );
             return NrConjugacyClasses( G ) = NrConjugacyClasses( tbl ) and
#T provide a utility that compares more invariants?
                    IsRecord( TransformingPermutationsCharacterTables(
                                  CharacterTable( G ), tbl ) );
           end );
    end;

    dupl:= attr.idenumerator.attributes.IdentifiersOfDuplicateTables;
    names:= Concatenation( [ id ], dupl.attributeValue( dupl, id ) );
    result:= [];

    for name in names do
      tbl:= CharacterTable( name );

      # Check for stored fusions into tables that know a table of marks.
      # (We need not store the table of marks of `tbl' itself,
      # because the `extract' function will deal with it.)
      for r in ComputedClassFusions( tbl ) do
        if Length( ClassPositionsOfKernel( r.map ) ) = 1 then
          super:= CharacterTable( r.name );
          if super <> fail and HasFusionToTom( super ) then
            # Identify the subgroup.
            tom:= TableOfMarks( super );
            if IsBound( r.specification ) and 4 < Length( r.specification )
               and r.specification{ [ 1 .. 4 ] } = "tom:" then
              # Restrict the test to the given subgroup.
              pos:= r.specification;
              pos:= Int( pos{ [ 5 .. Length( pos ) ] } );
              if IsInt( pos ) then
                i:= subgroupfits( tom, [ pos ], tbl );
                if i <> fail then
                  Add( result, [ Identifier( tom ), i ] );
#T and else? print an error because of the wrong stored value?
                fi;
              else
                Info( InfoDatabaseAttributeX, 1,
                      "specification ", r.specification,
                      " in table ", name, "?" );
              fi;
            elif HasMaxes( super ) and id in Maxes( super ) then
              mx:= MaximalSubgroupsTom( tom );
              if Sum( SizesConjugacyClasses( super ){ Set( r.map ) } )
                   = Size( tbl ) then
                pos:= Filtered( [ 1 .. Length( mx[2] ) ],
                                i -> mx[2][i] = 1 );
              else
                pos:= Filtered( [ 1 .. Length( mx[2] ) ],
                          i -> mx[2][i] = Size( super ) / Size( tbl ) );
              fi;
              if Length( pos ) = 1 then
                # Omit the check.
                Add( result, [ Identifier( tom ), mx[1][ pos[1] ] ] );
              else
                i:= subgroupfits( tom, mx[1]{ pos }, tbl );
                if i <> fail then
                  Add( result, [ Identifier( tom ), i ] );
                fi;
              fi;
            else
              # Loop over all classes of subgroups of the right order.
              orders:= OrdersTom( tom );
              pos:= Filtered( [ 1 .. Length( orders ) ],
                        i -> orders[i] = Size( tbl ) );
              i:= subgroupfits( tom, pos, tbl );
              if i <> fail then
                Add( result, [ Identifier( tom ), i ] );
              fi;
            fi;
          fi;
        fi;
      od;
    od;

    if IsEmpty( result ) then
      result:= attr.dataDefault;
    else
      result:= Set( result );
    fi;

    # Cache the result.
    CTblLib.Data.attrvalues_tom.( id ):= result;

    return result;
    end,
  string:= entry -> CTblLib.AttrDataString( entry, [], false ),
  check:= ReturnTrue,
  ) );

# Create the analogous attribute of 'CTblLib.Data.IdEnumeratorExt',
# and set also the 'eval' component.
CTblLib.ExtendAttributeOfIdEnumeratorExt( "tom", true );

# Set the attribute values that may have been added up to now.
# (As soon as the SpinSym package gets loaded, it notifies some data.)
if IsBound( CTblLib.IdEnumeratorExt_attributes_tom_data_automatic ) then
  CTblLib.Data.IdEnumeratorExt.attributes.tom.data.automatic:=
      CTblLib.IdEnumeratorExt_attributes_tom_data_automatic;
fi;


#############################################################################
##
#V  CTblLib.Data.IdEnumerator.attributes.HasFusionToTom
##
AddSet( CTblLib.SupportedAttributes, "HasFusionToTom" );

DatabaseAttributeAddX( CTblLib.Data.IdEnumerator, rec(
  identifier:= "HasFusionToTom",
  description:= "identifiers of GAP library character tables for which tables of marks are available",
  type:= "values",
  name:= "HasFusionToTom",
  align:= "c",
  categoryValue:= function( val )
    if val then
      return "table of marks available";
    else
      return "no table of marks available";
    fi;
    end,
  create:= function( attr, id )
    return LowercaseString( id ) in LIBLIST.TOM_TBL_INFO[2];
    end,
  version:= CTblLib.Data.IdEnumerator.version,
  viewValue:= x -> CTblLib.ReplacedEntry( x, [ false, true ],
                                                [ "-", "+" ] ),
  viewLabel:= "with t.o.m.?",
  sortParameters:= [ "add counter on categorizing", "yes" ],
  ) );

# Create the analogous attribute of 'CTblLib.Data.IdEnumeratorExt',
# and set also the 'eval' component.
CTblLib.ExtendAttributeOfIdEnumeratorExt( "HasFusionToTom", true );


#############################################################################
##
#E

