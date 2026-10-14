#############################################################################
##
#W  atlasimp.g           GAP 4 package CTblLib                  Thomas Breuer
##
##  This file contains the function 'BrowseAtlasImprovements'
##  and some code that was used to translate the contents of the file
##  'app2a.tex' to the JSON format file that is contained in
##  'data/atlasimp.json'.
##


#############################################################################
##
#F  CTblLib.SplitAtSubstring( <string>, <substring> )
##
CTblLib.SplitAtSubstring:= function( string, substring )
    local result, len, sublen, pos, pos2;

    result:= [];
    len:= Length( string );
    sublen:= Length( substring );
    pos:= 1;
    while pos <> fail do
      pos2:= PositionSublist( string, substring, pos - 1 );
      if pos2 = fail then
        Add( result, string{ [ pos .. len ] } );
      else
        Add( result, string{ [ pos .. pos2 - 1 ] } );
        pos2:= pos2 + sublen;
      fi;
      pos:= pos2;
    od;

    return result;
end;


#############################################################################
##
#F  CTblLib.AtlasErrorsData( <filename> )
##
##  Create the data list from the LaTeX file 'app2a.tex' or 'ABCerr.tex'
##  (if you have it).
##
CTblLib.AtlasErrorsData:= function( filename )
    local ABC, str, sections, records, sstr, pos, pos2, r, new, start,
          next, curr, line, type, text, page, lpage, lgroup, group, entry;

    ABC:= EndsWith( filename, "ABCerr.tex" );

    # Fetch the relevant sections
    str:= StringFile( filename );
    if ABC then
      sections:= CTblLib.SplitAtSubstring( str, "\\bf " );
      sections:= sections{ [ 2 .. Length( sections ) ] };
    else
      # from ``Introduction'' to ``Bibliography''.
      sections:= CTblLib.SplitAtSubstring( str, "\\section*" );
      sections:= sections{ [ 3 .. Length( sections ) - 1 ] };
    fi;

    # Run over the sections.
    records:= [];
    for sstr in sections do
      # Extract the title.
      if ABC then
        pos:= 0;
      else
        pos:= Position( sstr, '{' );
      fi;
      pos2:= Position( sstr, '}' );
      r:= rec( title:= sstr{ [ pos + 1 .. pos2 - 1 ] } );

      # Remove comments (from '%' to the next line break).
      new:= "";
      start:= 1;
      pos:= Position( sstr, '%' );
      while pos <> fail do
        pos2:= Position( sstr, '\n', pos );
        if pos2 = fail then
          Append( new, sstr{ [ start .. Length( sstr ) ] } );
          pos:= fail;
        else
          Append( new, sstr{ [ start .. pos-1 ] } );
          start:= pos2;
          pos:= Position( sstr, '%', start );
        fi;
      od;
      if new = "" then
        new:= sstr;
      fi;

      # Split the section into entries.
      # Omit the first line, which consists of formatting instructions.
      new:= CTblLib.SplitAtSubstring( new, "\\cr" );
      new:= new{ [ 2 .. Length( new ) ] };

      # Split each entry into column values.  We create the columns
      # - type (one of "***", "C", "M", "NEW"),
      # - page number,
      # - group name (may be empty),
      # - text.
      next:= [];
      curr:= 0;
      for line in new do
        pos:= Position( line, '&' );
        if pos <> fail then
          type:= line{ [ 1 .. pos - 1 ] };
          type:= ReplacedString( type, " ", "" );
          type:= ReplacedString( type, "\n", "" );
          if type = "" then
            # continuation of the previous text
            pos2:= PositionSublist( line, "&&&&&" );
            if pos2 <> fail then
              Append( next[ curr ][4],
                  Concatenation( "\n", line{ [ pos2+5 .. Length( line ) ] } ) );
            else
              pos2:= PositionSublist( line, "&&&&" );
              if pos2 = fail then
                Error( "&?" );
              fi;
              Append( next[ curr ][4],
                  Concatenation( "\n", line{ [ pos2+4 .. Length( line ) ] } ) );
            fi;
          elif PositionSublist( line, "\\halign" ) = fail then
            if not type in [ "***", "C", "M", "NEW" ] then
              Error( "unexpected type '", type, "'" );
            fi;
            pos2:= Position( line, '&', pos );
            if pos2 <> fail then
              if pos2 <> pos + 1 then
                page:= line{ [ pos + 1 .. pos2 - 1 ] };
              fi;
              if line{ [ pos2 .. pos2+2 ] } = "&:&" then
                # three columns, not group related
                text:= line{ [ pos2+3 .. Length( line ) ] };
                curr:= curr + 1;
                next[ curr ]:= [ type, page, "", text ];
              else
                # five to seven columns
                pos:= pos2;
                pos2:= Position( line, '&', pos );
                page:= Concatenation( page, " ",
                           line{ [ pos + 1 .. pos2 - 1 ] } );
                pos:= pos2;
                pos2:= Position( line, '&', pos );
                lgroup:= line{ [ pos + 1 .. pos2 - 1 ] };
                if lgroup = ":" then
                  # five columns, not group related
                  curr:= curr + 1;
                  text:= line{ [ pos2+1 .. Length( line ) ] };
                  next[ curr ]:= [ type, page, "", text ];
                elif line{ [ pos2 .. pos2+2 ] } = "&:&" then
                  # six columns
                  text:= line{ [ pos2+3 .. Length( line ) ] };
                  curr:= curr + 1;
                  if lgroup <> "" then
                    group:= lgroup;
                  fi;
                  next[ curr ]:= [ type, page, group, text ];
                elif line{ [ pos2 .. pos2+1 ] } = "&&" then
                  # six columns
                  text:= line{ [ pos2+2 .. Length( line ) ] };
                  curr:= curr + 1;
                  if lgroup <> "" then
                    group:= lgroup;
                  fi;
                  next[ curr ]:= [ type, page, group, text ];
                else
                  # seven columns (belongs to bibliography, page and line)
                  pos:= pos2;
                  pos2:= Position( line, '&', pos );
                  lpage:= Concatenation( page, " ",
                              line{ [ pos + 1 .. pos2 - 1 ] } );
                  pos:= pos2;
                  pos2:= Position( line, '&', pos );
                  lpage:= Concatenation( lpage, " ",
                              line{ [ pos + 1 .. pos2 - 1 ] } );
                  text:= line{ [ pos2+1 .. Length( line ) ] };
                  curr:= curr + 1;
                  if lgroup <> "" then
                    group:= lgroup;
                  fi;
                  next[ curr ]:= [ type, lpage, group, text ];
                fi;
              fi;
            fi;
          fi;
        fi;
      od;

      for entry in next do
        # Keep empty lines as paragraph separators.
        entry[4]:= ReplacedString( entry[4], "\n\n", " <<nl>> " );
        # Omit a trailing comma in group names.
        if entry[3] <> "" and entry[3][ Length( entry[3] ) ] = ',' then
          Unbind( entry[3][ Length( entry[3] ) ] );
        fi;
        # Omit a trailing colon in page numbers.
        if entry[2] <> "" and entry[2][ Length( entry[2] ) ] = ':' then
          Unbind( entry[2][ Length( entry[2] ) ] );
        fi;
      od;
      r.entries:= List( next, entry -> List( entry, NormalizedWhitespace ) );
      for entry in r.entries do
        entry[4]:= ReplacedString( entry[4], " <<nl>> ", "<<nl>>" );
      od;
      Add( records, r );
    od;

    return records;
