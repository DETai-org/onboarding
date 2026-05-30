# Raw Markdown source checklist

Use this checklist before running `publish-clickup-doc-version.ps1`.

## Goal

The raw Markdown source should represent the intended editorial change, not a
new formatting pass over the whole document.

If only one paragraph changed, the raw source should differ from the canonical
file by that paragraph plus required metadata only.

## Preparation

1. Start from the baseline Markdown file, not from ClickUp plain text.
2. Copy the ready-for-publication editorial changes into that baseline.
3. Preserve unchanged Markdown exactly where possible.
4. Keep the existing canonical path and MkDocs URL.
5. Set the new `descriptive.version`.
6. Leave `descriptive.status: draft`; the publish script turns it into
   `active` in the preview/apply step.

## Avoid accidental rewrites

Do not do these during publication:

- rewrap paragraphs;
- renumber headings for style only;
- add language hints to unchanged code fences;
- convert lists to tables unless the content change requires it;
- remove old trailing Markdown line-break spaces across the whole file;
- change all heading levels for visual neatness;
- normalize all links from old style to new style.

Those are valid cleanup tasks, but they belong in a separate normalization PR.

## Dry-run decision

After dry-run, inspect `diff_gate`.

For ordinary updates:

- `status` should be `ok`;
- changed lines should be close to the actual editorial change;
- `formatting_noise_lines` should be low.

For major version rewrites:

- `status: large-diff` can be acceptable;
- the reviewer must confirm that the large diff is real content change;
- use `-AllowLargeDiff` only after that confirmation.

## Manual comparison against ClickUp

Because ClickUp may normalize Markdown, compare meaning rather than raw syntax:

- same title;
- same version;
- same section order;
- all ready task paragraphs are represented;
- no baseline-only paragraphs survive by accident;
- links are upgraded only when intentional;
- tables/lists preserve the same cells/items as the ready task.
