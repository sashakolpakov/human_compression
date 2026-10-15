#############################################################################
##  
##  PackageInfo.g for CrystCat
##  

SetPackageInfo( rec(

PackageName := "CrystCat",

Subtitle := "The crystallographic groups catalog",

Version := "1.1.10",

Date := "29/07/2022", # dd/mm/yyyy format

License := "GPL-2.0-or-later",

ArchiveURL := Concatenation(
  "https://www.math.uni-bielefeld.de/~gaehler/gap/CrystCat/crystcat-", ~.Version ),

ArchiveFormats := ".tar.gz",

BinaryFiles := [ "doc/manual.pdf", "doc/manual.dvi" ],

Persons := [
  rec(
    LastName := "Felsch",
    FirstNames := "Volkmar",
    IsAuthor := true,
    IsMaintainer := true,
    Email := "Volkmar.Felsch@math.rwth-aachen.de",
    WWWHome := "http://www.math.rwth-aachen.de/~Volkmar.Felsch/",
    #PostalAddress := "",           
    Place := "Aachen",
    Institution := "Lehrstuhl D für Mathematik, RWTH Aachen"
  ),
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

README_URL := "https://www.math.uni-bielefeld.de/~gaehler/gap/CrystCat/README.crystcat",
PackageInfoURL := "https://www.math.uni-bielefeld.de/~gaehler/gap/CrystCat/PackageInfo.g",

AbstractHTML := 
"This package provides a catalog of crystallographic groups of \
dimensions 2, 3, and 4 which covers most of the data contained in \
the book <em>Crystallographic groups of four-dimensional space</em> \
by H. Brown, R. B&uuml;low, J. Neub&uuml;ser, H. Wondratschek, and \
H. Zassenhaus (John Wiley, New York, 1978). Methods for the \
computation with these groups are provided by the package \
<span class=\"pkgname\">Cryst</span>, which must be installed as well.",

PackageWWWHome := 
  "https://www.math.uni-bielefeld.de/~gaehler/gap/packages.php",

SourceRepository := rec(
  Type := "git",
  URL := Concatenation( "https://github.com/gap-packages/",
                        LowercaseString( ~.PackageName ) ) ),
IssueTrackerURL := Concatenation( ~.SourceRepository.URL, "/issues" ),
SupportEmail := "gaehler@math.uni-bielefeld.de",

PackageDoc  := rec(
  BookName  := "CrystCat",
  ArchiveURLSubset := ["doc", "htm"],
  HTMLStart := "htm/chapters.htm",
  PDFFile   := "doc/manual.pdf",
  SixFile   := "doc/manual.six",
  LongTitle := "The crystallographic groups catalog",
),

Dependencies := rec(
  GAP := ">=4.11",
  NeededOtherPackages := [ [ "Cryst", ">=4.1.24" ] ],
  SuggestedOtherPackages := [],
  ExternalConditions := []
),

AvailabilityTest := ReturnTrue,

TestFile := "tst/testall.g",

Keywords := [ "crystallographic groups", "space groups" ]

));
