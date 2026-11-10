from ollama import Client

class OllamaClient:
  def __init__(self,base_url: str, model: str, client=None):
    self.client = client or Client(host=base_url)
    self.model = model

  def generate(self, prompt: str) -> str:
    result = self.client.generate(model=self.model, prompt=prompt)
    return result.response