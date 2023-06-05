# This file is used to verify your http server acts as expected
# Run it with `python3 test.py``

import requests

model_inputs = {
    "prompt": "Generate an example car",
    "json_schema": {
      "type": "object",
      "properties": {
        "car": {
          "type": "object",
          "properties": {
            "make": {"type": "string"},
            "model": {"type": "string"},
            "year": {"type": "number"},
            "colors": {
              "type": "array",
              "items": {"type": "string"}
            },
            "features": {
              "type": "object",
              "properties": {
                "audio": {
                  "type": "object",
                  "properties": {
                    "brand": {"type": "string"},
                    "speakers": {"type": "number"},
                    "hasBluetooth": {"type": "boolean"}
                  }
                },
                "safety": {
                  "type": "object",
                  "properties": {
                    "airbags": {"type": "number"},
                    "parkingSensors": {"type": "boolean"},
                    "laneAssist": {"type": "boolean"}
                  }
                },
                "performance": {
                  "type": "object",
                  "properties": {
                    "engine": {"type": "string"},
                    "horsepower": {"type": "number"},
                    "topSpeed": {"type": "number"}
                  }
                }
              }
            }
          }
        },
        "owner": {
          "type": "object",
          "properties": {
            "firstName": {"type": "string"},
            "lastName": {"type": "string"},
            "age": {"type": "number"},
          }
        }
      }
    }
}

res = requests.post("http://localhost:8000/", json=model_inputs)

print(res.json())
