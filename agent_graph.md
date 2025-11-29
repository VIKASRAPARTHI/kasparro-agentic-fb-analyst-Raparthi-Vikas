# Agent Graph — Kasparro Agentic FB Performance Analyst

Overview

- Planner Agent: Receives the user query (intent) and decomposes it into structured subtasks (Data Summary, Hypothesis Generation, Validation, Creative Improvements).
- Data Agent: Loads dataset (sample/full), computes summaries (time series, group-bys), and returns compact summaries and visualizable statistics (JSON-ready).
- Insight Agent: Consumes data summaries, generates structured hypotheses explaining metric changes (e.g., ROAS decline), with reasoning steps (Think → Analyze → Conclude).
- Evaluator Agent: Quantitatively validates hypotheses using comparison windows, statistical checks, and returns evidence, p-values, and calibrated confidence.
- Creative Improvement Generator: For low-CTR campaigns, proposes new creative messages (headlines, CTAs, messaging angles) grounded in existing creative messages and observed performance.

Data Flow

1. User CLI query → Planner Agent produces subtasks.
2. Data Agent loads data per `config.yaml` and returns summarized signals.
3. Insight Agent proposes hypotheses with expected signals to check.
4. Evaluator Agent computes validation metrics and adjusts hypothesis confidence.
5. Creative Generator produces candidate creatives for low-CTR groups.
6. Orchestrator collects outputs, writes `reports/insights.json`, `reports/creatives.json`, `reports/report.md`, and structured logs.

Notes

- All agents communicate via JSON-serializable structures; datasets are summarized (not fully embedded in prompts).
- The system includes a reflection/retry loop: low-confidence hypotheses are flagged and retried with alternative analyses or longer windows.
- See `src/` for implementation skeleton and `prompts/` for structured prompt templates.