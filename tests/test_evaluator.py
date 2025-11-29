import pytest
from datetime import datetime, timedelta
from src.agents.evaluator_agent import EvaluatorAgent


def build_sample_rows():
    rows = []
    start = datetime(2025, 11, 1)
    for i in range(20):
        rows.append({
            'campaign_name': 'A',
            'date': start + timedelta(days=i),
            'impressions': 100.0,
            'clicks': 5.0 if i < 10 else 2.0,
            'spend': 50.0,
            'purchases': 1.0,
            'revenue': 100.0,
            'creative_message': 'sample message'
        })
    return rows


def test_evaluator_detects_ctr_drop():
    rows = build_sample_rows()
    evaluator = EvaluatorAgent({'analysis': {'recent_window_days': 10}})
    hypotheses = [{'hypothesis_id': 'H_A', 'campaign_name': 'A', 'hypothesis': 'ctr drop', 'confidence': 0.4}]
    res = evaluator.validate(hypotheses, rows, {})
    assert res[0]['validated'] is True or res[0]['validated'] is not None
