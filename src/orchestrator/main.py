import os
import sys
import json
try:
    import yaml
except Exception:
    yaml = None
import random
from pathlib import Path

from src.agents.planner import Planner
from src.agents.data_agent import DataAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator_agent import EvaluatorAgent
from src.agents.creative_generator import CreativeGenerator


def load_config(path="config/config.yaml"):
    # Try to load YAML if available; otherwise fall back to a minimal parser for known keys
    if yaml is not None:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    # minimal fallback: read file and extract a few known keys
    cfg = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read()
        # extract data.path
        for line in txt.splitlines():
            line = line.strip()
            if line.startswith('path:'):
                # basic parsing
                _, v = line.split(':', 1)
                cfg.setdefault('data', {})['path'] = v.strip().strip('"')
            if line.startswith('sample_mode:'):
                _, v = line.split(':', 1)
                cfg.setdefault('data', {})['sample_mode'] = v.strip().lower() in ('true', 'yes', '1')
            if line.startswith('random_seed:'):
                _, v = line.split(':', 1)
                try:
                    cfg['random_seed'] = int(v.strip())
                except Exception:
                    cfg['random_seed'] = 42
    except Exception:
        cfg = {'random_seed': 42, 'data': {'path': 'data/sample_small.csv'}}
    return cfg


class Orchestrator:
    def __init__(self, config):
        self.config = config
        random.seed(self.config.get("random_seed", 42))
        self.planner = Planner()
        self.data_agent = DataAgent(self.config)
        self.insight_agent = InsightAgent(self.config)
        self.evaluator = EvaluatorAgent(self.config)
        self.creative_gen = CreativeGenerator(self.config)

    def run(self, query):
        tasks = self.planner.decompose(query, self.config)
        df, summary = self.data_agent.load_and_summarize()

        hypotheses = self.insight_agent.generate(summary, query)
        validated = self.evaluator.validate(hypotheses, df, summary)

        creatives = self.creative_gen.generate(df, summary)

        # Prepare outputs
        reports_dir = Path(self.config.get("output", {}).get("reports_dir", "reports"))
        logs_dir = Path(self.config.get("output", {}).get("logs_dir", "logs"))
        reports_dir.mkdir(parents=True, exist_ok=True)
        logs_dir.mkdir(parents=True, exist_ok=True)

        insights_path = reports_dir / "insights.json"
        creatives_path = reports_dir / "creatives.json"
        report_md = reports_dir / "report.md"

        with open(insights_path, "w", encoding="utf-8") as f:
            json.dump(validated, f, indent=2)

        with open(creatives_path, "w", encoding="utf-8") as f:
            json.dump(creatives, f, indent=2)

        with open(report_md, "w", encoding="utf-8") as f:
            f.write("# Kasparro Agentic FB Analyst Report\n\n")
            f.write(f"Query: {query}\n\n")
            f.write("## Top Hypotheses\n")
            for h in validated:
                f.write(f"- {h.get('hypothesis_id')}: {h.get('hypothesis')} (confidence: {h.get('confidence')})\n")

        # logs
        log_path = logs_dir / "run_log.json"
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump({"query": query, "insights_file": str(insights_path), "creatives_file": str(creatives_path)}, f, indent=2)

        return {"insights": str(insights_path), "creatives": str(creatives_path), "report": str(report_md)}


def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py 'Analyze ROAS drop'")
        sys.exit(1)
    query = sys.argv[1]
    config = load_config()
    orch = Orchestrator(config)
    out = orch.run(query)
    print("Outputs:", out)


if __name__ == '__main__':
    main()
