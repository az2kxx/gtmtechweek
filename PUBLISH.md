# Publish this ZIP to az2kxx/gtmtechweek

The user authorized manual publication. No GitHub source upload was completed by the agent: the integration returned HTTP 403. The export is complete and contains dotfolders such as `.github/` and `.openai/`; preserve them when extracting.

## Using your CLI

Requires Git, an authenticated GitHub account with repository write permission, Python 3.12+ and Node 20+. The project itself has no pip/npm dependencies. Authenticate using your normal GitHub method; do not put tokens into files or command examples.

Clone the existing remote first to preserve its history. Substitute the actual downloaded ZIP path:

```sh
git clone https://github.com/az2kxx/gtmtechweek.git
python -m zipfile -e /absolute/path/gtmtechweek-poc.zip .
cd gtmtechweek
python scripts/checkup.py
git status --short
git add .
git commit -m "Publish documented tender PoC and validation evidence"
git push origin main
```

The ZIP has one top-level `gtmtechweek/` directory, so extraction in the clone's parent overlays the clone without replacing `.git`. Review any newer remote files before overlaying an existing working checkout. If main changed while you worked, fetch and reconcile those changes before pushing; do not force push. If Git requests an author identity, configure your own identity locally in this checkout.

## Confirm the first execution

Open https://github.com/az2kxx/gtmtechweek/actions . The push should trigger **Weekly tender demo**. Confirm the replay job succeeded and committed a run JSON and `dist/data.json`. Run artifact upload happens even if branch persistence fails. If a run is absent, enable Actions in repository settings; if its write fails, inspect the job log and repository workflow permissions/branch rules.

The Monday cron validates cached data only. It does not inherit ChatGPT MCP connections or execute fresh research. The separate ChatGPT research schedule remains in the owner's account and is not portable simply by copying this repository.

Once publication and its run succeed, update `config/readiness.json` with observed evidence for GitHub and its replay schedule, run `python scripts/build_dashboard.py`, and commit that update. Leave fresh research and live-tool gaps unresolved until separately tested.

## Dashboard

Local: `python -m http.server 8080 --directory dist` then open http://localhost:8080 . For an explicit local-data inspection, use http://localhost:8080/?local=1 . The hosted dashboard remains public. It prefers `main/dist/data.json` from this GitHub repo and falls back to hosted data if unavailable, displaying the source. UI changes in this ZIP require a dashboard redeployment; GitHub data commits alone do not update UI code.

For optional GitHub Pages hosting, choose Settings → Pages → GitHub Actions and set the repository variable `ENABLE_GITHUB_PAGES=true`; dispatch the workflow. The Sites manifest identifies the existing owner-authorized Site and is not needed for Pages. For Sites continuation use HANDOVER.md; do not create another Site.

## Beyond the PoC

A live execution host must implement and authenticate the provider dispatcher, share durable state and the Clay ledger, and prove retries/idempotency. Attio private IDs/emails must be retrieved from the owner account, never from this public ZIP. Keep distribution disabled until sender, suppression, eligibility and reply handling are validated and sending is authorized.
