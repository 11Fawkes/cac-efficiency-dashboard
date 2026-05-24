"""
Business-language recommendation engine for the CAC Efficiency Dashboard.
Returns stakeholder-grade insight strings per company profile.
"""

from __future__ import annotations
from model.cac_model import score_efficiency


EFFICIENCY_LABELS = {
    "excellent": "performing well above industry benchmark",
    "above benchmark": "above industry benchmark",
    "at benchmark": "roughly in line with industry benchmark",
    "below benchmark": "below industry benchmark — consider reallocation",
    "poor": "significantly underperforming — reallocate budget",
    "insufficient data": "insufficient data to benchmark",
}


def generate_recommendations(
    profile: dict,
    channel_results: dict,
    reallocation_result: dict | None = None,
) -> list[str]:
    """
    Return a list of stakeholder-grade recommendation strings.

    Parameters
    ----------
    profile           : company profile dict
    channel_results   : output of calculate_cac_per_channel()
    reallocation_result : output of model_budget_reallocation() if scenario was run
    """
    recs = []
    ratings = score_efficiency(channel_results)

    company_name = profile["display_name"]
    blended_cac = profile["marketing_spend_eur"] / profile["customers"] if profile.get("customers") else None
    blended_str = f"€{blended_cac:.0f}" if blended_cac else "N/A"

    # ---- Overview ----------------------------------------------------------
    mkt_pct = profile["marketing_spend_pct_revenue"] * 100
    recs.append(
        f"{company_name} spends approximately "
        f"€{profile['marketing_spend_eur']/1e6:.0f}M on marketing — "
        f"{mkt_pct:.1f}% of revenue. "
        f"Blended CAC: {blended_str}. "
        f"Under this channel scenario, the following efficiency gaps are modelled."
    )

    # ---- Per-channel insights ----------------------------------------------
    for key, data in channel_results.items():
        rating = ratings.get(key, "insufficient data")
        label_str = EFFICIENCY_LABELS.get(rating, rating)
        conf = data.get("confidence", "LOW")
        cac_str = f"€{data['cac_eur']:.0f}" if data.get("cac_eur") else "N/A"
        bench_str = f"€{data['benchmark_mid']}" if data.get("benchmark_mid") else "N/A"

        recs.append(
            f"**{data['label']}** [{conf} confidence] — "
            f"Scenario CAC: {cac_str} vs benchmark {bench_str}. "
            f"Under this scenario assumption, this channel is {label_str}."
        )

    # ---- Reallocation impact -----------------------------------------------
    if reallocation_result and reallocation_result.get("cac_delta") is not None:
        delta = reallocation_result["cac_delta"]
        delta_pct = reallocation_result["cac_delta_pct"] * 100
        direction = "reduces" if delta < 0 else "increases"
        recs.append(
            f"**Scenario reallocation:** {reallocation_result['scenario_note']} "
            f"The modelled shift {direction} blended CAC by €{abs(delta):.0f} "
            f"({abs(delta_pct):.1f}%) vs baseline — "
            f"from €{reallocation_result['original_blended_cac']:.0f} to "
            f"€{reallocation_result['new_blended_cac']:.0f}."
        )

    # ---- Company-specific context ------------------------------------------
    company_id = profile.get("id")
    if company_id == "aboutyou":
        recs.append(
            "**AboutYou context:** Zalando paid €1.2B to acquire AboutYou in July 2025 — "
            "which validates that the CAC efficiency gap was a real and financially "
            "material business problem. The same channel efficiency analysis now applies "
            "to Zalando integrating 12.9M new customers into a 52M-customer ecosystem."
        )
    elif company_id == "zalando":
        recs.append(
            "**Zalando integration context:** Post-acquisition, Zalando faces the challenge "
            "of efficiently scaling acquisition with two customer bases, two brand identities, "
            "and one consolidated budget. Channel efficiency decisions at this scale "
            "have material impact — €10B+ revenue with ~10% marketing spend."
        )
    elif company_id == "delivery_hero":
        recs.append(
            "**Delivery Hero context:** Still independently Frankfurt-listed (DHER). "
            "€800M+ marketing spend across 70+ markets makes this the most active "
            "acquisition efficiency challenge in Berlin's tech ecosystem. "
            "No acquisition risk — the data anchor is live."
        )

    return recs
