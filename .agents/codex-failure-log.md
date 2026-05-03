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

## 2026-04-14 - Do not chain git commands with `&&` in this PowerShell environment
- Context: Staging and committing repo changes from the Codex shell.
- Command/workflow: Git staging and commit commands in PowerShell.
- Failed approach: Ran combined commands like `git add ... && git commit -m ...`.
- Symptom: PowerShell rejected `&&` with `The token '&&' is not a valid statement separator in this version.`
- Working approach: Run git commands as separate shell invocations.
- Next-time rule: In this repo's PowerShell environment, do not chain commands with `&&`; execute sequential git commands separately.

## 2026-04-14 - Do not call `parseNumber` before its declaration in `map-widget.html`
- Context: Adding default auto-refresh wiring near the top-level query-param constants in `map-widget.html`.
- Command/workflow: Manual refresh-config edit with `apply_patch`.
- Failed approach: Computed `REFRESH_MS` with `parseNumber(...)` before the helper was defined later in the file.
- Symptom: The widget stayed on the loader with `ReferenceError: parseNumber is not defined`.
- Working approach: Use `Number(...)` directly in the early `REFRESH_MS` initializer.
- Next-time rule: In `map-widget.html`, top-level constants declared before helper functions must not rely on later function declarations.

## 2026-04-14 - Avoid the WindowsApps `python.exe` alias for local generation tasks
- Context: Regenerating `graphify-corpus/graphify-out/*` before committing widget tab-name changes.
- Command/workflow: Inline Python generation from PowerShell.
- Failed approach: Piped the script into `python -`, which resolved to `C:\Users\suhas.bhandari\AppData\Local\Microsoft\WindowsApps\python.exe`.
- Symptom: The shell failed with `Program 'python.exe' failed to run: The file cannot be accessed by the system`.
- Working approach: Run the script with `C:\Users\suhas.bhandari\AppData\Local\Programs\Python\Python312\python.exe -`.
- Next-time rule: In this repo, do not rely on the WindowsApps `python.exe` shim for local generation tasks; use the real Python 3.12 executable path.

## 2026-04-14 - Re-read the exact export-style block before patching lead-seat visuals
- Context: Removing the extra outline from leading seats in `seat-results-widget.html`.
- Command/workflow: Manual `apply_patch` edit spanning both live chart styling and the share/export clone CSS.
- Failed approach: Patched against an assumed lead-seat CSS block that no longer matched the current export-style text.
- Symptom: `apply_patch` failed with an expected-lines mismatch.
- Working approach: Read the exact surrounding lines for the clone CSS and seat render block, then patch against the current text.
- Next-time rule: When a visual treatment is implemented in both live rendering and export CSS, inspect both current blocks before applying a multi-hunk patch.

## 2026-04-20 - Re-read drifted graph corpus embed snippet before patching
- Context: Syncing the graph corpus copy of `home-special-events-seat-compact.html` with the root embed change.
- Command/workflow: `apply_patch` against `graphify-corpus/iframe embeds/home-special-events-seat-compact.html`.
- Failed approach: Reused the root-file patch context without re-reading the corpus copy.
- Symptom: `apply_patch` failed because the corpus file still pointed at `state=TAMIL_NADU` and had a different iframe line.
- Working approach: Re-read the exact corpus snippet, then patch against the current text.
- Next-time rule: When mirroring a change into graph-corpus copies, do not assume the snapshot matches the root file; inspect the corpus file first.

## 2026-04-20 - Compute widget height dynamically, not once at load
- Context: Adding a desktop 410px cap with a mobile 500px cap in `seat-results-widget.html`.
- Command/workflow: Desktop height cap and `fitWidgetToViewport()` scaling logic.
- Failed approach: Cached the embed max height in a top-level constant from `getComputedStyle(...)` during initial load.
- Symptom: The iframe could stay stuck at the old 500px inline height after resizing to desktop because the cached value did not update.
- Working approach: Read the current breakpoint in a helper (`window.matchMedia('(min-width: 768px)')`) each time `fitWidgetToViewport()` runs.
- Next-time rule: For responsive iframe sizing, compute breakpoint-dependent heights at render/resize time instead of caching them once at startup.

## 2026-04-24 - Use elevated git staging when index lock permission fails
- Context: Committing the state-tab persistence change in the election widgets.
- Command/workflow: `git add` for the modified widget files.
- Failed approach: Ran staging inside the sandbox without escalation.
- Symptom: `fatal: Unable to create .../.git/index.lock: Permission denied`.
- Working approach: Retry the git write operation with elevated permissions.
- Next-time rule: If `git add` or similar repo-write commands fail on `.git/index.lock`, rerun them with escalated permissions before changing strategy.

## 2026-04-24 - Use elevated git branch creation when ref lock permission fails
- Context: Starting a new branch for Assam pre-2023 SVG mapping work.
- Command/workflow: `git switch -c assam-pre2023-svg`.
- Failed approach: Created the branch inside the sandbox without escalation.
- Symptom: `Unable to create .../.git/refs/heads/...lock: Permission denied`.
- Working approach: Retry the branch-creation command with elevated permissions.
- Next-time rule: If branch creation or ref updates fail with a lock permission error, rerun the git command with escalation before trying a different branch name or workflow.

