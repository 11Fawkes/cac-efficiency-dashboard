"""
Plotly chart builders for the CAC Efficiency Dashboard.
All functions return plotly.graph_objects.Figure objects.
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots

BG_COLOR = "#0F1117"
PAPER_COLOR = "#0F1117"
GRID_COLOR = "#2D2D2D"
FONT_COLOR = "#FAFAFA"

CONFIDENCE_COLORS = {
    "HIGH": "#22C55E",
    "MEDIUM": "#3B82F6",
    "LOW": "#F59E0B",
}


def _base_layout(title: str) -> dict:
    return dict(
        title=dict(text=title, font=dict(color=FONT_COLOR, size=15)),
        paper_bgcolor=PAPER_COLOR,
        plot_bgcolor=BG_COLOR,
        font=dict(color=FONT_COLOR, size=12),
        xaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=50, r=30, t=60, b=60),
    )


def cac_bar_with_confidence(channel_results: dict, company_name: str) -> go.Figure:
    """
    Grouped bar: scenario CAC vs benchmark per channel.
    Bar colour encodes confidence level.
    """
    channels = []
    scenario_cacs = []
    bench_cacs = []
    bar_colors = []
    hover_texts = []

    for key, data in channel_results.items():
        if data.get("cac_eur") is None:
            continue
        channels.append(data["label"])
        scenario_cacs.append(data["cac_eur"])
        bench_cacs.append(data.get("benchmark_mid", 0))
        bar_colors.append(CONFIDENCE_COLORS.get(data["confidence"], "#9CA3AF"))
        hover_texts.append(
            f"{data['label']}<br>"
            f"Scenario CAC: €{data['cac_eur']:.0f}<br>"
            f"Benchmark: €{data.get('benchmark_mid', 'N/A')}<br>"
            f"Confidence: {data['confidence']}<br>"
            f"Signal: {data['signal_basis'][:80]}…"
        )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name="Scenario CAC (assumed)",
            x=channels,
            y=scenario_cacs,
            marker_color=bar_colors,
            text=[f"€{v:.0f}" for v in scenario_cacs],
            textposition="outside",
            hovertext=hover_texts,
            hoverinfo="text",
        )
    )

    fig.add_trace(
        go.Scatter(
            name="Industry Benchmark (mid)",
            x=channels,
            y=bench_cacs,
            mode="markers",
            marker=dict(symbol="diamond", size=10, color="#F59E0B"),
            hovertemplate="%{x}<br>Benchmark: €%{y}<extra>Benchmark</extra>",
        )
    )

    layout = _base_layout(f"CAC by Channel — {company_name} (Scenario Assumption)")
    layout["yaxis"]["title"] = "CAC (€ per customer)"
    layout["xaxis"]["tickangle"] = -20
    layout["barmode"] = "group"
    fig.update_layout(**layout)

    fig.add_annotation(
        text="Bar colour: GREEN=HIGH confidence · BLUE=MEDIUM · AMBER=LOW",
        xref="paper", yref="paper", x=0, y=-0.18,
        showarrow=False, font=dict(size=10, color="#9CA3AF"),
    )

    return fig


def efficiency_scatter(channel_results: dict, company_name: str) -> go.Figure:
    """
    Scatter: channel spend (x) vs CAC efficiency score (y).
    Bubble size = budget allocated. Colour = confidence.
    """
    fig = go.Figure()

    for key, data in channel_results.items():
        if data.get("cac_eur") is None or data.get("efficiency_score") is None:
            continue
        color = CONFIDENCE_COLORS.get(data["confidence"], "#9CA3AF")
        fig.add_trace(
            go.Scatter(
                x=[data["spend_eur"] / 1e6],
                y=[data["efficiency_score"]],
                mode="markers+text",
                text=[data["label"].split("(")[0].strip()],
                textposition="top center",
                marker=dict(
                    size=max(12, data["split_pct"] * 120),
                    color=color,
                    opacity=0.85,
                    line=dict(color="white", width=1),
                ),
                name=data["label"],
                hovertemplate=(
                    f"{data['label']}<br>"
                    f"Spend: €%{{x:.0f}}M<br>"
                    f"Efficiency score: %{{y:.2f}}<br>"
                    f"(>1.0 = better than benchmark)<br>"
                    f"Confidence: {data['confidence']}<extra></extra>"
                ),
            )
        )

    fig.add_hline(
        y=1.0, line_dash="dot", line_color="#6B7280",
        annotation_text="Benchmark = 1.0",
        annotation_position="right",
        annotation_font_color="#6B7280",
    )

    layout = _base_layout(f"Channel Efficiency — {company_name}")
    layout["showlegend"] = False
    layout["xaxis"]["title"] = "Channel Spend (€M)"
    layout["yaxis"]["title"] = "Efficiency Score (>1 = beats benchmark)"
    fig.update_layout(**layout)
    return fig


def blended_cac_trend(profiles_data: list[dict]) -> go.Figure:
    """
    Bar chart comparing blended CAC across all three company profiles.
    profiles_data: [{"name": str, "blended_cac": float, "marketing_pct": float}]
    """
    names = [d["name"] for d in profiles_data]
    cacs = [d["blended_cac"] for d in profiles_data]
    mkt_pcts = [d["marketing_pct"] * 100 for d in profiles_data]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            name="Blended CAC (€)",
            x=names,
            y=cacs,
            marker_color=["#6CC04A", "#3B82F6", "#F59E0B"],
            text=[f"€{c:.0f}" for c in cacs],
            textposition="outside",
            hovertemplate="%{x}<br>Blended CAC: €%{y:.0f}<extra></extra>",
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            name="Marketing % of Revenue",
            x=names,
            y=mkt_pcts,
            mode="markers+lines",
            marker=dict(size=10, color="#EF4444"),
            line=dict(color="#EF4444", dash="dot"),
            hovertemplate="%{x}<br>Marketing: %{y:.1f}% of revenue<extra></extra>",
        ),
        secondary_y=True,
    )

    layout = _base_layout("Blended CAC & Marketing Spend Intensity — All Profiles")
    layout["yaxis"] = dict(
        title="Blended CAC (€)", gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR
    )
    layout["yaxis2"] = dict(
        title="Marketing % of Revenue", overlaying="y", side="right", showgrid=False
    )
    fig.update_layout(**layout)
    return fig


def diminishing_returns_plot(
    channel_key: str,
    channel_label: str,
    current_spend: float,
    benchmark_cac: float,
    spend_multipliers: list[float] | None = None,
) -> go.Figure:
    """
    Illustrative diminishing returns curve for a single channel.
    Shows how CAC increases as spend increases beyond efficient range.
    """
    if spend_multipliers is None:
        spend_multipliers = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0]

    spends = [current_spend * m / 1e6 for m in spend_multipliers]
    # CAC increases with diminishing returns (log model)
    import math
    cacs = [benchmark_cac * (0.8 + 0.5 * math.log(m + 0.5)) for m in spend_multipliers]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=spends,
            y=cacs,
            mode="lines+markers",
            line=dict(color="#6CC04A", width=2.5),
            marker=dict(size=7),
            hovertemplate="Spend: €%{x:.1f}M<br>Est. CAC: €%{y:.0f}<extra></extra>",
        )
    )

    current_idx = spend_multipliers.index(1.0)
    fig.add_trace(
        go.Scatter(
            x=[spends[current_idx]],
            y=[cacs[current_idx]],
            mode="markers",
            marker=dict(size=14, color="#F59E0B", symbol="star"),
            name="Current spend level",
            hovertemplate=f"Current spend<br>€{spends[current_idx]:.1f}M<br>Est. CAC: €{cacs[current_idx]:.0f}<extra></extra>",
        )
    )

    layout = _base_layout(f"Diminishing Returns — {channel_label} (Illustrative)")
    layout["yaxis"]["title"] = "Estimated CAC (€)"
    layout["xaxis"]["title"] = "Channel Spend (€M)"
    fig.update_layout(**layout)

    fig.add_annotation(
        text="Illustrative model only — for directional scenario analysis",
        xref="paper", yref="paper", x=0, y=-0.15,
        showarrow=False, font=dict(size=10, color="#9CA3AF"),
    )

    return fig
