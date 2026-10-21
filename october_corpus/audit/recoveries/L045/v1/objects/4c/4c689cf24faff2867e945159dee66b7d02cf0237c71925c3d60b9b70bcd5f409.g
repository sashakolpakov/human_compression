#############################################################################
##
#W  atlasbro.g           GAP 4 package CTblLib                  Thomas Breuer
##
##  This file contains 'Browse' related functions for showing ATLAS stuff.
##
##  1. Show the tables related to a simple group as in the ATLAS.
##  2. Show the map of an ATLAS group.
##  3. Show the table of contents of the ATLAS.
##


#############################################################################
##
##  1. Show the tables related to a simple group as in the ATLAS.
##


#############################################################################
##
#F  BrowseAtlasTable( <filename> )
#F  BrowseAtlasTable( <simpname>[, <p>] )
##
##  <#GAPDoc Label="BrowseAtlasTable">
##  <ManSection>
##  <Func Name="BrowseAtlasTable" Arg='name[, p]'/>
##
##  <Returns>
##  nothing.
##  </Returns>
##
##  <Description>
##  <Ref Func="BrowseAtlasTable"/> displays the character tables of bicyclic
##  extensions of the simple group with the name <A>name</A> in a window,
##  in the same format as the &ATLAS; of Finite Groups <Cite Key="CCN85"/>
##  and the &ATLAS; of Brauer Characters <Cite Key="JLPW95"/> do.
##  For that, it is necessary that these tables are known,
##  as well as the class fusions between them and perhaps additional
##  information (e.&nbsp;g., about the existence of certain extensions).
##  These requirements are fulfilled if the tables are contained in
##  the &ATLAS;, but they may hold also in other cases.
##  <P/>
##  If a prime <A>p</A> is given as the second argument then the
##  <A>p</A>-modular Brauer tables are shown, otherwise (or if <A>p</A> is
##  zero) the ordinary tables are shown.
##  <P/>
##  <Example><![CDATA[
##  gap> d:= [ NCurses.keys.DOWN ];;  r:= [ NCurses.keys.RIGHT ];;
##  gap> c:= [ NCurses.keys.ENTER ];;
##  gap> BrowseData.SetReplay( Concatenation(
##  >        "/y",          # Find the string y,
##  >        c,             # start the search,
##  >        "nnnn",        # Find more occurrences,
##  >        "Q" ) );       # and quit the application.
##  gap> BrowseAtlasTable( "A6" );
##  gap> BrowseData.SetReplay( false );
##  ]]></Example>
##  <P/>
##  The function uses <Ref Func="NCurses.BrowseGeneric" BookName="browse"/>.
##  The identifier of the table is used as the static header.
##  The strings <C>X_1</C>, <C>X_2</C>, <M>\ldots</M> are used as row labels
##  for those table rows that contain character values,
##  and column labels are given by centralizer orders, power map information,
##  and class names.
##  </Description>
##  </ManSection>
##  <#/GAPDoc>
##
BindGlobal( "BrowseAtlasTable", function( arg )
    local history, scan, simpname, p, r, tblnames, comp, colwidths, n,
          fuscols, fuscolpos, fuspos, pos, l, i, row, jj, j, ii, gridfun,
          header, labelscol, width, str, size, len, matrix, offset;

    history:= rec();
    if Length( arg ) = 1 and IsString( arg[1] )
                         and IsReadableFile( arg[1] ) then
      # We assume that the file contains the required tables
      # in Cambridge format.
      scan:= CTblLib.ScanCambridgeFormatFile( arg[1] );
    else
      # The first argument must be the name of a simple ATLAS group.
      if Length( arg ) = 1 and IsString( arg[1] ) then
        # ordinary tables
        simpname:= arg[1];
        p:= 0;
      elif Length( arg ) = 2 and IsString( arg[1] )
                             and ( arg[2] = 0 or IsPrimeInt( arg[2] ) ) then
        # Brauer tables
        simpname:= arg[1];
        p:= arg[2];
      elif Length( arg ) = 1 and IsRecord( arg[1] ) then
        # variant that admits passing history
        simpname:= arg[1].name;
        p:= arg[1].char;
        history:= arg[1].history;
      else
        Error( "usage: BrowseAtlasTable( <simpname>[, <p>] )" );
      fi;

      r:= rec( name:= simpname, char:= p );
      if not CTblLib.StringsAtlasMap_CompleteData( r ) then
        # Some information is missing, a message has been printed already.
        return;
      fi;
      tblnames:= r.identifiers;

      # For some ATLAS groups, not all tables/fusions are available (yet);
      # we reduce the choice of tables to a smaller set.
      str:= StringOfCambridgeFormat( tblnames, p );
      if str = fail then
        if   simpname = "O8+(3)" then
          tblnames:= tblnames{ [ 1 ] }{ [ 1 ] };
        elif simpname = "2E6(2)" then
          tblnames:= tblnames{ [ 1, 2 ] }{ [ 1, 2 ] };
        else
          return fail;
        fi;
        str:= StringOfCambridgeFormat( tblnames, p );
      fi;
      if p <> 0 then
        simpname:= Concatenation( simpname, " mod ", String( p ) );
      fi;
      scan:= CTblLib.ScanCambridgeFormatFile( simpname, str );
    fi;

    # Split the data rows into entries.
    for comp in [ "#1", "#2", "#3", "#4", "#5", "#6", "#7", "#9" ] do
      if IsBound( scan.( comp ) ) then
        scan.( comp ):= List( scan.( comp ),
                              l -> List( l, r -> SplitString( r, " " ) ) );
      fi;
    od;

    # Compute column widths.
    # Note that some negative column widths occur in the ATLAS source files.
    colwidths:= List( List( scan.( "#7" )[1][1], Int ), AbsInt );
    n:= Length( colwidths );
#T remove this line?

    # Deal with the formatting information in the fusion columns.
    # - The symbols are always right justified,
    #   except if '?' symbols shift them to the left.
    #   At most two '?' can occur, which happens for "O8+(3)".
    #   (We must *not* replace the '?' symbols in indicator columns.)
    # - Write down the positions of pipes to be shown in separating rows.
    #   The positions of the 'fus' and 'ind' columns are given by the '#4'
    #   line.
    #   Whenever the 'ind' entry of a row is empty and the 'fus' entry is
    #   nonempty, we have to draw a fusion symbol up to the next row
    #   in which the entry of the 'fus' line is the same as the one in the
    #   current line.
    fuscols:= Positions( scan.( "#4" )[1][1], "fus" );
    fuscolpos:= List( fuscols, x -> Sum( colwidths{ [ 1 .. x-1 ] } ) );
    fuspos:= [];
    pos:= 0;
    for n in [ 1 .. Length( scan.( "#5" ) ) ] do
      l:= scan.( "#5" )[n];
      for i in [ 1 .. Length( l ) ] do
        pos:= pos + 2;
        row:= l[i];
        for jj in [ 1 .. Length( fuscols ) ] do
          j:= fuscols[ jj ];
          if row[ j + 1 ] = "|" and row[j] <> "|" then
            ii:= i;
            repeat
              ii:= ii - 1;
              if ii = 0 then
                # This happens for U3(8) mod 2.
                break;
              fi;
            until Length( l[ii][j] ) = Length( row[j] );
            if ii <> 0 then
              Append( fuspos, List( [ 3 .. 2*( i-ii ) + 1 ],
                  x -> [ pos - x, fuscolpos[ jj ] + 4 - Length( row[j] ) ] ) );
            fi;
          fi;
          row[j]:= ReplacedString( row[j], "?", " " );
        od;
      od;
      if IsBound( scan.( "#6" ) ) and IsBound( scan.( "#6" )[n] ) then
        # There must be an empty line below a dashed row portion,
        # except for the last portion of the whole table.
        pos:= pos + Length( scan.( "#6" )[n] ) + 1
              + Number( scan.( "#6" )[n], x -> x[1] = "no:" );
      fi;
    od;

    # Enter fusion signs (inside row separator lines)
    # using the 'SpecialGrid' component.
    gridfun:= function( t, data )
      local xmin, x0, ymin, y0, win, entry, x, y;

      xmin:= data.leftmargin + data.labelswidth;
      x0:= xmin - t.dynamic.topleft[4] + 1
           - Sum( t.work.widthCol{ [ 1 .. t.dynamic.topleft[2] - 1 ] }, 0 );

      ymin:= data.topmargin + data.headerLength + data.labelsheight;
      y0:= ymin - t.dynamic.topleft[3] + 1
           - Sum( t.work.heightRow{ [ 1 .. t.dynamic.topleft[1] - 1 ] }, 0 );

      win:= t.dynamic.window;
      size:= data.heightWidthWindow;

      for entry in fuspos do
        y:= y0 + entry[1];
        x:= x0 + entry[2];
        if xmin <= x and ymin <= y and x < size[2] and y < size[1] then
          # The fusion symbol appears in the visible area.
          NCurses.wmove( win, y, x );
          NCurses.waddch( win, NCurses.lineDraw.VLINE );
        fi;
      od;
    end;

    header:= scan.( "#23" )[1][1];
    if '?' in header then
      header:= header{ [ Position( header, '?' ) + 2 .. Length( header ) ] };
    fi;

    # Create the default table.
    r:= rec(
      work:= rec(
        align:= "c",
        header:= [ [ NCurses.attrs.BOLD, true, header ], "" ],
        labelsRow:= [],
        sepCol:= Concatenation( [ " " ], List( [ 1 .. n-1 ], x -> "" ),
                                [ " " ] ),
        sepRow:= [ "" ],
        widthCol:= Concatenation( TransposedMat(
                                      [ 0 * colwidths, colwidths ] ) ),
        SpecialGrid:= gridfun,
      ),
      dynamic:= rec(),
    );

    # Fill the column label rows.
    labelscol:= [ scan.( "#9" )[1][1] ];
    labelscol[2]:= List( labelscol[1], x -> "" );
    for comp in [ "#1", "#2", "#3", "#4" ] do
      Add( labelscol, scan.( comp )[1][1] );
    od;
    Add( labelscol, List( labelscol[1], x -> "" ) );
    width:= colwidths[1] + colwidths[2];
    str:= String( "p power", width );
    labelscol[4][1]:= str{ [ 1 .. colwidths[1] ] };
    labelscol[4][2]:= str{ [ colwidths[1] + 1 .. width ] };
    str:= String( "p' part", width );
    labelscol[5][1]:= str{ [ 1 .. colwidths[1] ] };
    labelscol[5][2]:= str{ [ colwidths[1] + 1 .. width ] };

    # The first centralizer order is shown in the first two columns.
    size:= labelscol[3][2];
    len:= Length( size );
    if len < width then
      str:= String( size, width - 1 );
      labelscol[3][1]:= str{ [ 1 .. colwidths[1] - 1 ] };
      labelscol[3][2]:= str{ [ colwidths[1] .. width - 1 ] };
    else
      str:= String( size{ [ 1 .. len - width + 1 ] }, width );
      labelscol[2][1]:= str{ [ 1 .. colwidths[1] ] };
      labelscol[2][2]:= str{ [ colwidths[1] + 1 .. width ] };
      str:= size{ [ len - width + 2 .. len ] };
      labelscol[3][1]:= str{ [ 1 .. colwidths[1] - 1 ] };
      labelscol[3][2]:= str{ [ colwidths[1] .. width - 1 ] };
    fi;

    # Distribute the other centralizer orders to two rows if necessary.
    for i in [ 3 .. Length( colwidths ) ] do
      len:= Length( labelscol[3][i] );
      if 2 * colwidths[i] - 2 < len then
        # There is no space for the centralizer order plus separating
        # whitespace in two lines.  Fill the *first* line completely,
        # and put the rest right justified into the *second* line.
        labelscol[2][i]:= labelscol[3][i]{ [ 1 .. colwidths[i] ] };
        labelscol[3][i]:= labelscol[3][i]{ [ colwidths[i] + 1 .. len ] };
      elif colwidths[i] <= len then
        # The centralizer order plus separating whitespace fits into two
        # lines.  Fill the *second* line except for the separator,
        # and put the rest right justified into the *first* line.
        labelscol[2][i]:= labelscol[3][i]{ [ 1 .. len - colwidths[i] + 1 ] };
        labelscol[3][i]:= labelscol[3][i]{ [ len - colwidths[i] + 2
                                             .. len ] };
      fi;
    od;

    # Create the rows and the row labels.
    matrix:= [];
    offset:= 0;
    for i in [ 1 .. Length( scan.( "#5" ) ) ] do
      Append( matrix, scan.( "#5" )[ i ] );
      Append( r.work.sepRow, List( [ 1 .. Length( scan.( "#5" )[i] ) ],
                                   x -> [ " " ] ) );
      Append( r.work.labelsRow,
              List( offset + [ 1 .. Length( scan.( "#5" )[i] ) ],
                    x -> [ Concatenation( "X_", String( x ) ) ] ) );

      if IsBound( scan.( "#6" ) ) and IsBound( scan.( "#6" )[i] ) then
        # There may be "and" and "no." rows for dashed row portions.
        Append( matrix, scan.( "#6" )[i] );
        Append( r.work.labelsRow, List( scan.( "#6" )[i], x -> [ "" ] ) );
        for j in [ 1 .. Length( scan.( "#6" )[i] ) - 1 ] do
          if scan.( "#6" )[i][j][1] = "no:" then
            # There must be an empty line below a dashed row portion,
            # except for the last portion of the whole table.
            Add( r.work.sepRow, [ " " ] );
          else
            Add( r.work.sepRow, [ "" ] );
          fi;
        od;

        Add( r.work.sepRow, [ " " ] );
      fi;

      offset:= offset + Length( scan.( "#5" )[i] );
    od;
    r.work.labelsCol:= labelscol;
    r.work.main:= matrix;
    for l in Concatenation( labelscol, r.work.main ) do
      for i in [ 1 .. Length( l ) ] do
        if l[i] = "|" then
          l[i]:= "";
        fi;
      od;
    od;

    # Enter the history if available.
    if IsBound( history.log ) and IsBound( history.replay ) then
      r.dynamic.log:= history.log;
      r.dynamic.replay:= history.replay;
    fi;

    NCurses.BrowseGeneric( r );
    end );


