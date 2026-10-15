# PackageInfo for matgrp

SetPackageInfo( rec(

##  This is case sensitive, use your preferred spelling.
PackageName := "classicpres",
Subtitle := "Classical Group Presentations",

##  See '?Extending: Version Numbers' in GAP help for an explanation
##  of valid version numbers.
Version := "1.22",

License := "GPL-2.0 OR GPL-3.0", # SPDX ID, see https://spdx.org

##  Release date of the current version in dd/mm/yyyy format.
Date := "06/05/2022",

##  URL of the archive(s) of the current package release, but *without*
##  the format extension(s), like '.zoo', which are given next.
##  The archive file name *must be changed* with each version of the archive
##  (and probably somehow contain the package name and version).
ArchiveURL := Concatenation(
  # avoid duplication of version number
  "http://www.math.colostate.edu/~hulpke/classicpres/classicpres",~.Version),

##  All provided formats as list of file extensions, separated by white
##  space or commas.
##      .tar.gz    the UNIX standard
##  
ArchiveFormats := ".tar.gz", # the others are generated automatically


##  Information about authors and maintainers. Specify for each person a 
##  record with the following information:
##  
##  
Persons := [
  rec(
    LastName := "Hulpke",
    FirstNames := "Alexander",
    IsAuthor := true,
    IsMaintainer := true,
    Email := "hulpke@math.colostate.edu",
    WWWHome := "http://www.math.colostate.edu/~hulpke",
    Place := "Fort Collins, CO",
    Institution := Concatenation( [
      "Department of Mathematics, ",
      "Colorado State University",
      ] )
    ),
    rec(
    LastName      := "O'Brien",
    FirstNames    := "Eamonn",
    IsAuthor      := true,
    IsMaintainer  := false,
    Email         := "obrien@math.auckland.ac.nz",
    WWWHome       := "http://www.math.auckland.ac.nz/~obrien",
    PostalAddress := Concatenation(
                       "Department of Mathematics\n",
                       "University of Auckland\n",
                       "Private Bag 92019\n",
                       "Auckland\n",
                       "New Zealand\n" ),
    Place         := "Auckland",
    Institution   := "University of Auckland"
  ),

    rec(
    LastName      := "Leedham-Green",
    FirstNames    := "Charles",
    IsAuthor      := true,
    IsMaintainer  := false,
  ),

    rec(
    LastName      := "Whybrow",
    FirstNames    := "Madeleine",
    IsAuthor      := true,
    IsMaintainer  := false,
  ),

    rec(
    LastName      := "de Franceschi",
    FirstNames    := "Giovanni",
    IsAuthor      := true,
    IsMaintainer  := false,
  ),
  
],
  

##  Status information. Currently the following cases are recognized:
##    "accepted"      for successfully refereed packages
##    "deposited"     for packages for which the GAP developers agreed 
##                    to distribute them with the core GAP system
##    "other"         for all other packages
##
Status := "deposited",

##  For a central overview of all packages and a collection of all package
##  archives it is necessary to have two files accessible which should be
##  contained in each package:
##     - A README file, containing a short abstract about the package
##       content and installation instructions.
##     - The file you are currently reading or editing!
##  You must specify URLs for these two files, these allow to automate 
##  the updating of package information on the GAP Website, and inclusion
##  and updating of the package in the GAP distribution.
##  
README_URL := "http://www.math.colostate.edu/~hulpke/classicpres/README.md",
PackageInfoURL := "http://www.math.colostate.edu/~hulpke/classicpres/PackageInfo.g",

SourceRepository := rec( 
  Type := "git", 
  URL := "https://github.com/hulpke/magmapresentations/"
),
IssueTrackerURL := Concatenation( ~.SourceRepository.URL, "/issues" ),

##  Here you  must provide a short abstract explaining the package content 
##  in HTML format (used on the package overview Web page) and an URL 
##  for a Webpage with more detailed information about the package
##  (not more than a few lines, less is ok):
##  Please, use '<span class="pkgname">GAP</span>' and
##  '<span class="pkgname">MyPKG</span>' for specifing package names.
##  
AbstractHTML := "The <span class=\"pkgname\">classicpres</span> package \
provides presentations for classical groups, translated from the \
corresponding Magma code.",

PackageWWWHome := "http://www.math.colostate.edu/~hulpke/classicpres",
                  
##  On the GAP Website there is an online version of all manuals in the
##  GAP distribution. To handle the documentation of a package it is
##  necessary to have:
##     - an archive containing the package documentation (in at least one 
##       of HTML or PDF-format, preferably both formats)
##     - the start file of the HTML documentation (if provided), *relative to
##       package root*
##     - the PDF-file (if provided) *relative to the package root*
##  For links to other package manuals or the GAP manuals one can assume 
##  relative paths as in a standard GAP installation. 
##  Also, provide the information which is currently given in your packages 
##  init.g file in the command DeclarePackage(Auto)Documentation
##  (for future simplification of the package loading mechanism).
##  
##  Please, don't include unnecessary files (.log, .aux, .dvi, .ps, ...) in
##  the provided documentation archive.
##  
# in case of several help books give a list of such records here:
PackageDoc := rec(
  # use same as in GAP            
  BookName := "classicpres",
  ArchiveURLSubset := [ "doc", "htm" ],
  PDFFile := "doc/manual.pdf",
  HTMLStart:="htm/chapters.htm",
  # the path to the .six file used by GAP's help system
  SixFile := "doc/manual.six",
  # a longer title of the book, this together with the book name should
  # fit on a single text line (appears with the '?books' command in GAP)
  LongTitle := "Classical Group Presentations",
  # Should this help book be autoloaded when GAP starts up? This should
  # usually be 'true', otherwise say 'false'. 
  Autoload := true
),


##  Are there restrictions on the operating system for this package? Or does
##  the package need other packages to be available?
Dependencies := rec(
  # GAP version, use version strings for specifying exact versions,
  # prepend a '>=' for specifying a least version.
  GAP := ">=4.11", # seems to work with recent 4.7
  # list of pairs [package name, (least) version],  package name is case
  # insensitive, least version denoted with '>=' prepended to version string.
  # without these, the package will not load
  NeededOtherPackages := [
    ["AtlasRep", ">= 1.4.0"],
  ],
  SuggestedOtherPackages := [],
  ExternalConditions := []
),

## Provide a test function for the availability of this package, see
## documentation of 'Declare(Auto)Package', this is the <tester> function.
## For packages which will not fully work, use 'Info(InfoWarning, 1,
## ".....")' statements. For packages containing nothing but GAP code,
## just say 'ReturnTrue' here.
## (When this is used for package loading in the future the availability
## tests of other packages, as given above, will be done automatically and
## need not be included here.)
AvailabilityTest := ReturnTrue,

TestFile := "tst/testall.g",

##  Suggest here if the package should be *automatically loaded* when GAP is 
##  started.  This should usually be 'false'. Say 'true' only if your package 
##  provides some improvements of the GAP library which are likely to enhance 
##  the overall system performance for many users.
Autoload := true,

##  If the default banner does not suffice then provide a string that is
##  printed when the package is loaded (not when it is autoloaded or if
##  command line options `-b' or `-q' are given).
BannerString := Concatenation("Classical Group Presentations, v.",
  ~.Version,"\n"),

TestFile := "tst/testall.g",

##  *Optional*: Here you can list some keyword related to the topic 
##  of the package.
# Keywords := ["Smith normal form", "p-adic", "rational matrix inversion"]
Keywords := ["classical group","presentation"]

));


