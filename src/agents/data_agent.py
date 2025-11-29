import csv
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple, Optional
from pathlib import Path


class DataAgent:
    def __init__(self, config):
        self.config = config
        # allow a missing config path and fall back to the bundled sample dataset
        cfg_path = config.get('data', {}).get('path') if config and isinstance(config, dict) else None
        if cfg_path:
            self.path = cfg_path
        else:
            # project-relative default
            self.path = str(Path('data') / 'synthetic_fb_ads_undergarments.csv')

    def _parse_row(self, row):
        # Convert types where possible
        out = dict(row)
        # parse date
        try:
            out['date'] = datetime.fromisoformat(row.get('date'))
        except Exception:
            try:
                out['date'] = datetime.strptime(row.get('date', ''), '%Y-%m-%d')
            except Exception:
                out['date'] = None
        for col in ['spend', 'impressions', 'clicks', 'purchases', 'revenue']:
            try:
                out[col] = float(row.get(col, 0) or 0)
            except Exception:
                out[col] = 0.0
        # keep creative_message as-is
        return out

    def load_and_summarize(self) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        # attempt to open the dataset; if missing, return empty summary
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for r in reader:
                    rows.append(self._parse_row(r))
        except FileNotFoundError:
            # Return empty structures but keep shapes expected by downstream code
            summary = {'overall': [], 'recent': [], 'samples': []}
            return rows, summary
        except Exception:
            summary = {'overall': [], 'recent': [], 'samples': []}
            return rows, summary

        # compute overall aggregates by campaign
        by_campaign = {}
        for r in rows:
            cname = r.get('campaign_name') or 'unknown'
            agg = by_campaign.setdefault(cname, {'spend': 0.0, 'impressions': 0.0, 'clicks': 0.0, 'purchases': 0.0, 'revenue': 0.0})
            agg['spend'] += r.get('spend', 0.0)
            agg['impressions'] += r.get('impressions', 0.0)
            agg['clicks'] += r.get('clicks', 0.0)
            agg['purchases'] += r.get('purchases', 0.0)
            agg['revenue'] += r.get('revenue', 0.0)

        overall = []
        for k, v in by_campaign.items():
            ctr = v['clicks'] / (v['impressions'] or 1)
            roas = v['revenue'] / (v['spend'] or 1)
            overall.append({'campaign_name': k, 'spend': v['spend'], 'impressions': v['impressions'], 'clicks': v['clicks'], 'purchases': v['purchases'], 'revenue': v['revenue'], 'ctr': ctr, 'roas': roas})

        # recent window
        recent_days = self.config.get('analysis', {}).get('recent_window_days', 14)
        max_date = max([r['date'] for r in rows if r['date'] is not None]) if rows else None
        recent_cut = (max_date - timedelta(days=recent_days)) if max_date else None
        recent_rows = [r for r in rows if r['date'] is not None and r['date'] >= recent_cut] if recent_cut else []

        by_campaign_recent = {}
        for r in recent_rows:
            cname = r.get('campaign_name') or 'unknown'
            agg = by_campaign_recent.setdefault(cname, {'spend': 0.0, 'impressions': 0.0, 'clicks': 0.0, 'purchases': 0.0, 'revenue': 0.0})
            agg['spend'] += r.get('spend', 0.0)
            agg['impressions'] += r.get('impressions', 0.0)
            agg['clicks'] += r.get('clicks', 0.0)
            agg['purchases'] += r.get('purchases', 0.0)
            agg['revenue'] += r.get('revenue', 0.0)

        recent = []
        for k, v in by_campaign_recent.items():
            ctr = v['clicks'] / (v['impressions'] or 1)
            roas = v['revenue'] / (v['spend'] or 1)
            recent.append({'campaign_name': k, 'spend': v['spend'], 'impressions': v['impressions'], 'clicks': v['clicks'], 'purchases': v['purchases'], 'revenue': v['revenue'], 'ctr': ctr, 'roas': roas})

        summary = {
            'overall': sorted(overall, key=lambda x: x.get('spend', 0), reverse=True)[:20],
            'recent': sorted(recent, key=lambda x: x.get('spend', 0), reverse=True)[:20],
            'samples': rows[:50]
        }
        return rows, summary
