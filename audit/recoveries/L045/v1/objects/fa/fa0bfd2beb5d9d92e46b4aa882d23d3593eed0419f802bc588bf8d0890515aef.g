#############################################################################
##
#W  ctbltocb.g           GAP 4 package CTblLib                  Thomas Breuer
##
##  This file contains functions for turning the information about a
##  character table contained in the GAP Character Table Library
##  see (`ctbltoct.g') into a Browse table.
##


##############################################################################
##
##  Links in Browse tables are shown by default in blue,
##  the active link is shown in red.
##
CTblLib.OpenLink:= [ NCurses.ColorAttr( "blue", "blue" ), true ];
CTblLib.CloseLink:= [ NCurses.ColorAttr( "blue", "blue" ), false ];

CTblLib.ActiveLink_on:= [ NCurses.ColorAttr( "red", "red" ), true ];
CTblLib.ActiveLink_off:= [ NCurses.ColorAttr( "red", "red" ), false ];


##############################################################################
##
#F  BrowseData.BrowseRender( <obj> )
##
##  returns a record with the following components.
##  `rows':
##      a list of attribute lines,
##  `links':
##      a list of entries of the form `[ i, js, je, jump ]',
##      meaning that the positions in row i from column js to je shall carry
##      a link with destination `jump',
##  `grid':
##      a record in the format needed by `NCurses.GridExt'.
##
BrowseData.BrowseRender:= function( obj )
    local len, list, entry, line, links, pos, i, lentry, link, width,
          colwidths, row, j, totalwidth, colinds, n, hlines, hlinem, hlinee,
          str, left, mid, right, res, header, matrix, frow, prefix, suffix,
          grid;

    if IsString( obj ) then
      return rec( rows:= SplitString( obj, "\n" ), links:= [] );
    elif not ( IsRecord( obj ) and IsBound( obj.type ) ) then
      Error( "<obj> must be a string or a record with `type' component" );
    fi;

    if   obj.type = "string" then
      return rec( rows:= SplitString( obj.value, "\n" ), links:= [] );
    elif obj.type = "linkedtext" then

      return rec( rows:= [ Concatenation( CTblLib.OpenLink, [ obj.display ],
                               CTblLib.CloseLink ) ],
                  links:= [ [ 1, 1, Length( obj.display ), obj.target ] ] );

    elif obj.type = "datalist" then

      # Break the list into lines.
      # (In each line, add at least one entry, then fill up.
      # Note that `FormatParagraph' would be allowed to add line breaks
      # inside entries.)
      len:= SizeScreen()[1] - 3;
#T better let the width be prescribed in obj?
      list:= [];
      entry:= BrowseData.BrowseRender( obj.list[1] );

      # We assume that there is one line with at most one link
      if Length( entry.rows ) <> 1 then
        Error( "<entry>.rows must have length 1" );
      elif Length( entry.links ) > 1 then
        Error( "<entry>.links must have length at most 1" );
      fi;

      line:= entry.rows[1];
      links:= [];
      if IsBound( entry.links[1] ) then
        links[1]:= entry.links[1];
      fi;
      pos:= NCurses.WidthAttributeLine( line );
      for i in [ 2 .. Length( obj.list ) ] do
        entry:= BrowseData.BrowseRender( obj.list[i] );

        # We assume that there is one line with at most one link
        if Length( entry.rows ) <> 1 then
          Error( "<entry>.rows must have length 1" );
        elif Length( entry.links ) > 1 then
          Error( "<entry>.links must have length at most 1" );
        fi;

        lentry:= NCurses.WidthAttributeLine( entry.rows[1] );
        if pos + lentry + 3 > len then
          line:= NCurses.ConcatenationAttributeLines( [ line, "," ], true );
          Add( list, line );
          line:= "";
          pos:= 0;
        fi;
        if pos <> 0 then
          line:= NCurses.ConcatenationAttributeLines(
                     [ line, ", " ], true );
          pos:= pos + 2;
        fi;
        if IsBound( entry.links[1] ) then
          link:= [ Length( list )+1, pos+1, pos+lentry, entry.links[1][4] ];
          Add( links, link );
        fi;
        line:= NCurses.ConcatenationAttributeLines(
                   [ line, entry.rows[1] ], true );
