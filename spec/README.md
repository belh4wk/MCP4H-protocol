# MCP4H Specification Layout

This directory currently contains two generations of MCP4H work.

## v0.1.x compatibility line

The existing v0.1.x specification remains in its historical paths for compatibility with validators, examples, bridges and relative `$ref` links.

Current v0.1.x material includes:

- `behavior/`
- `bindings/`
- `cues/`
- `domain_profiles/`
- `profiles/`
- `schema/`
- `schemas/`
- `SPEC_MCP4H_v0.1.0.md`
- `draft-mcp-00.md`
- `media-type.md`

These paths are not being moved yet.

Moving them into a new `v0.1/` directory before the migration work is ready would break existing relative references and tooling. The eventual versioned-layout cleanup should therefore be one controlled migration with updated references, validators and compatibility notes.

## v0.2 design line

New receiver-aware architecture work lives under:

`v0.2/`

v0.2 is currently a **design draft**, not the canonical runtime schema.

The v0.2 direction uses a shared envelope grammar with separately addressable record types, including:

- Observation;
- Interpretation;
- optional Policy Decision;
- Projection;
- optional Response;
- referenced Capability Profiles.

The records can be linked by IDs/relations and may be bundled in one low-latency transport message without losing their logical separation.

## Future cleanup target

After the first v0.2 schemas and migration fixtures exist, the repository can move toward a layout such as:

```text
spec/
  v0.1/
    ...compatibility material...
  v0.2/
    core/
    capability/
    policy/
    projection/
    profiles/
    examples/
```

Do not duplicate the current v0.1.x files into `v0.1/` in the meantime. Two apparent sources of truth would be worse than the current historical layout.
