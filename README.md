# CAC Efficiency Dashboard (Multi-Company)

Multi-company channel scenario modeller for fashion e-commerce acquisition efficiency.
Profiles: **AboutYou (pre-acquisition)** · **Zalando** · **Delivery Hero**

**Stack:** Python · Streamlit · Plotly · NumPy

---

## What it does

- Models CAC per channel under assumed budget splits for three companies
- All channel splits are labelled **SCENARIO ASSUMPTION** with HIGH/MEDIUM/LOW confidence
- Cross-company blended CAC comparison in a single view
- Scenario modeller: drag channel sliders to model budget reallocation impact
- Diminishing returns curve for top-spend channel
- Business-language recommendations per profile

## The acquisition narrative

AboutYou was acquired by Zalando for **€1.2 billion** in July 2025 — which validates the thesis:
CAC efficiency was a real and financially material business problem. The tool now includes
Zalando's combined entity profile and Delivery Hero, covering three of the largest acquisition
spenders in Berlin's tech ecosystem.

## Company profiles

| Company | Revenue | Marketing Spend | Customers | Status |
|---|---|---|---|---|
| AboutYou (FY2024/25) | ~€2B | ~€244M (12.2%) | 12.9M | Zalando subsidiary |
| Zalando (FY2025) | ~€10.5B | ~€1.05B (10%) | ~52M | Frankfurt-listed (ZAL) |
| Delivery Hero (FY2024) | €8.7B | €800M+ (9.4%) | 50M+ est | Frankfurt-listed (DHER) |

## Data provenance

- `DISCLOSED` = taken directly from annual reports / acquisition documentation
- `ESTIMATED` = published industry benchmark (AppsFlyer 2024, Adjust 2024)
- `SCENARIO ASSUMPTION` = channel splits derived from public signals (Meta Ad Library, SimilarWeb)

## File structure

```
app.py                          Streamlit entry point (4 tabs)
data/
  profiles/
    aboutyou.py                 AboutYou FY2024/25 profile + channel scenario
    zalando.py                  Zalando FY2025 combined entity profile
    delivery_hero.py            Delivery Hero FY2024 profile
  benchmarks.py                 Industry CAC benchmarks (AppsFlyer, Adjust)
model/
  cac_model.py                  calculate_cac_per_channel(), model_budget_reallocation()
  confidence.py                 Confidence indicator engine
recommendations.py              Business-language recommendation engine
charts.py                       Plotly chart builders
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect the repo, set `app.py` as the entry point

---

*Dhruv Kumar · Berlin 2026 · [Portfolio](https://11fawkes.github.io/Portfolio)*
