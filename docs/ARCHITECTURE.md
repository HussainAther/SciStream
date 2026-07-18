# Architecture

## Overview

SciStream is a server-rendered Django application with a small progressive JavaScript layer. The design deliberately keeps the hackathon flow in one deployable process.

```text
templates/streams/index.html  Product structure and accessible controls
static/streams/app.css        Responsive visual system
static/streams/app.js         Local session state and interaction orchestration
streams/views.py              Validated JSON boundary
streams/services/execution.py Deterministic scientific demo executor
streams/services/ai.py        Provider interface, mock provider, optional hosted provider
```

## Request flow

1. Django serves the landing page, setup dialog, and hidden room shell.
2. The browser holds temporary session state: metadata, code, output, questions, and explanations.
3. Running the cell posts only the code to `/api/execute/`. The execution service recognizes the bundled exponential-decay example and returns fixed calculations and chart points. It never calls `eval`, `exec`, or a shell.
4. An AI action posts a bounded context object to `/api/assistant/`. The provider factory selects deterministic mock mode by default. Optional hosted mode sends only title, goal, capped code/output, and latest question.
5. Summary generation posts the captured session artifacts to `/api/summary/`, which validates sizes and returns Markdown. Copy and download happen in the browser.

## Security and trust boundaries

- Arbitrary Python execution is intentionally unsupported.
- JSON inputs are type-checked, required strings are validated, and length limits are applied at the server boundary.
- Django CSRF middleware protects POST endpoints used by the browser.
- Secrets are read only from environment variables and `.env` is ignored.
- The generated summary is returned as JSON and placed into a textarea with `.value`, avoiding HTML interpretation.
- Production deployment still requires a strong `SECRET_KEY`, `DEBUG=False`, TLS, hardened allowed hosts, rate limiting, and provider monitoring.

## Why browser-local session state

Persistence is unnecessary for the judging path and would require lifecycle, privacy, and migration decisions beyond the prototype. The existing SQLite models are retained for future room records, but no claim is made that the hackathon session is durable.

## Future production path

A production implementation can replace interfaces independently: an isolated Jupyter gateway behind the executor, authenticated room/event storage behind the browser state, WebSockets for chat/presence, and WebRTC for host media. The current provider boundary also allows different AI vendors or an on-premises model.
