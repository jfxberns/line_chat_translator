# Repository Guidelines

## Project Structure & Module Organization
- Source: `translator_test_logged.py` — CLI to translate Thai/English via OpenAI or Gemini APIs and log usage.
- Logs: `translation_log.jsonl` — JSONL line per run (tokens, cost, duration). Safe to delete if too large.
- Config: `.env` — `OPENAI_API_KEY`, `GEMINI_API_KEY` (never commit).

## Build, Test, and Development Commands
- Install deps: `pip install -U openai requests python-dotenv`
- Run (GPT‑5): `python translator_test_logged.py gpt5 "สวัสดี"`
- Run (Gemini): `python translator_test_logged.py gemini "สวัสดี"`
- Help/usage: `python translator_test_logged.py` (lists models and syntax)
- Python: 3.9+ recommended; no build step required.

## Coding Style & Naming Conventions
- Style: PEP 8; 4‑space indentation; ~100 char line length.
- Names: files/modules and functions in `snake_case`; constants in `UPPER_SNAKE_CASE`.
- Types: add type hints for new/modified functions when clear and stable.
- Tools (optional): `black` for formatting; `ruff` for linting.

## Testing Guidelines
- Current: no formal test suite. Prefer `pytest` for additions.
- Layout: put tests under `tests/`, files named `test_*.py` mirroring CLI behavior.
- Quick checks: run both providers with short input and confirm a new line in `translation_log.jsonl` containing `tokens_in`, `tokens_out`, and `estimated_cost`.

## Commit & Pull Request Guidelines
- Commits: imperative, concise subject (e.g., "Add Gemini lite model"), with a brief rationale in the body if needed.
- PRs: include description, example run command + expected output snippet, any config changes, and link related issues.
- Keep diffs focused; avoid unrelated refactors.

## Security & Configuration Tips
- Create `.env` with:
  - `OPENAI_API_KEY=...`
  - `GEMINI_API_KEY=...`
- Do not commit `.env` or `translation_log.jsonl`; logs may contain sensitive text.
- Handle HTTP errors and timeouts; prefer minimal API key scopes.

## Architecture Overview
- Flow: parse args → map to provider/model → call API → print result → append JSONL log with tokens, cost, and duration.