#T this loop produces a lot of garbage!
        pos:= pos + lentry;
      od;
      Add( list, line );

      return rec( rows:= list, links:= links );

    elif obj.type = "datatable" then

      # Construct a table with grid information (separate the header row
      # from the rest of the table, separate all columns).
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
      totalwidth:= Sum( colwidths, 1 + 3 * Length( colwidths ) );

      colinds:= [ 0 ];
      pos:= 0;
      for i in colwidths do
        pos:= pos + i + 3;
        Add( colinds, pos );
      od;

      # Prepare a primitive grid (if the nice grid is not available).
      hlines:= RepeatedString( '-', totalwidth );
      hlinem:= hlines;
      hlinee:= hlines;
      left:= "| ";
      mid:= " | ";
      right:= " |";

      n:= Length( colwidths );
      for j in [ 1 .. n ] do
        if obj.colalign[j] = "left" then
          colwidths[j]:= -colwidths[j];
        fi;
      od;

      res:= [ hlines ];
      links:= [];

      if IsBound( obj.header ) then
        header:= List( [ 1 .. n ],
                       i -> String( CTblLib.StringRender( obj.header[i] ),
                                    colwidths[i] ) );
        Add( res, Concatenation( left,
                      JoinStringsWithSeparator( header, mid ), right ) );
        Add( res, hlinem );
      fi;

      for row in obj.matrix do
        frow:= left;
        for i in [ 1 .. n ] do
          entry:= BrowseData.BrowseRender( row[i] );

          # We assume that there is one line with at most one link
          if Length( entry.rows ) <> 1 then
            Error( "<entry>.rows must have length 1" );
          elif Length( entry.links ) > 1 then
            Error( "<entry>.links must have length at most 1" );
          fi;
          if colwidths[i] < 0 then
            # left alignment
            prefix:= "";
            suffix:= RepeatedString( " ", - colwidths[i]
                         - NCurses.WidthAttributeLine( entry.rows[1] ) );
          else
            # right alignment
            prefix:= RepeatedString( " ", colwidths[i]
                         - NCurses.WidthAttributeLine( entry.rows[1] ) );
            suffix:= "";
          fi;
          if IsBound( entry.links[1] ) then
            lentry:= NCurses.WidthAttributeLine( frow );
            Add( links, [ Length( res ) + 1,
                          lentry + Length( prefix ) + 1,
                          lentry + Length( prefix ) + entry.links[1][3],
                          entry.links[1][4] ] );
          fi;
          frow:= NCurses.ConcatenationAttributeLines(
                     [ frow, prefix, entry.rows[1], suffix ], true );
          if i < n then
            frow:= NCurses.ConcatenationAttributeLines(
                     [ frow, mid ], true );
          fi;
        od;
        frow:= NCurses.ConcatenationAttributeLines(
                   [ frow, right ], true );
        Add( res, frow );
      od;
      Add( res, hlinee );

      grid:= rec( trow:= 0,
                  brow:= Length( res ) - 1,
                  lcol:= 0,
                  rcol:= totalwidth - 1 );
      if IsBound( obj.header ) then
        grid.rowinds:= [ 0, 2, Length( res ) - 1 ];
      else
        grid.rowinds:= [ 0, Length( res ) - 1 ];
      fi;
      grid.colinds:= colinds;

      return rec( rows:= res, links:= links, grid:= grid );

    elif obj.type = "factored order" then

      return rec( rows:= [ Concatenation( String( obj.value ), " = ",
                               StringPP( obj.value ) ) ],
                  links:= [] );

    else
      Error( "unknown type `", obj.type, "'" );
    fi;
end;


##############################################################################
##
#F  BrowseData.SetActiveLink( <t>, <part>, <row>, <newlink> )
##
##  <t> is assumed to be a browse table with links only in the unique column,
##  such that each link is represented by one string surrounded by markup.
##  It is also assumed that the table is not sorted.
##  <part> is "header" or "main";
##  <row> is 0 in the case of "header",
##  and the row number in the case of "main";
##  <newlink> has the format `[ row in cell, startcol, endcol, info ]'.
##
BrowseData.SetActiveLink:= function( t, part, row, newlink )
    local oldlink, on, off, oldlinkpos, list, pos, line, listpos, from, len;

    oldlink:= t.dynamic.activeLink;

    if oldlink = fail or oldlink[1] <> part or oldlink[2] <> row
                      or oldlink[3] <> newlink then

      on:= CTblLib.ActiveLink_on;
      off:= CTblLib.ActiveLink_off;

      if oldlink <> fail then
        # Unset the previous active link ...
        if oldlink[1] = "header" then
          # ... in the header.
          list:= t.work.header;
        elif oldlink[1] = "main" then
          # ... in the main table.
          list:= t.work.main[ oldlink[2] ][1].rows;
        else
          Error( "not yet supported ..." );
        fi;
        pos:= oldlink[3][1];
        line:= list[ pos ];
        oldlinkpos:= oldlink[4];
        list[ pos ]:= Concatenation( line{ [ 1 .. oldlinkpos - 1 ] },
            [ line[ oldlinkpos + Length( on ) ] ],
            line{ [ oldlinkpos + Length( on ) + Length( off ) + 1
                    .. Length( line ) ] } );
      fi;

      # Set the active link ...
      if part = "header" then
        # ... in the header.
        list:= t.work.header;
      else
        # ... in the main table.
        list:= t.work.main[ row ][1].rows;
      fi;
      listpos:= newlink[1];
      line:= list[ listpos ];
      from:= newlink[2];
      pos:= 1;
      len:= 1;
      while len < from do
        while not IsString( line[ pos ] ) do
          pos:= pos + 1;
        od;
        len:= len + Length( line[ pos ] );
        pos:= pos + 1;
      od;
      while not IsString( line[ pos ] ) do
        pos:= pos + 1;
      od;
      list[ listpos ]:= Concatenation( line{ [ 1 .. pos-1 ] },
          on, [ line[ pos ] ], off, line{ [ pos+1 .. Length( line ) ] } );

      t.dynamic.activeLink:= [ part, row, newlink, pos ];
      BrowseData.MoveFocusToActiveLink( t );

      # Refresh the screen
      if not BrowseData.IsQuietSession( t.dynamic.replay ) then
        BrowseData.CurrentMode( t ).ShowTables( t );
        NCurses.update_panels();
        NCurses.doupdate();
        NCurses.curs_set( 0 );
      fi;
    fi;
end;


############################################################################
##
#V  BrowseData.LinkActions
##
##  We need three different actions.
##  - "details page":  Open another details page.
##  - "dec. matrix":   Open a page that displays a decomposition matrix.
##  - "show table":    Open a page that displays a character table.
##
BrowseData.LinkActions:= rec();

BrowseData.LinkActions.( "details page" ):= function( t, name, p )
    local stack, dispname, tt;

    # Create the details table for the link.
    if IsBound( t.dynamic.stack ) then
      stack:= t.dynamic.stack;
    else
      stack:= [ "overview" ];
    fi;
    if p = 0 then
      dispname:= name;
    else
      dispname:= Concatenation( name, " mod ", String( p ) );
    fi;
    tt:= BrowseCTblLibInfo_GroupInfoTable( name, p,
             t.dynamic.log, t.dynamic.replay,
             Concatenation( stack, [ dispname ] ) );
    if tt = fail then
      BrowseData.AlertWithReplay( t,
          Concatenation( "Sorry, no details for ", name ),
          NCurses.attrs.BOLD );
    else
      # Open a new window.
      NCurses.BrowseGeneric( tt );
      if tt.dynamic.interrupt then
        BrowseData.actions.QuitTable.action( t );
      fi;
    fi;
end;

