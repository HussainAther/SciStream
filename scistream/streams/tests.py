"""Tests for the complete credential-free research-session workflow."""

import json

from django.test import TestCase, override_settings
from django.urls import reverse

from .services.ai import AssistantContext, MockAIProvider
from .services.execution import UnsupportedCodeError, execute_demo_python


SAMPLE_CODE = """import math
half_life = 3.0
for time in range(0, 13, 2):
    print(100 * math.exp(-math.log(2) * time / half_life))
"""


class DemoPageTests(TestCase):
    def test_landing_page_explains_product_and_contains_room(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Research is better")
        self.assertContains(response, "Generate summary")
        self.assertContains(response, "deterministic demo mode")


class ExecutionServiceTests(TestCase):
    def test_sample_returns_reproducible_decay_series(self):
        result = execute_demo_python(SAMPLE_CODE)
        self.assertEqual(len(result.chart), 7)
        self.assertEqual(result.chart[0]["remaining"], 100.0)
        self.assertEqual(result.chart[-1]["remaining"], 6.25)
        self.assertIn("half-life = 3.0 hours", result.important_output)

    def test_unsupported_code_is_rejected(self):
        with self.assertRaises(UnsupportedCodeError):
            execute_demo_python("print('hello')")


@override_settings(DEBUG=False)
class ApiWorkflowTests(TestCase):
    def post_json(self, name: str, payload: dict):
        return self.client.post(reverse(name), data=json.dumps(payload), content_type="application/json")

    def test_execute_endpoint(self):
        response = self.post_json("execute_code", {"code": SAMPLE_CODE})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["ok"])
        self.assertEqual(response.json()["mode"], "deterministic-demo")

    def test_execute_validates_empty_code(self):
        response = self.post_json("execute_code", {"code": ""})
        self.assertEqual(response.status_code, 400)
        self.assertIn("required", response.json()["error"].lower())

    def test_mock_assistant_answers_with_limited_context(self):
        response = self.post_json(
            "assistant",
            {
                "action": "answer_question",
                "context": {
                    "title": "Decay",
                    "goal": "Estimate half-life",
                    "code": SAMPLE_CODE,
                    "output": "6.25%",
                    "question": "What does half-life mean?",
                },
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["mode"], "mock")
        self.assertIn("What does half-life mean?", response.json()["message"])

    def test_assistant_rejects_unknown_action(self):
        response = self.post_json("assistant", {"action": "delete_everything", "context": {}})
        self.assertEqual(response.status_code, 400)

    def test_summary_contains_all_required_sections(self):
        response = self.post_json(
            "generate_summary",
            {
                "title": "Protein Decay Analysis",
                "goal": "Estimate the sample half-life.",
                "code": SAMPLE_CODE,
                "output": "Half-life = 3.0 hours",
                "questions": ["Could noise alter the fit?"],
                "explanations": ["Compare confidence intervals."],
            },
        )
        self.assertEqual(response.status_code, 200)
        markdown = response.json()["markdown"]
        for heading in (
            "# Protein Decay Analysis",
            "## Research goal",
            "## Code executed",
            "## Important outputs",
            "## Participant questions",
            "## AI explanations",
            "## Conclusions",
            "## Suggested next steps",
        ):
            self.assertIn(heading, markdown)

    def test_invalid_json_returns_useful_error(self):
        response = self.client.post(reverse("execute_code"), data="not-json", content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("valid JSON", response.json()["error"])


class MockProviderTests(TestCase):
    def test_every_supported_action_is_deterministic(self):
        provider = MockAIProvider()
        context = AssistantContext("Title", "Goal", SAMPLE_CODE, "Output", "Question")
        for action in ("explain_code", "explain_error", "summarize_output", "answer_question", "next_experiment"):
            self.assertTrue(provider.respond(action, context))
