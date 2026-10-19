# AGENTS.md — qa-knowledge

Knowledge about the projects the QA platform serves. Read by agents; changed only through reviewed pull requests.

## Layout
`org/` (organisation-wide) · `projects/<project>/` (project.yaml, business rules, flows.md, risks) · `repos/<repo>/` (one per repository, shared repositories once) · `automation/` · `agents/` (agent calibration) · `case-candidates/` (golden-set case candidates awaiting review)

## Rules
1. **Notes and pointers only — never code.** Describe what code does and point to it as `file:line@SHA`. Allowed fenced blocks: `mermaid`, short `yaml` / `json` examples (≤ 15 lines). The PR check fails otherwise.
2. **No secrets, tokens or personal data.**
3. **Every fact has a source** (file:line@SHA, Jira key, document link).
4. **Rules seen only in code are `PROPOSED`** until the Product Owner confirms them.
5. **One folder per repository**; shared repositories are described once and referenced from each project.
6. **Every change is a pull request** reviewed by the CODEOWNERS of that folder.
