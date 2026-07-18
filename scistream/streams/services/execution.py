"""A deterministic, deliberately limited Python demo executor.

The hackathon prototype never evaluates arbitrary user input. It recognizes the
bundled decay experiment and returns a reproducible result suitable for a live
demo. A sandboxed kernel is intentionally left for future work.
"""

from dataclasses import asdict, dataclass
import math


class UnsupportedCodeError(ValueError):
    """Raised when code is outside the safe demo experiment."""


@dataclass(frozen=True)
class ExecutionResult:
    stdout: str
    important_output: str
    chart: list[dict[str, float]]
    mode: str = "deterministic-demo"

    def as_dict(self) -> dict:
        return asdict(self)


def execute_demo_python(code: str) -> ExecutionResult:
    """Return the deterministic result for the bundled exponential-decay study."""
    if not code.strip():
        raise UnsupportedCodeError("Add Python code before running the cell.")
    required_signals = ("exp", "half_life", "time")
    if not all(signal in code for signal in required_signals):
        raise UnsupportedCodeError(
            "Demo mode supports the bundled exponential-decay experiment only. Reset the cell to the sample and try again."
        )

    half_life = 3.0
    points = []
    for time in range(0, 13, 2):
        remaining = 100 * math.exp(-math.log(2) * time / half_life)
        points.append({"time": float(time), "remaining": round(remaining, 2)})

    stdout = "\n".join(f"t={int(point['time']):>2} h  remaining={point['remaining']:>6.2f}%" for point in points)
    important = "The sample falls below 10% between 9 and 12 hours; fitted half-life = 3.0 hours."
    return ExecutionResult(stdout=stdout, important_output=important, chart=points)
