#############################################################################
##
#W PackageInfo.g           The Congruence package                   Ann Dooms
#W                                                               Eric Jespers
#W                                                         Olexandr Konovalov
#W                                                             Helena Verrill
##
##
#############################################################################

SetPackageInfo( rec(

PackageName    := "Congruence",
Subtitle       := "Congruence subgroups of SL(2,Integers)",
Version        := "1.2.7",
Date           := "28/08/2024", # dd/mm/yyyy format
License        := "GPL-2.0-or-later",

SourceRepository := rec(
    Type := "git",
    URL := Concatenation( "https://github.com/gap-packages/", LowercaseString(~.PackageName) ),
),
IssueTrackerURL := Concatenation( ~.SourceRepository.URL, "/issues" ),
PackageWWWHome  := Concatenation( "https://gap-packages.github.io/", LowercaseString(~.PackageName) ),
README_URL      := Concatenation( ~.PackageWWWHome, "/README.md" ),
PackageInfoURL  := Concatenation( ~.PackageWWWHome, "/PackageInfo.g" ),
ArchiveURL      := Concatenation( ~.SourceRepository.URL,
                                 "/releases/download/v", ~.Version,
                                 "/", LowercaseString(~.PackageName), "-", ~.Version ),

ArchiveFormats := ".tar.gz",

Persons := [
  rec(
    LastName      := "Dooms",
    FirstNames    := "Ann",
    IsAuthor      := true,
    IsMaintainer  := true,
    Email         := "andooms@vub.ac.be",
    WWWHome       := "http://homepages.vub.ac.be/~andooms",
    PostalAddress := Concatenation( [
                     "Department of Mathematics\n",
                     "Vrije Universiteit Brussel\n", 
                     "Pleinlaan 2, Brussels, B-1050 Belgium" ] ),
    Place         := "Brussels",
    Institution   := "Vrije Universiteit Brussel"
     ),     
  rec(
    LastName      := "Jespers",
    FirstNames    := "Eric",
    IsAuthor      := true,
    IsMaintainer  := false,
    Email         := "efjesper@vub.ac.be",
    WWWHome       := "http://homepages.vub.ac.be/~efjesper",
    PostalAddress := Concatenation( [
                     "Department of Mathematics\n",
                     "Vrije Universiteit Brussel\n", 
                     "Pleinlaan 2, Brussels, B-1050 Belgium" ] ),
    Place         := "Brussels",
    Institution   := "Vrije Universiteit Brussel"
     ),
  rec(
    LastName      := "Konovalov",
    FirstNames    := "Olexandr",
    IsAuthor      := true,
    IsMaintainer  := true,
    Email         := "obk1@st-andrews.ac.uk",
    WWWHome       := "https://olexandr-konovalov.github.io/",
    PostalAddress := Concatenation( [
                     "School of Computer Science\n",
                     "University of St Andrews\n",
                     "Jack Cole Building, North Haugh,\n",
                     "St Andrews, Fife, KY16 9SX, Scotland" ] ),
    Place         := "St Andrews",
    Institution   := "University of St Andrews"
     ),
  rec(    
    LastName      := "Verrill",
    FirstNames    := "Helena",
    IsAuthor      := true,
    IsMaintainer  := true,
    Email         := "verrill@math.lsu.edu",
    WWWHome       := "http://www.math.lsu.edu/~verrill",
    PostalAddress := Concatenation( [
                     "Department of Mathematics\n",
                     "Louisiana State University\n",
                     "Baton Rouge, Louisiana, 70803-4918\n",
                     "USA" ] ),
    Place         := "Baton Rouge",
    Institution   := "Louisiana State University"
     )      
],

Status := "accepted",
CommunicatedBy := "Graham Ellis (Galway)",
AcceptDate := "09/2014",

AbstractHTML := "The <span class=\"pkgname\">Congruence </span> package provides functions to construct several types of canonical congruence subgroups in SL_2(Z), and also intersections of a finite number of such subgroups. Furthermore, it implements the algorithm for generating Farey symbols for congruence subgroups and using them to produce a system of independent generators for these subgroups",
                  
PackageDoc := rec(
  BookName := "Congruence",
  ArchiveURLSubset := ["doc"],
  HTMLStart := "doc/chap0_mj.html",
  PDFFile := "doc/manual.pdf",
  SixFile := "doc/manual.six",
  LongTitle := "Congruence subgroups of SL(2,Integers)",
  Autoload := true
),

Dependencies := rec(
  GAP := ">=4.8",
  NeededOtherPackages := [ ["GAPDoc", ">= 1.5.1"] ],
  SuggestedOtherPackages := [],
  ExternalConditions := []
),

AvailabilityTest := ReturnTrue,
TestFile := "tst/testall.g",

Keywords := ["congruence subgroup", "Farey symbol"],

AutoDoc := rec(
    entities := rec(
        VERSION := ~.Version,
        RELEASEDATE := function(date)
          local day, month, year, allMonths;
          day := Int(date{[1,2]});
          month := Int(date{[4,5]});
          year := Int(date{[7..10]});
          allMonths := [ "January", "February", "March", "April", "May", "June", "July",
                         "August", "September", "October", "November", "December"];
          return Concatenation(String(day)," ", allMonths[month], " ", String(year));
        end(~.Date),
        RELEASEYEAR := ~.Date{[7..10]},
    ),
),

));
