"""
Confidence indicator engine.
Returns HIGH / MEDIUM / LOW per channel per company profile,
and renders styled badges for Streamlit.
"""

CONFIDENCE_COLORS = {
    "HIGH": {"bg": "#166534", "text": "#BBF7D0"},
    "MEDIUM": {"bg": "#1E3A5F", "text": "#BAE6FD"},
    "LOW": {"bg": "#78350F", "text": "#FEF3C7"},
}


def get_confidence(profile: dict, channel_key: str) -> str:
    """Return HIGH / MEDIUM / LOW for the given channel in the given profile."""
    return profile["channel_splits"].get(channel_key, {}).get("confidence", "LOW")


def confidence_badge_html(level: str) -> str:
    """Return an HTML badge string for inline Streamlit markdown."""
    c = CONFIDENCE_COLORS.get(level, CONFIDENCE_COLORS["LOW"])
    return (
        f'<span style="background:{c["bg"]};color:{c["text"]};'
        f'padding:2px 7px;border-radius:4px;font-size:0.72rem;font-weight:600;">'
        f'{level}</span>'
    )


def all_channel_confidence(profile: dict) -> dict[str, str]:
    """Return {channel_key: confidence_level} for all channels in the profile."""
    return {
        key: data["confidence"]
        for key, data in profile["channel_splits"].items()
    }
