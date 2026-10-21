for n in [8..30] do
    if n mod 2 = 0 then
        x := PermList(Concatenation([1], [3..n], [2]));
        t := (1,2)(3,4);
    else
        x := PermList(Concatenation([2..n], [1]));
        t := (1,2)(3,6);
    fi;
    g := Group(x,t);
    if Size(g) <> Factorial(n)/2 then
        Print("FAIL ", n, "\n"); FORCE_QUIT_GAP(1);
    fi;
    Print("PASS ", n, " ", Size(g), "\n");
od;
Print("TERMINAL_PASS 23 finite generation checks\n");
QUIT;
