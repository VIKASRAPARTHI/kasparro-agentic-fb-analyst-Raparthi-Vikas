Planner Agent Prompt (structured)

Goal: Decompose the user query into specific subtasks to analyze Facebook Ads performance.

Input: JSON with keys: `query` (string), `constraints` (object), and `config_summary` (object).

Output (JSON schema):
{
  "query": "",
  "tasks": [
    {"id": "data_summary", "description": "Summarize dataset and time windows", "params": {}},
    {"id": "generate_hypotheses", "description": "List plausible hypotheses with expected signals", "params": {}},
    {"id": "validate_hypotheses", "description": "Quantitatively validate hypotheses", "params": {}},
    {"id": "creative_generation", "description": "Produce new creative messages for low-CTR campaigns", "params": {}}
  ],
  "notes": "Include rationale, priority order, and expected outputs for each task."
}

Reasoning structure: Think → Analyze → Conclude
Reflection: If tasks have low coverage for provided data, propose additional diagnostic subtasks.