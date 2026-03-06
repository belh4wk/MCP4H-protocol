# Arbiter

An arbiter is the **judgment-assist layer**.

It decides things bridges should not decide on their own, for example:

- priority between competing cues
- suppression windows and interruption budgets
- escalation rules
- cue merging / deduplication
- channel substitution based on context or capability

This repository primarily defines the **protocol** and the **bridge surface**.
It may contain examples or policy hooks that an arbiter could use, but a full arbiter should remain a separable component so the base protocol stays neutral and portable.