## 2026-04-24 - Graphify update does not rebuild this HTML widget corpus
- Context: Refreshing graph snapshots after changing `map-widget.html` Assam geometry behavior.
- Command/workflow: `graphify update graphify-corpus`.
- Failed approach: Tried to use the local graphify CLI update path as if it would rebuild the widget corpus from the mirrored HTML files.
- Symptom: The CLI reported `No code files found - nothing to rebuild`, so the graph snapshot did not refresh.
- Working approach: Use `scripts/sync_graphify_corpus.py` to mirror the root widget files into `graphify-corpus/` first; do not rely on `graphify update` for this repo's HTML widget snapshot.
- Next-time rule: For widget behavior changes in this repo, sync the corpus with `scripts/sync_graphify_corpus.py` and expect `graphify update` to skip HTML-only widget files.

## 2026-04-28 - Move binary map assets with filesystem commands
- Context: Consolidating unused geometry files into one folder under `root/`.
- Command/workflow: `apply_patch` move attempt for `*.geojson` assets.
- Failed approach: Tried to move the geometry files with a multi-file patch hunk.
- Symptom: `apply_patch` rejected the hunk as empty for the source file and did not move the assets.
- Working approach: Create the destination folder, then use `Move-Item -LiteralPath ... -Destination ...` for the asset files.
- Next-time rule: For bulk asset moves in this repo, use filesystem moves instead of `apply_patch` when the files are not being edited.

## 2026-04-29 - Patch widgets one file at a time when blocks differ
- Context: Replacing map asset URLs in the election widgets.
- Command/workflow: Single `apply_patch` touching `map-widget.html`, `seat-results-widget.html`, and `key-battles-widget.html`.
- Failed approach: Used one multi-file patch assuming all three files had the same `STATE_MINI_MAP_SOURCES` block.
- Symptom: `apply_patch` failed on `key-battles-widget.html` because that file does not have the expected map source table.
- Working approach: Patch the files that actually contain the asset URLs, then verify whether the third widget needs any change at all.
- Next-time rule: For cross-widget constant updates, inspect each target file first and patch only the ones whose current structure matches.

## 2026-04-30 - Avoid nested PowerShell for generated embed files
- Context: Reorganizing `iframe embeds/` and generating the new `2-iframes/` state embeds from the `3-iframes/` templates.
- Command/workflow: Bulk file generation with a PowerShell regex replace.
- Failed approach: Piped a script into a nested `powershell -NoProfile -Command -` invocation from the Codex PowerShell shell.
- Symptom: The command exited without error, but the expected generated files did not appear under `iframe embeds/2-iframes/`.
- Working approach: Run the PowerShell script directly in the current shell session and verify the output files immediately after generation.
- Next-time rule: For bulk PowerShell file generation in this repo, do not nest a second `powershell -Command -`; run the script directly and confirm the created files.

## 2026-04-30 - Patch exact active blocks when wiring sheet-driven Kannada labels
- Context: Making `seat-results-widget.html` prefer sheet-driven Kannada party/alliance names over the hardcoded `NAME_KN` map.
- Command/workflow: Manual `apply_patch` around the name-translation helpers and yearwise data parser.
- Failed approach: Patched against an assumed return block for `buildDataFromYearwisePartyRows` that no longer matched the live file text.
- Symptom: `apply_patch` failed to find the expected lines even though the functions existed.
- Working approach: Re-read the exact live block around the parser and helper functions, then patch the current text in smaller hunks.
- Next-time rule: When adding sheet-driven translation plumbing, inspect the current helper and parser blocks immediately before patching instead of reusing stale context.

## 2026-05-04 - Assam CDN SVGs are not guaranteed to stay polygon-based
- Context: Fixing `map-widget-2026?state=ASSAM` after production started failing with `SVG parse failed: no valid polygons found`.
- Command/workflow: Assam keyed SVG parsing in `buildFeaturesFromKeyedSvg()`.
- Failed approach: Assumed the live Assam CDN assets would keep the same `<polygon>` structure as the checked-in source SVGs.
- Symptom: The live widget fetched successfully, but the parser found zero polygons because the CDN-served SVG had been optimized into keyed `<path>` elements.
- Working approach: Verify the live asset markup, then support both keyed `<polygon>` and keyed `<path>` geometry when building Assam features.
- Next-time rule: When a widget depends on externally hosted SVG markup, inspect the live asset format before relying on source-file structure; accept both polygon and path keyed shapes where feasible.

## 2026-05-04 - Do not assign to PowerShell `$PID` when stopping local helpers
- Context: Cleaning up the detached local HTTP server after browser QA for the election widgets.
- Command/workflow: PowerShell process-stop helper around `Stop-Process`.
- Failed approach: Used `$pid = <number>` as a temporary variable name before calling `Stop-Process`.
- Symptom: PowerShell rejected the assignment with `Cannot overwrite variable PID because it is read-only or constant.`
- Working approach: Use a different variable name such as `$targetPid`, and escalate the stop command if the helper was launched outside the sandbox.
- Next-time rule: In this PowerShell environment, never reuse `$PID` as a scratch variable; use a non-reserved name for process IDs.
