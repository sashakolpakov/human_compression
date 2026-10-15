#
# curlInterface: Simple Web Access
#
# This file contains package meta data. For additional information on
# the meaning and correct usage of these fields, please consult the
# manual of the "Example" package as well as the comments in its
# PackageInfo.g file.
#
SetPackageInfo( rec(

PackageName := "curlInterface",
Subtitle := "Simple Web Access",
Version := "2.4.2",
Date := "20/06/2025", # dd/mm/yyyy format
License := "GPL-2.0-or-later",

Persons := [
  rec(
    IsAuthor := true,
    IsMaintainer := true,
    FirstNames := "Christopher",
    LastName := "Jefferson",
    WWWHome := "http://caj.host.cs.st-andrews.ac.uk/",
    Email := "caj21@st-andrews.ac.uk",
    PostalAddress := Concatenation(
               "School of Computer Science\n",
               "University of St Andrews\n",
               "Jack Cole Building, North Haugh\n",
               "St Andrews, Fife, KY16 9SX\n",
               "United Kingdom" ),
    Place := "St Andrews",
    Institution := "University of St Andrews",
  ),

  rec(
    IsAuthor := false,
    IsMaintainer := true,
    FirstNames := "Max",
    LastName := "Horn",
    WWWHome := "https://www.quendi.de/math",
    Email := "mhorn@rptu.de",
    PostalAddress := Concatenation(
               "Fachbereich Mathematik\n",
               "RPTU Kaiserslautern-Landau\n",
               "Gottlieb-Daimler-Straße 48\n",
               "67663 Kaiserslautern\n",
               "Germany" ),
    Place := "Kaiserslautern, Germany",
    Institution := "RPTU Kaiserslautern-Landau"
  ),

  rec(
    IsAuthor := true,
    IsMaintainer := true,
    FirstNames := "Michael",
    LastName := "Young",
    WWWHome := "http://mct25.host.cs.st-andrews.ac.uk/",
    Email := "mct25@st-andrews.ac.uk",
    PostalAddress := Concatenation(
               "School of Computer Science\n",
               "University of St Andrews\n",
               "Jack Cole Building, North Haugh\n",
               "St Andrews, Fife, KY16 9SX\n",
               "United Kingdom" ),
    Place := "St Andrews",
    Institution := "University of St Andrews",
  ),
],

SourceRepository := rec(
    Type := "git",
    URL := Concatenation( "https://github.com/gap-packages/", ~.PackageName ),
),
IssueTrackerURL := Concatenation( ~.SourceRepository.URL, "/issues" ),
#SupportEmail   := "TODO",
PackageWWWHome  := "https://gap-packages.github.io/curlInterface/",
PackageInfoURL  := Concatenation( ~.PackageWWWHome, "PackageInfo.g" ),
README_URL      := Concatenation( ~.PackageWWWHome, "README.md" ),
ArchiveURL      := Concatenation( ~.SourceRepository.URL,
                                 "/releases/download/v", ~.Version,
                                 "/", ~.PackageName, "-", ~.Version ),

ArchiveFormats := ".tar.gz",

##  Status information. Currently the following cases are recognized:
##    "accepted"      for successfully refereed packages
##    "submitted"     for packages submitted for the refereeing
##    "deposited"     for packages for which the GAP developers agreed
##                    to distribute them with the core GAP system
##    "dev"           for development versions of packages
##    "other"         for all other packages
##
Status := "deposited",

AbstractHTML   :=  "",

PackageDoc := rec(
  BookName  := "curl",
  ArchiveURLSubset := ["doc"],
  HTMLStart := "doc/chap0_mj.html",
  PDFFile   := "doc/manual.pdf",
  SixFile   := "doc/manual.six",
  LongTitle := "Simple Web Access",
),

Dependencies := rec(
  GAP := ">= 4.12",
  NeededOtherPackages := [ [ "GAPDoc", ">= 1.5" ] ],
  SuggestedOtherPackages := [ ],
  ExternalConditions := [ ],
),

AvailabilityTest := function()
  if not IsKernelExtensionAvailable("curlinterface", "curl") then
    LogPackageLoadingMessage(PACKAGE_WARNING,
                             ["the kernel module is not compiled, ",
                              "the package cannot be loaded."]);
    return false;
  fi;
  return true;
end,

# Show the libcurl version number in the banner string.
# (We assume that this function gets called *after* the package has been
# loaded, in particular after libcurl has been loaded.)
BannerFunction := function( info )
  local str, version;

  str := DefaultPackageBannerString( info );
  if not IsBoundGlobal( "CURL_VERSION" ) then
    return str;
  fi;
  version := ValueGlobal( "CURL_VERSION" )();

  return ReplacedString( str, "by Christopher",
             Concatenation( "Using ", version, "\n", "by Christopher" ) );
end,


TestFile := "tst/testall.g",

#Keywords := [ "TODO" ],

));
