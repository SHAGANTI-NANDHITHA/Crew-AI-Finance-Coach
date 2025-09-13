import os
import requests
from typing import Optional

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LLM_BACKEND = os.getenv("LLM_BACKEND", "none").lower()
MODEL_NAME = "gemini-1.5-flash"


def call_gemini(prompt: str, max_tokens: int = 300) -> Optional[str]:
   """
   Stub function for calling Gemini. The project intentionally leaves implementation
   details to you because Google/Gemini's Python SDK or HTTP endpoints may change.

   Replace this function with your preferred method. Two options:
   1. Use the official Google Generative AI Python library (google.generativeai)
   if available in your environment.
   2. Use an OpenAI-compatible gateway that exposes Gemini as an engine.

   A simple placeholder implementation below returns None when backend is 'none'.
   """
   if LLM_BACKEND != "gemini":
      return None

   if not GEMINI_API_KEY:
      raise EnvironmentError("GEMINI_API_KEY not set in environment")

   # Example: If you have an HTTP gateway that accepts POST to /v1/generate
   # This is pseudocode — adapt it to your provider's endpoint & auth.
   endpoint = f"https://api.your-gateway.example/v1/models/{MODEL_NAME}:generate"
   headers = {"Authorization": f"Bearer {GEMINI_API_KEY}", "Content-Type": "application/json"}
   payload = {
      "prompt": prompt,
      "max_tokens": max_tokens,
   "temperature": 0.2,
   }
   try:
      resp = requests.post(endpoint, json=payload, headers=headers, timeout=20)
      resp.raise_for_status()
      data = resp.json()
      # adapt the following to the real response shape
      return data.get("output_text") or data.get("choices", [{}])[0].get("text")
   except Exception as e:
      print("LLM call failed:", e)
      return None