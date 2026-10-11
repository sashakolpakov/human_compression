Checking the configured Lean proofs together
============================================

The new ``scripts/check_project_lean.py`` command calls the existing
100-module library checker and the separate Topic B checker in sequence.
It preserves both fresh child reports and records which sources this
invocation actually checked. It changes no mathematical source or
existing checker, and Lake's default library remains unchanged.

From the repository root, with the pinned compiler and package cache::

    python3 -B scripts/check_project_lean.py --lean LEAN --packages PACKAGES --out /fresh/directory --jobs 1

Both components are selected by default. ``--components topic-b`` or
``--components legacy`` explicitly selects a partial check. The output
directory must be fresh and outside the checkout. Use ``--repo CHECKOUT``
when calling the script from elsewhere.

The `admission <admission.json>`_ records independent review of dispatch,
input bindings, failure handling and coverage labels. All fourteen fixture
cases passed. A fresh public Topic B run checked one source, six axiom
reports and its hypothesis controls. It is correctly labelled partial;
this validation did not rerun the entire 100-module library. Full success
is available only after both configured child runs pass in the same
invocation. Synthetic fixtures establish no mathematical theorem.

The `author instructions <author/README.rst>`_ give the complete interface.
The `root review <root_review/review.json>`_ and individual child reports
state the validation performed. Existing compiler, cached dependency and
native-evaluation trust boundaries are unchanged. These supporting Lean
proofs do not certify all written manuscript results.
