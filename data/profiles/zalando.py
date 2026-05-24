"""
Zalando (Combined Entity, Post-Acquisition) — FY2025 data.

Source: Zalando FY2025 Annual Report + post-acquisition integration disclosures.
Includes AboutYou's 12.9M customers following the July 2025 acquisition.
"""

PROFILE = {
    "id": "zalando",
    "display_name": "Zalando (Combined Entity, FY2025)",
    "status": "Frankfurt-listed (ZAL) · Now includes AboutYou (acquired July 2025)",
    "narrative": (
        "Post-acquisition, Zalando now faces the challenge of efficiently scaling "
        "acquisition across a ~52M-customer base with integration overhead. "
        "Two customer bases, two brand identities, one budget — "
        "the efficiency question is now more complex."
    ),

    # --- Financials --------------------------------------------------------
    "revenue_eur": 10_500_000_000,
    "revenue_source": "Zalando FY2025 Annual Report (~€10.5B combined entity).",
    "revenue_provenance": "DISCLOSED",

    "marketing_spend_eur": 1_050_000_000,
    "marketing_spend_source": (
        "Zalando FY2025 — approximately 10% of revenue on marketing/acquisition "
        "(integrating AboutYou spend). Source: Zalando FY2025 Annual Report."
    ),
    "marketing_spend_provenance": "ESTIMATED",

    "marketing_spend_pct_revenue": 0.10,

    "customers": 52_000_000,
    "customers_source": (
        "Zalando FY2025 — ~39M pre-acquisition + AboutYou's 12.9M customers "
        "across 26 European markets."
    ),
    "customers_provenance": "DISCLOSED",

    "aov_eur": 62,
    "aov_source": (
        "Blended AOV estimate: Zalando ~€64 (FY2025 disclosures) + "
        "AboutYou €59 (acquisition docs) weighted by customer base."
    ),
    "aov_provenance": "ESTIMATED",

    "markets": 25,
    "markets_source": "Zalando FY2025 Annual Report.",
    "markets_provenance": "DISCLOSED",

    "blended_cac_eur": None,

    "channel_splits": {
        "paid_social": {
            "label": "Paid Social (Meta/Instagram/TikTok)",
            "split_pct": 0.30,
            "confidence": "HIGH",
            "signal_basis": (
                "Meta Ad Library active campaigns. TikTok advertising presence. "
                "SimilarWeb social traffic trends. Zalando runs high-volume "
                "paid social at scale across EU markets."
            ),
        },
        "paid_search": {
            "label": "Paid Search (Google)",
            "split_pct": 0.25,
            "confidence": "MEDIUM",
            "signal_basis": (
                "SimilarWeb paid search %. SEMrush competitive keyword data. "
                "Zalando competes heavily on branded + category keywords."
            ),
        },
        "organic_seo": {
            "label": "Organic / SEO",
            "split_pct": 0.20,
            "confidence": "HIGH",
            "signal_basis": (
                "SimilarWeb organic search %. Zalando has strong domain authority "
                "and invests in content/SEO across 25 markets."
            ),
        },
        "influencer_affiliate": {
            "label": "Influencer / Affiliate",
            "split_pct": 0.15,
            "confidence": "LOW",
            "signal_basis": (
                "Zalando Partner Programme and creator partnerships inferred from "
                "brand announcements and Instagram engagement. LOW confidence."
            ),
        },
        "referral_crm_email": {
            "label": "Referral / CRM / Email",
            "split_pct": 0.10,
            "confidence": "MEDIUM",
            "signal_basis": (
                "Zalando Plus loyalty programme creates referral loop. "
                "Direct traffic % from SimilarWeb. Email marketing estimated "
                "from direct/return visitor share."
            ),
        },
    },

    "channel_split_disclaimer": (
        "SCENARIO ASSUMPTION: Channel splits are derived from public signals "
        "(Meta Ad Library, SimilarWeb, LinkedIn Ad Library). These are scenario "
        "assumptions, not disclosed figures."
    ),
}
