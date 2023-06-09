from potassium import Potassium, Request, Response

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import time

from jsonformer.format import highlight_values
from jsonformer.main import Jsonformer
import os
MODEL_NAME = os.environ.get("MODEL_NAME", "databricks/dolly-v2-3b")
PORT = os.environ.get("PORT", 8000)


app = Potassium("dolly_jsonformer")

# @app.init runs at startup, and initializes the app's context
@app.init
def init():
    device = 0 if torch.cuda.is_available() else -1
    # MODEL_NAME = "databricks/dolly-v2-3b"

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, padding_side="left")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.bfloat16,
        device_map="auto",
    )

    context = {"model": model, "tokenizer": tokenizer}

    return context


# @app.handler is an http post handler running for every call
@app.handler()
def handler(context: dict, request: Request) -> Response:
    model = context.get("model")
    tokenizer = context.get("tokenizer")

    # Start timer
    t_1 = time.time()

    prompt = request.json.get("prompt")
    json_schema = request.json.get("json_schema")

    if not json_schema:
        return Response(
            json={
                "error": "No json_schema provided in the request body."
            },
            status=400,
        )

    builder = Jsonformer(
        model=model,
        tokenizer=tokenizer,
        json_schema=json_schema,
        prompt=prompt,
    )

    output = builder()

    highlight_values(output)

    t_2 = time.time()

    return Response(
        json={
            "output": output,
            "prompt": prompt,
            "inference_time": t_2 - t_1,
        },
        status=200,
    )


if __name__ == "__main__":
    app.serve(port=PORT)
