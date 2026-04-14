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

## 2026-04-09 - Do not scale the whole key battles widget to fit 500px
- Context: Making `key-battles-widget.html` use the full iframe width on embedded LP pages.
- Command/workflow: Fixed-height widget fitting logic in `fitWidgetToViewport()`.
- Failed approach: Scaled `#widgetScaleRoot` down with `transform: scale(...)` whenever the natural height exceeded `500px`.
- Symptom: The iframe itself was full width, but the live card rail shrank to a visibly narrower width because the whole widget was being transformed.
- Working approach: Keep the viewport fixed at `500px`, remove the root scale transform, and tighten internal spacing so the layout fits naturally.
- Next-time rule: For fixed-height embeds, do not solve overflow by scaling the full widget root; reduce internal spacing or restructure the layout so the content keeps its true width.

## 2026-04-09 - Rename wrapper selectors safely when UI spacing classes change
- Context: `key-battles-widget.html` got stuck on the loader after the search wrapper spacing class was changed.
- Command/workflow: Loader hide/show logic for the search shell.
- Failed approach: Continued using `searchEl.closest('.mb-5')` after the wrapper class was changed to `mb-3`.
- Symptom: The script threw `Cannot read properties of null (reading 'style')` during startup, so `widget-loading` was never cleared and the page stayed on the loader.
- Working approach: Give the wrapper a stable `id` (`search-shell`) and reference it directly with a null-safe check.
- Next-time rule: Do not couple JS behavior to utility spacing classes; use stable IDs or data attributes for elements the script needs to show or hide.

## 2026-04-10 - Verify web app endpoints with elevated curl and quoted URLs
- Context: Checking whether an Apps Script deployment supported the new `multiValues` action.
- Command/workflow: Network verification with `curl.exe` from PowerShell.
- Failed approach: Ran `curl` inside the sandbox and also passed URLs containing `&` without robust command quoting.
- Symptom: Requests either failed at the network layer or produced misleading empty/sign-in responses, making it unclear whether the deployment was actually serving the new code.
- Working approach: Run `curl.exe` with elevated permissions and pass the full URL as a single quoted `--url` argument.
- Next-time rule: For external endpoint verification in this repo, use elevated `curl.exe` and quote the entire URL explicitly so query params are not reinterpreted by PowerShell.

## 2026-04-13 - Use the exact workspace root in `apply_patch` targets
- Context: Cleaning up non-legacy source paths after switching the widgets to CloudFront-only mode.
- Command/workflow: Manual file edits with `apply_patch`.
- Failed approach: Used an absolute path that omitted the `Claude\Experiments` segment of the workspace root.
- Symptom: `apply_patch` failed with a file-not-found error even though the file existed in the repo.
- Working approach: Re-run `apply_patch` with the full absolute path under `C:\Users\suhas.bhandari\Downloads\Claude\Experiments\CMS Widgets\Elections`.
- Next-time rule: When patching by absolute path in this repo, copy the full `cwd` prefix exactly from the environment context before editing.

## 2026-04-14 - Use the real Python interpreter for detached local hosting
- Context: Starting the repo-root HTTP server for browser QA.
- Command/workflow: Detached local hosting with `Start-Process`.
- Failed approach: Launched `Start-Process` with `C:\Users\suhas.bhandari\.local\bin\py.cmd` and `-3 -m http.server ...`.
- Symptom: `Start-Process` returned a PID, but the process exited immediately and Playwright hit `ERR_CONNECTION_REFUSED`.
- Working approach: Launch `Start-Process` with `C:\Users\suhas.bhandari\AppData\Local\Programs\Python\Python312\python.exe -m http.server 8000 --bind 127.0.0.1`.
- Next-time rule: For detached local servers in this repo, do not use `py.cmd` as a launcher; use the real Python executable with escalated permissions.
