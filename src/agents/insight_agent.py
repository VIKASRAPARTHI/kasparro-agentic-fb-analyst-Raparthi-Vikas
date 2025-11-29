import math

class InsightAgent:
    def __init__(self, config=None):
        self.config = config or {}

    def generate(self, summary, query=None):
        # Heuristic hypotheses based on recent vs overall
        hypotheses = []
        recent = {r['campaign_name']: r for r in summary.get('recent', [])}
        overall = {r['campaign_name']: r for r in summary.get('overall', [])}

        for cname, o in overall.items():
            r = recent.get(cname)
            if not r:
                continue
            try:
                roas_drop = (o.get('roas', 0) - r.get('roas', 0)) / max(1e-9, o.get('roas', 0))
            except Exception:
                roas_drop = 0
            # Hypothesis if recent ROAS is substantially lower
            if roas_drop > 0.1:
                hypotheses.append({
                    'hypothesis_id': f'H_{cname[:8]}',
                    'campaign_name': cname,
                    'hypothesis': 'Recent ROAS decreased relative to prior period; possible creative fatigue or audience saturation.',
                    'expected_signals': ['ctr_decrease','impressions_stable_or_increase','cpa_increase'],
                    'confidence': 0.5,
                    'reasoning_steps': [
                        {'think': 'Compare recent vs prior ROAS and CTR'},
                        {'analyze': f'ROAS change {roas_drop:.2f}'},
                        {'conclude': 'If ROAS drop with falling CTR, creative likely underperforming.'}
                    ]
                })
        # If no explicit campaign-level issues found, add a global hypothesis
        if not hypotheses:
            hypotheses.append({
                'hypothesis_id': 'H_global_1',
                'hypothesis': 'No single campaign shows strong ROAS drop in recent window; consider audience-level or bid/market changes.',
                'expected_signals': ['audience_ctr_drop','increased_cpc','platform_wide_changes'],
                'confidence': 0.3,
                'reasoning_steps': [{'think':'Check audience and platform aggregates'},{'analyze':'No campaign-level signal'},{'conclude':'Expand diagnostics'}]
            })
        return hypotheses
