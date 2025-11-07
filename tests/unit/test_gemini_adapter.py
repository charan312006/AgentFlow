import json
from subprocess import CompletedProcess
from typing import List

import pytest

from agentflow.adapters.gemini_cli import GeminiCLIAdapter, GeminiCLIError


class SpyRun:
    """Helper to capture subprocess.run invocations."""

    def __init__(self, return_value: CompletedProcess) -> None:
        self.return_value = return_value
        self.calls: List[List[str]] = []

    def __call__(self, command, **kwargs):  # type: ignore[override]
        self.calls.append(command)
        return self.return_value


def make_completed_process(stdout_lines, returncode=0, stderr=""):
    stdout = "\n".join(stdout_lines)
    return CompletedProcess(args=[], returncode=returncode, stdout=stdout, stderr=stderr)


def test_gemini_adapter_parses_agent_message(monkeypatch, settings):
    event_lines = [
        json.dumps({"type": "thread.started", "thread_id": "abc"}),
        json.dumps(
            {"type": "item.completed", "item": {"type": "assistant_message", "text": "Hello Gemini!"}}
        ),
        json.dumps({"type": "turn.completed", "usage": {"output_tokens": 13}}),
    ]
    spy = SpyRun(make_completed_process(event_lines))
    monkeypatch.setattr("subprocess.run", spy)

    adapter = GeminiCLIAdapter(settings)
    result = adapter.run("Say hello.")

    assert result.message == "Hello Gemini!"
    assert result.usage == {"output_tokens": 13}

    assert len(spy.calls) == 1
    command = spy.calls[0]
    assert command[:2] == [getattr(settings, "gemini_cli_path", "gemini"), "chat"]


def test_gemini_adapter_raises_on_failure(monkeypatch, settings):
    spy = SpyRun(make_completed_process([], returncode=2, stderr="boom"))
    monkeypatch.setattr("subprocess.run", spy)

    adapter = GeminiCLIAdapter(settings)

    with pytest.raises(GeminiCLIError):
        adapter.run("test")
