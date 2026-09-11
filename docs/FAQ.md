# MCP4H FAQ

### What is MCP4H?

MCP4H is an open, receiver-aware communication framework.

It helps separate useful meaning from the form in which that meaning was first observed, so the information can be expressed through a carrier appropriate to the receiver.

The shortest version is:

> **Preserve meaning. Adapt the carrier.**

---

### Is MCP4H an app?

No.

It is a protocol/framework, plus reference schemas, tools, bridges and examples.

Products can implement MCP4H without the protocol becoming dependent on one product.

---

### Does MCP4H mean text + audio + visual + haptics?

No.

Those were important early reference carriers, but they are not a closed list.

The `4` in MCP4H means **For**:

**Multimodal Communications Protocol For Humanity.**

The framework should remain open to any carrier or renderer that can be described and used meaningfully.

---

### Does everything have to become text first?

No.

That was an early MCP4H assumption and is now explicitly superseded.

Text is one useful carrier, but some information is naturally temporal, spatial, relational, spectral, continuous or force-related.

See `ASSUMPTIONS.md`.

---

### Is the Arbiter required?

No.

An Arbiter is one useful optional policy/judgment-assist layer.

It can decide things such as:

- which cue has priority;
- whether cues should be merged;
- whether something should be suppressed;
- when escalation is warranted;
- which available output path is appropriate.

The base protocol must also support deterministic paths with no Arbiter or AI service.

---

### Is MCP4H an AI protocol?

No.

AI can participate in interpretation, classification, summarization or policy.

MCP4H is intended to remain useful with or without AI.

---

### How is this different from Model Context Protocol?

They address different layers.

Model Context Protocol helps software and AI systems expose tools, resources and results.

MCP4H focuses on how meaningful interpreted information can be structured and projected toward a receiver.

The repository includes an MCP bridge because the two can work together.

---

### Why is MCP4SH important to MCP4H?

MCP4SH is the clearest current real-world reference implementation.

It takes heterogeneous simulation telemetry, normalizes and interprets it, then renders useful state through tactile feedback.

That makes it a valuable pressure test for semantic boundaries, timing, calibration, receiver capability and output independence.

---

### Why racing and flight?

They provide dense real-time machine state and immediate feedback.

Racing gives an established land-chassis reference.

Flight forces the architecture to represent different dynamics without pretending an aircraft is a car.

If the same base works naturally for both, that is a stronger architectural proof.

---

### Is MCP4H only about simulation?

No.

Simulation is the first practical proving ground.

Future reference work may include accessibility or remote operation specifically because those domains are different enough to expose hidden assumptions in the protocol.

---

### What happened to the original Manifesto and Whitepaper?

They remain part of the published historical record.

They describe an important earlier stage of MCP4H and retain their original citation titles.

The current working architecture is documented in:

- `FOUNDATIONS.md`;
- `README.md`;
- `ASSUMPTIONS.md`;
- `ROADMAP.md`.

---

### Is MCP4H production-ready?

The current v0.1.x line is implementable and has working schemas, validation, bridge examples and transport/rendering demos.

The broader receiver-aware v0.2 architecture is still being designed.

MCP4H should therefore be treated as an active v0.x framework, not a finished universal standard.

---

### Is MCP4H trying to solve everything?

No.

A protocol that claims universality before proving it across unrelated domains is not very useful.

The plan is to test the architecture incrementally, keep the base small, and let domain profiles carry domain-specific meaning.
