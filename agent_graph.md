# Agent Graph — Kasparro Agentic Facebook Performance Analyst

## Purpose

This document describes the high-level agent architecture, the data flow between components, and reproducibility notes for reviewers. The system is designed to produce actionable diagnostics (hypotheses + evidence) and creative recommendations from ad performance CSVs.

## Agents

- **Planner Agent**: Accepts a natural-language query (e.g., "Analyze ROAS drop") and decomposes it into ordered subtasks such as data summarization, hypothesis generation, validation, and creative generation. Produces a JSON task plan consumed by the orchestrator.

- **Data Agent**: Loads CSV data (path controlled by `config/config.yaml`), parses rows robustly, and emits compact summaries used by downstream agents: per-campaign aggregates, recent vs prior windows, and a small sample of raw rows. Designed to work without heavy dependencies (pure-Python parsing).

- **Insight Agent**: Takes the Data Agent summary and task plan, then generates structured hypotheses explaining metric changes (e.g., CTR drop, ROAS decline). Each hypothesis includes an identifier, expected signals to check, reasoning steps, and initial confidence.

- **Evaluator Agent**: Performs lightweight statistical checks (two-sample proportion z-test for CTR differences, basic ROAS comparisons) using the provided rows and windows. It returns evidence strings, p-values, and adjusts hypothesis confidence.

- **Creative Generator**: For campaigns flagged with low CTR or creative fatigue, generates 2–4 headline/body/CTA variations grounded in existing creative messages and observed signals. Outputs are grouped by campaign for downstream export.

## Orchestrator

The orchestrator coordinates the agents:

- Loads configuration via `src.orchestrator.main.load_config()`.
- Instantiates agents and runs the task plan for a provided query.
- Persists artifacts to `reports/` and logs metadata to `logs/run_log.json`.

## Data flow (step-by-step)

1. CLI: `python run.py "Analyze ROAS drop (full data)"` → orchestrator receives query.
2. Orchestrator asks Planner to decompose the query into subtasks.
3. Data Agent reads CSV and returns `rows` and `summary` (overall & recent windows).
4. Insight Agent produces candidate hypotheses with expected signals.
5. Evaluator Agent validates each hypothesis using `rows` and returns `validated`, `p_value`, and `evidence`.
6. Creative Generator creates candidate creatives for campaigns that meet low-CTR thresholds.
7. Orchestrator writes `reports/insights.json`, `reports/creatives.json`, `reports/report.md`, and `logs/run_log.json`.

## Reproducibility & artifacts

- Default data path: controlled by `config/config.yaml` (`data.path`). The repository includes `data/synthetic_fb_ads_undergarments.csv` for full runs and a small sample for quick checks.
- Required artifacts for submission (include in repo):
	- `reports/insights.json` — structured hypotheses with evidence and p-values.
	- `reports/creatives.json` — creative recommendations per campaign.
	- `reports/report.md` — human-readable summary for stakeholders.
	- `logs/run_log.json` — run metadata pointing to the above artifacts (ensure paths are repo-local before release).

## Notes for reviewers

- The system was intentionally implemented without heavy numeric libs to improve portability; adding `pandas`/`scipy` would simplify computations but is optional.
- Randomness is seeded (`random_seed` in `config/config.yaml`) for deterministic creative generation during review.
- Tests: see `tests/test_evaluator.py` for a unit test exercising the evaluator's CTR-detection logic.
