# Notify Browse overviews of tables, irrationalities, and differences of data.
ReadPackage( "ctbllib", "gap4/brirrat.g" );

# Postpone some work until the functions are really needed.
DeclareAutoreadableVariables( "ctbllib", "gap4/ctbltocb.g",
    [ "BrowseCTblLibInfo", "BrowseCTblLibInfo_GroupInfoTable" ] );
DeclareAutoreadableVariables( "ctbllib", "gap4/brctdiff.g",
    [ "BrowseCTblLibDifferences" ] );

# Add the Browse applications to the list shown by `BrowseGapData'.
BrowseGapDataAdd( "Overview of GAP's Library of Character Tables",
    function() BrowseCTblLibInfo(); end, false, "\
an overview of the GAP library of character tables, \
details about individual tables are shown on click. \
Try ?BrowseCTblLibInfo for details" );

BrowseGapDataAdd( "Differences in GAP's Library of Character Tables",
    function() BrowseCTblLibDifferences(); end, false, "\
an overview of the differences between the versions of \
GAP's library of character tables, since version 1.1.3. \
Try ?BrowseCTblLibDifferences for details" );

# Notify ATLAS related stuff.
ReadPackage( "ctbllib", "gap4/atlasimp.g" );
ReadPackage( "ctbllib", "gap4/atlasbro.g" );

