## Copilot / AI helper notes — QuickPick Multi-Agent (Actionable highlights)

These notes are tuned to make an AI coding assistant immediately productive in this repository.
Keep suggestions small, focused, and aligned with existing patterns.

### Big-picture architecture (read before editing)
- FastAPI backend: `main.py` exposes endpoints (important: `/assistant`, `/speech-to-text`, `/quick-order`, `/payment/*`, `/status`).
- Master coordinator: `master/master_agent.py` analyzes intent and routes requests to domain agents.
- Domain agents: `agents/` contains `base_agent.py` (abstract), `food_agent.py`, `travel_agent.py`, `shopping_agent.py` (+ `QuickCommerceAgent`), `payment_agent.py`.
- MCP clients: `mcp/` contains external integrations (e.g., `speech_to_text_client.py`, `razorpay_api_client.py`, `quick_commerce_scrapper.py`).
- Frontend: `quickpick_frontend/` (dev server via `bun` or `npm`).

When making changes that affect behaviour, update both `master/master_agent.py` routing logic and the corresponding agent(s) in `agents/`.

### Message / data flow (concrete examples)
- Incoming HTTP -> `main.py` -> calls `await master_agent.process({"message":..., "user_id":..., "context":...})`.
- `MasterAgent._analyze_intent` returns an intent dict used by `_route_to_agents` to call each `Agent.process_request(data, context)`.
- Agents use `BaseAgent.add_to_history(...)`, `update_user_preferences(...)` and return a dict of `{"status":"success"|"error","data":...}`.

### Project-specific conventions and patterns
- Agents are async. Implement `async def process_request(self, data, context)` in subclasses of `BaseAgent`.
- Helper methods inside agents are underscore-prefixed (e.g., `FoodAgent._plan_meal`, `FoodAgent._generate_recipe`). Prefer adding small helpers following that pattern.
- Keep `conversation_history` bounded (see `BaseAgent` trims to last 100 entries) — follow the same memory-safety approach.
- Configuration is centralized in `config/settings.py`. Use `settings` or `get_agent_settings("food_agent")` rather than hardcoding values.
- Platform scraping selectors live in `config/settings.py` under `PlatformConfig` — update those when adding new quick-commerce platforms.

### Integration points to watch / external deps
- Razorpay: `mcp/razorpay_api_client.py` — payment creation, verification, payment link creation. Tests and endpoints reference `main.py:/payment/*`.
- Groq Whisper (speech-to-text): `mcp/speech_to_text_client.py` — used by `/speech-to-text` endpoint and `main.py` calls `transcribe_audio_bytes`.
- Quick commerce scrapers/optimizers: `mcp/quick_commerce_scrapper.py` and `quick_commerce_optimizer` usage in `agents/shopping_agent.py`.
- Dependencies in `pyproject.toml` (Python >=3.10). Optional test/dev extras include pytest, black, flake8, mypy.

### Developer workflows (commands you can rely on)
- Start dev servers (backend + frontend): `start_dev.sh` — script creates `myenv`, installs deps, starts backend (`python main.py`) and frontend (`bun dev` or `npm run dev`). Note: the script expects a `myenv` virtualenv and writes `logs/backend.pid`, `logs/frontend.pid`.
- Run tests and quality checks: the single-entry helper is `python run_tests.py` with flags:
  - `--all`, `--unit`, `--integration`, `--e2e`, `--ci`, `--lint`, `--format`, `--types`, `--report`.
  - CI pipeline mirrors GitHub Actions in `TESTING.md` and runs pytest, flake8, black/isort checks and mypy.
- Recommended manual FastAPI run (explicit):
  ```bash
  uvicorn main:app --reload --host 0.0.0.0 --port 8000
  ```

### Tests & mocks
- Tests are under `tests/` with `conftest.py` providing fixtures for agents (see `tests/conftest.py`).
- Use provided fixtures when adding unit tests for agents. Integration tests exercise HTTP endpoints.

### What to change where (quick mapping)
- New endpoint -> edit `main.py` + add tests under `tests/integration` (+ update `README.md` and `TESTING.md` if behavior changes).
- New agent capability -> add class in `agents/` extending `BaseAgent`, update `master/master_agent.py` routing and `tests/unit` tests.
- New external integration -> add client inside `mcp/` and wire it into `main.py` or agent constructors; add env var in `config/settings.py`.

### Safety & style rules (discoverable, enforced patterns)
- Use async APIs consistently for agent processing and external IO.
- Follow existing logging conventions (`logging.getLogger(__name__)`), and return structured dicts (status, data, agent_id where applicable).
- Avoid global mutable state outside agents; prefer per-agent `user_preferences` and `conversation_history` stored on agent instance.

### Quick references (files to open first)
- `main.py` — HTTP API and how MasterAgent is invoked.
- `master/master_agent.py` — routing, intent analysis, synthesis.
- `agents/base_agent.py` — base behaviors and message shapes.
- `agents/food_agent.py`, `agents/shopping_agent.py`, `agents/payment_agent.py` — concrete patterns and examples.
- `mcp/*.py` — external integrations to mock in tests.
- `run_tests.py` and `TESTING.md` — test & CI workflows.

If any of the above sections are unclear or you'd like more detail (examples for a specific agent, API contract, or test fixture usage), tell me which area and I will expand or iterate.
