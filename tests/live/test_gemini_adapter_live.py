import os

import pytest

from agentflow.adapters import GeminiCLIAdapter


pytestmark = pytest.mark.live


def _can_run_live() -> bool:
    return bool(os.environ.get("AGENTFLOW_GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY"))


@pytest.mark.skipif(not _can_run_live(), reason="GEMINI API key is required for live test.")
def test_gemini_adapter_live_round_trip(settings):
    adapter = GeminiCLIAdapter(settings)
    result = adapter.run("Return the word ok.")
    assert "ok" in result.message.lower()
    assert result.usage
