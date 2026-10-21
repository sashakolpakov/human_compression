#############################################################################
##
##  PackageInfo.g for the package `alco'
##

SetPackageInfo( rec(

  PackageName := "ALCO",
  Subtitle := "Tools for algebraic combinatorics",
  Version := "1.1.2",
  Date := "05/09/2025", # dd/mm/yyyy format
  License := "GPL-3.0-or-later",

  PackageWWWHome := "https://bnasmith.github.io/alco/",

  SourceRepository := rec(
      Type := "git",
      URL := Concatenation( "https://github.com/BNasmith/", LowercaseString( ~.PackageName ) ),
  ),
  IssueTrackerURL := Concatenation( ~.SourceRepository.URL, "/issues" ),
  SupportEmail := "bnasmith@proton.me",

  ##  URL of the archive(s) of the current package release, but *without*
  ##  the format extension(s), like '.tar.gz' or '-win.zip', which are given next.
  ##  The archive file name *must be changed* with each version of the archive
  ##  (and probably somehow contain the package name and version).
  ##  The paths of the files in the archive must begin with the name of the
  ##  directory containing the package (in our "example" probably:
  ##  example/init.g, ...    or example-3.3/init.g, ...  )
  #
  ArchiveURL := Concatenation( ~.SourceRepository.URL,
                                   "/releases/download/v", ~.Version,
                                   "/", ~.PackageName, "-", ~.Version ),

  ArchiveFormats := ".tar.gz",

  Persons := [
    rec(
      LastName      := "Nasmith",
      FirstNames    := "Benjamin",
      IsAuthor      := true,
      IsMaintainer  := true,
      Email         := "bnasmith@proton.me",
      WWWHome       := "https://github.com/BNasmith/"
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
  # Status := "accepted",
  Status := "deposited",

  ##  You must provide the next two entries if and only if the status is
  ##  "accepted" because is was successfully refereed:
  # format: 'name (place)'
  # CommunicatedBy := "Mike Atkinson (St Andrews)",
  #CommunicatedBy := "",
  # format: mm/yyyy
  # AcceptDate := "08/1999",
  #AcceptDate := "",

  ##  For a central overview of all packages and a collection of all package
  ##  archives it is necessary to have two files accessible which should be
  ##  contained in each package:
  ##     - A README file, containing a short abstract about the package
  ##       content and installation instructions.
  ##     - The PackageInfo.g file you are currently reading or editing!
  ##  You must specify URLs for these two files, these allow to automate
  ##  the updating of package information on the GAP Website, and inclusion
  ##  and updating of the package in the GAP distribution.
  #
  README_URL := Concatenation( ~.PackageWWWHome, "/README.md" ),
  PackageInfoURL := Concatenation( ~.PackageWWWHome, "/PackageInfo.g" ),

  ##  Provide a short (up to a few lines) abstract in HTML format, explaining
  ##  the package content. This text will be displayed on the package overview
  ##  Web page. Please use '<span class="pkgname">GAP</span>' for GAP and
  ##  '<span class="pkgname">MyPKG</span>' for specifing package names.
  ##
  AbstractHTML :=
    "The <span class=\"pkgname\">ALCO</span> package provides tools for algebraic combinatorics including implementations of octonion and Jordan algebras.",

  PackageDoc := rec(
    BookName  := ~.PackageName,
    ArchiveURLSubset := ["doc"],
    HTMLStart := "doc/chap0.html",
    PDFFile   := "doc/manual.pdf",
    SixFile   := "doc/manual.six",
    LongTitle := ~.Subtitle,
  ),



  ##  Are there restrictions on the operating system for this package? Or does
  ##  the package need other packages to be available?
  Dependencies := rec(
    # GAP version, use the version string for specifying a least version,
    # prepend a '=' for specifying an exact version.
    GAP := "4.14",
    SuggestedOtherPackages := [],
    ExternalConditions := [],
    NeededOtherPackages := [["ResClasses",">=4.7.3"]]
  ),

  AvailabilityTest := ReturnTrue,

  ##  *Optional*: the LoadPackage mechanism can produce a default banner from
  ##  the info in this file. If you are not happy with it, you can provide
  ##  a string here that is used as a banner. GAP decides when the banner is
  ##  shown and when it is not shown (note the ~-syntax in this example).
  BannerString := Concatenation(
      "----------------------------------------------------------------\n",
      "Loading  ALCO ", ~.Version, "\t(Tools for Algebraic Combinatorics)", "\n",
      "by ",
      JoinStringsWithSeparator( List( Filtered( ~.Persons, r -> r.IsAuthor ),
                                      r -> Concatenation(
          r.FirstNames, " ", r.LastName, " (", r.WWWHome, ")\n" ) ), "   " ),
      "This program is distributed under GNU General Public License 3.0", "\n",
      # "For help, type: ?ALCO package \n",
      "----------------------------------------------------------------\n" ),

  TestFile := "tst/testall.g",
  
  ##  *Optional*: Here you can list some keyword related to the topic
  ##  of the package.
  # Keywords := ["Smith normal form", "p-adic", "rational matrix inversion"]
  Keywords := ["Octonions", "Jordan algebras", "t-Designs"],

  AutoDoc := rec(
    entities := rec(
        VERSION := ~.Version,
        DATE := ~.Date,
        io := "<Package>io</Package>",
        ALCO := "<Package>ALCO</Package>" ,
    ),
    TitlePage := rec(
        Copyright := Concatenation(
            "&copyright; 2024 by Benjamin Nasmith<P/>\n\n",
            "This package may be distributed under the terms and conditions ", 
            "of the GNU Public License Version 3 or (at your option) any later version.\n"
            ), 
        Abstract := Concatenation(
            "ALCO provides implementations in &GAP; of octonion algebras, Jordan algebras, ",
            "and certain important integer subrings of those algebras. It also provides ", 
            "tools to compute the parameters of t-designs in spherical and projective spaces ", 
            "(modeled as manifolds of primitive idempotent elements in a simple Euclidean ", 
            "Jordan algebra). Finally, this package provides tools to explore octonion lattice ",
            "constructions, including octonion Leech lattices.\n" 
            ), 
        Acknowledgements := Concatenation( 
            "This documentation was prepared using the ", 
            "&GAPDoc; package.\n",  
            "<P/>\n" 
            ) 
    )
),

));
