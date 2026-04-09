# Codex Failure Log

Use this file to store short lessons from failed attempts that later had a working fix.
This includes code changes, shell commands, search/read patterns, replace/edit attempts, Git workflows, browser-testing steps, and other Codex operating mistakes.

## Entry Template
- Context: ...
- Command/workflow: ...
- Failed approach: ...
- Symptom: ...
- Working approach: ...
- Next-time rule: ...

## 2026-04-09 - Compact table placeholders in seat results
- Context: Stabilizing `seat-results-widget.html?compact=1` so party and alliance views keep the same internal table height.
- Command/workflow: Compact table placeholder rows in `renderTable()`.
- Failed approach: Added placeholder rows with `tr.style.visibility = 'hidden'`.
- Symptom: Alliance mode still rendered a much shorter table area than party mode, so the internal layout shifted even though the outer widget height stayed fixed.
- Working approach: Keep placeholder rows in the DOM with a `placeholder-row` class and hide them with `opacity: 0` plus `pointer-events: none` so they still reserve row height.
- Next-time rule: For layout-stabilizing placeholder table rows, do not hide the `<tr>` with `visibility: hidden`; use transparent rows that preserve normal table sizing.

## 2026-04-09 - Patch against exact live markup before editing
- Context: Removing the visible title and description from `map-widget.html`.
- Command/workflow: `apply_patch` against a UI markup block.
- Failed approach: Patched against an assumed controls block shape without re-reading the exact current HTML.
- Symptom: `apply_patch` failed because the expected lines did not match the file.
- Working approach: Read the exact surrounding HTML/CSS block first, then patch against the current text.
- Next-time rule: When editing UI markup that has already changed in prior iterations, inspect the exact current snippet before applying a structural patch.
