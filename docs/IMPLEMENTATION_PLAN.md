# Implementation Plan

## Baseline assessment

The repository began as a Django 4.2 scaffold with SQLite, `Stream` and `StreamKey` models, partial stream views, an undeclared Django Channels consumer, and a standalone WebXR cube template. Two competing settings/URL trees meant the tracked application exposed only Django admin; `/` rendered Django’s default install page. There were no discovered tests, migration for the stream models, wired product workflow, AI service, or accurate setup instructions.

## Smallest realistic hackathon scope

Build one understandable, local-first path: landing/setup → research room → deterministic scientific cell → visible output → participant question → scoped mock AI explanation → downloadable Markdown summary.

Real video, arbitrary kernels, multi-user sockets, authentication, and persistent rooms are explicitly excluded because each adds failure modes without improving the three-minute story.

## Vertical slices

1. **Application baseline** — unify the active Django configuration, connect routes/templates/static files, and replace the default install page.
2. **Research room** — collect session metadata and expose the host-share substitute, notebook cell, output, chat, AI, and timeline in one responsive view.
3. **Execution and assistance** — add the constrained decay experiment and provider-isolated AI actions, with deterministic mock mode as the default.
4. **Session artifact** — validate captured context and generate copyable/downloadable Markdown with every required section.
5. **Reliability** — add migration, environment example, error states, tests, one-command setup, and accurate docs.

## Acceptance criteria

- A judge can complete the full flow in under three minutes without credentials.
- Unsupported code fails with an honest, recoverable message.
- AI receives only bounded session context and has a deterministic fallback.
- Summary output contains title, goal, code, outputs, questions, explanations, conclusions, and next steps.
- All documented test and run commands execute successfully.