BrowseData.LinkActions.( "dec. matrix" ):= function( t, name, p, blocknr )
    local tbl;

    tbl:= CharacterTable( name );
    if tbl <> fail then
      tbl:= tbl mod p;
    fi;
    if tbl <> fail then
      if blocknr = 0 then
        BrowseDecompositionMatrix( tbl,
            rec( log:= t.dynamic.log, replay:= t.dynamic.replay ) );
      else
        BrowseDecompositionMatrix( tbl, blocknr,
            rec( log:= t.dynamic.log, replay:= t.dynamic.replay ) );
      fi;
    fi;
end;

BrowseData.LinkActions.( "show table" ):= function( t, name, p )
    local tbl;

    tbl:= CharacterTable( name );
    if tbl <> fail then
      if p <> 0 then
        tbl:= tbl mod p;
      fi;
    fi;
    if tbl <> fail then
      Browse( tbl, rec( log:= t.dynamic.log, replay:= t.dynamic.replay ) );
    fi;
end;

BrowseData.LinkActions.( "AtlasRep overview" ):= function( t, name )
    if NumberArgumentsFunction( BrowseData.AtlasInfoOverview ) = 4 then
#T This requires Browse newer than version 1.6!
      BrowseAtlasInfo( rec( log:= t.dynamic.log, replay:= t.dynamic.replay ),
                       name );
    else
      BrowseAtlasInfo( name );
    fi;
end;


############################################################################
##
#F  BrowseData.MoveFocusToActiveLink( <t> )
##
##  Change `<t>.dynamic.topleft' such that the active link becomes visible.
##
BrowseData.MoveFocusToActiveLink:= function( t )
    local i, j, bottom, n;

    if t.dynamic.activeLink = fail or t.dynamic.activeLink[1] = "header" then
      # Nothing is to do if there is no active link.
      return;
    fi;

    i:= 2 * t.dynamic.activeLink[2];
    j:= t.dynamic.activeLink[3][1] + BrowseData.HeightCategories( t, i );

    bottom:= BrowseData.BottomOrRight( t, "vert" );
    if i < t.dynamic.topleft[1] or
       ( i = t.dynamic.topleft[1] and j < t.dynamic.topleft[3] ) then
      # Move up.
      BrowseData.SetTopOrLeft( t, "vert", i, j );
    elif IsList( bottom ) and ( i > bottom[1] or
         ( i = bottom[1] and j > bottom[2] ) ) then
      # Move down.
      n:= Sum( List( [ bottom[1] .. i-1 ],
                     x -> BrowseData.LengthCell( t, x, "vert" ) ),
               j - bottom[2] );
      BrowseData.ScrollCharactersDownOrRight( t, "vert", n );
    fi;
  end;


