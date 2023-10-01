from flask import Flask, request, Response
from typing import Any, Dict

from model_run import predict, prepare_model


app = Flask("ai-api")
model = prepare_model()

@app.post("/")
def main_handler() -> Dict[str, Any]:
  data: Dict[str, Any] = request.json
  text: str = data.get('text', '')
  if not text:
    return Response(status=400)
  return {"result": predict(*model, text)}


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=3033)