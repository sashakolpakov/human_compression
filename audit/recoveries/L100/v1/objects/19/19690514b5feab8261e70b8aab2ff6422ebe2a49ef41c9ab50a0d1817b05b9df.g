#############################################################################
##
#W  PackageInfo.g                toric Package                 David Joyner
##
##

SetPackageInfo( rec(

  PackageName := "Toric",
    Subtitle  := "toric varieties and some combinatorial geometry computations",
  Version := "1.9.6",
  Date    := "04/07/2024", # dd/mm/yyyy format
  License := "MIT",

  Persons := [ 
    rec( 
      LastName      := "Joyner",
      FirstNames    := "David",
      IsAuthor      := true,
      IsMaintainer  := false,
      Email         := "wdjoyner@gmail.com",
      WWWHome       := "https://sites.google.com/site/wdjoyner/",
      PostalAddress := Concatenation( [
                         "W. David Joyner\n",
                         "Mathematics Department\n",
                         "U. S. Naval Academy\n",
                         "Annapolis, MD 21402\n",
                         "USA" ] ),
      Place         := "Annapolis",
      Institution   := "U. S. Naval Academy"
    ),

    rec(
      LastName      := "GAP Team",
      FirstNames    := "The",
      IsAuthor      := false,
      IsMaintainer  := true,
      Email         := "support@gap-system.org",
    ),
  ],  

  Status  := "accepted",
  CommunicatedBy 
          := "Gerhard Hiss (Aachen)",
  AcceptDate 
          := "10/2005",

  SourceRepository := rec(
      Type := "git",
      URL := Concatenation( "https://github.com/gap-packages/", LowercaseString( ~.PackageName ) ),
  ),
  IssueTrackerURL := Concatenation( ~.SourceRepository.URL, "/issues" ),
  PackageWWWHome  := Concatenation( "https://gap-packages.github.io/", LowercaseString( ~.PackageName ) ),
  README_URL      := Concatenation( ~.PackageWWWHome, "/README.md" ),
  PackageInfoURL  := Concatenation( ~.PackageWWWHome, "/PackageInfo.g" ),
  ArchiveURL      := Concatenation( ~.SourceRepository.URL,
                                   "/releases/download/v", ~.Version,
                                   "/", ~.PackageName, "-", ~.Version ),
  ArchiveFormats := ".tar.gz",

  AbstractHTML := 
    "<span class=\"pkgname\">toric</span> is a <span class=\"pkgname\">GAP</span>package for computing with toric varieties.",


  PackageDoc := rec(
    BookName  := "toric",
    ArchiveURLSubset := ["doc"],
    HTMLStart := "doc/chap0_mj.html",
    PDFFile   := "doc/manual.pdf",
    SixFile   := "doc/manual.six",
    LongTitle := "toric variety package",
    Autoload := true
  ),

  Dependencies := rec(
    GAP := ">= 4.5",
    NeededOtherPackages := [],
    SuggestedOtherPackages := [],
    ExternalConditions := []
  ),

  AvailabilityTest := ReturnTrue,

  Autoload := false,

  TestFile := "tst/testall.g",

  Keywords := [ "toric variety", "cone", "fan", "Riemann-Roch space" ],

  AutoDoc := rec(
    TitlePage := rec(
      Copyright := "&copyright; 2004-2017 David Joyner.",
      Acknowledgements :=
"""
The code for the <Package>toric</Package> package was written during the
summer of 2002. 
It was put into &GAP; package format in the summer of 2004.
<P/>
    <Package>toric</Package> is free software; you can redistribute it and/or modify
    it under the terms of the MIT License.
<P/>
    <Package>toric</Package> is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    MIT License for more details.
<P/>

<P/>This documentation was prepared with the 
<Package>GAPDoc</Package> package of Frank Lübeck and Max Neunhöffer. 
Moreover, a bug in toric 1.8 was fixed with the help of Max Horn, and this
documentation was modified accordingly. Finally, I thank Olexandr Konovalov
and Max Horn for transferring this package to the new Git repository.
"""
        ),
    ),
));
