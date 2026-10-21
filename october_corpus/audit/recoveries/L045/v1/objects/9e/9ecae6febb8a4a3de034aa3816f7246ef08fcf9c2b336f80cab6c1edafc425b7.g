#############################################################################
##
#V  CTblLib.Data.IdEnumerator.attributes.atlas
##
##  The mapping between the GAP Character Table Library and the AtlasRep
##  package is provided only if the two packages are available.
##
##  The mapping relies on the coincidence of group names.
##

## This function is used in the 'create' function below.
CTblLib.AtlasRepConstructions:= function( name, tocids )
    local pos, admissible, result, AtlasEntryOfTableIdentifier, entry, tbl,
          permrepinfo, r, super, maxpos, prefix, i, ii, prog, arec, repname,
          info;

    pos:= Position( LIBLIST.firstnames, name );
    if pos = fail then
      return [];
    fi;

    if IsBound( CTblLib.Data.invposition ) then
      admissible:= CTblLib.Data.invposition[ pos ];
    else
      admissible:= Positions( LIBLIST.position, pos );
    fi;

    result:= [];

    AtlasEntryOfTableIdentifier:= function( pos )
      local admissible, entry, pos2;

      if IsBound( CTblLib.Data.invposition ) then
        # The function was called inside the database attribute recomputation.
        admissible:= LIBLIST.allnames{ CTblLib.Data.invposition[ pos ] };
        return First( AtlasOfGroupRepresentationsInfo.GAPnames,
                      l -> LowercaseString( l[1] ) in admissible );
      else
        for entry in AtlasOfGroupRepresentationsInfo.GAPnames do
          pos2:= Position( LIBLIST.allnames, LowercaseString( entry[1] ) );
          if pos2 <> fail and LIBLIST.position[ pos2 ] = pos then
            return entry;
          fi;
        od;
        return fail;
      fi;
    end;

    # Check whether a name belongs to an Atlas group.
    entry:= AtlasEntryOfTableIdentifier( pos );
    if entry <> fail and
       OneAtlasGeneratingSetInfo( entry[1], "contents", tocids ) <> fail then
      # There is at least one representation from 'tocids'.
      Add( result, [ entry[1] ] );
    fi;

    # Check whether a name belongs to a maximal subgroup of an
    # Atlas group such that one of the following is available:
    # - a representation of the group and a straight line program
    #   for restricting it to the subgroup,
    # - a permutation representation of the group such that the subgroup
    #   is a point stabilizer.
    tbl:= CharacterTable( name );
    permrepinfo:= AtlasOfGroupRepresentationsInfo.permrepinfo;
    for r in ComputedClassFusions( tbl ) do
      if Length( ClassPositionsOfKernel( r.map ) ) = 1 then
        super:= CharacterTable( r.name );
        if super <> fail then
          entry:= AtlasEntryOfTableIdentifier(
                      Position( LIBLIST.firstnames, Identifier( super ) ) );
          if entry <> fail then
            maxpos:= [];
            if HasMaxes( super ) then
              # Try to find `tbl' among the maxes of `super'.
              maxpos:= Positions( Maxes( super ), Identifier( tbl ) );
            else
              # Try to find relative admissible names of `tbl' as a
              # maximal subgroup of `super'.
              prefix:= Concatenation(
                           LowercaseString( Identifier( super ) ), "m" );
              for i in Filtered( LIBLIST.allnames{ admissible },
                         x -> Length( x ) > Length( prefix ) and
                                x{ [ 1 .. Length( prefix ) ] } = prefix ) do
                ii:= Int( i{ [ Length( prefix ) + 1 .. Length( i ) ] } );
                if ii <> fail then
                  Add( maxpos, ii );
                fi;
              od;
            fi;
            for pos in maxpos do
              prog:= AtlasProgramInfo( entry[1], "maxes", pos,
                         "contents", tocids );
              if prog <> fail and
                 OneAtlasGeneratingSetInfo( entry[1],
                     prog.standardization ) <> fail then
                # There is a slp in 'tocids', for a representation from
                # anywhere.
                Add( result, [ entry[1], pos ] );
              fi;
              for arec in AllAtlasGeneratingSetInfos( entry[1],
                              IsPermGroup, true, "contents", tocids ) do
                # There is a perm. representation in 'tocids'
                # which has the given max. subgroup as a point stabilizer.
                repname:= arec.repname;
                if IsBound( permrepinfo.( repname ) ) then
                  info:= permrepinfo.( repname );
                  if IsBound( info.isPrimitive ) and
                     info.isPrimitive = true and
                     IsBound( info.maxnr ) and info.maxnr = pos then
                    Add( result, [ entry[1], repname ] );
                  fi;
                fi;
              od;
            od;
          fi;
        fi;
      fi;
    od;

    return result;
