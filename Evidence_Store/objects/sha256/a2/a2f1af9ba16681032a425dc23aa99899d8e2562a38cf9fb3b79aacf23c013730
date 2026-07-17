-- Stage 4 (workflow step 6 / section 5): realization-poset incidence table upstairs
load "/home/wlloyd/Cella Framework/docs/horizon_wreath_inertia_model.m2";

tbl = {
    ("IR", IR),
    ("Ceven", Ceven),
    ("Codd", Codd),
    ("IZ", IZ),
    ("Ceven+IZ", Ceven+IZ),
    ("Codd+IZ", Codd+IZ),
    ("IR+IZ", IR+IZ),
    ("SubEven", SubEven),
    ("SubOdd", SubOdd),
    ("IR+Ceven+IZ", IR+Ceven+IZ),
    ("IR+Codd+IZ", IR+Codd+IZ)
    };

scan(tbl, p -> (
    lbl := p#0; I := p#1;
    c := codim I;
    d := degree I;
    Icl := cleanGeneric I;
    isEmptyGeneric := (Icl == ideal(1_S));
    print(lbl
        | ": ambient codim=" | toString c
        | ", codim in X=" | toString(c - codim IX)
        | ", degree=" | toString d
        | ", empty after generic saturation: " | toString isEmptyGeneric);
    ));
