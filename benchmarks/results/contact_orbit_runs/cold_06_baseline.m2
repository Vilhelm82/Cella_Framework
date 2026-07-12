load "/home/wlloyd/Cella Framework/docs/files/horizon_wreath_inertia_model.m2";
contactImages = apply(epsilons, eps -> projectToBase(contactIdeal eps + ideal(0_S)));
print "CONTACT_COLD_BASELINE_RESULT=CLOSED";
