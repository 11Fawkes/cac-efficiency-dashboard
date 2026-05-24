"""
CAC Efficiency Dashboard — Multi-Company Channel Scenario Modeller
Targets: AboutYou (pre-acquisition) · Zalando · Delivery Hero
Stack: Python · Streamlit · Plotly · SciPy
"""

import streamlit as st

from data.profiles.aboutyou import PROFILE as ABOUTYOU
from data.profiles.zalando import PROFILE as ZALANDO
from data.profiles.delivery_hero import PROFILE as DELIVERY_HERO
from data.benchmarks import CHANNEL_BENCHMARKS, LTV_CAC_BENCHMARKS
from model.cac_model import (
    calculate_cac_per_channel,
    calculate_blended_cac,
    score_efficiency,
    model_budget_reallocation,
)
from model.confidence import confidence_badge_html, all_channel_confidence
from recommendations import generate_recommendations
from charts import (
    cac_bar_with_confidence,
    efficiency_scatter,
    blended_cac_trend,
    diminishing_returns_plot,
)

st.set_page_config(
    page_title="CAC Efficiency Dashboard | Multi-Company",
    page_icon="📈",
    layout="wide",
)

st.markdown(
    """
    <style>
    .scenario-badge {
        background:#78350F; color:#FEF3C7; padding:3px 8px;
        border-radius:4px; font-size:0.75rem; font-weight:700;
        letter-spacing:0.05em;
    }
    .disclosed-badge {
        background:#166534; color:#BBF7D0; padding:2px 6px;
        border-radius:4px; font-size:0.72rem; font-weight:600;
    }
    .estimated-badge {
        background:#1E3A5F; color:#BAE6FD; padding:2px 6px;
        border-radius:4px; font-size:0.72rem; font-weight:600;
    }
    .modelled-badge {
        background:#4A1D96; color:#DDD6FE; padding:2px 6px;
        border-radius:4px; font-size:0.72rem; font-weight:600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

PROFILES = {
    "AboutYou (Pre-Acquisition, FY2024/25)": ABOUTYOU,
    "Zalando (Combined Entity, FY2025)": ZALANDO,
    "Delivery Hero (FY2024)": DELIVERY_HERO,
}

PROV_BADGE = {
    "DISCLOSED": '<span class="disclosed-badge">DISCLOSED</span>',
    "ESTIMATED": '<span class="estimated-badge">ESTIMATED</span>',
    "MODELLED": '<span class="modelled-badge">MODELLED</span>',
}

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("CAC Efficiency Dashboard")
st.markdown(
    "**Multi-company channel scenario modeller** for fashion e-commerce acquisition efficiency. "
    "Profiles: AboutYou (pre-acquisition) · Zalando · Delivery Hero. "
    '<span class="scenario-badge">CHANNEL SPLITS = SCENARIO ASSUMPTION</span> '
    "— not disclosed figures. Confidence indicators shown throughout.",
    unsafe_allow_html=True,
)
st.divider()

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
st.sidebar.header("Company Profile")
selected_name = st.sidebar.selectbox(
    "Select Company",
    options=list(PROFILES.keys()),
    index=0,
)
profile = PROFILES[selected_name]

st.sidebar.markdown(f"**Status:** {profile['status']}")
st.sidebar.markdown(f"> *{profile['narrative']}*")
st.sidebar.divider()

st.sidebar.subheader("Channel Split Adjustments")
st.sidebar.caption(
    "These are SCENARIO ASSUMPTIONS derived from public signals. "
    "Adjust to model different budget allocation scenarios."
)

channel_keys = list(profile["channel_splits"].keys())
adjusted_splits = {}
total_split = 0.0

for key in channel_keys:
    ch = profile["channel_splits"][key]
    conf_badge = confidence_badge_html(ch["confidence"])
    adjusted_splits[key] = st.sidebar.slider(
        f"{ch['label']} ({ch['confidence']})",
        min_value=0,
        max_value=60,
        value=int(ch["split_pct"] * 100),
        help=ch["signal_basis"],
    ) / 100
    total_split += adjusted_splits[key]

split_sum = sum(adjusted_splits.values())
if abs(split_sum - 1.0) > 0.005:
    st.sidebar.warning(
        f"Channel splits sum to {split_sum*100:.1f}% — should total 100%. "
        "Adjust sliders to rebalance."
    )

# Build a modified profile with adjusted splits
adjusted_profile = dict(profile)
adjusted_profile = {**profile}
adjusted_channel_splits = {}
for key in channel_keys:
    adjusted_channel_splits[key] = {
        **profile["channel_splits"][key],
        "split_pct": adjusted_splits[key],
    }
adjusted_profile = {**profile, "channel_splits": adjusted_channel_splits}

# ---------------------------------------------------------------------------
# Run model
# ---------------------------------------------------------------------------
channel_results = calculate_cac_per_channel(adjusted_profile)
blended_cac = calculate_blended_cac(adjusted_profile)
ratings = score_efficiency(channel_results)

delta_pct = {
    key: adjusted_splits[key] - profile["channel_splits"][key]["split_pct"]
    for key in channel_keys
}
reallocation_result = model_budget_reallocation(profile, delta_pct)

recs = generate_recommendations(adjusted_profile, channel_results, reallocation_result)

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab_overview, tab_channel, tab_scenario, tab_about = st.tabs(
    ["Overview", "Channel Detail", "Scenario Modeller", "About"]
)

# ============================================================
# TAB 1 — OVERVIEW
# ============================================================
with tab_overview:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Marketing Spend",
            f"€{profile['marketing_spend_eur']/1e6:.0f}M",
            delta=f"{profile['marketing_spend_pct_revenue']*100:.1f}% of revenue",
            delta_color="off",
        )
    with col2:
        st.metric(
            "Blended CAC (scenario)",
            f"€{blended_cac:.0f}",
            help="Total marketing spend / total customers. Scenario figure.",
        )
    with col3:
        customers = profile.get("customers")
        st.metric(
            "Customers",
            f"{customers/1e6:.1f}M" if customers else "N/A",
            delta=PROV_BADGE.get(profile["customers_provenance"], ""),
            delta_color="off",
        )
    with col4:
        st.metric(
            "Avg Order Value",
            f"€{profile['aov_eur']}",
            delta=PROV_BADGE.get(profile["aov_provenance"], ""),
            delta_color="off",
        )

    st.divider()

    # Cross-company comparison bar
    all_blended = []
    for name, p in PROFILES.items():
        b_cac = calculate_blended_cac(p)
        all_blended.append({
            "name": name.split("(")[0].strip(),
            "blended_cac": b_cac,
            "marketing_pct": p["marketing_spend_pct_revenue"],
        })

    fig = blended_cac_trend(all_blended)
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "Blended CAC derived from total marketing spend / customer base. "
        "Marketing spend figures: AboutYou = DISCLOSED (FY2024/25 Annual Report); "
        "Zalando = ESTIMATED; Delivery Hero = DISCLOSED (FY2024 Annual Report)."
    )

    st.divider()
    st.subheader("Growth Analysis")
    for i, rec in enumerate(recs, 1):
        if i == 1:
            st.markdown(f"**{i}.** {rec}")
        else:
            st.markdown(f"**{i}.** {rec}", unsafe_allow_html=True)

# ============================================================
# TAB 2 — CHANNEL DETAIL
# ============================================================
with tab_channel:
    st.markdown(
        f'<span class="scenario-badge">SCENARIO ASSUMPTION</span> '
        "Channel splits are modelled under assumed budget distributions derived from "
        "public signals. Not disclosed figures.",
        unsafe_allow_html=True,
    )
    st.markdown("")

    fig = cac_bar_with_confidence(channel_results, profile["display_name"])
    st.plotly_chart(fig, use_container_width=True)

    fig2 = efficiency_scatter(channel_results, profile["display_name"])
    st.plotly_chart(fig2, use_container_width=True)

    # Confidence + detail table
    st.subheader("Channel Detail Table")
    rows = []
    for key, data in channel_results.items():
        rows.append({
            "Channel": data["label"],
            "Scenario Split": f"{data['split_pct']*100:.0f}%",
            "Scenario Spend (€M)": f"€{data['spend_eur']/1e6:.1f}M",
            "Scenario CAC": f"€{data['cac_eur']:.0f}" if data.get("cac_eur") else "N/A",
            "Benchmark CAC (mid)": f"€{data['benchmark_mid']}" if data.get("benchmark_mid") else "N/A",
            "Confidence": data["confidence"],
            "Efficiency": ratings.get(key, "N/A"),
        })
    st.dataframe(rows, use_container_width=True)
    st.caption(profile["channel_split_disclaimer"])

# ============================================================
# TAB 3 — SCENARIO MODELLER
# ============================================================
with tab_scenario:
    st.markdown(
        "Adjust channel splits in the sidebar to model budget reallocation impact. "
        "All outputs use industry benchmark CAC per channel as the modelling basis."
    )

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric(
            "Original Blended CAC",
            f"€{reallocation_result['original_blended_cac']:.0f}",
        )
    with col_b:
        delta_val = reallocation_result["cac_delta"]
        st.metric(
            "Scenario Blended CAC",
            f"€{reallocation_result['new_blended_cac']:.0f}",
            delta=f"€{delta_val:+.0f} vs original",
            delta_color="inverse",
        )
    with col_c:
        st.metric(
            "CAC Change",
            f"{reallocation_result['cac_delta_pct']*100:+.1f}%",
            delta_color="inverse",
        )

    st.caption(reallocation_result["scenario_note"])
    st.divider()

    # Diminishing returns for top-spend channel
    if channel_results:
        top_channel_key = max(
            channel_results,
            key=lambda k: channel_results[k].get("spend_eur", 0),
        )
        top_ch = channel_results[top_channel_key]
        bench = CHANNEL_BENCHMARKS.get(top_channel_key, {})

        if top_ch.get("spend_eur") and bench.get("cac_mid"):
            st.subheader(f"Diminishing Returns — {top_ch['label']}")
            st.caption(
                "Illustrative model showing how CAC increases as spend scales "
                "beyond the efficient range. For directional analysis only."
            )
            fig3 = diminishing_returns_plot(
                channel_key=top_channel_key,
                channel_label=top_ch["label"],
                current_spend=top_ch["spend_eur"],
                benchmark_cac=bench["cac_mid"],
            )
            st.plotly_chart(fig3, use_container_width=True)

# ============================================================
# TAB 4 — ABOUT
# ============================================================
with tab_about:
    st.subheader("About this tool")
    st.markdown(
        """
        **CAC Efficiency Dashboard** models the impact of budget reallocation under
        assumed channel splits for three Berlin-ecosystem companies.

        **Why multi-company?**
        - **AboutYou** — acquired by Zalando for €1.2B (July 2025). The acquisition *validates*
          the thesis: CAC efficiency was a financially material problem. Framed as historical.
        - **Zalando** — post-acquisition entity now managing ~52M customers across 25 markets.
          Two customer bases, two brand identities, one budget.
        - **Delivery Hero** — still independently listed (DHER), Berlin HQ, €800M+ marketing
          across 70+ markets. The most active live acquisition efficiency problem in Berlin tech.

        **Data sources**
        | Company | Source | Status |
        |---|---|---|
        | AboutYou marketing spend €244M | FY2024/25 Annual Report | DISCLOSED |
        | AboutYou customers 12.9M | Zalando acquisition docs | DISCLOSED |
        | Zalando revenue €10.5B | FY2025 Annual Report | DISCLOSED |
        | Delivery Hero revenue €8.7B | FY2024 Annual Report | DISCLOSED |
        | Channel CAC benchmarks | AppsFlyer 2024, Adjust 2024 | ESTIMATED |
        | Channel splits | Meta Ad Library, SimilarWeb | SCENARIO ASSUMPTION |

        **Framing note:** Channel splits are *scenario assumptions* derived from public signals —
        not disclosed figures. Each channel carries a HIGH / MEDIUM / LOW confidence indicator
        based on signal quality. Scenario analysis under uncertainty is a core BA skill.
        """
    )

    st.subheader("Interview answer (AboutYou acquisition)")
    st.info(
        "\"I started building this tool when AboutYou was independently listed and their "
        "management described marketing efficiency improvement as a strategic priority. "
        "Zalando acquired them for €1.2 billion in July 2025 — which validates that "
        "the CAC efficiency gap was a real and material business problem. The tool now "
        "includes Zalando's combined entity profile and Delivery Hero, so the analysis "
        "covers three of the largest acquisition spenders in Berlin's tech ecosystem.\""
    )

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.divider()
st.caption(
    "Dhruv Kumar · Berlin 2026 · "
    "[GitHub](https://github.com/11fawkes) · "
    "[LinkedIn](https://linkedin.com/in/dhruv-kumar-a54a2916b) · "
    "[Portfolio](https://11fawkes.github.io/Portfolio)"
)
