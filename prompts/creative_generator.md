Creative Improvement Generator Prompt (structured)

Purpose: For campaigns/adsets flagged as low-CTR, generate alternative creative messages grounded in existing creative messaging.

Input: `campaign_summary` (top messages, CTR, impressions), `creative_messages_sample` (list), `constraints` (tone, max length)

Output JSON schema:
[
  {
    "campaign_name": "",
    "creative_recommendations": [
      {"id":"C1","headline":"","body":"","cta":"","rationale":""}
    ]
  }
]

Reasoning: Analyze common successful message patterns, propose variations across hooks (scarcity, social proof, benefit), CTAs, and readability.

Include: A diversity of voice and 3-5 candidates per low-CTR campaign. Flag if data is insufficient to suggest grounded changes.