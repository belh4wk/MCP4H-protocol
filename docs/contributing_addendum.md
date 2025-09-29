# CONTRIBUTING Addendum — Schema/Examples

- **Schemas:** additive-only on v0.1.x. New fields MUST be optional and documented.
- **Examples:** each new field/profile MUST include at least one example in `/examples*` and a short doc blurb.
- **CI:** all PRs MUST pass CI (`.github/workflows/ci.yml`). Add/update tests in `tests/` for new examples.
- **No PII:** Do not include personal data in examples.
