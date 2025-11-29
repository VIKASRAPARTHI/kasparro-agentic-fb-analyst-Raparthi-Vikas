import random

class CreativeGenerator:
    def __init__(self, config=None):
        self.config = config or {}
        self.low_ctr = self.config.get('thresholds', {}).get('low_ctr', 0.02)

    def generate(self, df, summary):
        # Find campaigns with low recent CTR
        recents = summary.get('recent', [])
        candidates = [r for r in recents if r.get('ctr', 0) < self.low_ctr]
        out = []
        for c in candidates:
            cname = c.get('campaign_name')
            sample_msgs = self._sample_messages(df, cname)
            recs = []
            for i in range(3):
                head = self._variation_title(sample_msgs)
                body = self._variation_body(sample_msgs)
                cta = random.choice(['Shop now','Learn more','Get yours','Limited time'])
                recs.append({'id': f'{cname[:6]}_C{i+1}', 'headline': head, 'body': body, 'cta': cta, 'rationale': 'Variation derived from top-performing message patterns'})
            out.append({'campaign_name': cname, 'creative_recommendations': recs})
        return out

    def _sample_messages(self, df, campaign_name, n=20):
        # df is list of rows (dicts)
        if not isinstance(df, list):
            return []
        camp_msgs = [r.get('creative_message') for r in df if (r.get('campaign_name') or 'unknown') == campaign_name and r.get('creative_message')]
        # dedupe while preserving order
        seen = set()
        msgs = []
        for m in camp_msgs:
            if m not in seen:
                seen.add(m)
                msgs.append(m)
        random.shuffle(msgs)
        return msgs[:n]

    def _variation_title(self, msgs):
        if not msgs:
            return 'New Angle: Comfort Meets Style'
        m = random.choice(msgs)
        # simple heuristics: pick first 5-8 words and add hook
        words = m.split()
        title = ' '.join(words[:6])
        hooks = ['— Now 20% Off', 'Limited Run', 'Best Seller', 'Try Today']
        return f"{title} {random.choice(hooks)}"

    def _variation_body(self, msgs):
        if not msgs:
            return 'Upgrade your comfort with our newest undergarments. Soft, breathable, and built for all-day wear.'
        m = random.choice(msgs)
        return m + ' — Upgrade your comfort and confidence today.'