#############################################################################
##
##  2. Show the map of an ATLAS group.
##


#############################################################################
##
#F  BrowseAtlasMap( <arec> )
#F  BrowseAtlasMap( <name>[, <p>] )
##
##  <#GAPDoc Label="BrowseAtlasMap">
##  <ManSection>
##  <Func Name="BrowseAtlasMap" Arg='name[, p]'/>
##
##  <Returns>
##  nothing.
##  </Returns>
##
##  <Description>
##  For a string <A>name</A> that is the identifier of the character table
##  of a simple group from the &ATLAS; of Finite Groups <Cite Key="CCN85"/>,
##  <Ref Func="BrowseAtlasMap"/> shows the map that describes the bicyclic
##  extensions of this group, see <Cite Key="CCN85" Where="Chapter 6"/>.
##  If the optional argument <A>p</A> is not given or if <A>p</A> is zero
##  then the map for the ordinary character tables is shown,
##  if <A>p</A> is a prime integer then the map for the <A>p</A>-modular
##  Brauer character tables is shown, as in <Cite Key="JLPW95"/>.
##  <P/>
##  Clicking on a square of the map opens the character table information
##  for the extension in question, by calling
##  <Ref Func="BrowseCTblLibInfo"/>.
##  <P/>
##  <Example><![CDATA[
##  gap> d:= [ NCurses.keys.DOWN ];;  r:= [ NCurses.keys.RIGHT ];;
##  gap> c:= [ NCurses.keys.ENTER ];;
##  gap> BrowseData.SetReplay( Concatenation(
##  >        "T",           # show the ATLAS table for (extensions of) M12
##  >        "Q",           # quit the ATLAS table,
##  >        "se",          # select the box of the simple group,
##  >        c,             # click the box,
##  >        "Q",           # quit the info overview for M12,
##  >        r, d,          # select the box for the bicyclic extension,
##  >        c,             # click the box,
##  >        "Q",           # quit the info overview,
##  >        "Q" ) );       # and quit the application.
##  gap> BrowseAtlasMap( "M12" );
##  gap> BrowseData.SetReplay( false );
##  ]]></Example>
##  </Description>
##  </ManSection>
##  <#/GAPDoc>
##
BindGlobal( "BrowseAtlasMap", function( arg )
    local arec, groupname, good, comp, repl, repllabels, shortened, widthCol,
          i, heightRow, firstline, leftlabels, main, j, modes, mode,
          sel_action, specialGrid, table;

    if Length( arg ) = 1 and IsString( arg[1] ) then
      arec:= rec( name:= arg[1] );
    elif Length( arg ) = 1 and IsRecord( arg[1] ) then
      arec:= ShallowCopy( arg[1] );
    elif Length( arg ) = 2 and IsString( arg[1] )
                           and ( arg[2] = 0 or IsPrimeInt( arg[2] ) ) then
      arec:= rec( name:= arg[1], char:= arg[2] );
    else
      Error( "usage: BrowseAtlasMap( <name>[, <p>] ) ",
             "or BrowseAtlasMap( <arec> )" );
    fi;

    if not CTblLib.StringsAtlasMap_CompleteData( arec ) then
      return fail;
    fi;

    if arec.char = 0 then
      groupname:= arec.name;
    else
      groupname:= Concatenation( arec.name,
                                 " (Mod ", String( arec.char ), ")" );
    fi;

    # Omit rows corresponding to dashed names if wanted.
    if ( not IsBound( arec.showdashedrows ) )
       or arec.showdashedrows <> true then
      good:= Positions( arec.dashedhorz, false );
      for comp in [ "identifiers", "labels", "labelsrow", "shapes",
                    "dashedhorz" ] do
        if IsBound( arec.( comp ) ) then
          arec.( comp ):= arec.( comp ){ good };
        fi;
      od;
    fi;

    # Browse does not support special characters.
    repl:= function( str )
      str:= ReplacedString( str, "₁", "_1" );
      str:= ReplacedString( str, "₂", "_2" );
      str:= ReplacedString( str, "₃", "_3" );

      return str;
    end;

    repllabels:= List( arec.labels, row -> List( row, repl ) );

    # Some labels do not fit into their boxes ...
    shortened:= function( label, shape )
      local max, pos;

      if shape = "open" then
        max:= 8;
      else
        max:= 7;
      fi;
      while Length( label ) > max do
        pos:= Position( label, '_' );
        if pos = fail then
          break;
        fi;
        label:= label{ Concatenation( [ 1 .. pos - 1 ],
                           [ pos + 1 .. Length( label ) ] ) };
      od;
      return label;
    end;

    if true in arec.dashedhorz then
      # The dashed names are shown in the first separator column,
      # by the function that inserts the grids.
      widthCol:= [ Maximum( List( repllabels{
                                      Positions( arec.dashedhorz, true ) },
                                  l -> Length( l[1] ) ) ) + 1 ];
    else
      widthCol:= [ 0 ];
    fi;
    for i in arec.dashedvert do
      if i then
        Append( widthCol, [ 3, 1 ] );
      else
        Append( widthCol, [ 9, 1 ] );
      fi;
    od;
    widthCol[ Length( widthCol ) ]:= Maximum(
                                       List( arec.labelsrow, Length ) ) + 1;

    if true in arec.dashedvert then
      # The dashed names are shown above the first row of boxes,
      # by the function that inserts the grids.
      heightRow:= [ 1 ];
      firstline:= CTblLib.AtlasMapFirstLine( repllabels[1],
                      widthCol{ [ 2, 4 .. Length( widthCol ) - 1 ] },
                      arec.dashedvert );
    else
      heightRow:= [ 0 ];
      firstline:= fail;
    fi;
    leftlabels:= [];
    for i in [ 1 .. Length( arec.dashedhorz ) ] do
      if arec.dashedhorz[i] then
        Append( heightRow, [ 2, 0 ] );
        leftlabels[i]:= String( repllabels[i][1], widthCol[1] - 1 );
      else
        Append( heightRow, [ 5, 0 ] );
      fi;
    od;
    heightRow[ Length( heightRow ) ]:= 1;

    main:= [];
    for i in [ 1 .. Length( arec.labels ) ] do
      main[i]:= [];
      for j in [ 1 .. Length( arec.labels[i] ) ] do
        if arec.shapes[i][j] in [ "closed", "open", "broken" ] and
           not arec.dashedhorz[i] and not arec.dashedvert[j] then
          main[i][j]:= rec( rows:= [ shortened( repllabels[i][j],
                                                arec.shapes[i][j] ) ],
                            align:= "c" );
        else
          main[i][j]:= rec( rows:= [ "" ], align:= "c" );
        fi;
      od;
    od;

    # Construct the extended modes if necessary.
    if not IsBound( BrowseData.defaults.work.customizedModes.atlasmap ) then
      # Create a shallow copy of each default mode for 'Browse',
      # and add new actions to all available modes (except the help mode):
      # - T: Open the ATLAS format table.
      modes:= List( BrowseData.defaults.work.availableModes,
                    BrowseData.ShallowCopyMode );
      BrowseData.defaults.work.customizedModes.atlasmap:= modes;
      for mode in modes do
        if mode.name <> "help" then
          BrowseData.SetActions( mode, [
            [ [ "T" ], rec( helplines := [
                 "open the corresponding ATLAS format character table" ],
              action := function( t )
                BrowseAtlasTable( rec( name:= t.arec.name,
                                       char:= t.arec.char,
                                       history:= rec(
                                         log:= t.dynamic.log,
                                         replay:= t.dynamic.replay ) ) );
                return t.dynamic.changed;
              end ) ],
          ] );
        fi;
      od;
    else
      modes:= BrowseData.defaults.work.customizedModes.atlasmap;
    fi;

    # Provide functionality for the 'Click' function.
    sel_action:= rec(
      helplines:= [ "open the relevant character table information" ],
      action:= function( t )
        local pos, id, dispname;

        if t.dynamic.selectedEntry <> [ 0, 0 ] then
          pos:= [ t.dynamic.indexRow[ t.dynamic.selectedEntry[1] ] / 2,
                  t.dynamic.indexCol[ t.dynamic.selectedEntry[2] ] / 2 ];
          if arec.shapes[ pos[1] ][ pos[2] ] <> "empty" then
            id:= arec.identifiers[ pos[1] ][ pos[2] ];
            if LibInfoCharacterTable( id  ) <> fail then
              if arec.char = 0 then
                dispname:= id;
              else
                dispname:= Concatenation( id, " mod ", String( arec.char ) );
              fi;
              t:= BrowseCTblLibInfo_GroupInfoTable( id, arec.char,
                      t.dynamic.log, t.dynamic.replay,
                      [ dispname ] );
              if t = fail then
                NCurses.Alert(
                    Concatenation( "Sorry, no details for ", dispname ),
                    2000, NCurses.attrs.BOLD );
              else
                NCurses.BrowseGeneric( t );
              fi;
            fi;
          fi;
        fi;
      end );

    # Provide the function that inserts the grid
    # after the texts have been rendered.
    # (The local variables 'firstline', 'arec', 'leftlabels', 'widthCol'
    # are used inside this function.)
    specialGrid:= function( t, data )
      local win, size, ld, trow, top, left, right, bottom, lcol, from,
            to, cutfirstline, i, hr, brow, j, wc, rcol, flag, attrs,
            shape;

      win:= t.dynamic.window;
      size:= NCurses.getmaxyx( win );
      if size = false then
        return false;
      fi;

      ld:= NCurses.lineDraw;
      trow:= data.headerLength;
      top:= t.dynamic.topleft{ [ 1, 3 ] };
      left:= t.dynamic.topleft{ [ 2, 4 ] };
      right:= BrowseData.BottomOrRight( t, "horz" );
      if IsInt( right ) then
        # The right end of the table is visible.
        right:= size[2] - right + data.leftmargin;
      else
        # The right end of the table is not visible.
        right:= size[2];
      fi;
      bottom:= BrowseData.BottomOrRight( t, "vert" );
      if IsInt( bottom ) then
        # The lower end of the table is visible.
        bottom:= size[1] - bottom;
      else
        # The lower end of the table is not visible.
        bottom:= size[1];
      fi;

      if top = [ 1, 1 ] and firstline <> fail then
        # Add the dashed names on the top.
        # Determine the column from where the line starts.
        lcol:= data.leftmargin;
        if left[1] = 1 then
          lcol:= lcol + t.work.widthCol[1] - left[2] + 1;
        fi;
        # Determine what to cut out from the line.
        from:= 1;
        for i in [ 2 .. left[1] - 1 ] do
          from:= from + t.work.widthCol[i];
        od;
        from:= from - left[2] + 1;
        to:= from + right - lcol;
        if Length( firstline ) < to then
          cutfirstline:= firstline{ [ from .. Length( firstline ) ] };
        else
          cutfirstline:= firstline{ [ from .. to ] };
        fi;
        NCurses.PutLine( win, trow, lcol, cutfirstline );
        trow:= trow + t.work.heightRow[1];
      fi;

      for i in [ 1 .. t.work.m ] do
        if top[1] <= 2 * i and trow < bottom then
          if arec.dashedhorz[i] and left[1] = 1 then
            # Add the dashed name on the left.
            NCurses.PutLine( win, trow, data.leftmargin,
              leftlabels[i]{ [ left[2] .. Length( leftlabels[i] ) ] } );
          fi;

          # Draw the boxes in the i-th row.
          hr:= t.work.heightRow[ 2*i ];
          brow:= trow + hr - 1;
          lcol:= data.leftmargin;
          if left[1] = 1 then
            lcol:= lcol + t.work.widthCol[1] - left[2] + 1;
          elif left[1] mod 2 = 1 then
            lcol:= lcol + t.work.widthCol[ left[1] ];
          fi;
          for j in [ 1 .. t.work.n ] do
            if left[1] <= 2 * j and lcol < right then
              wc:= t.work.widthCol[ 2*j ];
              rcol:= lcol + wc - 1;
              # Set attributes for this box.
              flag:= BrowseData.CurrentMode( t ).flag;
              if ( flag = "select_entry" and
                   t.dynamic.selectedEntry[1] = 2 * i and
                   t.dynamic.selectedEntry[2] = 2 * j ) or
                 ( flag = "select_row" and
                   t.dynamic.selectedEntry[1] = 2 * i ) or
                 ( flag = "select_column" and
                   t.dynamic.selectedEntry[2] = 2 * j ) then
                attrs:= NCurses.attrs.STANDOUT;
              else
                attrs:= NCurses.attrs.NORMAL;
              fi;
              NCurses.wattrset( win, attrs );
              shape:= arec.shapes[i][j];
              # At least the leftmost column of the box is visible.
              if shape in [ "closed", "open", "broken" ] and
                 ( left[1] < 2*j or ( left[1] = 2*j and left[2] = 1 ) ) and
                 ( top[1] < 2*i or ( top[1] = 2*i and top[2] = 1 ) ) then
                # upper left corner
                NCurses.wmove( win, trow, lcol );
                NCurses.waddch( win, ld.ULCORNER );
              fi;
              if shape in [ "closed", "open" ] and
                 ( not arec.dashedhorz[i] ) and
                 ( left[1] < 2*j or ( left[1] = 2*j and left[2] = 1 ) ) then
                # left vertical line
                NCurses.wmove( win, trow + 1, lcol );
                NCurses.wvline( win, ld.VLINE, 3 );
              fi;
              if shape = "broken" and
                 ( not arec.dashedhorz[i] ) and
                 ( left[1] < 2*j or ( left[1] = 2*j and left[2] = 1 ) ) then
                # left vertical lines
                NCurses.wmove( win, trow + 1, lcol );
                NCurses.wvline( win, ld.VLINE, 1 );
                NCurses.wmove( win, trow + 3, lcol );
                NCurses.wvline( win, ld.VLINE, 1 );
              fi;
              if shape in [ "closed", "broken" ] and
                 ( left[1] < 2*j or ( left[1] = 2*j and left[2] = 1 ) ) and
                 ( top[1] < 2*i or
                   ( top[1] = 2*i and top[2] <= brow - trow ) ) and
                 ( brow < bottom ) then
                # lower left corner
                NCurses.wmove( win, brow, lcol );
                NCurses.waddch( win, ld.LLCORNER );
              fi;
              # Part of the upper and lower horizontal lines may be visible.
              if shape in [ "closed", "open" ] and
                 ( lcol + 1 < right ) and
                 ( top[1] < 2*i or ( top[1] = 2*i and top[2] = 1 ) ) then
                # upper horizontal line
                NCurses.wmove( win, trow, lcol + 1 );
                NCurses.whline( win, ld.HLINE, rcol - lcol - 1 );
              fi;
              if shape = "closed" and
                 ( lcol + 1 < right ) and
                 ( top[1] < 2*i or
                   ( top[1] = 2*i and top[2] <= brow - trow ) ) and
                 ( brow < bottom ) then
                # lower horizontal line
                NCurses.wmove( win, brow, lcol + 1 );
                NCurses.whline( win, ld.HLINE, rcol - lcol - 1 );
              fi;
              if shape = "broken" and
                 ( not arec.dashedvert[j] ) and
                 ( lcol + 1 < right ) and
                 ( top[1] < 2*i or ( top[1] = 2*i and top[2] = 1 ) ) then
                # upper horizontal lines
                NCurses.wmove( win, trow, lcol + 1 );
                NCurses.whline( win, ld.HLINE, 2 );
                if lcol + 6 < right then
                  NCurses.wmove( win, trow, lcol + 6 );
                  NCurses.whline( win, ld.HLINE, 2 );
                fi;
              fi;
              if shape = "broken" and
                 ( not arec.dashedvert[j] ) and
                 ( lcol + 1 < right ) and
                 ( top[1] < 2*i or
                   ( top[1] = 2*i and top[2] <= brow - trow ) ) and
                 ( brow < bottom ) then
                # lower horizontal lines
                NCurses.wmove( win, brow, lcol + 1 );
                NCurses.whline( win, ld.HLINE, 2 );
                if lcol + 6 < right then
                  NCurses.wmove( win, brow, lcol + 6 );
                  NCurses.whline( win, ld.HLINE, 2 );
                fi;
              fi;
              # The rightmost column may be visible.
              if shape in [ "closed", "broken" ] and
                 ( rcol < right ) and
                 ( left[1] < 2*j or
                   ( left[1] = 2*j and left[2] <= rcol - lcol ) ) and
                 ( top[1] < 2*i or ( top[1] = 2*i and top[2] = 1 ) ) then
                # upper right corner
                NCurses.wmove( win, trow, rcol );
                NCurses.waddch( win, ld.URCORNER );
              fi;
              if shape in [ "closed", "broken" ] and
                 ( rcol < right ) and
                 ( left[1] < 2*j or
                   ( left[1] = 2*j and left[2] <= rcol - lcol ) ) and
                 ( top[1] < 2*i or
                   ( top[1] = 2*i and top[2] <= brow - trow ) ) and
                 ( brow < bottom ) then
                # lower right corner
                NCurses.wmove( win, brow, rcol );
                NCurses.waddch( win, ld.LRCORNER );
              fi;
              if shape = "closed" and
                 ( rcol < right ) and
                 ( not arec.dashedhorz[i] ) and
                 ( left[1] < 2*j or
                   ( left[1] = 2*j and left[2] <= rcol - lcol ) ) then
                # right vertical line
                NCurses.wmove( win, trow + 1, rcol );
                NCurses.wvline( win, ld.VLINE, 3 );
              fi;
              if shape = "broken" and
                 ( rcol < right ) and
                 ( not arec.dashedhorz[i] ) and
                 ( left[1] < 2*j or
                   ( left[1] = 2*j and left[2] <= rcol - lcol ) ) then
                # right vertical lines
                NCurses.wmove( win, trow + 1, rcol );
                NCurses.wvline( win, ld.VLINE, 1 );
                NCurses.wmove( win, trow + 3, rcol );
                NCurses.wvline( win, ld.VLINE, 1 );
              fi;
              # Reset the attributes.
              NCurses.wattrset( win, NCurses.attrs.NORMAL );
              lcol:= rcol + 2;
            fi;
          od;

          if arec.labelsrow[i] <> "" then
            # Add the i-th number on the right.
            NCurses.PutLine( win, trow + 2, rcol + 2,
                String( arec.labelsrow[i],
                        widthCol[ Length( widthCol ) ] - 1 ) );
          fi;

          trow:= brow + 1;
        fi;
      od;

      # Add the numbers on the bottom.
      lcol:= data.leftmargin;
      if left[1] mod 2 = 1 then
        lcol:= lcol + t.work.widthCol[ left[1] ];
      fi;
      for j in [ 1 .. t.work.n ] do
        if left[1] <= 2 * j and lcol <= right then
          wc:= t.work.widthCol[ 2 * j ];
          if arec.labelscol[j] <> "" then
            NCurses.PutLine( win, trow, lcol,
                String( arec.labelscol[j],
                    Int( ( 10 + Length( arec.labelscol[j] ) ) / 2 ) ) );
          fi;
          lcol:= lcol + wc + 1;
        fi;
      od;
    end;

    # Create the Browse table.
    table:= rec(
      arec:= arec,
      work:= rec(
        align:= "ct",
        header:= [ [ NCurses.attrs.BOLD, true, groupname ], "" ],
        heightRow:= heightRow,
        widthCol:= widthCol,
        main:= main,
        sepRow:= " ",
        sepCol:= [ " " ],
        corner:= [],
        availableModes:= modes,
        Click:= rec(
          select_entry:= sel_action,
          select_row_and_entry:= sel_action,
          select_column_and_entry:= sel_action,
        ),
        SpecialGrid:= specialGrid,
        cacheEntries:= true,
      ),
      dynamic:= rec(
        activeModes:= [ First( modes, x -> x.name = "browse" ) ],
      ),
    );

    # Enter the history if available.
    if IsBound( arec.log ) and IsBound( arec.replay ) then
      table.dynamic.log:= arec.log;
      table.dynamic.replay:= arec.replay;
    fi;

    NCurses.BrowseGeneric( table );
end );


