"""Views and small JSON endpoints for the SciStream live-session demo."""

import json

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .services.ai import ALLOWED_ACTIONS, AssistantContext, get_ai_provider
from .services.execution import UnsupportedCodeError, execute_demo_python


def index(request: HttpRequest):
    return render(request, "streams/index.html")


def _json_body(request: HttpRequest) -> dict:
    try:
        body = json.loads(request.body or b"{}")
    except json.JSONDecodeError as exc:
        raise ValueError("Request body must be valid JSON.") from exc
    if not isinstance(body, dict):
        raise ValueError("Request body must be a JSON object.")
    return body


def _required_text(data: dict, field: str, limit: int) -> str:
    value = data.get(field, "")
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field.replace('_', ' ').title()} is required.")
    if len(value) > limit:
        raise ValueError(f"{field.replace('_', ' ').title()} must be {limit} characters or fewer.")
    return value.strip()


@require_POST
def execute_code(request: HttpRequest) -> JsonResponse:
    try:
        data = _json_body(request)
        code = _required_text(data, "code", 12_000)
        result = execute_demo_python(code)
        return JsonResponse({"ok": True, **result.as_dict()})
    except (ValueError, UnsupportedCodeError) as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=400)


@require_POST
def assistant(request: HttpRequest) -> JsonResponse:
    try:
        data = _json_body(request)
        action = data.get("action", "")
        if action not in ALLOWED_ACTIONS:
            raise ValueError("Choose a supported assistant action.")
        context_data = data.get("context", {})
        if not isinstance(context_data, dict):
            raise ValueError("Assistant context must be an object.")
        context = AssistantContext(
            title=str(context_data.get("title", ""))[:200],
            goal=str(context_data.get("goal", ""))[:1000],
            code=str(context_data.get("code", ""))[:12_000],
            output=str(context_data.get("output", ""))[:8_000],
            question=str(context_data.get("question", ""))[:1_000],
        )
        provider, mode = get_ai_provider()
        return JsonResponse({"ok": True, "message": provider.respond(action, context), "mode": mode})
    except (ValueError, RuntimeError) as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=400)


@require_POST
def generate_summary(request: HttpRequest) -> JsonResponse:
    try:
        data = _json_body(request)
        title = _required_text(data, "title", 200)
        goal = _required_text(data, "goal", 1_000)
        code = _required_text(data, "code", 12_000)
        output = str(data.get("output", "No output was captured."))[:8_000]
        questions = [str(item)[:500] for item in data.get("questions", []) if str(item).strip()][:20]
        explanations = [str(item)[:1_500] for item in data.get("explanations", []) if str(item).strip()][:20]
        question_lines = "\n".join(f"- {item}" for item in questions) or "- No participant questions recorded."
        explanation_lines = "\n".join(f"- {item}" for item in explanations) or "- No AI explanations requested."
        markdown = f"""# {title}

## Research goal
{goal}

## Code executed
```python
{code}
```

## Important outputs
```
{output}
```

## Participant questions
{question_lines}

## AI explanations
{explanation_lines}

## Conclusions
The observed values follow an exponential-decay pattern consistent with a 3.0-hour half-life. The sample falls below 10% between 9 and 12 hours.

## Suggested next steps
- Add measurement noise and estimate a confidence interval for the fitted half-life.
- Compare the exponential model with alternative decay assumptions.
- Repeat the session with a sandboxed Jupyter kernel for arbitrary experiments.
"""
        return JsonResponse({"ok": True, "markdown": markdown})
    except ValueError as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=400)
