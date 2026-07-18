# Judging Checklist

Run this checklist from a fresh clone or extracted repository.

## Startup and configuration

- [ ] `./scripts/run_demo.sh` creates the environment, installs dependencies, migrates, and starts the project.
- [ ] `http://127.0.0.1:8000` opens the SciStream landing page rather than Django’s default page.
- [ ] `.env.example` documents every supported variable.
- [ ] `SCISTREAM_AI_MODE=mock` works without external credentials or network access after dependencies are installed.
- [ ] `.env`, virtual environments, Python caches, and collected static files are ignored.
- [ ] Repository search finds no committed API keys, passwords, or production secrets.

## Core session flow

- [ ] **Start research session** opens the setup dialog.
- [ ] Empty title or research question is blocked with a useful error.
- [ ] The seeded Python session opens the research room.
- [ ] Host share is visibly labeled as a local demo substitute.
- [ ] **Run cell** displays deterministic textual output, a chart, and an important result.
- [ ] Unsupported code shows a recoverable message; **Reset sample** restores the demo.
- [ ] Chat accepts and displays a participant question.
- [ ] All four AI controls return a useful response in mock mode.
- [ ] The assistant indicates its operating mode and context boundary.
- [ ] The activity timeline records the major actions.
- [ ] **Generate summary** creates every required Markdown section.
- [ ] Copy and download summary controls work.
- [ ] No visible button is inert.

## Quality checks

- [ ] `.venv/bin/python scistream/manage.py check` passes.
- [ ] `.venv/bin/python scistream/manage.py test streams` passes all tests.
- [ ] The landing page and room remain usable at desktop, tablet, and narrow mobile widths.
- [ ] Keyboard focus is visible and dialogs/inputs have accessible labels.
- [ ] Browser console shows no obvious errors during the judging path.
- [ ] README commands were rerun exactly as written.
- [ ] README limitations match actual implementation boundaries.
- [ ] Claims avoid real-time video, arbitrary Jupyter, multi-user chat, or production-readiness language.

## Submission readiness

- [ ] Capture landing, research room, and summary screenshots using README instructions.
- [ ] Rehearse `docs/DEMO_SCRIPT.md` under three minutes.
- [ ] Verify `docs/HACKATHON_SUBMISSION.md` matches the current build.