#############################################################################
##
##  3. Show the table of contents of the ATLAS.
##


#############################################################################
##
#F  BrowseAtlasContents()
##
##  <#GAPDoc Label="BrowseAtlasContents">
##  <ManSection>
##  <Func Name="BrowseAtlasContents" Arg=''/>
##
##  <Returns>
##  nothing.
##  </Returns>
##
##  <Description>
##  <Ref Func="BrowseAtlasContents"/> shows the list of names of simple
##  groups and the corresponding page numbers in the
##  &ATLAS; of Finite Groups <Cite Key="CCN85"/>,
##  as given on page v of this book,
##  plus a few groups for which <Cite Key="JLPW95" Where="Appendix 2"/>
##  states that their character tables in &ATLAS; format have been obtained;
##  if applicable then also the corresponding page numbers in the
##  &ATLAS; of Brauer Characters <Cite Key="JLPW95"/> are shown.
##  <P/>
##  Clicking on a page number opens the &ATLAS; map for the group in
##  question, see <Ref Func="BrowseAtlasMap"/>.
##  (From the map, one can open the &ATLAS; style display using the input
##  <C>"T"</C>.)
##  <P/>
##  <Example><![CDATA[
##  gap> d:= [ NCurses.keys.DOWN ];;  r:= [ NCurses.keys.RIGHT ];;
##  gap> c:= [ NCurses.keys.ENTER ];;
##  gap> BrowseData.SetReplay( Concatenation(
##  >        "/J2",         # Find the string J2,
##  >        c,             # start the search,
##  >        r,             # select the page for the ordinary table,
##  >        c,             # click the entry,
##  >        "se",          # select the box of the simple group,
##  >        c,             # click the box,
##  >        "Q",           # quit the info overview for J2,
##  >        d,             # move down to 2.J2,
##  >        c,             # click the box,
##  >        "Q",           # quit the info overview for 2.J2,
##  >        "T",           # show the ATLAS table for (extensions of) J2
##  >        "Q",           # quit the ATLAS table,
##  >        "Q",           # quit the map,
##  >        r,             # select the page for the 2-modular table,
##  >        c,             # click the entry,
##  >        "T",           # show the 2-modular ATLAS table
##  >        "Q",           # quit the ATLAS table,
##  >        "Q",           # quit the map,
##  >        "Q" ) );       # and quit the application.
##  gap> BrowseAtlasContents();
##  gap> BrowseData.SetReplay( false );
##  ]]></Example>
##  </Description>
##  </ManSection>
##  <#/GAPDoc>
##
BindGlobal( "BrowseAtlasContents", function()
    local lines, entry, name, ordpages, info, i, sel_action, table;

    lines:= [];
    for entry in CTblLib.AtlasPages do
      name:= JoinStringsWithSeparator( entry[1], " = " );
      if Length( entry[2] ) > 1 then
        ordpages:= Concatenation( " (", String( entry[2][2] ), ")" );
      else
        ordpages:= "";
      fi;
      if Length( entry[2] ) > 0 then
        ordpages:= Concatenation( String( entry[2][1], 3 ),
                                  String( ordpages, -6 ) );
      fi;
      info:= [ rec( rows:= [ name ], align:= "l" ),
               ordpages ];
      for i in [ 2, 4 .. Length( entry[3] ) ] do
        Add( info, rec( rows:= [ Concatenation( String( entry[3][ i-1 ] ),
                                     ":", String( entry[3][i] ) ) ],
                        align:= "l" ) );
      od;
      Add( lines, info );
    od;

    # Provide functionality for the 'Click' function.
    sel_action:= rec(
      helplines:= [ "open the relevant ATLAS map" ],
      action:= function( t )
        local pos, entry, p;

        if t.dynamic.selectedEntry <> [ 0, 0 ] then
          pos:= [ t.dynamic.indexRow[ t.dynamic.selectedEntry[1] ] / 2,
                  t.dynamic.indexCol[ t.dynamic.selectedEntry[2] ] / 2 ];
          if pos[1] = 0 then
            return;
          fi;
          entry:= CTblLib.AtlasPages[ pos[1] ];
          if pos[2] <= 2 then
            # Show the map for the (available) ordinary table.
            BrowseAtlasMap( rec( name:= entry[1][1],
                                 char:= 0,
                                 log:= t.dynamic.log,
                                 replay:= t.dynamic.replay ) );
          elif Length( entry[3] ) >= 2 * ( pos[2] - 2 ) then
            # Show the map for the (available) Brauer table.
            BrowseAtlasMap( rec( name:= entry[1][1],
                                 char:= entry[3][ 2 * pos[2] - 5 ],
                                 log:= t.dynamic.log,
                                 replay:= t.dynamic.replay ) );
          fi;
        fi;
      end );

    table:= rec(
      work:= rec(
        align:= "ct",
        header:= [ "ATLAS Contents", "" ],
        main:= lines,
        sepRow:= "",
        sepCol:= [ "", " " ],
        corner:= [],
        Click:= rec(
          select_row:= sel_action,
          select_entry:= sel_action,
          select_row_and_entry:= sel_action,
          select_column_and_entry:= sel_action,
        ),
        cacheEntries:= true,
      ),
      dynamic:= rec(
        sortFunctionsForColumns:= List( [ 0, 1 ],
            x -> BrowseData.CompareAsNumbersAndNonnumbers ),
      ),
    );

    NCurses.BrowseGeneric( table );
end );


#############################################################################
##
##  Add the Browse application to the list shown by 'BrowseGapData'.
##
BrowseGapDataAdd( "ATLAS Contents",
    BrowseAtlasContents, false, "\
the list of names of simple groups and the corresponding page numbers \
in the ATLAS of Finite Groups, \
as shown on page v of this book; \
if applicable then also the corresponding page numbers in the \
ATLAS of Brauer Characters are shown. \
Clicking on a page number opens the ATLAS map for the group in question. \
Try ?BrowseAtlasContents for details" );


#############################################################################
##
#E