end;


#############################################################################
##
#F  BrowseAtlasImprovements( [<choice>] )
##
##  <#GAPDoc Label="BrowseAtlasImprovements">
##  <ManSection>
##  <Func Name="BrowseAtlasImprovements" Arg='[choice]'/>
##
##  <Returns>
##  nothing.
##  </Returns>
##
##  <Description>
##  Called without argument or with the string <C>"ordinary"</C>,
##  <Ref Func="BrowseAtlasImprovements"/> shows the lists of improvements to
##  the &ATLAS; of Finite Groups <Cite Key="CCN85"/>
##  that are contained in <Cite Key="BN95"/> and <Cite Key="AtlasImpII"/>.
##  <P/>
##  Called with the string <C>"modular"</C>,
##  <Ref Func="BrowseAtlasImprovements"/> shows the list of improvements to
##  the &ATLAS; of Brauer Characters <Cite Key="JLPW95"/>
##  that are contained in <Cite Key="ABCImp"/>.
##  <P/>
##  Called with <K>true</K>, the concatenation of the above lists are shown.
##  <P/>
##  The overview table contains one row for each improvement,
##  and has the following columns.
##  <P/>
##  <List>
##  <Mark><C>Section</C></Mark>
##  <Item>
##    the part in the &ATLAS; to which the entry belongs
##    (Introduction, The Groups, Additional information, Bibliography,
##    Appendix 1, Appendix 2),
##  </Item>
##  <Mark><C>Src</C></Mark>
##  <Item>
##    <C>1</C> for entries from <Cite Key="BN95"/>,
##    <C>2</C> for entries from <Cite Key="AtlasImpII"/>,
##    and <C>3</C> for entries from <Cite Key="ABCImp"/>,
##  </Item>
##  <Mark><C>Typ</C></Mark>
##  <Item>
##    the type of the improvement, one of
##    <C>***</C> (for mathematical errors),
##    <C>NEW</C> (for new information),
##    <C>C</C> (for improvements concerning grammar or notational
##    consistency), or
##    <C>M</C> (for misprints or cases of illegibility),
##  </Item>
##  <Mark><C>Page</C></Mark>
##  <Item>
##    the page and perhaps the line in the (ordinary or modular) &ATLAS;,
##  </Item>
##  <Mark><C>Group</C></Mark>
##  <Item>
##    the name of the simple group to which the entry belongs
##    (empty for entries not from the section <Q>The Groups</Q>),
##  </Item>
##  <Mark><C>Text</C></Mark>
##  <Item>
##    the description of the entry,
##  </Item>
##  <Mark><C>**</C></Mark>
##  <Item>
##    for each entry of the type <C>***</C>, the subtype of the error
##    to which some statements in <Cite Key="BMO17"/> refer, one of
##    <C>CH</C> (character values),
##    <C>P</C> (power maps, element orders, and class names),
##    <C>FI</C> (fusions and indicators),
##    <C>I</C> (Introduction, Bibliography, the list showing
##    the orders of multipliers and outer automorphism group,
##    and the list of Conway polynomials),
##    <C>MP</C> (maps),
##    <C>MX</C> (descriptions of maximal subgroups), and
##    <C>G</C> (other information about the group).
##  </Item>
##  </List>
##  <P/>
##  The full functionality of the function
##  <Ref Func="NCurses.BrowseGeneric" BookName="Browse"/> is available.
##  <P/>
##  The following example shows the input for
##  first restricting the list to errors (type <C>***</C>),
##  then categorizing the filtered list by the subtype of the error,
##  and then expanding the category for the subtype <C>CH</C>.
##  <P/>
##  <Example><![CDATA[
##  gap> n:= [ 14, 14, 14, 14, 14, 14 ];;  # ``do nothing''
##  gap> enter:= [ NCurses.keys.ENTER ];;
##  gap> BrowseData.SetReplay( Concatenation(
##  >        "scrr",                   # select the 'Typ' column,
##  >        "f***", enter,            # filter rows containing '***',
##  >        "scrrrrrrsc", enter,      # categorize by the error kind
##  >        "sr", enter,              # expand the 'CH' category
##  >        n, "Q" ) );               # and quit
##  gap> BrowseAtlasImprovements();
##  gap> BrowseData.SetReplay( false );
##  ]]></Example>
##  </Description>
##  </ManSection>
##  <#/GAPDoc>
##
BindGlobal( "BrowseAtlasImprovements", function( choice... )
    local ordinary, modular, dir, file, str, simplifiedPageNumber,
          simplifiedGroupName, formattedText, data, matrix, sections, r,
          entry, source, row, pagewidth, groupwidth, descrwidth, t, i;

    ordinary:= true;
    modular:= false;
    if Length( choice ) = 1 then
      if choice[1] = true or choice[1] = "modular" then
        modular:= true;
      fi;
      if choice[1] = "modular" then
        ordinary:= false;
      fi;
    fi;

    dir:= DirectoriesPackageLibrary( "ctbllib", "data" )[1];
    if ordinary and not IsBound( CTblLib.AtlasImprovements ) then
      file:= Filename( dir, "atlasimp.json" );
      str:= StringFile( file );
      if str = fail then
        Error( "the data file '", file, "' is not available" );
      fi;
      CTblLib.AtlasImprovements:= AGR.GapObjectOfJsonText( str ).value.data;
    fi;
    if modular and not IsBound( CTblLib.ABCImprovements ) then
      file:= Filename( dir, "abcimp.json" );
      str:= StringFile( file );
      if str = fail then
        Error( "the data file '", file, "' is not available" );
      fi;
      CTblLib.ABCImprovements:= AGR.GapObjectOfJsonText( str ).value.data;
    fi;

    simplifiedPageNumber:= function( pagenumber )
      pagenumber:= ReplacedString( pagenumber, "p. ", "" );
      return ReplacedString( pagenumber, "Page ", "" );
    end;

    # Remove LaTeX markup from group names, and uniformize
    # O_n^+(q) and O^+_n(q) (both occur in the source files).
    simplifiedGroupName:= function( latexname )
      local list, entry;

      list:= [ [ "$", "" ], [ "O^-_8", "O_8^-" ], [ "O^+_8", "O_8^+" ],
               [ "O^-_{10}", "O_{10}^-" ], [ "O^+_{10}", "O_{10}^+"],
               [ "^", "" ], [ "_", "" ], [ "{", "" ], [ "}", "" ] ];

      for entry in list do
        latexname:= ReplacedString( latexname, entry[1], entry[2] );
      od;

      return latexname;
    end;

    formattedText:= function( text, width )
      # Remove \\- (hyphenation).
      text:= ReplacedString( text, "\\-", "" );

      # Finally, format the text; the <<nl>> marks separate paragraphs.
      text:= List( CTblLib.SplitAtSubstring( text, "<<nl>>" ),
               x -> BrowseData.ReallyFormatParagraph( x, width, "left" ) );
      return SplitString( JoinStringsWithSeparator( text, "\n\n" ), "\n" );
    end;

    data:= [];
    if ordinary then
      Append( data, CTblLib.AtlasImprovements );
    fi;
    if modular then
      Append( data, CTblLib.ABCImprovements );
    fi;
    matrix:= [];
    sections:= [];
    for r in data do
      if not r.section in sections then
        Add( sections, r.section );
      fi;
      for entry in r.entries do
        source:= "3";
        if IsBound( r.source ) then
          source:= r.source;
        fi;
        if Length( entry ) = 4 then
          row:= Concatenation( [ r.section, source ], entry, [ "" ] );
        else
          row:= Concatenation( [ r.section, source ], entry );
        fi;
        row[4]:= simplifiedPageNumber( row[4] );
        row[5]:= simplifiedGroupName( row[5] );
        Add( matrix, row );
      od;
    od;
    sections:= List( sections, LowercaseString );

    # Prescribe widths:
    # Columns 2, 3, 7 are assumed to have widths 3, 3, 2.
    # The widths of columns 4 and 5 are computed.
    # Column 1 is assumed to be used for categorizing,
    # in order to leave more space for column 6, which takes what is left.
    pagewidth:= Maximum( List( matrix, l -> Length( l[4] ) ) );
    groupwidth:= Maximum( List( matrix, l -> Length( l[5] ) ) );
    descrwidth:= SizeScreen()[1] - pagewidth - groupwidth - 18;

    matrix:= List( matrix, entry ->
      [ rec( align:= "tl", rows:= [ entry[1] ] ),
        rec( align:= "tc", rows:= [ entry[2] ] ),
        rec( align:= "tr", rows:= [ entry[3] ] ),
        rec( align:= "tl", rows:= [ entry[4] ] ),
        rec( align:= "tl", rows:= [ entry[5] ] ),
        rec( align:= "tl", rows:= formattedText( entry[6], descrwidth ) ),
        rec( align:= "tl", rows:= [ entry[7] ] ) ] );

    # Construct the browse table.
    t:= rec(
      work:= rec(
        align:= "tl",
        header:= t -> BrowseData.HeaderWithRowCounter( t,
                   "Improvements to the ATLAS",
                   Length( matrix ) ),
        main:= matrix,
        labelsCol:= [ [ rec( rows:= [ "Section" ], align:= "l" ),
                        rec( rows:= [ "Src" ], align:= "l" ),
                        rec( rows:= [ "Typ" ], align:= "l" ),
                        rec( rows:= [ "Page" ], align:= "l" ),
                        rec( rows:= [ "Group" ], align:= "l" ),
                        rec( rows:= [ "Text" ], align:= "l" ),
                        rec( rows:= [ "**" ], align:= "l" ) ] ],
        sepLabelsCol:= "=",
        sepRow:= "-",
        sepCol:= [ "|" ],
        widthCol:= [ ,,, 3,, 3,, pagewidth,, groupwidth,, descrwidth,, 2 ],
        SpecialGrid:= BrowseData.SpecialGridLineDraw,
        CategoryValues:= function( t, i, j )
          local val;

          val:= BrowseData.defaults.work.CategoryValues( t, i, j );
          if val = [ "(empty category)" ] then
            if j = 10 then   # "Group"
              val:= [ "(not assigned to a group)" ];
            elif j = 14 then # "**"
              val:= [ "(not a mathematical error)" ];
            fi;
          elif j = 4 then # "Src"
            if val = [ "1" ] then
              val:= [ "from [BN95]" ];
            elif val = [ "2" ] then
              val:= [ "from [Nor]" ];
            elif val = [ "3" ] then
              val:= [ "from [ABC]" ];
            fi;
          fi;

          return val;
        end,
      ),
      dynamic:= rec(
        sortFunctionsForColumns:= [
          function( val1, val2 )
            return Position( sections, val1 ) < Position( sections, val2 );
          end ],
      ),
    );

    # Customize the sort parameters.
    for i in [ 1, 2, 3, 4, 5, 7 ] do
      BrowseData.SetSortParameters( t, "column", i,
          [ "add counter on categorizing", "yes" ] );
    od;

    # Show the browse table.
    NCurses.BrowseGeneric( t );
end );


#############################################################################
##
##  Add the Browse application to the list shown by `BrowseGapData'.
##
BrowseGapDataAdd( "ATLAS Improvements",
    BrowseAtlasImprovements, false, "\
the lists of improvements to the ATLAS of Finite Groups \
that are contained in [BN95] and [Nor]. \\
Try ?BrowseAtlasImprovements for details" );


#############################################################################
##
#E