##############################################################################
##
#F  BrowseCTblLibInfo_GroupInfoTable( <groupname>, <p>, <log>, <replay>,
#F                                    <stack> )
##
##  This function is called by 'BrowseCTblLibInfo', either directly or in
##  second level calls.
##  Also 'BrowseAtlasMap' calls it.
##
BindGlobal( "BrowseCTblLibInfo_GroupInfoTable",
    function( groupname, p, log, replay, stack )
    local activelink_on, activelink_off, name, title,
          cats, headerlink, main, mainlink, grid, data, sep, info,
          i, fun, val, cell, modes, myDealWithMouseClick, selectNextLink,
          selectPreviousLink, toggleCategoryOrFollowActiveLink, myShowTables,
          replactions, mode, windowhistory, len, pos, t;

    activelink_on:= CTblLib.ActiveLink_on;
    activelink_off:= CTblLib.ActiveLink_off;

    name:= LibInfoCharacterTable( groupname );
    if name = fail then
      return fail;
    fi;
    groupname:= name.firstName;

    # Construct the information about `groupname'.
    title:= Concatenation( "Character Table info for ", groupname );
    if p <> 0 then
      Append( title, Concatenation( " mod ", String( p ) ) );
    fi;
    cats:= [];
    headerlink:= [ [ 3, 3 + Length( title ), 14 + Length( title ),
                     [ "show table", [ groupname, p ] ] ] ];
    main:= [];
    mainlink:= [];
    grid:= [];
    data:= [];
    sep:= " ";

    if p = 0 then
      info:= CTblLib.OrdinaryTableInfo;
    else
      info:= CTblLib.BrauerTableInfo;
    fi;

    i:= 1;
    for fun in info do
      val:= fun( groupname, p );
      if val <> fail then
        cell:= BrowseData.BrowseRender( val );
        cats[i]:= rec( pos:= 2*i,
                       level:= 1,
                       value:= Concatenation( String( i ), ". ",
                                              val.title, ":" ),
                       separator:= sep,
                       isUnderCollapsedCategory:= false,
                       isRejectedCategory:= false );
        main[i]:= [ rec( rows:= cell.rows, align:= "tl" ) ];
        mainlink[i]:= cell.links;

        # Add a link in a special case.
        # (This is an ugly hack.)
        if val.title = "Number of p-regular classes" then
          mainlink[i][1]:= [ 1, Length( main[i][1].rows[1] ) + 3,
                             Length( main[i][1].rows[1] ) + 20,
                             [ "dec. matrix", [ groupname, p, 0 ] ] ];
          main[i][1].rows[1]:= Concatenation( [ main[i][1].rows[1], "  " ],
              CTblLib.OpenLink, [ "(show dec. matrix)" ], CTblLib.CloseLink );
        fi;

        if IsBound( cell.grid ) then
          grid[ 2*i ]:= cell.grid;
        fi;
        i:= i + 1;
      fi;
    od;

    if i = 1 then
      return fail;
    fi;

    # Construct the extended modes if necessary.
    if not IsBound( BrowseData.defaults.work.customizedModes.ctbllib ) then

      # The meaning of mouse clicks is as follows.
      # - single click:
      #   - If the mouse pointer is on the selected category then toggle
      #     (collapse/expand).
      #   - If the mouse pointer is on another category then select it.
      #   - If the mouse pointer is on a link that is not active
      #     then select this link.
      #   - If the mouse pointer is on the active link then follow it.
      # - double click:
      #   - If the mouse pointer is on the selected category then toggle
      #     (collapse/expand).
      #   - If the mouse pointer is on another category then select it.
      #   - If the mouse pointer is on a link then
      #     select this link and follow it.
      myDealWithMouseClick:= function( t, data, flag )
        local pos, link, jump, name, i;

        pos:= BrowseData.PositionInBrowseTable( t, data );
        if pos[1] = "header" then
          for link in t.dynamic.link.header do
            if pos[2][1] = link[1]
               and link[2] <= pos[2][2] and pos[2][2] <= link[3] then
              # The click happened on this link.
              jump:= false;
              if t.dynamic.activeLink = fail or
                 t.dynamic.activeLink[1] <> "header" or
                 t.dynamic.activeLink[3] <> link then
                BrowseData.SetActiveLink( t, "header", 0, link );
                if flag then
                  jump:= true;
                  t.dynamic.changed:= true;
                else
                  break;
                fi;
              else
                jump:= true;
                t.dynamic.changed:= true;
              fi;
              if jump then
                link:= link[4];
                if IsBound( t.work.linkActions.( link[1] ) ) then
                  CallFuncList( t.work.linkActions.( link[1] ),
                      Concatenation( [ t ], link[2] ) );
                fi;
              fi;
              break;
            fi;
          od;
        elif pos[1] in [ "main", "row labels" ] and Length( pos ) = 3 then
          # The click happened on a category row.
          if t.dynamic.selectedCategory <> [ 0, 0 ] then
            # A category row is already selected.
            if pos[2][1] = t.dynamic.selectedCategory[1] and
              pos[3] = t.dynamic.selectedCategory[2] then
              # The click happened on the selected category.
              BrowseData.actions.ClickOrToggle.action( t );
              t.dynamic.changed:= true;
            else
              # Move the selection to another category row.
              t.dynamic.selectedCategory:= [ pos[2][1], pos[3] ];
              t.dynamic.changed:= true;
            fi;
          elif t.dynamic.selectedEntry <> [ 0, 0 ] then
            # Move the selection to a category row.
            t.dynamic.selectedEntry:= [ 0, 0 ];
            t.dynamic.selectedCategory:= [ pos[2][1], pos[3] ];
            t.dynamic.changed:= true;
          else
            # Nothing is selected yet.
            if ForAny( t.work.availableModes,
                       x -> x.name = "select_entry" ) then
#T ???
              # Select the category row.
              if BrowseData.PushMode( t, "select_entry" ) then
                t.dynamic.selectedCategory:= [ pos[2][1], pos[3] ];
                t.dynamic.changed:= true;
              fi;
            fi;
          fi;
        elif pos[1] = "main" and pos[2][2] = 2 then
          # The click happened on the unique data column.
          i:= pos[2][1];
          if IsEvenInt( i ) then
            for link in t.dynamic.link.main[ i/2 ] do
              if pos[2][3] = link[1] + BrowseData.HeightCategories( t, i )
                 and link[2] <= pos[2][4] and pos[2][4] <= link[3] then
                # The click happened on this link.
                jump:= false;
                if t.dynamic.activeLink = fail or
                   t.dynamic.activeLink[1] <> "main" or
                   t.dynamic.activeLink[2] <> i/2 or
                   t.dynamic.activeLink[3] <> link then
                  BrowseData.SetActiveLink( t, "main", i/2, link );
                  if flag then
                    jump:= true;
                    t.dynamic.changed:= true;
                  else
                    break;
                  fi;
                else
                  jump:= true;
                  t.dynamic.changed:= true;
                fi;
                if jump then
                  # Set the active link, and call its action.
                  BrowseData.SetActiveLink( t, "main", i/2, link );
                  link:= link[4];
                  if IsBound( t.work.linkActions.( link[1] ) ) then
                    CallFuncList( t.work.linkActions.( link[1] ),
                        Concatenation( [ t ], link[2] ) );
                  fi;
                  break;
                fi;
              fi;
            od;
          fi;
        fi;

        return t.dynamic.changed;
      end;

      selectNextLink:= function( t )
        local oldlink, oldlinkpos, links, i, list;

        # If no link was selected before then select the link in the header.
        if t.dynamic.activeLink = fail then
          BrowseData.SetActiveLink( t, "header", 0, t.dynamic.link.header[1] );
          return;
        fi;

        oldlink:= t.dynamic.activeLink;
        oldlinkpos:= oldlink[4];

        links:= t.dynamic.link.main;
        if oldlink[1] = "header" then
          # The link in the header was selected,
          # take the first link in an expanded cell.
          for i in [ 1 .. Length( links ) ] do
            list:= links[i];
            if not IsEmpty( list ) and 0 < BrowseData.HeightRow( t, 2*i ) then
              BrowseData.SetActiveLink( t, "main", i, list[1] );
              return;
            fi;
          od;
        else
          # A link in the list was selected,
          # take the next one in an expanded cell.
          i:= oldlink[2];
          list:= links[i];
          pos:= Position( list, oldlink[3] );
          if pos < Length( list ) and 0 < BrowseData.HeightRow( t, 2*i ) then
            # Take the next link in the same cell.
            BrowseData.SetActiveLink( t, "main", i, list[ pos + 1 ] );
            return;
          else
            # Take a link in another expanded cell.
            for i in [ oldlink[2] + 1 .. Length( links ) ] do
              list:= links[i];
              if not IsEmpty( list ) and 0 < BrowseData.HeightRow( t, 2*i ) then
                BrowseData.SetActiveLink( t, "main", i, list[1] );
                return;
              fi;
            od;

            # Take the link in the header.
            BrowseData.SetActiveLink( t, "header", 0, t.dynamic.link.header[1] );
          fi;
        fi;
      end;

      selectPreviousLink:= function( t )
        local oldlink, oldlinkpos, links, i, list;

        links:= t.dynamic.link.main;

        # If no link was selected before then
        # take the last link in an expanded cell.
        if t.dynamic.activeLink = fail then
          for i in Reversed( [ 1 .. Length( links ) ] ) do
            list:= links[i];
            if not IsEmpty( list ) and 0 < BrowseData.HeightRow( t, 2*i ) then
              BrowseData.SetActiveLink( t, "main", i, list[ Length( list ) ] );
              return;
            fi;
          od;

          # Take the link in the header.
          BrowseData.SetActiveLink( t, "header", 0, t.dynamic.link.header[1] );
          return;
        fi;

        oldlink:= t.dynamic.activeLink;
        oldlinkpos:= oldlink[4];

        links:= t.dynamic.link.main;
        if oldlink[1] = "header" then
          # The link in the header was selected,
          # take the last link in an expanded cell.
          for i in Reversed( [ 1 .. Length( links ) ] ) do
            list:= links[i];
            if not IsEmpty( list ) and 0 < BrowseData.HeightRow( t, 2*i ) then
              BrowseData.SetActiveLink( t, "main", i, list[ Length( list ) ] );
              return;
            fi;
          od;
        else
          # A link in the list was selected,
          # take the previous one in an expanded cell.
          i:= oldlink[2];
          list:= links[i];
          pos:= Position( list, oldlink[3] );
          if 1 < pos and 0 < BrowseData.HeightRow( t, 2*i ) then
            # Take the next link in the same cell.
            BrowseData.SetActiveLink( t, "main", i, list[ pos - 1 ] );
            return;
          else
            # Take a link in another expanded cell.
            for i in Reversed( [ 1 .. oldlink[2] - 1 ] ) do
              list:= links[i];
              if not IsEmpty( list ) and 0 < BrowseData.HeightRow( t, 2*i ) then
                BrowseData.SetActiveLink( t, "main", i, list[ Length( list ) ] );
                return;
              fi;
            od;

            # Take the link in the header.
            BrowseData.SetActiveLink( t, "header", 0, t.dynamic.link.header[1] );
          fi;
        fi;
      end;

      toggleCategoryOrFollowActiveLink:= function( t )
        local link;

        if   t.dynamic.selectedCategory <> [ 0, 0 ] then
          # Expand or collapse the category.
          BrowseData.actions.ClickOrToggle.action( t );
        elif t.dynamic.activeLink <> fail then
          # Follow the active link.
          link:= t.dynamic.activeLink;
          if link[1] = "main" then
            # The active link is in the main table.
            # Follow it only if the cell is expanded.
            if BrowseData.HeightRow( t, 2 * link[2] ) = 0 then
              return false;
            fi;
          fi;

          link:= link[3][4];
          if IsBound( t.work.linkActions.( link[1] ) ) then
            CallFuncList( t.work.linkActions.( link[1] ),
                Concatenation( [ t ], link[2] ) );
            return true;
          fi;
        fi;

        return false;
      end;

      # extended `ShowTables' function:
      # - show grids inside table cells
      myShowTables:= function( t )
        local ws, tl, bl, min, max, win, inittrow, i, offset, attr, sel, grid;

        BrowseData.ShowTables( t );
        ws:= BrowseData.WindowStructure( t );
        tl:= t.dynamic.topleft;
        bl:= BrowseData.BottomOrRight( t, "vert" );
        min:= tl[1];
        if IsInt( bl ) then
          max:= 2 * t.work.m + 1;
        else
          max:= bl[1];
        fi;
        if BrowseData.IsQuietSession( t.dynamic.replay ) then
          win:= 0;
        else
          win:= t.dynamic.window;
        fi;
        inittrow:= ws.topmargin + ws.headerLength + ws.labelsheight;
        offset:= ws.topmargin + ws.headerLength + ws.labelsheight + 1 - tl[3];
        for i in [ min .. max ] do
          offset:= offset + BrowseData.HeightCategories( t, i );
          if IsBound( t.dynamic.grid[i] )
             and 0 < BrowseData.HeightRow( t, i ) then
            grid:= ShallowCopy( t.dynamic.grid[i] );
            if grid.trow + offset < inittrow then
              grid.trow:= inittrow;
              grid.rowinds:= Filtered( grid.rowinds + offset,
                                       x -> x >= inittrow );
              if Length( grid.rowinds )
                   < Length( t.dynamic.grid[i].rowinds ) then
                grid.tend:= false;
              fi;
            else
              grid.trow:= grid.trow + offset;
              grid.rowinds:= grid.rowinds + offset;
            fi;
            grid.lcol:= grid.lcol + BrowseData.WidthCol( t, 1 );
            grid.rcol:= grid.rcol + BrowseData.WidthCol( t, 1 );
            grid.colinds:= grid.colinds + BrowseData.WidthCol( t, 1 );
            grid.brow:= grid.brow + offset;
            attr:= NCurses.attrs.NORMAL;
            sel:= t.dynamic.selectedEntry;
            mode:= BrowseData.CurrentMode( t );
            if sel[1] = i and
               ( mode.name = "select_row" or
                 ( mode.name = "select_entry" and sel[2] = 4 ) or
                 ( mode.name = "select_row_and_entry" and sel[2] <> 4 ) ) then
              attr:= NCurses.attrs.STANDOUT;
            elif sel[2] = 4 and
               ( mode.name = "select_column" or
                 ( mode.name = "select_column_and_entry"
                   and sel[1] <> i ) ) then
              attr:= NCurses.attrs.STANDOUT;
            fi;
            if not BrowseData.IsQuietSession( t.dynamic.replay ) then
              NCurses.GridExt( win, grid, attr );
            fi;
          fi;
          offset:= offset + BrowseData.HeightRow( t, i );
        od;
      end;

      # Create help mode and browse mode.
      # The browse mode differs from the one in standard browse applications,
      # as follows:
      # - It *does not support*
      #   - switching ("se", "sr", "sc"),
      #   - searching (because this would mean switching),
      #   - filtering (which would hide rows depending on the contents), and
      #   - resetting the table (clearing sorting/categorizing/hiding);
      # - *Changed* are the actions for
      #   - mouse clicks on links inside table cells (select a link or follow
      #     a link instead of selecting a whole cell),
      #   - for <Return> and <Enter> (follow a link inside a cell instead of
      #     executing a function that depends on the mode and the whole cell)
      # - *New* are
      #   - <Tab>, <ShiftTab> for navigating through the links.
      modes:= [ First( BrowseData.defaults.work.availableModes,
                       r -> r.name = "help" ),
                BrowseData.CreateMode( "browse_with_links", "browse",
                    myShowTables, [
        # standard actions
        [ [ "E" ], BrowseData.actions.Error ],
        [ [ "q", [ [ 27 ], "<Esc>" ] ],
          BrowseData.actions.QuitMode ],
        [ [ "Q" ], BrowseData.actions.QuitTable ],
        [ [ "?", [ [ NCurses.keys.F1 ], "<F1>" ] ],
          BrowseData.actions.ShowHelp ],
        [ [ [ [ NCurses.keys.F2 ], "<F2>" ] ],
          BrowseData.actions.SaveWindow ],
        [ [ [ [ 14 ], "<Ctrl-N>" ] ], BrowseData.actions.DoNothing ],
        # scroll
        [ [ [ [ NCurses.keys.HOME ], "<Home>" ] ],
          BrowseData.actions.ScrollToFirstRow ],
        [ [ [ [ NCurses.keys.END ], "<End>" ] ],
          BrowseData.actions.ScrollToLastRow ],
        [ [ "R" ], BrowseData.actions.ScrollScreenRight ],
        [ [ "L" ], BrowseData.actions.ScrollScreenLeft ],
        [ [ "D", [ [ NCurses.keys.NPAGE ], "<PageDown>" ],
          [ [ 32 ], "<Space>" ] ],
          BrowseData.actions.ScrollScreenDown ],
        [ [ "U", [ [ NCurses.keys.PPAGE ], "<PageUp>" ] ],
          BrowseData.actions.ScrollScreenUp ],
        [ [ "r", [ [ NCurses.keys.RIGHT ], "<Right>" ] ],
          BrowseData.actions.ScrollCellRight ],
        [ [ "l", [ [ NCurses.keys.LEFT ], "<Left>" ] ],
          BrowseData.actions.ScrollCellLeft ],
        [ [ "d", [ [ NCurses.keys.DOWN ], "<Down>" ] ],
          BrowseData.actions.ScrollCellDown ],
        [ [ "u", [ [ NCurses.keys.UP ], "<Up>" ] ],
          BrowseData.actions.ScrollCellUp ],
        # mouse events
        [ [ "M" ], BrowseData.actions.ToggleMouseEvents ],
        [ [ [ [ NCurses.keys.MOUSE, "BUTTON1_PRESSED" ],
              "<Mouse1Down>" ],
            [ [ NCurses.keys.MOUSE, "BUTTON1_CLICKED" ],
              "<Mouse1Click>" ] ], rec(
          helplines:= [
            "select the current category row or link;",
            "if the current link was already selected",
            "then follow this link;",
            "if the current category row was already selected",
            "then collapse/expand this category row" ],
          action:= function( t, data )
            return myDealWithMouseClick( t, data, false );
          end ) ],
        [ [ [ [ NCurses.keys.MOUSE, "BUTTON1_DOUBLE_CLICKED" ],
              "<Mouse1DoubleClick>" ] ], rec(
          helplines:= [
            "select the current category row or link;",
            "in the latter case, follow this link;",
            "if the current category row was already selected",
            "then collapse/expand this category row" ],
          action:= function( t, data )
            return myDealWithMouseClick( t, data, true );
          end ) ],
        # expand and collapse
        [ [ "X" ], BrowseData.actions.ExpandAllCategories ],
        [ [ "C" ], BrowseData.actions.CollapseAllCategories ],
        # navigate
        [ [ [ [ 13 ], "<Return>" ], [ [ NCurses.keys.ENTER ], "<Enter>" ] ],
          rec(
          helplines:= [ "toggle (expand/collapse) the selected category,",
                        "or follow the active link" ],
          action:= toggleCategoryOrFollowActiveLink ) ],
        [ [ [ [ 9 ], "<Tab>" ] ], rec(
          helplines:= [ "select the next link" ],
          action:= selectNextLink ) ],
        [ [ [ [ 353 ], "<ShiftTab>" ] ], rec(
          helplines:= [ "select the previous link" ],
          action:= selectPreviousLink ) ],
      ] ) ];

      BrowseData.defaults.work.customizedModes.ctbllib:= modes;
    fi;
    modes:= BrowseData.defaults.work.customizedModes.ctbllib;

    # Construct the window history in the first header line.
    windowhistory:= JoinStringsWithSeparator( stack, " -> " );
    len:= Length( windowhistory );
    while SizeScreen()[1] - 3 < len do
      pos:= PositionSublist( windowhistory, " -> " );
      if pos = fail then
        windowhistory:= Concatenation( "...", windowhistory{
            [ len - ( SizeScreen()[1] - 7 ) .. len ] } );
      elif windowhistory[1] <> '.' then
        windowhistory:= Concatenation( "...",
            windowhistory{ [ pos .. len ] } );
      else
        pos:= PositionSublist( windowhistory, " -> ", pos );
        if pos = fail then
          windowhistory:= Concatenation( "...", windowhistory{
              [ len - ( SizeScreen()[1] - 7 ) .. len ] } );
        else
          windowhistory:= Concatenation( "...", windowhistory{
              [ pos .. len ] } );
        fi;
      fi;
      len:= Length( windowhistory );
    od;

    # Construct the browse table.
    t:= rec(
      work:= rec(
        align:= "tl",
        availableModes:= modes,
        header:= [ windowhistory,
                   "",
                   Concatenation( [ NCurses.attrs.UNDERLINE, true,
                     title,
                     NCurses.attrs.UNDERLINE, false,
                     "  " ],
                     CTblLib.OpenLink,
                     [ "(show table)" ],
                     CTblLib.CloseLink ) ],
        main:= main,
        sepCol:= [ "  ", "" ],
        sepRow:= [ " " ],
        sepCategories:= " ",

        linkActions:= BrowseData.LinkActions,
      ),
      dynamic:= rec(
        activeModes:= [ First( modes, x -> x.name = "browse_with_links" ) ],
        categories:= [ List( cats, x -> x.pos ), cats, [] ],

        stack:= stack,
        link:= rec( header:= headerlink,
                    main:= mainlink ),
        activeLink:= fail,
        grid:= grid,
      ),
    );

    if log <> fail then
      t.dynamic.log:= log;
      t.dynamic.replay:= replay;
    fi;

    return t;
end );


