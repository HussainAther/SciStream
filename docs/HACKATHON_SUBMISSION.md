# Hackathon Submission

## Project name

SciStream

## Tagline

Live collaborative research sessions with code, discussion, and AI-generated documentation.

## Short description

SciStream is a live research room that combines a notebook-style workspace, participant questions, contextual AI explanations, and automatic Markdown documentation. A host can open a focused session, run a reproducible scientific example, answer audience questions with a context-limited assistant, and leave with a complete record of the code, outputs, reasoning, conclusions, and next steps.

## Inspiration and problem

Research collaboration often splits across repositories, notebooks, calls, chat, and personal notes. Repositories preserve final artifacts, while meetings capture a moment and then disappear. SciStream explores a tighter workflow for collaboration while research is happening.

## What we built

- A concise product landing and session setup experience.
- A responsive research room with a labeled host-share substitute.
- A notebook-like cell running a deterministic exponential-decay experiment.
- Clear textual and visual output.
- Local participant Q&A and a session activity trail.
- An AI provider layer for code explanations, error help, output summaries, question answering, and next-experiment suggestions.
- Credential-free deterministic AI mode plus an optional hosted provider.
- Downloadable Markdown summaries containing all major session artifacts.

## How it works

Django serves the interface and validates three small JSON APIs. The demo executor safely recognizes one bundled experiment rather than evaluating arbitrary Python. Assistant actions receive only bounded current-session context. The browser keeps temporary session state and downloads the generated Markdown artifact.

## What is deliberately simulated

The host share, participant presence, and chat are local demo abstractions. Code execution supports the bundled experiment only. Mock AI mode is the recommended judging path. These boundaries keep the prototype dependable and make every product claim verifiable.

## What is next

Isolated Jupyter kernels, authenticated persistent rooms, WebSockets, WebRTC screen sharing, notebook export, citations, provenance, and human review controls for generated conclusions.

## Three-minute judging path

Open a session, run the decay experiment, add a participant question, ask the assistant to answer it and suggest a follow-up, then generate and download the Markdown summary.
