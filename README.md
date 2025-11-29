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

Submission checklist & next steps
--------------------------------
To prepare the public GitHub submission, follow these steps (examples provided in `submission_instructions.md`):

1. Create a public repository named `kasparro-agentic-fb-analyst-<firstname-lastname>`.
2. Commit the project files (at least 3 commits recommended): scaffold, agent implementation, final polish.
3. Tag a release `v1.0` and create a PR titled `self-review` describing design choices and how to run the analysis.
4. Include the generated artifacts in `reports/` (`insights.json`, `creatives.json`, `report.md`) and `logs/` in the repo for reviewers.

Contact / Next steps
--------------------
If you want, I can:
- Add a `Makefile` and CI workflow for automated testing and linting.
- Expand the evaluator with ROAS- and CPA-level tests and a reflection/retry loop for low-confidence hypotheses.
- Add short-term memory to store insights across runs.

Thank you — tell me which next step you'd like me to do and I'll implement it.