
import os
import sys
import openai
import requests
import json
import time
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Basic pricing per 1M tokens (USD)
PRICING = {
    "gpt-5": {"in": 1.25, "out": 10.00},
    "gpt-5-mini": {"in": 0.25, "out": 2.00},
    "gpt-5-nano": {"in": 0.05, "out": 0.40},
    "gemini-2.5-pro": {"in": 1.25, "out": 10.00},
    "gemini-2.5-flash-lite": {"in": 0.10, "out": 0.40}
}

LOG_FILE = "translation_log.jsonl"

def log_translation(log_data):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_data, ensure_ascii=False) + "\n")

def estimate_cost(model, tokens_in, tokens_out):
    """Estimate API cost based on per-1M token pricing."""
    if model not in PRICING:
        return 0.0
    price = PRICING[model]
    cost_in = (tokens_in / 1_000_000) * price["in"]
    cost_out = (tokens_out / 1_000_000) * price["out"]
    return round(cost_in + cost_out, 6)

def call_gpt5(text, model="gpt-5"):
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a professional Thai-English translator. Return only the translation, no explanations."},
            {"role": "user", "content": text}
        ]
    )
    content = response["choices"][0]["message"]["content"]
    tokens_in = response["usage"]["prompt_tokens"]
    tokens_out = response["usage"]["completion_tokens"]
    total_tokens = response["usage"]["total_tokens"]
    return content, tokens_in, tokens_out, total_tokens

def call_gemini(text, model="gemini-2.5-pro"):
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY not set. Add it to your .env file.")
    # Gemini Generative Language API expects the API key as a query parameter, not a Bearer token.
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {
                "parts": [
                    {"text": f"You are a professional Thai-English translator. Return only the translation, no explanations.\n\n{text}"}
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    output = result["candidates"][0]["content"]["parts"][0]["text"]

    tokens_in = result.get("usageMetadata", {}).get("promptTokenCount", 0)
    tokens_out = result.get("usageMetadata", {}).get("candidatesTokenCount", 0)
    total_tokens = tokens_in + tokens_out
    return output, tokens_in, tokens_out, total_tokens

def main():
    if len(sys.argv) < 3:
        print("Usage: python translator_test_logged.py [model] [text]")
        print("Models: gpt5, gpt5-mini, gpt5-nano, gemini, gemini-lite")
        sys.exit(1)

    model_arg = sys.argv[1].lower()
    text = " ".join(sys.argv[2:])
    model_map = {
        "gpt5": "gpt-5",
        "gpt5-mini": "gpt-5-mini",
        "gpt5-nano": "gpt-5-nano",
        "gemini": "gemini-2.5-pro",
        "gemini-lite": "gemini-2.5-flash-lite"
    }

    model = model_map.get(model_arg)
    if not model:
        print("Unknown model. Use one of: gpt5, gpt5-mini, gpt5-nano, gemini, gemini-lite")
        sys.exit(1)

    start = time.time()
    if model.startswith("gpt"):
        output, tokens_in, tokens_out, total_tokens = call_gpt5(text, model)
    else:
        output, tokens_in, tokens_out, total_tokens = call_gemini(text, model)
    duration = round(time.time() - start, 3)

    cost_usd = estimate_cost(model, tokens_in, tokens_out)
    # Display cost in THB first, with USD in parentheses (1 USD = 32 THB)
    cost_thb = round(cost_usd * 32, 6)

    print(f"\n--- Translation Result ---\n{output}\n")
    print(f"Tokens In: {tokens_in} | Tokens Out: {tokens_out} | Total: {total_tokens}")
    print(f"Estimated Cost: ฿{cost_thb} (US${cost_usd}) | Time: {duration}s\n")

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "model": model,
        "input": text,
        "output": output,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "total_tokens": total_tokens,
        "estimated_cost_usd": cost_usd,
        "estimated_cost_thb": cost_thb,
        "duration_sec": duration
    }
    log_translation(log_entry)

if __name__ == "__main__":
    main()
