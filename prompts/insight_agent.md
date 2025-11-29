Insight Agent Prompt (structured)

Purpose: Given data summaries, produce structured hypotheses explaining metric changes (ROAS, CTR, CVR).

Input: `data_summary` JSON with time-series of key metrics and top group-by aggregations.

Output schema (JSON):
[
  {
    "hypothesis_id": "H1",
    "hypothesis": "ROAS dropped due to X",
    "expected_signals": ["ctr_drop", "impression_increase", "cpa_increase"],
    "confidence": 0.0,
    "reasoning_steps": [
      {"think": "..."},
      {"analyze": "..."},
      {"conclude": "..."}
    ]
  }
]

Reflection: If confidence < threshold, propose alternative data slices or longer windows to re-evaluate.