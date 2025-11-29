import math
from math import sqrt
from datetime import timedelta


def normal_two_sided_pvalue(z):
    # use complementary error function to get two-sided p-value
    try:
        p = math.erfc(abs(z) / math.sqrt(2))
        return p
    except Exception:
        return None


class EvaluatorAgent:
    def __init__(self, config=None):
        self.config = config or {}

    def _filter_campaign(self, rows, campaign_name):
        return [r for r in rows if (r.get('campaign_name') or 'unknown') == campaign_name]

    def validate(self, hypotheses, rows, summary):
        results = []
        for h in hypotheses:
            cid = h.get('campaign_name')
            if cid:
                camp = self._filter_campaign(rows, cid)
                if not camp:
                    h_res = {**h, 'validated': None, 'evidence': 'No data for campaign', 'p_value': None}
                    h_res['confidence'] = 0.2
                    results.append(h_res)
                    continue
                recent_days = self.config.get('analysis', {}).get('recent_window_days', 14)
                max_date = max([r['date'] for r in camp if r.get('date') is not None])
                recent_cut = max_date - timedelta(days=recent_days)
                recent = [r for r in camp if r.get('date') is not None and r['date'] >= recent_cut]
                prior = [r for r in camp if r.get('date') is not None and r['date'] < recent_cut]
                if not recent or not prior:
                    h_res = {**h, 'validated': None, 'evidence': 'Insufficient window data', 'p_value': None}
                    h_res['confidence'] = 0.25
                    results.append(h_res)
                    continue
                r_clicks = sum([r.get('clicks', 0) for r in recent])
                r_impr = sum([r.get('impressions', 0) for r in recent])
                p_clicks = sum([r.get('clicks', 0) for r in prior])
                p_impr = sum([r.get('impressions', 0) for r in prior])
                r_ctr = r_clicks / max(1, r_impr)
                p_ctr = p_clicks / max(1, p_impr)
                # z-test for proportions (manual)
                try:
                    pooled = (r_clicks + p_clicks) / max(1, (r_impr + p_impr))
                    se = sqrt(pooled * (1 - pooled) * (1 / max(1, r_impr) + 1 / max(1, p_impr)))
                    z = (r_ctr - p_ctr) / max(1e-9, se)
                    pval = normal_two_sided_pvalue(z)
                except Exception:
                    pval = None
                evidence = f'recent_ctr={r_ctr:.4f}, prior_ctr={p_ctr:.4f}'
                validated = (pval is not None and pval < 0.05 and r_ctr < p_ctr)
                conf = h.get('confidence', 0.5)
                if pval is not None:
                    conf = min(0.95, conf + (0.5 if validated else -0.2))
                h_res = {**h, 'validated': bool(validated) if pval is not None else None, 'evidence': evidence, 'p_value': pval, 'confidence': float(conf)}
                results.append(h_res)
            else:
                results.append({**h, 'validated': None, 'evidence': 'Global check not implemented', 'p_value': None})
        return results
