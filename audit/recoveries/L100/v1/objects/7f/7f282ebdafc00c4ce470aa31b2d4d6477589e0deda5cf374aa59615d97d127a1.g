#############################################################################
##  
#W PackageInfo.g               FGA package                  Christian Sievers
##
## The package info file for the FGA package
##
#Y 2003 - 2018
##

SetPackageInfo( rec(

PackageName := "FGA",
Subtitle := "Free Group Algorithms",
Version := "1.5.0",
Date := "04/04/2023", # dd/mm/yyyy format
License := "GPL-2.0-or-later",

Persons := [
  rec( 
    LastName      := "Sievers",
    FirstNames    := "Christian",
    IsAuthor      := true,
    IsMaintainer  := false,
    Email         := "c.sievers@tu-bs.de",
  ),
  rec(
    LastName      := "GAP Team",
    FirstNames    := "The",
    IsAuthor      := false,
    IsMaintainer  := true,
    Email         := "support@gap-system.org",
  ),
],

Status := "accepted",

CommunicatedBy := "Edmund Robertson (St. Andrews)",
AcceptDate := "05/2005",

##  For a central overview of all packages and a collection of all package
##  archives it is necessary to have two files accessible which should be
##  contained in each package:
##     - A README file, containing a short abstract about the package
##       content and installation instructions.
##     - The file you are currently reading or editing!
##  You must specify URLs for these two files, these allow to automate 
##  the updating of package information on the GAP Website, and inclusion
##  and updating of the package in the GAP distribution.
#

PackageWWWHome := "https://gap-packages.github.io/fga/",

README_URL     := Concatenation( ~.PackageWWWHome, "README.md" ),
PackageInfoURL := Concatenation( ~.PackageWWWHome, "PackageInfo.g" ),
SourceRepository := rec( 
  Type := "git", 
  URL := "https://github.com/gap-packages/fga"
),
IssueTrackerURL := Concatenation( ~.SourceRepository.URL, "/issues" ),

ArchiveFormats := ".tar.gz",
ArchiveURL     := Concatenation( ~.SourceRepository.URL,
                                 "/releases/download/v", ~.Version,
                                 "/fga-", ~.Version ),

##  Here you  must provide a short abstract explaining the package content 
##  in HTML format (used on the package overview Web page) and an URL 
##  for a Webpage with more detailed information about the package
##  (not more than a few lines, less is ok):
##  Please, use '<span class="pkgname">GAP</span>' and
##  '<span class="pkgname">MyPKG</span>' for specifying package names.
##  
AbstractHTML := 
  "The <span class=\"pkgname\">FGA</span> package installs methods for \
   computations with finitely generated subgroups of free groups and \
   provides a presentation for their automorphism groups.",

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
##  Also, provide the information about autoloadability of the documentation.
##  
##  Please, don't include unnecessary files (.log, .aux, .dvi, .ps, ...) in
##  the provided documentation archive.
##  
# in case of several help books give a list of such records here:
PackageDoc := rec(
  # use same as in GAP            
  BookName  := "FGA",
  ArchiveURLSubset := ["doc"],
  HTMLStart := "doc/chap0_mj.html",
  PDFFile   := "doc/manual.pdf",
  SixFile   := "doc/manual.six",
  LongTitle := "Free Group Algorithms",
),


##  Are there restrictions on the operating system for this package? Or does
##  the package need other packages to be available?
Dependencies := rec(
  GAP := ">=4.8",
  NeededOtherPackages := [],
  SuggestedOtherPackages := [],
  ExternalConditions := []
),

AvailabilityTest := ReturnTrue,
#BannerString := ""

##  *Optional*, but recommended: path relative to package root to a file which 
##  contains as many tests of the package functionality as sensible.
TestFile := "tst/testall.g",

Keywords := ["free groups", "inverse finite automata",
             "basic coset enumeration",
             "finite presentation of the automorphism group of a free group"],

AutoDoc := rec(
    TitlePage := rec(
        TitleComment := "<E>Note:</E> This version of FGA is a fork of the original FGA, maintained by the GAP Team.",
    ),
),

));
