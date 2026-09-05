# Tender Observatory — gtmtechweek PoC

A repository-first demonstration of utility tender origination, supplier matching and technical-dialogue preparation. The repository is the demo source of truth; the dashboard is a generated, read-only projection. Attio remains an optional mirror, with its existing integration preserved.

> Publication status: GitHub integration upload was rejected with HTTP 403 `Resource not accessible by integration`. Source and workflow are prepared; the remote repository has not received them. See HANDOVER.md for recovery. The public dashboard uses its hosted fallback until publication succeeds.

## Start here

- [JUDGES.md](JUDGES.md): evidence, limitations and a five-minute walkthrough.
- [QA_REPORT.md](QA_REPORT.md): actual checks for this export.
- [PUBLISH.md](PUBLISH.md): manual CLI publication of the ZIP.
- [HANDOVER.md](HANDOVER.md): continuation context and live integration requirements.

## Included

- 10 tender dossiers across six regions, from the existing 2026-09-04 research snapshot.
- 12 companies and 13 named professional contacts; direct business emails and private CRM/Clay identifiers are excluded from the public export.
- 6 proposed delivery pairings covering 8 tender records. Two tenders still need qualified actors. A separate unmatched contact remains visible.
- 17 actor/tender packets: tailored email and LinkedIn sequences, each with four followups. Some people appear under several tenders; these are associations, not extra contacts.
- One technology/use-case blog draft that avoids identifying a proposed consortium or exposing a deal strategy.
- Weekly execution records, public-data validation, an interactive dashboard and optional GitHub Pages publishing.

Every message is a draft. No distribution, enrichment or fresh scraping occurs in the repository replay. HeyReach trial is expired. Mentic and Surfer adapters remain documented, unconnected interfaces. A local replay is not evidence that all external tools are connected.

## Structure

| Path | Role |
|---|---|
| `tenders/UT-xxx/tender.json` | Canonical tender facts, evidence and qualification gaps |
| `tenders/UT-xxx/delivery-options/` | Proposed team, roles, interfaces and unresolved gates |
| `tenders/UT-xxx/actors/CONTACT-xx/` | Actor-specific offer, email and LinkedIn drafts |
| `partners/<company>/company.json` | Canonical company dossier |
| `partners/<company>/contacts/` | Professional identity and remit, without direct email |
| `content/blog/` | Editorial drafts |
| `executions/YYYY-Www/` | Actual run history by ISO week |
| `integrations/` | Retained provider contracts, Attio mapping and credit guard |
| `scripts/` | Validation, execution logging and dashboard projection |
| `dist/` | Static dashboard and generated `data.json`; not a second source of truth |

## Run locally

Python 3 standard library and Node are sufficient. From the repository root:

```sh
python scripts/record_execution.py
node --check dist/app.js
python -m http.server 8080 --directory dist
```

Open `http://localhost:8080`. The dashboard refreshes its projection every 30 seconds. Canonical file changes become visible after `python scripts/build_dashboard.py`; hosted changes require redeployment or the GitHub Pages workflow.

## Publish to your public GitHub repository

Repository: https://github.com/az2kxx/gtmtechweek . The source is authorized for direct commits and pushes. Start with [HANDOVER.md](HANDOVER.md) and [AGENTS.md](AGENTS.md) when continuing with another agent.

Public dashboard: https://gtmtechweek-tender-observatory.adrian-k-zebrowski.chatgpt.site . Its Diagnostics tab inspects run records, current Actions status and outstanding readiness gaps. It refreshes the GitHub data projection every 30 seconds with a clearly labeled hosted fallback.

The prepared workflow runs each Monday at 22:57 UTC and on manual dispatch/source changes. It validates and commits a real replay record and generated dashboard data. It does not call paid services. The existing ChatGPT weekly research task is separate and remains enabled; after the remote is available, fresh research can be written into canonical files using the connected GitHub tools. Do not treat the two schedules as two enrichment budgets for the same flow.

For GitHub Pages: choose **Settings → Pages → GitHub Actions**, then set the repository variable `ENABLE_GITHUB_PAGES=true`. Until enabled, the workflow only records runs and uploads the static artifact. Branch protection or missing Actions write permission can block commits and must be resolved in the repository. Check current Actions evidence in the diagnostics GUI; Pages deployment remains optional.

GitHub cron execution can be delayed. Public-repository schedules may be disabled after 60 days without repository activity. Check run records, not just the presence of a cron expression.

## Reading the demo honestly

The first week contains an actual local input/draft validation run. Future weeks display **not run** until an execution record exists. A completed replay means local inputs and draft coverage validated; it does not mean a buyer was scraped again, an email was verified, a partner consented or a message was delivered.

Tender and partner views show the current repository snapshot. The week selector filters execution history; it does not pretend to reconstruct historical company data. To inspect an older research state, use the Git commit associated with that run.

The E2E route does not require two companies. A consortium route needs a complementary scope and a credible lead contractor. Technical fit, eligibility, capacity, willingness and mutual introduction consent are separate facts.

## Attio stays intact

Existing Attio records, notes, integration and permissions are unchanged. The public repo stores professional identity only. Keep any private record-ID mapping and direct business emails in `.private/` or a secret-backed runtime, never in the public commit. `integrations/attio.md` explains upsert ownership and the optional mirror contract. Replay does not write to Attio.

## Cost control

The retained guard caps a logical execution at 299 Clay DATA credits, including branches and resumes. The PoC uses cached inputs and makes no Clay calls. Real calls need known cost bounds and the shared durable reservation ledger; otherwise remain cache-only. Media budgets are independent and no paid advertising is enabled.

## Maintenance and public data

Run `python scripts/validate.py` before publication. It validates associations and four-followup coverage and rejects direct emails/private UUIDs in public data. No credentials, raw enrichment exports or XLSX backfill are included. Professional profiles are research candidates, not endorsements or confirmed participants; remove or correct outdated records through normal commits.

## Sources and implementation references

- Tender source URLs and evidence dates are included in each dossier; this repo republishes summaries, not tender-document copies.
- [GitHub Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [GitHub scheduled workflow behavior](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)
- [Surfer MCP beta](https://surferseo.com/updates/surfer-mcp-august2026/)
- [HeyReach MCP setup](https://help.heyreach.io/en/articles/12117291-how-does-heyreach-mcp-work-with-popular-tools)
- [Mentic](https://www.mentic.io/)

Public visibility does not imply a software or data license. No broad reuse license is assigned to third-party professional data by this demo.
