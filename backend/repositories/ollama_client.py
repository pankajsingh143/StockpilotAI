from ollama import Client

class OllamaClient:
  def __init__(self,base_url: str, model: str, client=None):
    self.client = client or Client(host=base_url)
    self.model = model

  def generate(self, prompt: str, format: dict | str | None = None) -> str:
    options = {
      "model": self.model,
      "prompt": prompt
    }
    if format is not None:
      options["format"] = format
    result = self.client.generate(**options)
    return result.response