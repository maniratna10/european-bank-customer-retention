from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt


# Matplotlib defaults for the dark dashboard.
plt.rcParams.update({
    "figure.facecolor": "#17211c",
    "axes.facecolor": "#17211c",
    "axes.edgecolor": "#81958a",
    "axes.labelcolor": "#d8e5dc",
    "xtick.color": "#c0cec5",
    "ytick.color": "#c0cec5",
    "text.color": "#e5ece7",
    "grid.color": "#34463c",
    "savefig.facecolor": "#17211c",
})

st.set_page_config(page_title="European Bank | Customer Insights", page_icon="EB", layout="wide")

# A restrained editorial style: warm background, clear hierarchy and minimal decoration.
st.markdown("""
<style>
/* Force the whole Streamlit canvas into a consistent dark palette */
:root { color-scheme: dark; }
html, body, [data-testid="stApp"], .stApp,
[data-testid="stAppViewContainer"], [data-testid="stMain"],
[data-testid="stMainBlockContainer"], section.main {
    background: #101715 !important;
    color: #e6eee8 !important;
}
[data-testid="stHeader"] { background: #101715 !important; }
[data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child {
    background: #17221d !important;
    border-right: 1px solid #2b3c33 !important;
}
[data-testid="stSidebar"] * { color: #d5e1d9 !important; }
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] textarea,
[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="popover"] {
    background-color: #202d26 !important;
    color: #e7efe9 !important;
    border-color: #3b5145 !important;
}
[data-testid="stFileUploader"], [data-testid="stFileUploader"] section {
    background: #202d26 !important; color: #dce8e0 !important;
}
.page-kicker { color: #8eaa99; font-size: .72rem; letter-spacing: .16em;
    text-transform: uppercase; font-weight: 700; margin-bottom: .35rem; }
.page-title { color: #e6f0e9; font-family: Georgia, 'Times New Roman', serif;
    font-size: 2.25rem; line-height: 1.12; margin: 0 0 .35rem 0; }
.page-subtitle { color: #a5b6ac; font-size: .96rem; margin-bottom: 1.35rem; }
.section-heading { color: #dcebe1; font-family: Georgia, 'Times New Roman', serif;
    font-size: 1.45rem; margin: .3rem 0 .35rem 0; }
.section-note { color: #a1b2a8; font-size: .88rem; margin-bottom: .9rem; }
[data-testid="stMetric"] { background: #1b2922 !important; border: 1px solid #34483c !important;
    border-radius: 7px; padding: 14px 16px; box-shadow: none; }
[data-testid="stMetricLabel"] { color: #a8b9ae !important; }
[data-testid="stMetricValue"] { color: #e5f1e9 !important; font-family: Georgia, serif; }
[data-testid="stMetricDelta"] { color: #9fc8ad !important; }
div[data-testid="stTabs"] button { color: #b4c5ba !important; font-weight: 600; }
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #b9e0c5 !important; border-bottom-color: #78a889 !important;
}
.analyst-note { background: #1b2b23; border-left: 3px solid #79a78a;
    padding: 12px 15px; color: #d1e2d7; font-size: .9rem; margin: .65rem 0 1rem 0; }
.source-line { color: #91a398; font-size: .75rem; border-top: 1px solid #2b3a32;
    padding-top: 12px; margin-top: 22px; }
[data-testid="stDataFrame"], [data-testid="stTable"] { background: #18231e !important; }
[data-testid="stDataFrame"] * { color: #e0e9e3 !important; }
.stAlert { background: #1a2821 !important; color: #dce9e1 !important; }
p, label, span { color: inherit; }
.block-container { padding-top: 2rem; max-width: 1440px; }
</style>
<div class="page-kicker">European Bank · Customer analytics</div>
<div class="page-title">Customer engagement & product use</div>
<div class="page-subtitle">A practical review of relationship depth, inactivity and customer exits</div>
""", unsafe_allow_html=True)

DEFAULT_FILE = Path(__file__).parent / "data" / "European_Bank.csv"

@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        raw = pd.read_csv(uploaded_file)
    else:
        raw = pd.read_csv(DEFAULT_FILE)
    required = ["CustomerId", "Geography", "Age", "Tenure", "Balance", "NumOfProducts",
                "HasCrCard", "IsActiveMember", "EstimatedSalary", "Exited"]
    missing = sorted(set(required) - set(raw.columns))
    if missing:
        raise ValueError("Required columns missing: " + ", ".join(missing))
    return raw

uploaded = st.sidebar.file_uploader("Use another CSV (optional)", type=["csv"])
try:
    data = load_data(uploaded)
except Exception as exc:
    st.error(f"Could not load the dataset: {exc}")
    st.stop()

