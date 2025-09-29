# MCP4H™ v0.1.1 Release Checklist

Date: 2025-09-29

## 0) Preconditions
- [ ] CI is green on `main`
- [ ] README contains Quick Start + links to `docs/`
- [ ] `spec/schema/mcp4h-v0.1.1.json` is present and referenced
- [ ] Examples and tests updated (`examples_v0.1.1`, `tests/vectors/*`)

## 1) Bump CHANGELOG
- [ ] Update `docs/addenda/CHANGELOG_addendum_v0.1.1.md` if needed
- [ ] Summarize: envelope fields, profiles, content types, examples, tools, CI

## 2) Tag and push
```bash
git pull --rebase
git tag -a v0.1.1 -m "MCP4H™ v0.1.1 (additive): envelope fields + profiles + examples + CI"
git push origin v0.1.1
```

## 3) GitHub Release
- [ ] Create release from tag **v0.1.1**
- [ ] Use `docs/addenda/CHANGELOG_addendum_v0.1.1.md` as notes (edit for clarity)
- [ ] Attach any artifacts (e.g., infographic PNGs if desired)

## 4) Zenodo
- [ ] Ensure GitHub-Zenodo integration is on (repo connected)
- [ ] Trigger a new Zenodo snapshot by publishing the GitHub release
- [ ] Edit Zenodo record metadata (version, description, contributors, keywords)
- [ ] Record DOI in README badges if applicable

## 5) HAL / OSF preprints
- [ ] Upload or update the v0.1.1 whitepaper/handbook excerpt if needed
- [ ] Reference the GitHub tag and Zenodo DOI in the submission text
- [ ] Add links back to repo and docs

## 6) README badges (optional)
- [ ] Add CI badge
- [ ] Add DOI badge (Zenodo)
- [ ] Add license badge

## 7) Announce
- [ ] Short LinkedIn post (quiet swagger tone): what changed, why it matters (LED cues PoC), call for contributors
- [ ] Link to: GitHub release + article/post (if any)

## 8) Post-release tasks
- [ ] Open issues for: UDP discovery (mDNS), CBOR-first examples, SimHub bridge PoC
- [ ] Milestone `v0.1.2` (additive), sketch scope
