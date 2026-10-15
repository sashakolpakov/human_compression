#############################################################################
##  
##  PackageInfo.g for the package `NoCK'                     
##   
##  (created from Frank Lübeck's PackageInfo.g template file)
##  
##  This is a GAP readable file.
##

SetPackageInfo( rec(


PackageName := "NoCK",
Subtitle := "Computing obstruction for the existence of compact Clifford-Klein form",
Version := "1.5",
Date := "30/03/2022",
License := "GPL-2.0-or-later",

PackageWWWHome :=
   "https://gap-packages.github.io/NoCK",


SourceRepository := rec(
    Type := "git",
    URL :=  "https://github.com/gap-packages/NoCK",
),
IssueTrackerURL := Concatenation( ~.SourceRepository.URL, "/issues" ),
SupportEmail := "piojas@matman.uwm.edu.pl",

ArchiveURL      := Concatenation( ~.SourceRepository.URL,
                                 "/releases/download/v", ~.Version,
                                 "/", ~.PackageName, "-", ~.Version ),

ArchiveFormats := ".tar.gz",

Persons := [
  rec( 
    LastName      := "Bocheński",
    FirstNames    := "Maciej",
    IsAuthor      := true,
    IsMaintainer  := true,
    Email         := "mabo@matman.uwm.edu.pl",
    Place         := "Olsztyn, Poland",
    Institution   := "Faculty of Mathematics and Computer Science, University of Warmia and Mazury in Olsztyn"
  ),
  rec( 
    LastName      := "Jastrzębski",
    FirstNames    := "Piotr",
    IsAuthor      := true,
    IsMaintainer  := true,
    Email         := "piojas@matman.uwm.edu.pl",
    WWWHome       := "http://wmii.uwm.edu.pl/~piojas/",
    Place         := "Olsztyn, Poland",
    Institution   := "Faculty of Mathematics and Computer Science, University of Warmia and Mazury in Olsztyn"
  ),
    rec( 
    LastName      := "Szczepkowska",
    FirstNames    := "Anna",
    IsAuthor      := true,
    IsMaintainer  := true,
    Email         := "anna.szczepkowska@matman.uwm.edu.pl",
    Place         := "Olsztyn, Poland",
    Institution   := "Faculty of Mathematics and Computer Science, University of Warmia and Mazury in Olsztyn"
  ),
    rec( 
    LastName      := "Tralle",
    FirstNames    := "Aleksy",
    IsAuthor      := true,
    IsMaintainer  := true,
    Email         := "tralle@matman.uwm.edu.pl",
    WWWHome       := "http://wmii.uwm.edu.pl/~tralle/",
    Place         := "Olsztyn, Poland",
    Institution   := "Faculty of Mathematics and Computer Science, University of Warmia and Mazury in Olsztyn"
  ),
    rec( 
    LastName      := "Woike",
    FirstNames    := "Artur",
    IsAuthor      := true,
    IsMaintainer  := true,
    Email         := "awoike@matman.uwm.edu.pl",
    WWWHome       := "http://wmii.uwm.edu.pl/~awoike",
    Place         := "Olsztyn, Poland",
    Institution   := "Faculty of Mathematics and Computer Science, University of Warmia and Mazury in Olsztyn"
  ),

  rec(
    LastName      := "GAP Team",
    FirstNames    := "The",
    IsAuthor      := false,
    IsMaintainer  := true,
    Email         := "support@gap-system.org",
  ),

],

##  Status information. Currently the following cases are recognized:
##    "accepted"      for successfully refereed packages
##    "submitted"     for packages submitted for the refereeing
##    "deposited"     for packages for which the GAP developers agreed 
##                    to distribute them with the core GAP system
##    "dev"           for development versions of packages 
##    "other"         for all other packages
##
Status := "accepted",
##  You must provide the next two entries if and only if the status is
##  "accepted":
# format: 'name (place)'
CommunicatedBy := "Leonard Soicher (QMUL)",
# format: mm/yyyy
AcceptDate := "07/2019", # or whenever the accepted version is complete


README_URL := 
  Concatenation( ~.PackageWWWHome, "/README.md" ),
PackageInfoURL := 
  Concatenation( ~.PackageWWWHome, "/PackageInfo.g" ),


AbstractHTML := 
  "The <span class=\"pkgname\">NoCK</span> package \
   is used for computing Tolzanos's obstruction \
   for compact Clifford-Klein forms",

##  Here is the information on the help books of the package, used for
##  loading into GAP's online help and maybe for an online copy of the 
##  documentation on the GAP website.
##  
##  For the online help the following is needed:
##       - the name of the book (.BookName)
##       - a long title, shown by ?books (.LongTitle, optional)
##       - the path to the manual.six file for this book (.SixFile)
##  
##  For an online version on a Web page further entries are needed, 
##  if possible, provide an HTML- and a PDF-version:
##      - if there is an HTML-version the path to the start file,
##        relative to the package home directory (.HTMLStart)
##      - if there is a PDF-version the path to the .pdf-file,
##        relative to the package home directory (.PDFFile)
##      - give the paths to the files inside your package directory
##        which are needed for the online manual (as a list 
##        .ArchiveURLSubset of names of directories and/or files which 
##        should be copied from your package archive, given in .ArchiveURL 
##        above (in most cases, ["doc"] or ["doc","htm"] suffices).
##  
##  For links to other GAP or package manuals you can assume a relative 
##  position of the files as in a standard GAP installation.
##  
# in case of several help books give a list of such records here:
PackageDoc := rec(
  BookName  := "NoCK",
  ArchiveURLSubset := ["doc"],
  HTMLStart := "doc/chap0.html",
  PDFFile   := "doc/manual.pdf",
  # the path to the .six file used by GAP's help system
  SixFile   := "doc/manual.six",
  # a longer title of the book, this together with the book name should
  # fit on a single text line (appears with the '?books' command in GAP)
  LongTitle := "Computing obstruction for the existence of compact Clifford-Klein form",
),


##  Are there restrictions on the operating system for this package? Or does
##  the package need other packages to be available?
Dependencies := rec(
  GAP := ">=4.8",
  NeededOtherPackages := [["sla", ">=1.2"], ["CoReLG", ">=1.20"]],

  # list of pairs [package name, version] as above,
  # these package are will be loaded if they are available,
  # but the current package will be loaded if they are not available
  # SuggestedOtherPackages := [],
  SuggestedOtherPackages := [["GAPDoc", "1.5"]],

  # *Optional*: a list of pairs as above, denoting those needed packages
  # that must be completely loaded before loading of the current package
  # is started (if this is not possible due to a cyclic dependency
  # then the current package is regarded as not loadable);
  # this component should be used only if functions from the needed packages
  # in question are called (or global lists or records are accessed)
  # while the current package gets loaded
  # OtherPackagesLoadedInAdvance := [],

  # needed external conditions (programs, operating system, ...)  provide 
  # just strings as text or
  # pairs [text, URL] where URL  provides further information
  # about that point.
  # (no automatic test will be done for this, do this in your 
  # 'AvailabilityTest' function below)
  # ExternalConditions := []
  ExternalConditions := []
                      
),

AvailabilityTest := ReturnTrue,

BannerString := Concatenation( 
    "----------------------------------------------------------------\n",
    "NoCK Package ", ~.Version, "\n",
    "by ",
    JoinStringsWithSeparator( List( Filtered( ~.Persons, r -> r.IsAuthor ),
                                    r -> Concatenation(
        r.FirstNames, " ", r.LastName  ) ), ", " ),".\n",
    
    "----------------------------------------------------------------\n" ),

TestFile := "tst/testall.g",

Keywords := ["real lie algebras", "clifford-klein forms"],

AutoDoc := rec(
    TitlePage := rec(
        Abstract := """
        In this package we develop functions for an algorithm designed
        to find homogeneous spaces of semisimple non-compact Lie groups
        which do not admit compact Clifford-Klein forms.
        """,

        Acknowledgements := """
        We thank Willem de Graaf for his help in getting some literature sources.
        """,

        Copyright := """
        NoCK Package is free software;  you can redistribute it and/or modify it under the terms of the
        <URL Text="GNU General Public License">https://www.fsf.org/licenses/gpl.html</URL>
        as published by the Free Software Foundation; either version 2 of the License,
        or (at your option) any later version.
        """,
    ),
),

));

