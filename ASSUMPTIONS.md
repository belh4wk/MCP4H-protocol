# MCP4H: Assumptions & Design Rationale

**Current foundation review:** 2026-09-11
**Compatibility baseline:** v0.1.x
**Next architecture target:** v0.2

## 1. Purpose

This document preserves the reasoning behind MCP4H design decisions.

Each entry is treated as a **commit of understanding**. Early assumptions are retained when superseded so the project history remains reconstructable.

## 2. Historical conceptual assumptions

### A-001 - Clarity > Fidelity

**Status:** EVOLVED, not discarded.

Original idea: people often respond faster to categorical cues than continuous telemetry under cognitive load.

Current interpretation: clarity should not require destructive loss of source truth. A projection may simplify information for a receiver while provenance, confidence and richer structure remain available upstream.

### A-002 - Contextual Trust Formation

**Status:** ACTIVE, broadened.

Consistent timing, semantics and behavior help a receiver learn what a system's output means.

The carrier can change without silently changing the meaning.

### A-003 - Modality Independence

**Status:** SUPERSEDED on 2026-09-11.

Historical assumption:

> Every signal must resolve first to a text-based semantic layer before any other form.

Why it is superseded:

Text is itself a carrier. Machine dynamics, spatial relations, force, motion, acoustic/spectral structure and probabilistic interpretations can lose useful information when forced through text first.

Replacement:

**A-004 - Semantic Representation Precedes Carrier Selection.**

## 3. Current conceptual assumptions

### A-004 - Semantic Representation Precedes Carrier Selection

**Status:** ACTIVE.

Meaning should be represented independently enough from its source and destination carriers that an appropriate projection can be selected without requiring text as the universal intermediate.

### A-005 - Receiver Capability Determines Projection

**Status:** ACTIVE.

A technically available output is not automatically an appropriate output.

Projection may consider supported carriers, topology, frequency/timing range, dynamic range, latency, accessibility constraints, calibration/fingerprint data, context and preferences.

### A-006 - Temporal, Spatial, Relational and Spectral Structure Can Be Semantic

**Status:** ACTIVE.

Important information may exist in rate of change, sequence, recurrence, rhythm, oscillation, frequency, phase, modulation, position, direction or relationships between signals.

### A-007 - Provenance Survives Translation

**Status:** ACTIVE.

Where relevant, MCP4H should retain source identity, timestamp, interpreter identity, confidence, transformation lineage and projection origin.

### A-008 - Intelligence Is Optional

**Status:** ACTIVE.

AI or an Arbiter may improve interpretation, prioritization or projection, but cannot be a mandatory dependency of the base protocol.

Deterministic paths remain first-class.

### A-009 - Domain Profiles May Be Specific; the Base Envelope Must Stay Neutral

**Status:** ACTIVE.

Conversation, automotive dynamics, aircraft dynamics, industrial state, navigation and future biological research can require different semantic vocabularies.

Those domains should extend a neutral base rather than forcing unrelated sources into one vocabulary.

### A-010 - Preserve Agency and State Boundaries

**Status:** ACTIVE.

Observed state, interpreted state and recommended action should remain distinguishable.

### A-011 - Communication Can Be Bidirectional

**Status:** ACTIVE.

A receiver response can become a new observation in a continuing loop.

### A-012 - Semantic Records Are Independently Addressable

**Status:** ACTIVE.

Observation, Interpretation, Policy, Projection and Response should not be forced into one monolithic record.

A shared envelope grammar with linked records allows one Observation to support multiple Interpretations and one Interpretation to support multiple Projections. Low-latency transports may still bundle records together.

### A-013 - Confidence Is Scoped to What It Describes

**Status:** ACTIVE.

Observation confidence/quality and Interpretation confidence are different claims and should be represented separately. Measurements may also express uncertainty where relevant.

The core should avoid one ambiguous top-level confidence value.

### A-014 - Domain Seriousness Is Not Attention Priority

**Status:** ACTIVE.

Severity/criticality is domain-specific and belongs in a profile where meaningful. Priority, interruption and escalation belong to Policy.

The base protocol should not assume that a semantically severe state always requires the highest immediate attention behavior.

## 4. Historical design assumptions

### D-001 - Three-Stage Flow Architecture

**Status:** SUPERSEDED as the universal model on 2026-09-11.

Historical model:

```text
Input -> MCP4H Core Translator -> Output Adapter
```

Replacement architectural model:

```text
Observation
  -> Interpretation
  -> optional Policy
  -> Projection
  -> Transport
  -> Rendering
  -> optional Response
```

Not every implementation must deploy each step as a separate process. The separation is conceptual and contractual first.

### D-002 - Schema Minimalism

**Status:** ACTIVE, evolved.

MCP4H should remain implementable without a large runtime or mandatory service mesh.

Minimalism now means a small base envelope, explicit extensions and profiles, optional richer structures, and no destructive simplification merely to keep one example short.

## 5. Current design rules

### D-003 - Domain Logic Terminates at the Semantic Boundary Where Practical

Source-specific quirks belong upstream. Renderer-specific quirks belong downstream.

### D-004 - Bridges Map; They Do Not Own Universal Meaning

A bridge may normalize values where a domain profile defines that operation.

It should not arbitrarily collapse every source into one 0.0-1.0 intensity scale if doing so destroys useful information.

### D-005 - Policy Is Separable

Prioritization, suppression, deduplication, escalation and interruption rules are useful but separable.

The Arbiter remains one implementation pattern for this optional policy layer.

### D-006 - Transport Is Replaceable

The semantic model should not require one transport.

### D-007 - Compatibility Is Explicit

v0.1.x remains a compatibility line.

v0.2 should not silently redefine v0.1.x packets and call them unchanged.

## 6. Reference tests for the next cycle

The v0.2 foundations are not considered proven until the same base architecture can naturally represent:

1. a tyre approaching breakaway;
2. an aircraft entering a meaningful load state;
3. one non-simulation accessibility or remote-operation event.

If those examples require unrelated domains to impersonate one another, the base is still too narrow.

## 7. Related foundation

See [`FOUNDATIONS.md`](FOUNDATIONS.md) for the current project-level architectural principles.

Historical publications and citations remain preserved as historical records even where terminology has evolved.
