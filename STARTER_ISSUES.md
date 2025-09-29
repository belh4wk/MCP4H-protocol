# Starter Issues for MCP4H™

Use these as copy/paste text when creating issues on GitHub. Labels in **bold** are suggested.

---

## 1) examples: add SimHub → MCP4H-L1 → Arduino windsim
**Labels:** examples, good first issue

**Why**
Provide a hands-on proof that MCP4H™ can act as a neutral line protocol between SimHub telemetry and Arduino devices.

**Tasks**
- [ ] Add `/examples/arduino/windsim/` with:
  - [ ] `README.md` (wiring, SimHub config, run steps, safety note)
  - [ ] `mcp4h_windsim.ino` (Arduino sketch)
  - [ ] `simhub_format.txt` (one-line format string)
- [ ] Record a 20–30s demo clip (optional) and link it in README.
- [ ] Add `examples/mcp4h_windsim_example.json` that matches the schema.

**Acceptance Criteria**
- Wind fan speed scales with telemetry speed; LED brightness reflects gear.
- `tests/validate_messages.py` passes in CI.

---

## 2) spec: refine JSON Schema (units, enums, ranges)
**Labels:** spec, enhancement

**Why**
Developers need clarity and validation. A stronger schema enables higher-quality integrations.

**Tasks**
- [ ] Add `signal.type` enum (e.g., `telemetry`, `axis`, `button`, `haptic`, `event`)
- [ ] Define common fields: `units`, `frame`, optional `rate_hz`
- [ ] Add constraints (e.g., `confidence` 0..1, numeric ranges when known)
- [ ] Add a `telemetry` sub-schema example in `/spec/examples/`

**Acceptance Criteria**
- New examples validate.
- README references the schema file and examples.

---

## 3) tests: add more MCP4H™ example messages
**Labels:** tests, examples

**Why**
Broaden coverage so CI guards the contract as the spec evolves.

**Tasks**
- [ ] Add examples for `axis`, `button`, and `haptic` under `/examples/`
- [ ] Ensure each one validates against the schema
- [ ] Update `PROJECT_STATUS.md`

**Acceptance Criteria**
- CI passes with new examples.

---

## 4) docs: add “Getting Started” and diagram callouts
**Labels:** docs

**Why**
First-time visitors should be able to try MCP4H™ within minutes.

**Tasks**
- [ ] Add a “Getting Started” section to `README.md`
- [ ] Link the flow diagram and the Arduino example
- [ ] Mention CI badge and how to interpret it

**Acceptance Criteria**
- README renders links/images and steps clearly.

---

## 5) governance: branch protection & contribution flow
**Labels:** governance, meta

**Why**
Encourage high-quality contributions and keep `main` stable.

**Tasks**
- [ ] Document required checks for `main` (CI must pass)
- [ ] Recommend PR flow and labeling
- [ ] Add note about SECURITY.md and responsible disclosure

**Acceptance Criteria**
- CONTRIBUTING.md references these guidelines.
