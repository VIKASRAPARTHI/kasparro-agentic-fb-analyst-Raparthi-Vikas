# Kasparro — Agentic Facebook Performance Analyst

A small multi-agent system that analyzes Facebook Ads performance, diagnoses ROAS changes, validates hypotheses quantitatively, and generates creative recommendations for low-CTR campaigns.

## Prerequisites

- Python 3.11+ recommended (3.10 should work, but tests were run on 3.11+).
- Optional: create and activate a virtual environment.

## Install

PowerShell:

```powershell
python -m pip install -r requirements.txt
```

The project is intentionally dependency-light and includes pure-Python fallbacks so reviewers can run without heavy binary builds.

## Data and Configuration

- Default config: `config/config.yaml` contains `data.path`, thresholds, and `random_seed`.
- Sample CSV for quick runs: `data/sample_small.csv` (small subset).
- Full dataset (included in this workspace): `data/synthetic_fb_ads_undergarments.csv`.

To run the full analysis, ensure `config/config.yaml` points to the full CSV or set `data.path` to the file location.

## Run (exact reproducible command)

PowerShell (recommended for reviewers):

```powershell
$env:PYTHONPATH='.'; python run.py "Analyze ROAS drop (full data)"
```

The same command is executed by `run.sh` on Unix-like systems (it sets `PYTHONPATH` and calls `run.py`).

## What the runner produces

After a successful run you will find:

- `reports/insights.json` — structured hypotheses (fields include `hypothesis_id`, `confidence`, `validated`, `evidence`, `p_value`).
- `reports/creatives.json` — recommended creative variants for campaigns with low CTR.
- `reports/report.md` — a human-readable markdown summary of top hypotheses and recommendations.
- `logs/run_log.json` — run metadata pointing to produced artifacts.

Example (short excerpt from `reports/report.md`):

```
# Kasparro Agentic FB Analyst Report

Query: Analyze ROAS drop (full data)

## Top Hypotheses
- H_women Su: Recent ROAS decreased relative to prior period; possible creative fatigue or audience saturation. (confidence: 0.95)
```

## Tests

Run the unit tests with pytest:

```powershell
$env:PYTHONPATH='.'; python -m pip install pytest; pytest -q
```

## Submission checklist (what to include in the public repo)

1. Repository name: `kasparro-agentic-fb-analyst-<firstname-lastname>`.
2. Commits (example flow):

```powershell
git init
git add .
git commit -m "scaffold: initial project structure"
# implement agents and orchestrator
git add .
git commit -m "feat: agent implementations and orchestrator"
# final polish and artifacts
git add .
git commit -m "chore: finalize readme, scripts, and reports"
```

3. Create a release tag and push tags:

```powershell
git tag -a v1.0 -m "v1.0 release — kasparro agentic fb analyst"
git push origin main --tags
```

4. Include generated artifacts inside the repository to provide evidence to reviewers:

- `reports/insights.json`
- `reports/creatives.json`
- `reports/report.md`
- `logs/run_log.json` (ensure it references the repo-local `reports/` paths)

5. PR: Open a pull request titled `self-review` and describe:
- High-level architecture (Planner → Data → Insight → Evaluator → Creative).
- Validation approach (what tests were run, statistical checks performed).
- Commands to reproduce outputs (exact commands above).
- Limitations and next steps.

## Notes & recommendations

- If `logs/run_log.json` points to external paths (Downloads or other folders), update it to point to the repo-local artifact paths prior to tagging the release so reviewers can find evidence directly in the repository.
- Consider adding a short `RELEASE_NOTES.md` in the root with a bulleted summary of v1.0 changes.
- Add CI (GitHub Actions) to run `pytest` and lint the code to increase reviewer confidence.

---

If you want, I can:

- Update `logs/run_log.json` to reference `reports/insights.json` and `reports/creatives.json` and commit that change.
- Create `RELEASE_NOTES.md` and annotate the existing `v1.0` tag locally.
- Push the `v1.0` tag to `origin`.

Tell me which of these you'd like me to do next.
Kasparro — Agentic Facebook Performance Analyst
===============================================

Overview
--------
This project implements a small multi-agent system that analyzes Facebook Ads performance, diagnoses ROAS changes, validates hypotheses quantitatively, and generates creative recommendations for low-CTR campaigns.

Quick start (Windows PowerShell)
--------------------------------
- Install dependencies (optional — the core runner uses pure-Python so this is minimal):

```powershell
python -m pip install -r requirements.txt
```

- Run the full analysis (uses `config/config.yaml` data path):

```powershell
$env:PYTHONPATH='.'; python run.py "Analyze ROAS drop (full data)"
```

- Run tests:

```powershell
$env:PYTHONPATH='.'; python -m pip install pytest; pytest -q
```

Files & layout
--------------
- `run.py` — CLI entrypoint (calls orchestrator)
- `config/config.yaml` — thresholds, data path, seeds
- `src/` — agent code: `agents/` (Planner, DataAgent, InsightAgent, EvaluatorAgent, CreativeGenerator), `orchestrator/`
- `prompts/` — structured prompt templates for each agent (Planner, Insight, Evaluator, Creative)
- `data/` — sample CSV (`sample_small.csv`) and full dataset (`synthetic_fb_ads_undergarments.csv`)
- `reports/` — outputs: `insights.json`, `creatives.json`, `report.md`
- `logs/` — run logs (e.g., `run_log.json`)
- `tests/` — unit tests (evaluator)
- `Makefile`, `run.sh`, `run.ps1` — convenience run/test scripts

Design & Architecture
---------------------
The system follows this loop:
- Planner Agent: decomposes the user's query into subtasks.
- Data Agent: loads CSV, computes compact summaries (overall & recent windows).
- Insight Agent: proposes structured hypotheses (Think → Analyze → Conclude).
- Evaluator Agent: quantitatively validates hypotheses (proportion z-test for CTR), returns p-values and calibrated confidences.
- Creative Generator: produces 3 message/CTA variants for campaigns with low CTR, grounded in existing creatives.

Prompts
-------
See the `prompts/` folder for layered prompt templates used to structure agent reasoning and outputs. Prompts are designed to return JSON-like structured outputs and include reflection instructions for low-confidence results.

Reproducibility
---------------
- Seeded randomness: `config/config.yaml` contains `random_seed`.
- `config/config.yaml` also contains thresholds (`low_ctr`, `significant_roas_drop`) and analysis window sizes.
- The repo provides `data/sample_small.csv` for quick runs. To run with the full dataset, set `data.path` in `config/config.yaml` to `data/synthetic_fb_ads_undergarments.csv` (this is the default for full run provided in this submission).

Outputs
-------
- `reports/insights.json`: Structured hypotheses with fields: `hypothesis_id`, `hypothesis`, `expected_signals`, `confidence`, `reasoning_steps`, `validated`, `evidence`, `p_value`.
- `reports/creatives.json`: Creative recommendations for low-CTR campaigns with `headline`, `body`, `cta`, and `rationale`.
- `reports/report.md`: Human-readable summary of top hypotheses and recommendations.

Validation approach
-------------------
- The Evaluator Agent compares recent vs prior windows (configurable via `recent_window_days`) and performs a two-sided z-test for CTR differences (implemented in pure-Python). It returns a p-value and adjusts hypothesis confidence based on statistical evidence.


Testing
-------
Run unit tests with `pytest tests/` to validate the Evaluator Agent's statistical tests.
