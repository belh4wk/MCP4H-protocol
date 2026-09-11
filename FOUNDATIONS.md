# MCP4H Foundations

**Multimodal Communications Protocol For Humanity**

> **Preserve meaning. Adapt the carrier.**

MCP4H is an open, receiver-aware communication framework for translating meaningful information across source systems, transports, software, devices and sensory carriers.

It starts from a simple problem:

**Useful information often exists in a form the receiver cannot use directly.**

A machine may expose telemetry. A person may need touch. A software agent may need structured state. A remote operator may need a combination of force, sound and visual cues. A future accessibility system may need to move information away from a channel that is unavailable or overloaded.

MCP4H aims to preserve what matters while allowing the carrier to change.

## 1. Tyto thesis

Tyto Sensory Labs explores how meaningful patterns in complex systems can be interpreted, translated and expressed through the sensory channels available to the receiver.

Systems continuously express state through patterns of change.

Depending on the domain, useful information may appear in:

- magnitude;
- timing;
- rate of change;
- rhythm;
- oscillation;
- frequency;
- phase;
- modulation;
- recurrence;
- spatial position or direction;
- topology;
- relationships between signals;
- uncertainty and confidence.

Frequency and resonance are therefore recurring tools in Tyto's work, but MCP4H does not claim that every property of every system is literally reducible to frequency.

The engineering question is narrower and more useful:

> **Which patterns carry meaning for the task, and how can that meaning survive translation into another form?**

## 2. Core separation

MCP4H separates concepts that are often mixed together:

1. **Observation** - what a source measured, reported or emitted.
2. **Interpretation** - what that observation appears to mean in context.
3. **Policy** - optional decisions about priority, suppression, escalation, merging, rate limits or attention.
4. **Projection** - how the meaning should be expressed for a particular receiver and context.
5. **Transport** - how the information moves between components.
6. **Rendering** - the final physical or digital expression: touch, force, audio, light, text, spatial cues, machine-readable state or another supported carrier.
7. **Response** - optional feedback or action that becomes part of the next state of the system.

```text
state
  -> observation
  -> interpretation
  -> optional policy
  -> projection
  -> transport
  -> rendering
  -> perception / response
  -> state
```

Communication is therefore treated as a loop, not only as a one-way payload.

In the v0.2 design, these conceptual stages can be represented by separately addressable records linked through IDs/relations. Implementations may still bundle records together when low latency or simplicity requires it.

## 3. Text is a carrier

Text is valuable for inspection, logs, validation, accessibility and many interfaces.

It is not the mandatory canonical representation of all meaning.

Forcing every source through text first can damage information that is naturally temporal, spatial, relational, spectral, force-related, probabilistic or continuous.

MCP4H therefore aims to represent meaning independently enough that text can be one projection among many.

## 4. Receiver capability is first-class

A receiver or renderer may describe capabilities such as:

- available modalities;
- spatial layout or actuator topology;
- temporal resolution;
- usable frequency range;
- dynamic range;
- latency limits;
- device identity;
- calibration or fingerprint information;
- accessibility constraints;
- current context;
- preferences.

The same semantic event may therefore produce different valid projections for different receivers.

## 5. Structure can carry meaning

A scalar value is not always the message.

A change can mean something different depending on how quickly it changed, whether it oscillates, where it occurred, whether another signal changed first, whether it repeats and whether the pattern is stable or transient.

MCP4H should preserve temporal, spatial, relational and spectral structure when those structures matter to interpretation.

## 6. Provenance and uncertainty

Translation should not hide where a conclusion came from.

Where appropriate, an MCP4H representation should be able to retain:

- source identity;
- observation time;
- interpretation origin;
- confidence or uncertainty;
- transformation history;
- relevant assumptions;
- projection origin.

## 7. AI is optional

AI may act as an interpreter, classifier, summarizer, planner or policy engine.

It is not required for MCP4H to function.

Deterministic paths remain first-class, especially where latency, repeatability, validation or safety matter.

The existing Arbiter concept remains useful as an optional judgment-assist or policy component; it is not "the brain" of the protocol and should remain separable from the neutral protocol layer.

## 8. Domain-specific meaning belongs at explicit boundaries

Conversation, automotive dynamics, aircraft dynamics, industrial machinery, navigation and future biological research may require very different semantic vocabularies.

They should not be forced into one universal list of domain concepts.

A guiding implementation rule is:

> **Domain-specific logic terminates at the semantic boundary wherever reasonably possible.**

## 9. x-agnostic by design

MCP4H should minimize unnecessary binding to application, game, vehicle, machine, vendor, hardware, operating system, platform, transport, modality, AI model or species.

This does not mean every implementation supports everything.

It means the base architecture should not require unrelated domains to impersonate one another.

## 10. Reference implementation strategy

MCP4SH is currently the strongest practical reference for the MCP4H direction.

It demonstrates:

```text
heterogeneous simulation telemetry
  -> normalization and interpretation
  -> meaningful machine-state cues
  -> tactile rendering
```

The next architectural proof is deliberately cross-domain:

- land-chassis semantics;
- airframe semantics;
- the same neutral base envelope;
- more than one output path.

A later non-simulation reference should test whether the framework still feels natural in an accessibility or remote-operation context.

Generality has to be earned through implementation.

## 11. Open protocol, focused implementations

MCP4H is the open protocol/framework.

Commercial or specialized Tyto products can implement the framework without the protocol becoming dependent on those products.

## 12. Foundational principle

> **Preserve meaning. Adapt the carrier.**
