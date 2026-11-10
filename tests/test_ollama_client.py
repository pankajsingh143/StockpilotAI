from types import SimpleNamespace

from backend.repositories.ollama_client import OllamaClient


class MockOllamaClient:
    def generate(self, model: str, prompt: str):
        assert model == "phi4-mini:latest"
        assert prompt == "Explain revenue growth."
        return SimpleNamespace(
            response="Revenue growth measures the increase in sales."
        )


def test_generate_returns_response_text():
    ollama_client = OllamaClient(
        base_url="http://localhost:11434",
        model="phi4-mini:latest",
        client=MockOllamaClient(),
    )

    result = ollama_client.generate(
        prompt="Explain revenue growth."
    )

    assert result == "Revenue growth measures the increase in sales."


def test_initializes_sdk_client_with_base_url(monkeypatch):
    captured = {}
    mock_client = object()

    def mock_client_factory(host):
        captured["host"] = host
        return mock_client

    monkeypatch.setattr(
        "backend.repositories.ollama_client.Client",
        mock_client_factory,
    )

    ollama_client = OllamaClient(
        base_url="http://localhost:11434",
        model="phi4-mini:latest",
    )

    assert captured["host"] == "http://localhost:11434"
    assert ollama_client.client is mock_client
    assert ollama_client.model == "phi4-mini:latest"
    
def test_generate_passes_json_schema_to_ollama():
    captured = {}

    class StructuredMockClient:
        def generate(self, **kwargs):
            captured.update(kwargs)
            return SimpleNamespace(response='{"summary": "Test"}')

    schema = {
        "type": "object",
        "properties": {
            "summary": {"type": "string"}
        },
        "required": ["summary"],
    }

    ollama_client = OllamaClient(
        base_url="http://localhost:11434",
        model="phi4-mini:latest",
        client=StructuredMockClient(),
    )

    result = ollama_client.generate(
        prompt="Generate structured output",
        format=schema,
    )

    assert captured["format"] == schema
    assert captured["model"] == "phi4-mini:latest"
    assert result == '{"summary": "Test"}'