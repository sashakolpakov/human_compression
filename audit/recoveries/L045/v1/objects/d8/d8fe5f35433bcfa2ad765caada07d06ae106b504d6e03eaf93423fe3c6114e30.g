# This file is needed only for technical reasons.
# We cannot execute the calls already when SpinSym notifies the tables,
# because we are not yet allowed to call functions from `CTblLib`.

Perform( CTblLib.SpinSymNames, CTblLib.SetAttributesForSpinSymTable );