end;


Add( CTblLib.Data.attributesRelevantForGroupInfoForCharacterTable, "atlas" );

DatabaseAttributeAddX( CTblLib.Data.IdEnumerator, rec(
  identifier:= "atlas",
  description:= "mapping between CTblLib and AtlasRep, via group names",
  type:= "pairs",
  datafile:= Filename( DirectoriesPackageLibrary( "ctbllib", "data" )[1],
                       "grp_atlas.json" ),
  dataDefault:= [],
  isSorted:= true,
  eval:= function( attr, l )
    local result, entry;

    result:= [];
    for entry in l do
      if Length( entry ) = 1 then
        Add( result, [ "AtlasGroup", entry ] );
      elif IsInt( entry[2] ) then
        Add( result, [ "AtlasSubgroup", entry ] );
      else
        Add( result, [ "AtlasStabilizer", entry ] );
      fi;
    od;
    return result;
    end,
  reverseEval:= function( attr, info )
    local entry;

    if ( info[1] = "AtlasGroup" and Length( info[2] ) = 1 ) or
       ( info[1] = "AtlasSubgroup" and Length( info[2] ) = 2 ) or
       ( info[1] = "AtlasStabilizer" and Length( info[2] ) = 2 ) then
      if not IsBound( attr.data )  then
        Read( attr.datafile );
      fi;
      for entry in Concatenation( attr.data.automatic,
                                  attr.data.nonautomatic ) do
        if info[2] in entry[2] then
          return entry[1];
        fi;
      od;
    fi;
    return fail;
    end,
  neededAttributes:= [ "IsDuplicateTable", "IdentifiersOfDuplicateTables" ],
  prepareAttributeComputation:= function( attr )
    local i;

    CTblLib.Data.invposition:= InverseMap( LIBLIST.position );
    for i in [ 1 .. Length( CTblLib.Data.invposition ) ] do
      if IsInt( CTblLib.Data.invposition[i] ) then
        CTblLib.Data.invposition[i]:= [ CTblLib.Data.invposition[i] ];
      fi;
    od;
    CTblLib.Data.attrvalues_atlas:= rec();
    end,
  cleanupAfterAttributeComputation:= function( attr )
    Unbind( CTblLib.Data.invposition );
    Unbind( CTblLib.Data.attrvalues_atlas );
    end,
  create:= function( attr, id )
    local main, mainid, dupl, names, result, name;

    # For duplicate tables, take (and cache) the result for the main table.
    main:= attr.idenumerator.attributes.IdentifierOfMainTable;
    mainid:= main.attributeValue( main, id );
    if mainid <> fail then
      id:= mainid;
    fi;
    if IsBound( CTblLib.Data.attrvalues_atlas ) and
       IsBound( CTblLib.Data.attrvalues_atlas.( id ) ) then
      return CTblLib.Data.attrvalues_atlas.( id );
    fi;

    # Now we know that we have to work.
    dupl:= attr.idenumerator.attributes.IdentifiersOfDuplicateTables;
    names:= Concatenation( [ id ], dupl.attributeValue( dupl, id ) );
    result:= [];

    for name in names do
      Append( result, CTblLib.AtlasRepConstructions( name,
                          [ "core", "internal", "mfer", "ctblocks" ] ) );
    od;

    if IsEmpty( result ) then
      result:= attr.dataDefault;
    else
      result:= Set( result );
    fi;

    # Cache the result.
    CTblLib.Data.attrvalues_atlas.( id ):= result;

    return result;
    end,
  string:= entry -> CTblLib.AttrDataString( entry, [], false ),
  check:= ReturnTrue,
  ) );

# Create the analogous attribute of 'CTblLib.Data.IdEnumeratorExt',
# and set also the 'eval' component.
CTblLib.ExtendAttributeOfIdEnumeratorExt( "atlas", true );

# Set the attribute values that may have been added up to now.
# (As soon as the SpinSym package gets loaded, it notifies some data.)
if IsBound( CTblLib.IdEnumeratorExt_attributes_atlas_data_automatic ) then
  CTblLib.Data.IdEnumeratorExt.attributes.atlas.data.automatic:=
      CTblLib.IdEnumeratorExt_attributes_atlas_data_automatic;
fi;

