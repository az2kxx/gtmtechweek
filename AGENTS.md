# Agent instructions

Read `HANDOVER.md` first, then `config/readiness.json`, the latest file under `executions/`, and the affected tender/partner files. Keep this repo usable by a new agent without chat history.

## Standing user intent

The user is a middleman-integrator: source utility tenders worldwide, identify a single E2E supplier or a complementary team, approach relevant technical/commercial owners and coordinate technical dialogue. The current deliverable is a public PoC, with real professional research and unsent channel drafts. Distribution is secondary and is not required for the demo.

The user authorizes commits/pushes to `az2kxx/gtmtechweek` and public access to the dashboard. Preserve unrelated changes and never force-push. Public access is not permission to disclose private contact emails, CRM identifiers or credentials. Keep Attio integrations intact.

## Rules

- Canonical research lives under `tenders/` and `partners/`; regenerate `dist/data.json` after changes. Do not manually patch the generated projection.
- Preserve evidence dates, source URLs, uncertainty and earlier procurement gates. Do not relabel old snapshots as newly researched.
- Never equate a future closing date with eligibility, a role/title with willingness, or a proposed pair with a confirmed consortium.
- A single E2E provider needs no second company. Use no-pair status when the chosen route actually needs a counterpart.
- Keep initial email plus four followups and LinkedIn script plus four followups per identified actor/tender. Keep script copies and `outreach.json` consistent.
- Clay must stay below 300 DATA credits: conservative ceiling 299 for one logical execution, shared by branches, retries and resumes. Unknown cost or absent durable reservation enforcement means cache-only. Never reset the budget by inventing another run ID.
- No automatic paid top-ups. No media spend or distribution authorization is implied by this PoC.
- HeyReach trial is expired. Mentic/Surfer accounts were reported MCP-compatible but were not callable in this session. Do not claim tool connections from the mere existence of adapter code.
- Attio owns private relationship history. Mirror only research fields; preserve opt-outs, replies, consent and manual corrections. Never post private mapping into public Git.
- Store real run timestamps, source revisions, stage results, error information and tool/cost evidence. Never fabricate execution history. Repo replays are not live scraping/enrichment runs.
- After meaningful edits, run `python scripts/validate.py`, `node --check dist/app.js`, and relevant guard tests. Use `python scripts/build_dashboard.py` for projection only; `record_execution.py` deliberately creates a new observed run record.
- Update `HANDOVER.md` and readiness evidence when implementation or connection state changes. Describe exactly what was tested and what remains pending.

No subagent delegation is required. Use the host's applicable Site skills for hosted edits and deployment.
