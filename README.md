# Line Chat Translator PoC

A minimal CLI to translate Thai/English text via OpenAI or Gemini APIs, with token and cost logging (THB-first display).  Performance using Gemini-Flash-Lite it was fast, accurate enough and the cost was very cheap.  

Further development as a full-fledged Line Chatbot is feasible, but the value to me vs. the red-tape of setting up an auto-bot made me think twice about proceeding. 

## Quick Start
- Python: 3.9+
- Create venv (uv):
  - `uv venv .venv && source .venv/bin/activate`
  - Install: `uv pip install -U openai==0.28.1 requests python-dotenv`
- Configure `.env`:
  - `OPENAI_API_KEY=...`
  - `GEMINI_API_KEY=...`

## Usage
- GPT‑5: `python translator_test_logged.py gpt5 "สวัสดี"`
- Gemini: `python translator_test_logged.py gemini "สวัสดี"`
- Help: `python translator_test_logged.py`

Outputs translation plus token counts, estimated cost (฿ first, US$ in parentheses), and duration. Appends a JSON line to `translation_log.jsonl`.

## Files
- `translator_test_logged.py` — CLI entrypoint.
- `translation_log.jsonl` — JSONL log (ignored by Git) including `estimated_cost_thb` and `estimated_cost_usd`.
- `.env` — API keys (ignored). See `AGENTS.md` for contributor details.

## Notes
- OpenAI SDK version is pinned to `0.28.1` to match `ChatCompletion` usage.
- If you prefer pip: `python -m venv .venv && source .venv/bin/activate && python -m ensurepip --upgrade && pip install -U openai==0.28.1 requests python-dotenv`.

## License
MIT — see `LICENSE`.