st.sidebar.markdown("## Analysis controls")
st.sidebar.caption("Adjust the customer group shown in the report below.")
countries = sorted(data["Geography"].dropna().unique().tolist())
selected_countries = st.sidebar.multiselect("Geography", countries, default=countries)
active_filter = st.sidebar.selectbox("Engagement status", ["All", "Active", "Inactive"])
min_products, max_products = int(data.NumOfProducts.min()), int(data.NumOfProducts.max())
product_range = st.sidebar.slider("Number of products", min_products, max_products, (min_products, max_products))
balance_floor = float(data.Balance.min())
balance_ceiling = float(data.Balance.max())
balance_range = st.sidebar.slider("Balance range", balance_floor, balance_ceiling,
                                   (balance_floor, balance_ceiling), step=1000.0)
salary_floor = float(data.EstimatedSalary.min())
salary_ceiling = float(data.EstimatedSalary.max())
salary_range = st.sidebar.slider("Estimated salary range", salary_floor, salary_ceiling,
                                  (salary_floor, salary_ceiling), step=1000.0)

filtered = data[
    data.Geography.isin(selected_countries) &
    data.NumOfProducts.between(*product_range) &
    data.Balance.between(*balance_range) &
    data.EstimatedSalary.between(*salary_range)
].copy()
if active_filter == "Active":
    filtered = filtered[filtered.IsActiveMember.eq(1)]
elif active_filter == "Inactive":
    filtered = filtered[filtered.IsActiveMember.eq(0)]

if filtered.empty:
    st.warning("No customers match the selected filters. Widen the filters to continue.")
    st.stop()

filtered["EngagementProfile"] = np.select(
    [
        (filtered.IsActiveMember.eq(1)) & (filtered.NumOfProducts.ge(2)),
        (filtered.IsActiveMember.eq(0)) & (filtered.Balance.ge(filtered.Balance.median())),
        (filtered.IsActiveMember.eq(1)) & (filtered.NumOfProducts.eq(1)),
        filtered.IsActiveMember.eq(0)
    ],
    ["Active / broader relationship", "Inactive / higher balance",
     "Active / single product", "Inactive / lower balance"],
    default="Other"
)
filtered["RelationshipStrengthIndex"] = (
    filtered.IsActiveMember * 40 +
    (filtered.NumOfProducts.clip(upper=2) / 2) * 40 +
    filtered.HasCrCard * 20
).round(0)

n = len(filtered)
churn = filtered.Exited.mean()
active = filtered[filtered.IsActiveMember.eq(1)]
inactive = filtered[filtered.IsActiveMember.eq(0)]
active_churn = active.Exited.mean() if len(active) else np.nan
inactive_churn = inactive.Exited.mean() if len(inactive) else np.nan
high_balance_cut = float(st.sidebar.number_input("High-balance threshold", min_value=0.0,
                                  value=100000.0, step=10000.0))
premium_risk = filtered[(filtered.IsActiveMember.eq(0)) & (filtered.Balance.ge(high_balance_cut))]
premium_risk_churn = premium_risk.Exited.mean() if len(premium_risk) else np.nan

k1,k2,k3,k4 = st.columns(4)
k1.metric("Customers in view", f"{n:,}")
k2.metric("Churn rate", f"{churn:.1%}")
k3.metric("Active customer churn", "—" if pd.isna(active_churn) else f"{active_churn:.1%}")
k4.metric("Inactive customer churn", "—" if pd.isna(inactive_churn) else f"{inactive_churn:.1%}")

tab1, tab2, tab3, tab4 = st.tabs(["Engagement & churn", "Product utilization", "At-risk customers", "Retention strength"])

