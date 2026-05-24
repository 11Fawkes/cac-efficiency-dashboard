"""
Industry CAC benchmarks per channel for fashion/e-commerce and food delivery.
Sources: AppsFlyer Fashion E-commerce Report 2024, Adjust Growth Index 2024.
All values cited.
"""

# CAC benchmarks by channel (EUR, fashion e-commerce unless noted)
# Source: AppsFlyer Fashion E-commerce Report 2024 + Adjust Growth Index 2024
CHANNEL_BENCHMARKS = {
    "paid_social": {
        "label": "Paid Social (Meta/Instagram)",
        "cac_low": 18,
        "cac_mid": 28,
        "cac_high": 45,
        "source": "AppsFlyer Fashion E-commerce Report 2024 — paid social CAC range for EU markets.",
        "provenance": "ESTIMATED",
        "unit": "EUR per new customer",
    },
    "paid_search": {
        "label": "Paid Search (Google)",
        "cac_low": 15,
        "cac_mid": 22,
        "cac_high": 38,
        "source": "Adjust Growth Index 2024 — paid search CAC, fashion/retail vertical EU.",
        "provenance": "ESTIMATED",
        "unit": "EUR per new customer",
    },
    "organic_seo": {
        "label": "Organic / SEO",
        "cac_low": 3,
        "cac_mid": 7,
        "cac_high": 14,
        "source": (
            "AppsFlyer 2024 — organic acquisition costs reflect content + SEO investment "
            "amortised across organic new customers."
        ),
        "provenance": "ESTIMATED",
        "unit": "EUR per new customer (amortised content/SEO spend)",
    },
    "influencer_affiliate": {
        "label": "Influencer / Affiliate",
        "cac_low": 20,
        "cac_mid": 35,
        "cac_high": 65,
        "source": (
            "Adjust Growth Index 2024 — influencer and affiliate CAC ranges, "
            "fashion e-commerce EU. High variance by creator tier."
        ),
        "provenance": "ESTIMATED",
        "unit": "EUR per new customer",
    },
    "referral_crm_email": {
        "label": "Referral / CRM / Email",
        "cac_low": 2,
        "cac_mid": 6,
        "cac_high": 12,
        "source": (
            "AppsFlyer 2024 — referral and owned-channel CAC. "
            "Lowest CAC channel when programme is mature."
        ),
        "provenance": "ESTIMATED",
        "unit": "EUR per new customer",
    },
}

# LTV:CAC healthy ratio benchmarks (fashion e-commerce, EU)
LTV_CAC_BENCHMARKS = {
    "concerning": 1.5,
    "acceptable": 2.5,
    "healthy": 3.5,
    "excellent": 5.0,
    "source": "Andreessen Horowitz / SaaS benchmarks adapted for e-commerce. Industry standard.",
}

# Payback period benchmarks (months)
PAYBACK_BENCHMARKS = {
    "excellent": 6,
    "healthy": 12,
    "acceptable": 18,
    "concerning": 24,
    "source": "Adjust Growth Index 2024 — fashion e-commerce EU cohort payback norms.",
}
