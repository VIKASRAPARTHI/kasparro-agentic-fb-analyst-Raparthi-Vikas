import json

class Planner:
    """Simple Planner Agent: decomposes query into subtasks."""

    def decompose(self, query, config_summary=None):
        tasks = [
            {"id": "data_summary", "description": "Summarize dataset and time windows", "params": {}},
            {"id": "generate_hypotheses", "description": "List plausible hypotheses with expected signals", "params": {}},
            {"id": "validate_hypotheses", "description": "Quantitatively validate hypotheses", "params": {}},
            {"id": "creative_generation", "description": "Produce new creative messages for low-CTR campaigns", "params": {}}
        ]
        return {"query": query, "tasks": tasks}
