# Daily Cycle Contract

Use the repository runbook as the canonical source:

```text
VK/auto_funnel/docs/operations/daily-cycle.md
VK/auto_funnel/state/operations/daily_cycle_context.json
```

Director responsibilities after a runner cycle:

- read fresh state, ledger, account plans, TOML registry, chat history and source-list state;
- detect account health blocks before proposing any API activity;
- update code/config/tests/docs/state when the pipeline exposes a concrete gap;
- write per-account `api_direct_plan.json` updates only for safe next actions;
- keep cross-profile message deduplication strict;
- record director history in `state/continuous_improvement/autofunnel-api-director`.

The automation prompt should stay short and link to the repository runbook instead
of duplicating this contract.

