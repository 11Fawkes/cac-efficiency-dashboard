"""
AboutYou (Pre-Acquisition) — FY2024/25 data.

Source: AboutYou FY2024/25 Annual Report + Zalando acquisition documentation
        (acquisition closed July 11, 2025; AboutYou fully delisted November 2025).

IMPORTANT CONTEXT: AboutYou was acquired by Zalando for €1.2B in July 2025.
All data here reflects the pre-acquisition standalone entity. The acquisition
validates the CAC efficiency thesis — Zalando paid €1.2B to solve the problem
this tool analyses.
"""

PROFILE = {
    "id": "aboutyou",
    "display_name": "AboutYou (Pre-Acquisition, FY2024/25)",
    "status": "Acquired by Zalando July 2025 · Delisted November 2025",
    "narrative": (
        "I started building this tool when AboutYou was independently listed. "
        "Zalando paid €1.2B to acquire them in July 2025 — which validates that "
        "the CAC efficiency gap was a real and financially material business problem."
    ),

    # --- Financials --------------------------------------------------------
    "revenue_eur": 2_000_000_000,
    "revenue_source": "AboutYou FY2024/25 Annual Report (~€2B revenue)",
    "revenue_provenance": "DISCLOSED",

    "marketing_spend_eur": 244_000_000,
    "marketing_spend_source": (
        "AboutYou FY2024/25 Annual Report. ~12.2% of ~€2B revenue. "
        "Down from €420M (FY2023) — part of efficiency programme pre-acquisition."
    ),
    "marketing_spend_provenance": "DISCLOSED",

    "marketing_spend_pct_revenue": 0.122,

    "customers": 12_900_000,
    "customers_source": "Zalando acquisition documentation, July 2025.",
    "customers_provenance": "DISCLOSED",

    "aov_eur": 59,
    "aov_source": "Disclosed in Zalando acquisition documentation.",
    "aov_provenance": "DISCLOSED",

    "markets": 26,
    "markets_source": "AboutYou FY2024/25 Annual Report.",
    "markets_provenance": "DISCLOSED",

    # --- Derived CAC -------------------------------------------------------
    "blended_cac_eur": None,  # calculated by model

    # --- Channel splits (SCENARIO ASSUMPTION — not disclosed figures) ------
    # Confidence: HIGH = strong signal from multiple public sources
    #             MEDIUM = single source
    #             LOW = inference only
    "channel_splits": {
        "paid_social": {
            "label": "Paid Social (Meta/Instagram)",
            "split_pct": 0.38,
            "confidence": "HIGH",
            "signal_basis": (
                "Meta Ad Library: active ad count, estimated reach range, campaign duration. "
                "Cross-referenced with SimilarWeb social traffic %. "
                "Significant reduction in Meta spend observed FY2024 — consistent with "
                "€420M→€244M marketing cut."
            ),
        },
        "paid_search": {
            "label": "Paid Search (Google)",
            "split_pct": 0.22,
            "confidence": "MEDIUM",
            "signal_basis": (
                "SimilarWeb paid search traffic %. "
                "Relative to organic. Google Ads auction visibility (SEMrush free tier)."
            ),
        },
        "organic_seo": {
            "label": "Organic / SEO",
            "split_pct": 0.18,
            "confidence": "HIGH",
            "signal_basis": (
                "SimilarWeb organic search %. Consistent across multiple measurement periods. "
                "Most reliable channel to estimate from public data."
            ),
        },
        "influencer_affiliate": {
            "label": "Influencer / Affiliate",
            "split_pct": 0.12,
            "confidence": "LOW",
            "signal_basis": (
                "Inferred from brand partnership announcements and social media engagement "
                "patterns. Least reliable — flagged as LOW confidence."
            ),
        },
        "referral_crm_email": {
            "label": "Referral / CRM / Email",
            "split_pct": 0.10,
            "confidence": "MEDIUM",
            "signal_basis": (
                "App Store review sentiment patterns for referral programme mentions. "
                "Direct traffic % from SimilarWeb as proxy."
            ),
        },
    },

    "channel_split_disclaimer": (
        "SCENARIO ASSUMPTION: Channel splits are derived from public signals "
        "(Meta Ad Library, SimilarWeb, LinkedIn Ad Library). These are scenario "
        "assumptions, not disclosed figures. Each channel carries a confidence "
        "indicator (HIGH/MEDIUM/LOW) reflecting signal quality."
    ),
}
