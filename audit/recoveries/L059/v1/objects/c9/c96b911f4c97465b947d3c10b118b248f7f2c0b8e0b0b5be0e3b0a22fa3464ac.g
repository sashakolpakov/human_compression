L059Result := rec(
  A := Group( [ (4,8)(6,7), (2,4)(5,6), (1,5)(2,3) ] ),
  F := Group( [ (4,8)(6,7), (2,4)(5,6), (1,2)(3,5)(4,6)(7,8) ] ),
  b := 1,
  base_edge := [ 1, 2 ],
  black := [ 1, 5, 6, 7 ],
  edges := [ [ 1, 2 ], [ 1, 4 ], [ 1, 8 ], [ 2, 6 ], [ 2, 7 ], [ 3, 5 ], 
      [ 3, 6 ], [ 3, 7 ], [ 4, 5 ], [ 4, 7 ], [ 5, 8 ], [ 6, 8 ] ],
  label := "VT3_8_2",
  n := 8,
  retained_edge_transitive_classes := 2,
  search := rec(
      method := "maximal_subgroup_descent",
      nodes := [ rec(
              H := Group( [ (4,8)(6,7), (2,4)(5,6), (1,5)(2,3) ] ),
              children := [ rec(
                      K := 
                       Group( [ (2,8,4)(5,7,6), (1,6)(2,8)(3,4)(5,7), 
                          (1,5)(2,3)(4,8)(6,7) ] ),
                      reason := "retained_class",
                      target := 2 ), rec(
                      K := Group( [ (4,8)(6,7), (1,6)(2,8)(3,4)(5,7) ] ),
                      reason := "order" ), rec(
                      K := Group( [ (4,8)(6,7), (2,8,4)(5,7,6) ] ),
                      reason := "order" ) ] ), rec(
              H := 
               Group( [ (2,8,4)(5,7,6), (1,6)(2,8)(3,4)(5,7), 
                  (1,5)(2,3)(4,8)(6,7) ] ),
              children := [ rec(
                      K := 
                       Group( [ (1,6)(2,8)(3,4)(5,7), (1,7)(2,4)(3,8)(5,6) ] )
                       ,
                      reason := "order" ), rec(
                      K := Group( [ (2,8,4)(5,7,6) ] ),
                      reason := "order" ) ] ) ] ),
  w := 2,
  white := [ 2, 3, 4, 8 ],
  witnesses := [ rec(
          B := Group( [ (4,8)(6,7) ] ),
          H := Group( [ (4,8)(6,7), (2,4)(5,6), (1,5)(2,3) ] ),
          H0 := Group( [ (4,8)(6,7), (2,4)(5,6) ] ),
          H1 := Group( [ (4,8)(6,7), (1,6)(3,4) ] ),
          dualorder := 2,
          group_order := 24,
          maxcode := [ "2T", "2T", "2T", "2T" ],
          maxorder := 4,
          normcode := [ true, false, false, false ],
          structure := [ "S4", "S3", "S3", "C2" ],
          subgroup_orders := [ 6, 6, 2 ] ), rec(
          B := Group( () ),
          H := 
           Group( [ (2,8,4)(5,7,6), (1,6)(2,8)(3,4)(5,7), 
              (1,5)(2,3)(4,8)(6,7) ] ),
          H0 := Group( [ (2,8,4)(5,7,6) ] ),
          H1 := Group( [ (1,6,7)(3,4,8) ] ),
          dualorder := 2,
          group_order := 12,
          maxcode := [ "M", "M", "2T", "2T" ],
          maxorder := 3,
          normcode := [ true, false, false, true ],
          structure := [ "A4", "C3", "C3", "1" ],
          subgroup_orders := [ 3, 3, 1 ] ) ] );
