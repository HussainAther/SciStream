# SciStream

**Live collaborative research sessions with code, discussion, and AI-generated documentation.**

SciStream is a focused hackathon prototype for scientists, programmers, educators, and students who want to show not only a result, but the live reasoning that produced it.

Devpost link: https://devpost.com/software/scistream
## The problem

Code repositories are excellent records after work is complete. Video calls and streams help while work is happening, but usually separate the code, questions, explanations, and decisions. SciStream combines those artifacts in one notebook-inspired research room and turns the session into a reusable Markdown record.

## Implemented demo workflow

1. Open the landing page and select **Start research session**.
2. Enter a title and research question; choose the Python notebook demo.
3. Run the bundled exponential-decay experiment.
4. Inspect textual output and a generated decay chart.
5. Add a participant question in local chat.
6. Ask SciStream AI to explain the code, summarize the output, answer the latest question, or suggest a next experiment.
7. Generate, copy, or download a Markdown session summary.

Every step works without external credentials. The demo executor is deterministic and intentionally accepts only the bundled experiment. Chat, the host share, and participants are local UI abstractions rather than real multi-user/video infrastructure.

## Quick start

Requires Python 3.10 or newer.

```bash
./scripts/run_demo.sh
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000). The script creates `.venv`, installs Django, applies migrations, and starts the demo.

Manual setup:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scistream/manage.py migrate
.venv/bin/python scistream/manage.py runserver
```

## Configuration

Copy `.env.example` values into your shell or a local environment loader. Django does not load `.env` files automatically.

| Variable | Default | Purpose |
| --- | --- | --- |
| `SCISTREAM_AI_MODE` | `mock` | `mock` for the deterministic demo or `openai` for the optional hosted provider |
| `OPENAI_API_KEY` | empty | Required only when `SCISTREAM_AI_MODE=openai` |
| `OPENAI_MODEL` | `gpt-4.1-mini` | Model name passed to the optional provider |
| `SECRET_KEY` | local demo value | Django signing key; replace outside local development |
| `DEBUG` | `True` | Django debug mode |
| `ALLOWED_HOSTS` | `127.0.0.1,localhost` | Comma-separated Django hosts |

If hosted AI is unavailable, set `SCISTREAM_AI_MODE=mock` and restart. Relevant context is capped and limited to the session title, goal, code, output, and latest question.

## Architecture

```text
Browser (Django template + CSS + JavaScript)
  ├── POST /api/execute/   → constrained deterministic Python service
  ├── POST /api/assistant/ → mock or optional hosted AI provider
  └── POST /api/summary/   → validated Markdown generator
```

Django 4.2 serves the interface and JSON endpoints. SQLite is retained for the pre-existing stream models, though the hackathon flow keeps its temporary session state in the browser. See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for boundaries and design decisions.

## Testing

```bash
.venv/bin/python scistream/manage.py check
.venv/bin/python scistream/manage.py test streams
```

The tests cover the landing page, supported/unsupported execution, all mock AI actions, input errors, and every required summary section.

Optional formatting/lint configuration is included in `pyproject.toml` for Ruff and Black; these tools are not required to run the demo and are not added as runtime dependencies.

## Screenshots

No screenshots are committed yet. Capture them after starting the demo:

1. **Landing:** 1440 × 1000 at `/`, with the headline and room preview visible. Save as `docs/screenshots/landing.png`.
2. **Research room:** open the sample session, run the cell, and request **Summarize output**. Capture the notebook, chart, chat, and assistant at 1440 × 1100. Save as `docs/screenshots/research-room.png`.
3. **Summary:** select **Generate summary** and capture the Markdown dialog at 1200 × 900. Save as `docs/screenshots/summary.png`.

## Known limitations

- The host video/screen share is a labeled local visual substitute.
- Code execution is a deterministic simulation of the bundled decay experiment, not an arbitrary Python or Jupyter kernel.
- Chat and participant presence are local to one browser; there are no WebSockets or rooms.
- Session state is not persisted after a refresh.
- The hosted AI provider is optional and not exercised by the credential-free test suite.
- There is no authentication, authorization, deployment hardening, or production monitoring.

## Roadmap

- Isolated Jupyter kernels with resource and package controls.
- Real rooms using authenticated WebSockets and persisted session events.
- WebRTC screen sharing after the collaborative notebook is proven useful.
- Export to `.ipynb`, GitHub issues, and laboratory knowledge bases.
- Citations, data provenance, and human approval controls for AI-generated conclusions.

## Built During the Hackathon

### Pre-existing repository work

- Django project scaffold and SQLite database.
- Initial `Stream` and `StreamKey` models.
- Partial, disconnected stream API and Channels experiments.
- Standalone WebXR cube proof of concept and placeholder README.

### Added during this development sprint

- Unified, working Django configuration and routes.
- Purpose-built landing page and notebook-inspired research room.
- Session setup, deterministic scientific code demo, output visualization, local chat, activity timeline, and summary export.
- Context-limited AI provider interface, deterministic mock mode, and optional hosted provider.
- Input validation, useful error responses, migrations, environment example, one-command setup, and automated workflow tests.
- Accurate architecture, implementation, demo, submission, and judging documentation.

## Three-minute demo script

**0:00–0:25** — State the problem on the landing page: repositories preserve final code; meetings lose live reasoning.  
**0:25–0:45** — Start “Protein Decay Analysis” and show the research goal.  
**0:45–1:20** — Run the sample cell and point to the reproducible output and chart.  
**1:20–1:55** — Add “Why does the rate slow over time?” to chat and ask AI to answer the latest question.  
**1:55–2:30** — Ask for the next experiment, then generate the Markdown summary.  
**2:30–3:00** — Download the record and clearly name the prototype boundaries: local host-share substitute, deterministic kernel, and mock AI fallback.

The expanded script is in [`docs/DEMO_SCRIPT.md`](docs/DEMO_SCRIPT.md).

## Submission description

SciStream is a live research room that brings a notebook, participant questions, contextual AI explanations, and automatic documentation into one focused workflow. In the credential-free demo, a host opens a session, runs a reproducible scientific experiment, answers audience questions with a context-limited AI assistant, and downloads a Markdown record of the code, outputs, discussion, conclusions, and next steps. It is an honest local prototype of collaborative research while it is happening—not a claim to be production video or Jupyter infrastructure.

See [`docs/HACKATHON_SUBMISSION.md`](docs/HACKATHON_SUBMISSION.md) for submission-ready copy.
