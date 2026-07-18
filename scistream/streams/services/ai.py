"""Context-limited AI providers for research-session assistance."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
import os
from urllib import error, request


ALLOWED_ACTIONS = {"explain_code", "explain_error", "summarize_output", "answer_question", "next_experiment"}


@dataclass(frozen=True)
class AssistantContext:
    title: str
    goal: str
    code: str
    output: str
    question: str = ""


class AIProvider(ABC):
    """Interface implemented by mock and hosted model providers."""

    @abstractmethod
    def respond(self, action: str, context: AssistantContext) -> str:
        raise NotImplementedError


class MockAIProvider(AIProvider):
    """Deterministic explanations that keep the whole demo credential-free."""

    def respond(self, action: str, context: AssistantContext) -> str:
        responses = {
            "explain_code": (
                "The cell models exponential decay. It converts a 3-hour half-life into a decay constant, "
                "then evaluates the percentage remaining every two hours. The formula ensures the value halves every 3 hours."
            ),
            "explain_error": (
                "This prototype runs a constrained local demonstration, not arbitrary Python. Restore the bundled decay example; "
                "a production version would send the cell to an isolated Jupyter kernel."
            ),
            "summarize_output": (
                "The output follows the expected exponential curve: 100% initially, about 25% after two half-lives, "
                "and about 6.25% after four. That supports a fitted half-life of 3.0 hours."
            ),
            "answer_question": (
                f"For the participant question “{context.question or 'How should we interpret this result?'}”: "
                "half-life is the time required for the measured quantity to decrease by half. Here each 3-hour interval "
                "multiplies the remaining amount by 0.5, so the change is proportional rather than linear."
            ),
            "next_experiment": (
                "Repeat the fit with noisy observations and compare confidence intervals across 2.5, 3.0, and 3.5-hour "
                "half-life assumptions. That tests how sensitive the conclusion is to measurement uncertainty."
            ),
        }
        return responses[action]


class OpenAIProvider(AIProvider):
    """Minimal optional provider using the Responses API without another dependency."""

    def __init__(self, api_key: str, model: str) -> None:
        self.api_key = api_key
        self.model = model

    def respond(self, action: str, context: AssistantContext) -> str:
        prompt = (
            "You are a concise scientific collaboration assistant. Use only the supplied session context. "
            "State uncertainty and do not invent results.\n"
            f"Action: {action}\nTitle: {context.title}\nGoal: {context.goal}\n"
            f"Code:\n{context.code[:5000]}\nOutput:\n{context.output[:3000]}\nQuestion: {context.question[:1000]}"
        )
        payload = json.dumps({"model": self.model, "input": prompt}).encode()
        api_request = request.Request(
            "https://api.openai.com/v1/responses",
            data=payload,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(api_request, timeout=30) as response:
                data = json.load(response)
        except (error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise RuntimeError("The configured AI provider is unavailable. Switch SCISTREAM_AI_MODE to mock.") from exc
        text = data.get("output_text")
        if not text:
            raise RuntimeError("The AI provider returned no explanation.")
        return text


def get_ai_provider() -> tuple[AIProvider, str]:
    """Select the configured provider, defaulting to the reliable demo implementation."""
    mode = os.getenv("SCISTREAM_AI_MODE", "mock").lower()
    api_key = os.getenv("OPENAI_API_KEY", "")
    if mode == "openai" and api_key:
        return OpenAIProvider(api_key, os.getenv("OPENAI_MODEL", "gpt-4.1-mini")), "openai"
    return MockAIProvider(), "mock"
