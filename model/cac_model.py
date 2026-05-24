"""
CAC model: calculates per-channel CAC, scores efficiency, and models
budget reallocation impact for a given company profile.
"""

from __future__ import annotations
from data.benchmarks import CHANNEL_BENCHMARKS, LTV_CAC_BENCHMARKS


def calculate_cac_per_channel(profile: dict) -> dict[str, dict]:
    """
    Calculate actual CAC per channel given the profile's marketing spend
    and assumed channel splits.

    Returns a dict keyed by channel_key:
      {
        "label": str,
        "spend_eur": float,
        "split_pct": float,
        "confidence": str,
        "cac_eur": float,       # spend / estimated customers acquired via channel
        "benchmark_mid": float, # industry mid benchmark
        "efficiency_score": float,  # benchmark_mid / cac (>1 = better than benchmark)
      }
    """
    total_spend = profile["marketing_spend_eur"]
    results = {}

    for key, ch in profile["channel_splits"].items():
        split_pct = ch["split_pct"]
        channel_spend = total_spend * split_pct

        bench = CHANNEL_BENCHMARKS.get(key, {})
        bench_mid = bench.get("cac_mid")

        # CAC estimated from benchmark midpoint for this channel type.
        # Each channel has a structurally different cost-per-acquisition based on
        # industry data (AppsFlyer 2024). This is the scenario assumption.
        cac = bench_mid if bench_mid else None

        # Customers this channel is estimated to acquire at its benchmark CAC
        channel_customers = (channel_spend / cac) if cac else None

        # Efficiency: blended_cac / channel_cac.
        # >1 means channel is cheaper than the blended average (efficient).
        # <1 means it's more expensive (inefficient).
        blended = calculate_blended_cac(profile)
        efficiency = (blended / cac) if (cac and blended) else 1.0

        results[key] = {
            "label": ch["label"],
            "spend_eur": channel_spend,
            "split_pct": split_pct,
            "confidence": ch["confidence"],
            "cac_eur": round(cac, 2) if cac else None,
            "benchmark_mid": bench_mid,
            "efficiency_score": round(efficiency, 2) if efficiency else None,
            "signal_basis": ch["signal_basis"],
        }

    return results


def calculate_blended_cac(profile: dict) -> float:
    """Blended CAC = total marketing spend / total customers."""
    customers = profile.get("customers") or _estimate_customers(profile)
    if not customers:
        return 0.0
    return profile["marketing_spend_eur"] / customers


def score_efficiency(channel_results: dict) -> dict[str, str]:
    """
    Return an efficiency rating per channel:
    'excellent' | 'above benchmark' | 'at benchmark' | 'below benchmark' | 'poor'
    """
    ratings = {}
    for key, data in channel_results.items():
        score = data.get("efficiency_score")
        if score is None:
            ratings[key] = "insufficient data"
        elif score >= 1.5:
            ratings[key] = "excellent"
        elif score >= 1.1:
            ratings[key] = "above benchmark"
        elif score >= 0.9:
            ratings[key] = "at benchmark"
        elif score >= 0.7:
            ratings[key] = "below benchmark"
        else:
            ratings[key] = "poor"
    return ratings


def model_budget_reallocation(
    profile: dict,
    delta_pct: dict[str, float],
) -> dict:
    """
    Model the impact of reallocating budget across channels.

    Parameters
    ----------
    profile   : company profile dict
    delta_pct : {channel_key: delta_percentage_points}
                e.g. {"paid_social": -0.05, "referral_crm_email": +0.05}
                Must sum to approximately 0 (reallocation, not new spend).

    Returns
    -------
    {
      "original_blended_cac": float,
      "new_blended_cac": float,
      "cac_delta": float,
      "cac_delta_pct": float,
      "channel_detail": {channel_key: {original, new, delta}},
      "scenario_note": str,
    }
    """
    original_results = calculate_cac_per_channel(profile)
    original_blended = calculate_blended_cac(profile)

    total_spend = profile["marketing_spend_eur"]
    customers = profile.get("customers") or _estimate_customers(profile)

    new_customers = 0.0
    channel_detail = {}

    for key, ch in profile["channel_splits"].items():
        original_split = ch["split_pct"]
        new_split = max(0.0, original_split + delta_pct.get(key, 0.0))
        new_spend = total_spend * new_split

        bench = CHANNEL_BENCHMARKS.get(key, {})
        bench_mid = bench.get("cac_mid", 25)
        channel_new_customers = new_spend / bench_mid if bench_mid else 0

        new_customers += channel_new_customers

        channel_detail[key] = {
            "label": ch["label"],
            "original_split": original_split,
            "new_split": new_split,
            "original_spend": total_spend * original_split,
            "new_spend": new_spend,
            "benchmark_cac": bench_mid,
        }

    new_blended = total_spend / new_customers if new_customers > 0 else float("inf")
    cac_delta = new_blended - original_blended
    cac_delta_pct = cac_delta / original_blended if original_blended > 0 else 0

    return {
        "original_blended_cac": round(original_blended, 2),
        "new_blended_cac": round(new_blended, 2),
        "cac_delta": round(cac_delta, 2),
        "cac_delta_pct": round(cac_delta_pct, 4),
        "channel_detail": channel_detail,
        "scenario_note": (
            "Under this channel scenario assumption, budget reallocation modelled "
            "using industry benchmark CAC per channel (AppsFlyer 2024)."
        ),
    }


def _estimate_customers(profile: dict) -> int:
    """Fallback: estimate customers from revenue and AOV."""
    revenue = profile.get("revenue_eur", 0)
    aov = profile.get("aov_eur", 50)
    orders_per_customer = 8
    if revenue and aov:
        return int(revenue / aov / orders_per_customer)
    return 1_000_000
