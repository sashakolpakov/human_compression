#############################################################################
##  
##  PackageInfo.g for the package `InduceReduce'              Jonathan Gruber
##                                                            
##  This file contains meta-information on the package. It is used by
##  the package loading mechanism and the upgrade mechanism for the
##  redistribution of the package via the GAP website.
##

SetPackageInfo( rec(

PackageName := "InduceReduce",
Subtitle := "Unger's algorithm to compute character tables of finite groups",
Version := "1.3",
Date := "16/10/2025", # dd/mm/yyyy format
License := "GPL-3.0-or-later",

Persons := [
  rec(
    IsAuthor := true,
    IsMaintainer := true,
    FirstNames := "Jonathan",
    LastName := "Gruber",
    Email := "jonathan.gruber@fau.de",
    Place := "Erlangen",
    Institution := "University Erlangen-Nuremberg",
    #PostalAddress := Concatenation(
    #  ),
  ),
  rec(
    IsAuthor := false,
    IsMaintainer := true,
    LastName := "Breuer",
    FirstNames := "Thomas",
    Email := "sam@math.rwth-aachen.de",
    WWWHome := "https://www.math.rwth-aachen.de/~Thomas.Breuer",
    Place := "Aachen",
    Institution := "Lehrstuhl für Algebra und Zahlentheorie, RWTH Aachen",
    PostalAddress := Concatenation(
      "Thomas Breuer\n",
      "Lehrstuhl für Algebra und Zahlentheorie\n",
      "Pontdriesch 14/16\n",
      "52062 Aachen\n",
      "Germany" ),
  ),
  rec(
    IsAuthor := false,
    IsMaintainer := true,
    FirstNames := "Max",
    LastName := "Horn",
    Email := "mhorn@rptu.de",
    WWWHome := "https://www.quendi.de/math",
    GitHubUsername := "fingolfin",
    Place := "Kaiserslautern, Germany",
    Institution := "RPTU Kaiserslautern-Landau",
    PostalAddress := Concatenation(
      "Fachbereich Mathematik\n",
      "RPTU Kaiserslautern-Landau\n",
      "Gottlieb-Daimler-Straße 48\n",
      "67663 Kaiserslautern\n",
      "Germany" ),
  ),
],

SourceRepository := rec(
    Type := "git",
    URL := "https://github.com/gap-packages/InduceReduce",
),
IssueTrackerURL := Concatenation( ~.SourceRepository.URL, "/issues" ),
#SupportEmail := "TODO",

PackageWWWHome :="https://gap-packages.github.io/InduceReduce/",

PackageInfoURL := Concatenation( ~.PackageWWWHome, "PackageInfo.g" ),
README_URL     := Concatenation( ~.PackageWWWHome, "README.md" ),
ArchiveURL     := Concatenation( ~.SourceRepository.URL,
                                 "/releases/download/v", ~.Version,
                                 "/", ~.PackageName, "-", ~.Version ),

ArchiveFormats := ".tar.gz",

Status := "deposited",

AbstractHTML   :=  "This package provides an implementation of Unger's algorithm\
 to compute the character table of a finite group.",

PackageDoc := rec(
  BookName  := "InduceReduce",
  ArchiveURLSubset := ["doc"],
  HTMLStart := "doc/chap0_mj.html",
  PDFFile   := "doc/manual.pdf",
  SixFile   := "doc/manual.six",
  LongTitle := "Computing Character Tables using Unger's algorithm",
),

Dependencies := rec(
  GAP := ">= 4.9",
  NeededOtherPackages := [ [ "GAPDoc", ">= 1.5" ] ],
  SuggestedOtherPackages := [ ],
  ExternalConditions := [ ],
),

AvailabilityTest := ReturnTrue,

TestFile := "tst/testall.g",

Keywords := [ "character table", "elementary subgroups", "induced characters" ],

AutoDoc := rec(
    entities := rec(
        VERSION := ~.Version,
        RELEASEYEAR := ~.Date{[7..10]},
        RELEASEDATE := function(date)
          local day, month, year, allMonths;
          day := Int(date{[1,2]});
          month := Int(date{[4,5]});
          year := Int(date{[7..10]});
          allMonths := [ "January", "February", "March", "April", "May", "June", "July",
                         "August", "September", "October", "November", "December"];
          return Concatenation(String(day)," ", allMonths[month], " ", String(year));
        end(~.Date),
    ),
),

));
