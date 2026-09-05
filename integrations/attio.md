# Attio optional mirror

The repo is the PoC SSOT for research, delivery hypotheses and drafts. Attio retains live relationship history and private contact data. Existing records are preserved; no deletion, disconnection or permission change is part of this demo.

## Upsert contract

1. Read attribute definitions before writes. Resolve companies by normalized domain; people by existing record mapping, normalized LinkedIn profile or already-known business email. On ambiguous identity, queue review rather than create.
2. Patch research fields only: evidence date, source links, remit confidence, capabilities, tender associations and draft versions. Never overwrite replies, opt-outs, manual changes or introduction consent with initial snapshot defaults.
3. Missing pairs are persisted with a reason and next-review date. A single E2E-capable company does not require a counterpart.
4. Read back successful writes. Retry transient errors at most twice. After an uncertain write, read before retrying creation.
5. Store multiple tender/partner associations separately. Where custom objects are unavailable, use versioned project notes. Native schema expansion is not automatically provisioned.

## Private runtime boundary

Use `.private/attio-map.json` for a local map from public company/contact IDs to actual Attio record IDs, if needed. This path is ignored and must not be published. Direct emails and credentials also remain outside public data. Do not log them in GitHub Actions.

The existing ChatGPT Attio plugin handles actual writes. GitHub Actions does not magically inherit an MCP connection. The included repository replay makes no Attio calls. To automate mirroring from a different host, connect its account using documented credentials, discover actual schemas and test a research-only upsert while verifying history preservation.