#############################################################################
##
#F  BrowseCTblLibInfo( [<func>, <val>, ...] )
#F  BrowseCTblLibInfo( <tbl> )
#F  BrowseCTblLibInfo( <name>[, <p>] )
##
##  <#GAPDoc Label="BrowseCTblLibInfo">
##  <ManSection>
##  <Func Name="BrowseCTblLibInfo" Arg='[func, val, ...]'/>
##  <Func Name="BrowseCTblLibInfo" Arg='tbl' Label="for a character table"/>
##  <Func Name="BrowseCTblLibInfo" Arg='name[, p]' Label="for a name"/>
##
##  <Returns>
##  nothing.
##  </Returns>
##
##  <Description>
##  Called without arguments,
##  <Ref Func="BrowseCTblLibInfo"/> shows the contents of the
##  &GAP; Character Table Library in an <E>overview table</E>, see below.
##  <P/>
##  When arguments <A>func</A>, <A>val</A>, <A>...</A> are given
##  that are admissible arguments for <Ref Func="AllCharacterTableNames"/>
##  &ndash;in particular, the first argument must be a function&ndash;
##  then the overview is restricted to those character tables that match the
##  conditions.
##  The global option <C>"OrderedBy"</C> is supported as in
##  <Ref Func="AllCharacterTableNames"/>.
##  <P/>
##  When <Ref Func="BrowseCTblLibInfo"/> is called with a character table
##  <A>tbl</A> then a <E>details table</E> is opened that gives an overview
##  of the information available for this character table.
##  When <Ref Func="BrowseCTblLibInfo"/> is called with a string <A>name</A>
##  that is an admissible name for an ordinary character table
##  then the details table for this character table is opened.
##  If a prime integer <A>p</A> is entered in addition to <A>name</A> then
##  information about the <A>p</A>-modular character table is shown instead.
##  <P/>
##  The overview table has the following columns.
##  <P/>
##  <List>
##  <Mark><C>name</C></Mark>
##  <Item>
##     the
##     <Ref Func="Identifier" Label="for character tables" BookName="ref"/>
##     value of the table,
##  </Item>
##  <Mark><C>size</C></Mark>
##  <Item>
##    the group order,
##  </Item>
##  <Mark><C>nccl</C></Mark>
##  <Item>
##    the number of conjugacy classes,
##  </Item>
##  <Mark><C>fusions -> G</C></Mark>
##  <Item>
##    the list of identifiers of tables on which a fusion
##    to the given table is stored, and
##  </Item>
##  <Mark><C>fusions G -></C></Mark>
##  <Item>
##    the list of identifiers of tables to which a fusion is stored
##    on the given table.
##  </Item>
##  </List>
##  <P/>
##  The details table for a given character table has exactly one column.
##  Only part of the functionality of the function
##  <Ref Func="NCurses.BrowseGeneric" BookName="Browse"/> is available
##  in such a table.
##  On the other hand,
##  the details tables contain <Q>links</Q> to other Browse applications,
##  for example other details tables.
##  <P/>
##  When one <Q>clicks</Q> on a row or an entry in the overview table then
##  the details table for the character table in question is opened.
##  One can navigate from this details table to a related one,
##  by first <E>activating</E> a link (via repeatedly hitting the <B>Tab</B>
##  key) and then <E>following</E> the active link (via hitting the
##  <B>Return</B> key).
##  If mouse actions are enabled (by hitting the <B>M</B> key, see
##  <Ref Func="NCurses.UseMouse" BookName="browse"/>) then one can
##  alternatively activate a link and click on it via mouse actions.
##  <P/>
##  <Example><![CDATA[
##  gap> tab:= [ 9 ];;         # hit the TAB key
##  gap> n:= [ 14, 14, 14 ];;  # ``do nothing'' input (means timeout)
##  gap> BrowseData.SetReplay( Concatenation(
##  >         # select the first column, search for the name A5
##  >         "sc/A5", [ NCurses.keys.DOWN, NCurses.keys.DOWN,
##  >         NCurses.keys.RIGHT, NCurses.keys.ENTER ],
##  >         # open the details table for A5
##  >         [ NCurses.keys.ENTER ], n, n,
##  >         # activate the link to the character table of A5
##  >         tab, n, n,
##  >         # show the character table of A5
##  >         [ NCurses.keys.ENTER ], n, n, "seddrr", n, n,
##  >         # close this character table
##  >         "Q",
##  >         # activate the link to the maximal subgroup D10
##  >         tab, tab, n, n,
##  >         # jump to the details table for D10
##  >         [ NCurses.keys.ENTER ], n, n,
##  >         # close this details table
##  >         "Q",
##  >         # activate the link to a decomposition matrix
##  >         tab, tab, tab, tab, tab, n, n,
##  >         # show the decomposition matrix
##  >         [ NCurses.keys.ENTER ], n, n,
##  >         # close this table
##  >         "Q",
##  >         # activate the link to the AtlasRep overview
##  >         tab, tab, tab, tab, tab, tab, tab, n, n,
##  >         # show the overview
##  >         [ NCurses.keys.ENTER ], n, n,
##  >         # close this table
##  >         "Q",
##  >         # and quit the applications
##  >         "QQ" ) );
##  gap> BrowseCTblLibInfo();
##  gap> BrowseData.SetReplay( false );
##  ]]></Example>
##  </Description>
##  </ManSection>
##  <#/GAPDoc>
##
BindGlobal( "BrowseCTblLibInfo", function( arg )
    local sel_action, columnids, columns, columnsext, choice, args, t,
          aligned, groupname, p, name;

    if Length( arg ) = 0 or IsFunction( arg[1] ) then

      # Construct the overview table.
      sel_action:= function( t )
        local groupname;

        if t.dynamic.selectedEntry <> [ 0, 0 ] then
          groupname:= choice[ 
              t.dynamic.indexRow[ t.dynamic.selectedEntry[1] ] / 2 ];
          BrowseData.LinkActions.( "details page" )( t, groupname, 0 );
        fi;
      end;

      columnids:= [ "self", "Size", "NrConjugacyClasses",
          "NamesOfFusionSources", "FusionsTo", "KnowsSomeGroupInfo" ];
      columns:= List( columnids,
          id -> CTblLib.Data.IdEnumerator.attributes.( id ) );
      columnsext:= List( columnids,
          id -> CTblLib.Data.IdEnumeratorExt.attributes.( id ) );

      # The rows of the table will be sorted in the same way as the
      # result of 'AllCharacterTableNames'.
      choice:= CallFuncList( AllCharacterTableNames, arg );

      args:= [ CTblLib.Data.IdEnumerator,
        # no row labels (one cannot search for them)
        [],
        # columns of the table
        columnids,
        # header
        t -> BrowseData.HeaderWithRowCounter( t,
                 "GAP Character Table Library Overview", t.work.m ),
        # no footer
        [],
        # restrict the choice, and support the global option
        choice ];

      t:= CallFuncList( BrowseTableFromDatabaseIdEnumerator, args );

      # Adjust the functions that create table entries and category values
      # (row labels do not appear in our table).
      # Note that we have to deal with two enumerators.
      aligned:= function( list, align )
        local max;

        if IsEmpty( list ) then
          return list;
        fi;
        max:= Maximum( List( list, Length ) );
        if align = "left" then
          max:= - max;
        fi;
        return List( list, x -> String( x, max ) );
      end;

      t.work.Main:= function( t, i, j )
        local id, width, attr, val, align;

        id:= choice[i];
        width:= t.work.widthCol;
        if id in CTblLib.Data.IdEnumerator.identifiers then
          attr:= columns[j];
        else
          attr:= columnsext[j];
        fi;

        # Compute the attribute value, and the table cell data object.
        val:= attr.viewValue( attr.attributeValue( attr, id ) );

        # Format the entry.
        if not IsRecord( val ) then
          if IsBound( width[ 2*j ] ) then
            if 'l' in attr.align then
              align:= "left";
            else
              align:= "right";
            fi;
            if IsString( val ) then
              # It is documented that non-strings need no additional
              # formatting if the column width is prescribed.
              val:= rec( rows:= aligned( SplitString(
                           BrowseData.ReallyFormatParagraph( val,
                                     width[ 2*j ], align ), "\n" ),
                             align ),
                         align:= attr.align );
            fi;
          else
            val:= rec( rows:= [ val ], align:= attr.align );
          fi;
        fi;
        return val;
      end;

      t.work.CategoryValues:= function( t, i, j )
        local id, val;

        i:= i / 2;
        j:= j / 2;
        id:= choice[i];
        if id in CTblLib.Data.IdEnumerator.identifiers then
          val:= columns[j].attributeValue( columns[j], id );
          val:= columns[j].categoryValue( val );
        else
          val:= columnsext[j].attributeValue( columnsext[j], id );
          val:= columnsext[j].categoryValue( val );
        fi;
        return BrowseData.CategoryValuesFromEntry( t, val, j );
      end;

      # Install the 'Click' code (not available in the default).
      t.work.Click:= rec(
        select_entry:= rec(
          helplines:= [ "open an overview for the selected entry" ],
          action:= sel_action ),
        select_row:= rec(
          helplines:= [ "open an overview for the selected row" ],
          action:= sel_action ),
        select_row_and_entry:= rec(
          helplines:= [ "open an overview for the selected entry" ],
          action:= sel_action ),
        select_column_and_entry:= rec(
          helplines:= [ "open an overview for the selected entry" ],
          action:= sel_action ),
      );

    elif Length( arg ) = 1 and IsCharacterTable( arg[1] ) then
      groupname:= Identifier( arg[1] );
      p:= UnderlyingCharacteristic( arg[1] );
      if p <> 0 then
        name:= PartsBrauerTableName( groupname );
        if name <> fail then
          groupname:= name.ordname;
        fi;
      fi;
      t:= BrowseCTblLibInfo_GroupInfoTable( groupname, p,
              fail, fail, [ groupname ] );
    elif Length( arg ) = 1 and IsString( arg[1] ) then
      groupname:= arg[1];
      t:= BrowseCTblLibInfo_GroupInfoTable( groupname, 0,
              fail, fail, [ groupname ] );
    elif Length( arg ) = 2 and IsString( arg[1] ) and IsPosInt( arg[2] ) then
      groupname:= arg[1];
      p:= arg[2];
      t:= BrowseCTblLibInfo_GroupInfoTable( groupname, p,
              fail, fail, [ groupname ] );
    else
      Error( "usage: BrowseCTblLibInfo( [<conditions>] ) or\n",
             "  BrowseCTblLibInfo( <tbl> ) or\n",
             "  BrowseCTblLibInfo( <name>[, <p>] )" );
    fi;

    if t = fail then
      NCurses.Alert(
        Concatenation( "Sorry, no details for ", groupname ), 2000,
        NCurses.attrs.BOLD );
    else
      NCurses.BrowseGeneric( t );
    fi;
    end );


#############################################################################
##
#E

