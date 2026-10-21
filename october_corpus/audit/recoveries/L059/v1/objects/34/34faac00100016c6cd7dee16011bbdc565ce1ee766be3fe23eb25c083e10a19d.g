L059Result := rec(
  A := Group( [ ( 3, 5)( 8,10), (2,4)(7,9), ( 2,10)( 5, 7), (1,3)(6,8) ] ),
  F := Group( [ ( 3, 5)( 8,10), (3,9)(4,8), (2,4)(7,9), 
      ( 1, 2)( 3,10, 9, 8, 5, 4)( 6, 7) ] ),
  b := 1,
  base_edge := [ 1, 2 ],
  black := [ 1, 3, 5, 7, 9 ],
  edges := [ [ 1, 2 ], [ 1, 4 ], [ 1, 8 ], [ 1, 10 ], [ 2, 3 ], [ 2, 5 ], 
      [ 2, 9 ], [ 3, 4 ], [ 3, 6 ], [ 3, 10 ], [ 4, 5 ], [ 4, 7 ], [ 5, 6 ], 
      [ 5, 8 ], [ 6, 7 ], [ 6, 9 ], [ 7, 8 ], [ 7, 10 ], [ 8, 9 ], [ 9, 10 ] ]
   ,
  label := "010_002",
  n := 10,
  subgroup_classes := 19,
  w := 2,
  white := [ 2, 4, 6, 8, 10 ],
  witnesses := [ rec(
          B := Group( () ),
          H := 
           Group( [ ( 1, 3)( 2,10)( 5, 7)( 6, 8), ( 2, 4, 8,10)( 3, 5, 7, 9) 
             ] ),
          H0 := 
           Group( [ ( 2, 4, 8,10)( 3, 5, 7, 9), ( 2, 8)( 3, 7)( 4,10)( 5, 9) 
             ] ),
          H1 := Group( [ ( 1, 3, 9, 5)( 4,10, 6, 8) ] ),
          dualorder := 2,
          group_order := 20,
          maxcode := [ "X", "X", "2T", "2T" ],
          maxorder := 5,
          normcode := [ false, false, false, true ],
          structure := [ "C5 : C4", "C4", "C4", "1" ],
          subgroup_orders := [ 4, 4, 1 ] ), rec(
          B := Group( [ ( 3, 5, 9)( 4, 8,10) ] ),
          H := Group( [ ( 2, 8)( 3, 7)( 4,10)( 5, 9), (1,3,9)(4,6,8) ] ),
          H0 := Group( [ ( 2, 8)( 3, 7)( 4,10)( 5, 9), ( 2, 4,10)( 5, 7, 9) 
             ] ),
          H1 := Group( [ ( 3, 5, 9)( 4, 8,10), (1,3,9)(4,6,8) ] ),
          dualorder := 2,
          group_order := 60,
          maxcode := [ "2T", "2T", "2T", "2T" ],
          maxorder := 5,
          normcode := [ true, false, false, false ],
          structure := [ "A5", "A4", "A4", "C3" ],
          subgroup_orders := [ 12, 12, 3 ] ), rec(
          B := Group( [ (3,9)(4,8), ( 3, 9, 5)( 4,10, 8) ] ),
          H := Group( [ (1,3)(6,8), ( 2, 4, 8,10)( 3, 5, 7, 9) ] ),
          H0 := Group( [ ( 2, 4, 8,10)( 3, 5, 7, 9), (3,9)(4,8) ] ),
          H1 := Group( [ (3,9)(4,8), ( 3, 9, 5)( 4,10, 8), (1,3)(6,8) ] ),
          dualorder := 2,
          group_order := 120,
          maxcode := [ "2T", "2T", "2T", "2T" ],
          maxorder := 6,
          normcode := [ true, false, false, false ],
          structure := [ "S5", "S4", "S4", "S3" ],
          subgroup_orders := [ 24, 24, 6 ] ) ] );
