"""
Delivery Hero — FY2024 data.

Source: Delivery Hero FY2024 Annual Report.
Still independently Frankfurt-listed (DHER). Berlin-headquartered.
€800M+ marketing spend across 70+ markets — the strongest live anchor
for acquisition efficiency analysis.
"""

PROFILE = {
    "id": "delivery_hero",
    "display_name": "Delivery Hero (FY2024)",
    "status": "Frankfurt-listed (DHER) · Independent · Berlin HQ · 70+ markets",
    "narrative": (
        "Delivery Hero is still independently listed, still burning significant "
        "marketing spend on acquisition across 70+ markets. Berlin-headquartered, "
        "directly relevant to Berlin BA roles. No acquisition risk — the data anchor "
        "is live and the problem is active."
    ),

    # --- Financials --------------------------------------------------------
    "revenue_eur": 8_700_000_000,
    "revenue_source": "Delivery Hero FY2024 Annual Report (€8.7B revenue).",
    "revenue_provenance": "DISCLOSED",

    "marketing_spend_eur": 820_000_000,
    "marketing_spend_source": (
        "Delivery Hero FY2024 Annual Report — €800M+ on marketing and promotions. "
        "Includes rider acquisition, restaurant marketing, and consumer acquisition."
    ),
    "marketing_spend_provenance": "DISCLOSED",

    "marketing_spend_pct_revenue": 0.094,

    "gmv_eur": 33_000_000_000,
    "gmv_source": "Delivery Hero FY2024 Annual Report (€33B GMV).",
    "gmv_provenance": "DISCLOSED",

    "customers": None,
    "customers_source": (
        "Active users not separately disclosed; 70+ markets. "
        "Estimated 50M+ active users globally."
    ),
    "customers_provenance": "ESTIMATED",

    "aov_eur": 25,
    "aov_source": (
        "Derived: GMV €33B / estimated order volume. "
        "Food delivery AOV lower than fashion e-commerce."
    ),
    "aov_provenance": "MODELLED",

    "markets": 70,
    "markets_source": "Delivery Hero FY2024 Annual Report.",
    "markets_provenance": "DISCLOSED",

    "blended_cac_eur": None,

    "channel_splits": {
        "paid_social": {
            "label": "Paid Social (Meta/TikTok/Snap)",
            "split_pct": 0.35,
            "confidence": "HIGH",
            "signal_basis": (
                "Meta Ad Library: extensive multi-market campaigns. TikTok and "
                "Snapchat presence in younger-demographic markets. "
                "SimilarWeb social traffic %."
            ),
        },
        "paid_search": {
            "label": "Paid Search (Google)",
            "split_pct": 0.20,
            "confidence": "MEDIUM",
            "signal_basis": (
                "SimilarWeb paid search %. SEMrush — Delivery Hero brands "
                "(Talabat, Foodpanda, etc.) bid heavily on category keywords."
            ),
        },
        "organic_seo": {
            "label": "Organic / SEO",
            "split_pct": 0.10,
            "confidence": "HIGH",
            "signal_basis": (
                "SimilarWeb organic %. Multi-brand SEO across 70+ market domains. "
                "Relatively lower SEO share vs fashion — food delivery is intent-driven."
            ),
        },
        "influencer_affiliate": {
            "label": "Influencer / Affiliate",
            "split_pct": 0.15,
            "confidence": "LOW",
            "signal_basis": (
                "Brand partnership announcements across multiple markets. "
                "Restaurant partner co-marketing included here. LOW confidence."
            ),
        },
        "referral_crm_email": {
            "label": "Referral / CRM / App Push",
            "split_pct": 0.20,
            "confidence": "MEDIUM",
            "signal_basis": (
                "App-centric business model means push notification and in-app "
                "referral are disproportionately important vs fashion e-commerce. "
                "App Store review sentiment + direct traffic share."
            ),
        },
    },

    "channel_split_disclaimer": (
        "SCENARIO ASSUMPTION: Channel splits are derived from public signals "
        "(Meta Ad Library, SimilarWeb, LinkedIn Ad Library). These are scenario "
        "assumptions, not disclosed figures. Delivery Hero's multi-brand, "
        "multi-market structure means channel mix varies significantly by region."
    ),
}
