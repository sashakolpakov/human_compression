#############################################################################
##
##  PackageInfo.g for CaratInterface
##

SetPackageInfo( rec(

PackageName := "CaratInterface",

Subtitle := "Interface to CARAT, a crystallographic groups package",

Version := "2.3.7",

Date := "16/10/2024", # dd/mm/yyyy format
License := "GPL-2.0-or-later",

ArchiveURL := Concatenation( 
  "https://www.math.uni-bielefeld.de/~gaehler/gap/CaratInterface/CaratInterface-", ~.Version ),

ArchiveFormats := ".tar.gz",

BinaryFiles := [ "doc/manual.pdf", "doc/manual.dvi", "carat.tgz" ],

Persons := [
  rec(
    LastName := "Gähler",
    FirstNames := "Franz",
    IsAuthor := true,
    IsMaintainer := true,
    Email := "gaehler@math.uni-bielefeld.de",
    WWWHome := "https://www.math.uni-bielefeld.de/~gaehler/",
    #PostalAddress := "",           
    Place := "Bielefeld",
    Institution := "Mathematik, Universität Bielefeld"
  )
],

Status := "accepted",

CommunicatedBy := "Herbert Pahlings (Aachen)",

AcceptDate := "02/2000",

README_URL := 
  "https://www.math.uni-bielefeld.de/~gaehler/gap/CaratInterface/README.CaratInterface",
PackageInfoURL := 
  "https://www.math.uni-bielefeld.de/~gaehler/gap/CaratInterface/PackageInfo.g",

AbstractHTML := 
"This package provides <span class=\"pkgname\">GAP</span> interface \
routines to some of the stand-alone programs of <a \
href=\"https://lbfm-rwth.github.io/carat\">CARAT</a>, a package \
for the computation with crystallographic groups. CARAT is to a large \
extent complementary to the <span class=\"pkgname\">GAP</span> package \
<span class=\"pkgname\">Cryst</span>. In particular, it provides \
routines for the computation of normalizers and conjugators of \
finite unimodular groups in GL(n,Z), and routines for the computation \
of Bravais groups, which are all missing in <span class=\"pkgname\">Cryst\
</span>. A catalog of Bravais groups up to dimension 6 is also provided.",

PackageWWWHome := 
  "https://www.math.uni-bielefeld.de/~gaehler/gap/packages.php",

SourceRepository := rec(
  Type := "git",
  URL := Concatenation( "https://github.com/gap-packages/",
                        LowercaseString( ~.PackageName ) ) ),
IssueTrackerURL := Concatenation( ~.SourceRepository.URL, "/issues" ),
SupportEmail := "gaehler@math.uni-bielefeld.de",

PackageDoc  := rec(
  BookName  := "CaratInterface",
  ArchiveURLSubset := ["doc", "htm"],
  HTMLStart := "htm/chapters.htm",
  PDFFile   := "doc/manual.pdf",
  SixFile   := "doc/manual.six",
  LongTitle := "Interface to CARAT, a crystallographic groups package"
),

Dependencies := rec(
  GAP := ">=4.11.1",
  NeededOtherPackages := [ [ "IO", ">=4.8.0" ] ],
  SuggestedOtherPackages := [ [ "Cryst", ">=4.1.24" ] ],
  ExternalConditions := []
),

AvailabilityTest := function()
  local path;
  # test the existence of a compiled binary; since there are
  # so many, we do not test for all of them, hoping for the best
  path := DirectoriesPackagePrograms( "CaratInterface" );
  if Filename( path, "Z_equiv" ) = fail then
     LogPackageLoadingMessage(PACKAGE_WARNING, "CARAT binaries must be compiled" );
     return false;
  fi;
  return true;
end,

TestFile := "tst/testall.g",

Keywords := [ "crystallographic groups", "finite unimodular groups", "GLnZ" ]

));