with tab1:
    st.markdown('<div class="section-heading">Engagement and customer exits</div><div class="section-note">A comparison of the activity flag against the recorded exit outcome.</div>', unsafe_allow_html=True)
    a,b = st.columns(2)
    with a:
        labels = ["Active", "Inactive"]
        vals = [active_churn if not pd.isna(active_churn) else 0,
                inactive_churn if not pd.isna(inactive_churn) else 0]
        fig, ax = plt.subplots()
        ax.bar(labels, vals, color=["#78a889", "#b87968"], width=0.58)
        ax.set_ylabel("Observed churn rate")
        ax.set_ylim(0, max(vals+[0.05])*1.2)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0%}"))
        st.pyplot(fig)
        plt.close(fig)
    with b:
        prof = filtered.groupby("EngagementProfile", observed=True).agg(
            Customers=("Exited","size"), ChurnRate=("Exited","mean")).reset_index()
        st.dataframe(prof.style.format({"ChurnRate":"{:.1%}"}), use_container_width=True)
    st.markdown('<div class="analyst-note"><strong>Reading the result.</strong> In this extract, inactive customers leave more often than active customers. The activity field is only a broad proxy, so transaction recency and channel usage would help explain the difference.</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-heading">Product breadth and retention</div><div class="section-note">Observed exit rates by number of products held, with group sizes shown for context.</div>', unsafe_allow_html=True)
    product_stats = filtered.groupby("NumOfProducts").agg(
        Customers=("Exited","size"), ChurnRate=("Exited","mean")).reset_index()
    fig, ax = plt.subplots()
    ax.bar(product_stats.NumOfProducts.astype(str), product_stats.ChurnRate, color="#78a889", width=0.58)
    ax.set_xlabel("Number of products")
    ax.set_ylabel("Observed churn rate")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0%}"))
    st.pyplot(fig)
    plt.close(fig)
    st.dataframe(product_stats.style.format({"ChurnRate":"{:.1%}"}), use_container_width=True)
    card_stats = filtered.groupby("HasCrCard").agg(Customers=("Exited","size"), ChurnRate=("Exited","mean")).reset_index()
    card_stats["Card ownership"] = card_stats.HasCrCard.map({0:"No credit card",1:"Has credit card"})
    st.dataframe(card_stats[["Card ownership","Customers","ChurnRate"]].style.format({"ChurnRate":"{:.1%}"}), use_container_width=True)
    st.markdown('<div class="analyst-note"><strong>Analyst note.</strong> The relationship is not a straight line: the three- and four-product groups show unusually high exit rates. Check the segment sizes and customer journeys before recommending product bundles.</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-heading">Inactive customers with higher balances</div><div class="section-note">A review list for relationship teams; balance alone does not establish customer value or risk.</div>', unsafe_allow_html=True)
    st.write(f"Customers who are inactive and have balance at or above ₹/currency-unit {high_balance_cut:,.0f} (dataset currency is not specified): **{len(premium_risk):,}**")
    if len(premium_risk):
        st.metric("Observed churn in this segment", f"{premium_risk_churn:.1%}")
        display_cols = [c for c in ["CustomerId","Geography","Age","Tenure","Balance","NumOfProducts",
                                    "HasCrCard","IsActiveMember","EstimatedSalary","Exited"] if c in premium_risk]
        st.dataframe(premium_risk[display_cols].sort_values("Balance", ascending=False), use_container_width=True)
        st.download_button("Download at-risk segment CSV",
                           premium_risk[display_cols].to_csv(index=False).encode("utf-8"),
                           "high_value_disengaged_customers.csv", "text/csv")
    else:
        st.info("No customers meet the selected inactivity and balance criteria.")

with tab4:
    st.markdown('<div class="section-heading">Relationship strength overview</div><div class="section-note">A simple, transparent score for exploring customer groups—not a churn probability.</div>', unsafe_allow_html=True)
    st.write("Transparent descriptive score: activity (40 points), product depth (up to 40 points for two or more products), and credit-card ownership (20 points). It is a prioritisation aid, not a validated probability of retention.")
    fig, ax = plt.subplots()
    ax.hist(filtered.RelationshipStrengthIndex, bins=[-0.5,19.5,39.5,59.5,79.5,100.5], edgecolor="black")
    ax.set_xlabel("Relationship Strength Index")
    ax.set_ylabel("Customer count")
    st.pyplot(fig)
    plt.close(fig)
    score_summary = filtered.groupby(pd.cut(filtered.RelationshipStrengthIndex, [ -1, 39, 59, 79, 100])).agg(
        Customers=("Exited","size"), ChurnRate=("Exited","mean")).reset_index()
    st.dataframe(score_summary.style.format({"ChurnRate":"{:.1%}"}), use_container_width=True)
    st.metric("Average relationship score", f"{filtered.RelationshipStrengthIndex.mean():.1f}/100")

st.divider()
st.markdown('<div class="section-heading">Data checks</div><div class="section-note">Basic checks applied to the supplied customer extract.</div>', unsafe_allow_html=True)
quality = pd.DataFrame({
    "Check":["Rows loaded","Duplicate customer IDs","Missing values (all columns)","Invalid binary values"],
    "Result":[len(data), int(data.CustomerId.duplicated().sum()), int(data.isna().sum().sum()),
              int((~data.HasCrCard.isin([0,1])).sum() + (~data.IsActiveMember.isin([0,1])).sum() + (~data.Exited.isin([0,1])).sum())]
})
st.dataframe(quality, hide_index=True, use_container_width=True)
st.markdown('<div class="source-line">Source: supplied European_Bank.csv · Customer names are excluded from the analysis · Figures describe this extract and should be checked against operational records before action.</div>', unsafe_allow_html=True)
