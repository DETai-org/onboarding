---
name: log-summary
description: Create, update, or close a compact daily log-summary in the owning project's ClickUp List `logs`. Use for a requested log summary, daily recap, mini-report, «на сегодня хватит», «подведём итоги», or a consequential completed checkpoint. Use project-local routing first, write a separate linked entry for each materially affected neighboring project, and never create a local Markdown log-summary.
---

# Log Summary

Keep one compact, portable record of what actually changed in one project
container during a Moscow working date. A `log-summary` is historical evidence,
not a plan, machine inventory, or second source of truth.

## Resolve The Owning Container

1. Read the active project's `AGENTS.md` and use its `log_summary` route first:

   ```yaml
   log_summary:
     list_id: <ClickUp logs List ID>
     scope: <registered scope>
     context: <registered single context>
     navigation_key: <project key in the shared map>
     global_navigation: D:\dev\DETai-org\Management_Layer\docs\clickup-navigation\index.yaml
   ```

2. Treat `scope` as the registered area and `context` as the single concrete
   project, tool, or operational container. Do not put several contexts in one
   record.
3. Use `global_navigation` only when completed work materially changed a
   neighboring project and its local route is not already known. Resolve only
   the required neighbor by `navigation_key`; do not crawl all ClickUp.
4. For a real cross-project result, update each affected project's own daily
   record with only its local consequence. Add reciprocal links under
   `Связанные логи`; do not paste the same report into several containers.
5. Before a neighbor write, live-check that the resolved target is the List
   `logs` inside the expected Folder. Treat the shared map as navigation, not
   as proof that stale external state is still correct.
6. Keep classification out of the global navigation map. Project `scope` and
   `context` are local cached defaults governed by the metadata schema registry.
7. If a required route remains unknown or inaccessible, report the missing
   List ID. Never substitute a local `*log-summary.md`.
8. When a new workspace has no project-local route yet, follow the team setup
   tutorial: <https://github.com/DETai-org/onboarding/issues/32>. Do not turn a
   whole-Workspace scan into the normal logging procedure.

## Identify The Daily Record

1. Determine the working date in `Europe/Moscow`.
   - Use the Moscow calendar date by default.
   - Between `00:00` and `03:59`, retain the previous date only when the
     conversation clearly continues that previous day's session.
   - An explicit user-supplied date wins.
2. In the resolved List, find `Logs DD.MM.YYYY`. There is exactly one task per
   Folder and working date. Create it only when absent; otherwise update it.
3. Request existing content with `include_markdown_description=true` when using
   the ClickUp API.
4. Create or update task content through `markdown_description`, not the plain
   `description` field.

## Resolve Provenance

Read `~/.codex/detai-user.yaml`. Accept only this confirmed local profile:

```yaml
schema: detai-local-user-profile
version: 1
identity:
  person_id: github-user-<numeric-github-id>
  display_name: <confirmed display name>
  github_username: <GitHub login>
  clickup_username: <matching ClickUp username>
  clickup_user_id: <numeric ClickUp user ID>
```

- Never infer identity from the OpenAI profile, Windows username, or prose in
  the conversation.
- Treat GitHub numeric user ID as stable `person_id`; use GitHub login as the
  team username and cross-check it against ClickUp without case sensitivity.
- If the profile is absent or the usernames conflict, stop identity resolution
  and use the onboarding tutorial and prompt to create or repair the profile.
- Never store tokens, passwords, email, cookies, or other secrets.

## Portable Metadata

Begin `markdown_description` with a fenced YAML block. Follow the canonical
`type: log-summary` contract and preserve valid creation values when updating.

````markdown
```yaml
---
type: log-summary
classification:
  scope: <registered scope>
  context: <registered single context>
  function: log-summary
descriptive:
  id: log-summary-<clickup-list-id>-<YYYY-MM-DD>
  date_ymd: <YYYY-MM-DD>
  status: draft
  created_at_msk: <YYYY-MM-DDTHH:MM:SS+03:00>
  updated_at_msk: <YYYY-MM-DDTHH:MM:SS+03:00>
provenance:
  performed_by:
    person_id: <profile identity.person_id>
    display_name: <profile identity.display_name>
    github_username: <profile identity.github_username>
    clickup_username: <profile identity.clickup_username>
  recorded_by: Codex
links:
  related_logs: []
---
```
````

After the metadata block, show only `@<clickup_username>` on its own line. Do
not prefix it with `Участник:`.

## Write Checkpoints And Close Deliberately

Write a checkpoint only after a completed result, decision, handoff, or
unresolved blocker would otherwise be lost.

- Add the smallest useful chronological block, normally one to three bullets.
- Link the owning artifact, task, verification, or related project log.
- Keep technical specifications, raw output, and inventories in their owning
  reference; link them instead of copying them.
- Do not create a log merely because time passed or work is still planned.

Treat «на сегодня хватит», «закрываем день», «подведём итоги», or equivalent
language as finalization. Consolidate duplicates, add one daily outcome, and
change `status` to `final`. Do not infer closure from the clock alone.

## Compact Description Shape

````markdown
<fenced metadata block>

@<clickup_username>

Контур: <context>

## Ход работы

### <HH:MM> — <короткое действие>
- <проверяемый результат>
- <ссылка на owning artifact или проверку>

## Связанные логи
- <ссылка на лог соседнего контейнера, только если он реально затронут>

## Открыто
- <фактический gate или blocker>

## Итог дня
<одно предложение>

🎯 **КВЦ дня достигнута:** `<одно короткое утверждение>`
````

Omit empty sections. At an ordinary checkpoint omit `Итог дня`, keep
`status: draft`, and do not add KVC.

## Prompt Resources

- Read [`references/mini-report-prompt.md`](references/mini-report-prompt.md)
  for a terse checkpoint or requested mini-report.
- Read [`references/daily-summary-prompt.md`](references/daily-summary-prompt.md)
  only for an explicitly requested end-of-day narrative or KVC framing.

Prompts are editable resources. Routing, one-task-per-date, metadata,
provenance, compactness, cross-project separation, and no-local-log rules in
this file remain authoritative.
