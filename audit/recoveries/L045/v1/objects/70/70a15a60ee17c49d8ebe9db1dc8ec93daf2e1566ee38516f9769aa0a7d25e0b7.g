#############################################################################
##
#W  brctdiff.g           GAP 4 package CTblLib                  Thomas Breuer
##


#############################################################################
##
#F  BrowseCTblLibDifferences()
##
##  <#GAPDoc Label="BrowseCTblLibDifferences">
##  <ManSection>
##  <Func Name="BrowseCTblLibDifferences" Arg=''/>
##
##  <Returns>
##  nothing.
##  </Returns>
##
##  <Description>
##  <Ref Func="BrowseCTblLibDifferences"/> lists the differences between the
##  versions of the character table data in the
##  <Package>CTblLib</Package> package, since version 1.1.3.
##  <P/>
##  The overview table contains one row for each change,
##  where <Q>change</Q> means the addition, modification, or removal of
##  information,
##  and has the following columns.
##  <P/>
##  <List>
##  <Mark><C>Identifier</C></Mark>
##  <Item>
##    the
##    <Ref Func="Identifier" Label="for character tables" BookName="ref"/>
##    value of the character table,
##  </Item>
##  <Mark><C>Type</C></Mark>
##  <Item>
##    one of
##    <C>NEW</C> (for the addition of previously not available information),
##    <C>***</C> (for a bugfix), or
##    <C>C</C> (for a change that does not really fix a bug,
##    typically a change motivated by a new consistency criterion),
##  </Item>
##  <Mark><C>What</C></Mark>
##  <Item>
##    one of
##    <C>class fusions</C> (some class fusions from or to the
##    table in question were changed),
##    <C>maxes</C> (the value of the attribute <Ref Attr="Maxes"/>
##    was changed),
##    <C>names</C> (incorrect admissible names were removed),
##    <C>table</C> or <C>table mod </C><M>p</M> (the ordinary or
##    <M>p</M>-modular character table was changed),
##    <C>maxes</C> (the value of the attribute <Ref Attr="Maxes"/>
##    was changed),
##    <C>tom fusion</C> (the value of the attribute <Ref Attr="FusionToTom"/>
##    was changed),
##  </Item>
##  <Mark><C>Description</C></Mark>
##  <Item>
##    a description what has been changed,
##  </Item>
##  <Mark><C>Flag</C></Mark>
##  <Item>
##    one of
##    <C>Dup</C> (the table is a duplicate, in the sense of
##    <Ref Prop="IsDuplicateTable"/>),
##    <C>Der</C> (the row belongs to a character table that is derived from
##    other tables),
##    <C>Fus</C> (the row belongs to the addition of class fusions),
##    <C>Max</C> (the row belongs to a character table that was added
##    because its group is maximal in another group), or
##    <C>None</C> (in all other cases &ndash;these rows are to some extent
##    the interesting ones).
##    The information in this column can be used to restrict the overview
##    to interesting subsets.
##  </Item>
##  <Mark><C>Vers.</C></Mark>
##  <Item>
##    the package version in which the change described by the row appeared
##    first.
##  </Item>
##  </List>
##  <P/>
##  The full functionality of the function
##  <Ref Func="NCurses.BrowseGeneric" BookName="Browse"/> is available.
##  <P/>
##  The following examples show the input for
##  <P/>
##  <List>
##  <Item>
##    restricting the overview to error rows,
##  </Item>
##  <Item>
##    restricting the overview to <Q>None</Q> rows, and
##  </Item>
##  <Item>
##    restricting the overview to rows about a particular table.
##  </Item>
##  </List>
##  <P/>
##  <Example><![CDATA[
##  gap> n:= [ 14, 14, 14, 14, 14, 14 ];;  # ``do nothing''
##  gap> enter:= [ NCurses.keys.ENTER ];;
##  gap> down:= [ NCurses.keys.DOWN ];;
##  gap> right:= [ NCurses.keys.RIGHT ];;
##  gap> BrowseData.SetReplay( Concatenation(
##  >        "scr",                    # select the 'Type' column,
##  >        "f***", enter,            # filter rows containing '***',
##  >        n, "Q" ) );               # and quit
##  gap> BrowseCTblLibDifferences();
##  gap> BrowseData.SetReplay( Concatenation(
##  >        "scrrrr",                 # select the 'Flag' column,
##  >        "fNone", enter,           # filter rows containing 'None',
##  >        n, "Q" ) );               # and quit
##  gap> BrowseCTblLibDifferences();
##  gap> BrowseData.SetReplay( Concatenation(
##  >        "fM",                     # filter rows containing 'M',
##  >        down, down, down, right,  # but 'M' as a whole word,
##  >        enter,                    #
##  >        n, "Q" ) );               # and quit
##  gap> BrowseCTblLibDifferences();
##  gap> BrowseData.SetReplay( false );
##  ]]></Example>
##  </Description>
##  </ManSection>
##  <#/GAPDoc>
##
BindGlobal( "BrowseCTblLibDifferences", function()
    local file, str, namewidth, whatwidth, descrwidth, matrix, t, i;

    if not IsBound( CTblLib.DiffInfo ) then
      file:= Filename( DirectoriesPackageLibrary( "ctbllib", "data" )[1],
                       "ctbldiff.json" );
      str:= StringFile( file );
      if str = fail then
        Error( "the data file '", file, "' is not available" );
      fi;
      CTblLib.DiffInfo:= EvalString( str )[2];
    fi;

    # Set column widths,
    # make sure that the "Description" column is wide enough.
    namewidth:= Maximum( List( CTblLib.DiffInfo, l -> Length( l[1] ) ) );
    whatwidth:= Maximum( List( CTblLib.DiffInfo, l -> Length( l[3] ) ) );
    descrwidth:= SizeScreen()[1] - namewidth - whatwidth - 20;
    if descrwidth < 20 then
      descrwidth:= 20;
    fi;

    matrix:= List( CTblLib.DiffInfo, entry ->
      [ rec( align:= "tl", rows:= [ entry[1] ] ),
        rec( align:= "tl", rows:= [ entry[2] ] ),
        rec( align:= "tl", rows:= [ entry[3] ] ),
        rec( align:= "tl", rows:= SplitString(
                             BrowseData.ReallyFormatParagraph( entry[4],
                               descrwidth, "left" ), "\n" ) ),
        rec( align:= "tl", rows:= [ entry[5] ] ),
        rec( align:= "tl", rows:= [ entry[6] ] ) ] );

    # Construct the browse table.
    t:= rec(
      work:= rec(
        align:= "tl",
        header:= t -> BrowseData.HeaderWithRowCounter( t,
                   "Changes of CTblLib Data since version 1.1.3",
                   Length( matrix ) ),
        main:= matrix,
        labelsCol:= [ [ rec( rows:= [ "Identifier" ], align:= "l" ),
                        rec( rows:= [ "Type" ], align:= "l" ),
                        rec( rows:= [ "What" ], align:= "l" ),
                        rec( rows:= [ "Description" ], align:= "l" ),
                        rec( rows:= [ "Flag" ], align:= "l" ),
                        rec( rows:= [ "Vers." ], align:= "l" ) ] ],
        sepLabelsCol:= "=",
        sepRow:= "-",
        sepCol:= [ "|" ],
        widthCol:= [ , namewidth,, 4,, whatwidth,, descrwidth,, 4,, 5 ],
        SpecialGrid:= BrowseData.SpecialGridLineDraw,
      ),
      dynamic:= rec(
        sortFunctionsForColumns:= [ ,,
          function( val1, val2 )
            if val1[1] <> val1[2] then
              return val1 < val2;
            else
              return BrowseData.CompareLenLex( val1, val2 );
            fi;
          end ],
      ),
    );

    # Customize the sort parameters.
    for i in [ 1, 2, 3, 5, 6 ] do
      BrowseData.SetSortParameters( t, "column", i,
          [ "add counter on categorizing", "yes" ] );
    od;

    # Show the browse table.
    NCurses.BrowseGeneric( t );
end );


#############################################################################
##
#E

