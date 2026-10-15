#############################################################################
##  
##  PackageInfo.g for the package `Nilmat'                       Bettina Eick 
##  
##  This is a GAP readable file. Of course you can change and remove all
##  comments as you like.
##  
##  This file contains meta-information on the package. It is used by
##  the package loading mechanism and the upgrade mechanism for the
##  redistribution of the package via the GAP website.
##  
##  For the LoadPackage mechanism in GAP >= 4.4 only the entries
##  .PackageName, .Version, .PackageDoc, .Dependencies, .AvailabilityTest
##  .Autoload   are needed. The other entries are relevant if the
##  package shall be distributed for other GAP users, in particular if it
##  shall be redistributed via the GAP Website.
##
##  With a new release of the package at least the entries .Version, .Date and
##  .ArchiveURL must be updated.

SetPackageInfo( rec(

PackageName := "Nilmat",
Subtitle := "Computing with nilpotent matrix groups",
Version := "1.4.2",
Date := "05/08/2022", # dd/mm/yyyy format
License := "GPL-2.0-or-later",

Persons := [
  rec( 
    LastName      := "Detinko",
    FirstNames    := "Alla",
    IsAuthor      := true,
    IsMaintainer  := true,
    Email         := "ad271@st-andrews.ac.uk",
    WWWHome       := "https://ad271.host.cs.st-andrews.ac.uk/",
    PostalAddress := Concatenation( [
                       "School of Computer Science\n",
                       "University of St Andrews\n",
                       #"University Road, Galway\n",
                       "UK" ] ),
    Place         := "St Andrews",
    Institution   := "University of St Andrews"),
  rec( 
    LastName      := "Eick",
    FirstNames    := "Bettina",
    IsAuthor      := true,
    IsMaintainer  := true,
    Email         := "beick@tu-bs.de",
    WWWHome       := "http://www.iaa.tu-bs.de/beick/",
    PostalAddress := Concatenation( [
               "Institut Analysis und Algebra\n",
               "TU Braunschweig\n",
               "Universitätsplatz 2\n",
               "D-38106 Braunschweig\n",
               "Germany" ] ),
    Place         := "Braunschweig",
    Institution   := "TU Braunschweig"),
  rec( 
    LastName      := "Flannery",
    FirstNames    := "Dane",
    IsAuthor      := true,
    IsMaintainer  := true,
    Email         := "dane.flannery@nuigalway.ie",
    WWWHome       := "http://www.maths.nuigalway.ie/~dane",
    PostalAddress := Concatenation( [
                       "Department of Mathematics\n",
                       "National University of Ireland, Galway\n",
                       "University Road, Galway\n",
                       "Ireland" ] ),
    Place         := "Galway",
    Institution   := "NUI Galway")
],

Status := "accepted",
CommunicatedBy := "Derek Holt (Warwick)",
AcceptDate := "08/2007",

SourceRepository := rec(
    Type := "git",
    URL := "https://github.com/gap-packages/nilmat",
),
IssueTrackerURL := Concatenation( ~.SourceRepository.URL, "/issues" ),
PackageWWWHome  := "https://gap-packages.github.io/nilmat",
README_URL      := Concatenation( ~.PackageWWWHome, "/README.md" ),
PackageInfoURL  := Concatenation( ~.PackageWWWHome, "/PackageInfo.g" ),
ArchiveURL      := Concatenation( ~.SourceRepository.URL,
                                 "/releases/download/v", ~.Version,
                                 "/nilmat-", ~.Version ),
ArchiveFormats := ".tar.gz .tar.bz2",

AbstractHTML := 
  "The <span class=\"pkgname\">Nilmat</span> package contains methods for checking whether a finitely generated matrix group over a finite field or the field of rational numbers is nilpotent, methods for computing with such nilpotent matrix groups and methods for constructing important classes of such nilpotent matrix groups.",
               
PackageDoc := rec(
  BookName  := "Nilmat",
  ArchiveURLSubset := ["doc", "htm"],
  HTMLStart := "htm/chapters.htm",
  PDFFile   := "doc/manual.pdf",
  SixFile   := "doc/manual.six",
  LongTitle := "Computation with nilpotent matrix groups",
  Autoload  := true
),

Dependencies := rec(
  GAP := ">=4.8",
  NeededOtherPackages := [["Polenta", ">=1.0"]],
  SuggestedOtherPackages := [],
  ExternalConditions := []
),

AvailabilityTest := ReturnTrue,
BannerString := Concatenation("Loading Nilmat ", String( ~.Version ), "...\n"),
Autoload := false,
TestFile := "tst/testall.g",
Keywords := ["nilpotent groups", "matrix groups"],

));
