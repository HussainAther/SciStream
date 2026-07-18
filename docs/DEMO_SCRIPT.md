# Three-Minute Demo Script

## Before presenting

- Run `./scripts/run_demo.sh` and open `http://127.0.0.1:8000`.
- Keep `SCISTREAM_AI_MODE=mock` so the demo has no network or credential dependency.
- Use a browser width of at least 1280 pixels.

## 0:00–0:25 — Frame the problem

On the landing page, say:

> GitHub is a great record after research is done. Calls and streams help while it is happening, but the code, questions, and reasoning get separated. SciStream puts that live workflow in one room and leaves a useful record behind.

Point to “Notebook-style coding,” “Live Q&A,” “Context-aware AI,” and “Markdown records.”

## 0:25–0:45 — Open the room

Select **Start research session**. Keep the seeded title and question, then select **Open research room**.

Call out the labeled host-share substitute. Be direct that it is the reliable hackathon abstraction for future screen sharing.

## 0:45–1:20 — Run the experiment

Select **Run cell**. Show the time-series values, bar chart, and important-output callout.

Say:

> This is a deterministic local demo kernel for one exponential-decay experiment. It demonstrates the workflow without pretending arbitrary code execution is safely solved.

## 1:20–1:55 — Capture discussion and use AI

In participant chat, send: `Why does the rate slow over time?`

Select **Answer latest question**, then **Suggest next experiment**. Point out the mock badge and explain that the service interface can use a hosted provider, but the fallback is deliberately credential-free and receives only bounded session context.

## 1:55–2:35 — Generate the record

Select **Generate summary**. Scroll through the title, goal, executed code, outputs, questions, AI explanations, conclusions, and next steps. Select **Copy Markdown** or **Download .md**.

## 2:35–3:00 — Close with scope

> The hackathon result is one complete, honest workflow: create a session, run a scientific example, discuss it, ask for contextual help, and leave with documentation. The next engineering steps are isolated Jupyter kernels, authenticated real-time rooms, and WebRTC sharing—not more dashboard surface area.

## Recovery notes

- If code was edited into an unsupported form, select **Reset sample** and run again.
- If a hosted provider fails, restart with `SCISTREAM_AI_MODE=mock`.
- A refresh resets the local session by design.
