# PoC checkup report

Checked: 2026-09-29T00:14:13.368309+00:00

Result: **PASS for offline PoC checks**. This is not end-to-end production certification.

- PASS: Public data and four-followup validation
- PASS: Six budget, concurrency, resume and channel guard tests
- PASS: Dashboard JavaScript syntax
- PASS: Actual local replay and projection
- PASS: All seven views and empty-week diagnostics
- PASS: Injected projection failure retains FAILED run and nonzero exit
- PASS: Handover, judge guide and workflow files present

The offline checkup itself made no external provider, paid-enrichment or distribution calls. The associated W40 run separately verified 26 Attio note write/read-backs, GitHub fast-forward publication and two successful cached replay Actions; those are recorded in `executions/2026-W40/run.json`. Six guard tests are included within the check groups. Raw output: `qa/checks.json`. Reproduce: `python scripts/checkup.py`.

Verified outside the offline checkup:

- PASS: GitHub research commit `a7800f2d81a174259980b017b4720c7d3b908a3c` fast-forwarded and canonical read-backs matched.
- PASS: Push-triggered cached replay runs `36502456313` and `36502746014` completed successfully. They validate cached artifacts, not fresh collection.
- PASS: Attio W40 notes were read back without resetting relationship state.

Not verified:

- Scheduled fresh research completion
- Live MCP adapter round trips
- Deliverability or distribution
- Browser interactions / mobile layout
- Tender eligibility and partner willingness
