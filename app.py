"""
Revenue Growth & Personalization Analytics Dashboard
=====================================================
Run with:  streamlit run app.py
Place all CSV files in the same folder as app.py
"""

import random
import warnings
import pathlib

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Revenue Growth Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS — premium dark-accented theme
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

[data-testid="stAppViewContainer"] {
    background: linear-gradient(145deg,#f4f7ff 0%,#fafbff 55%,#f6f0ff 100%);
    min-height:100vh;
}
[data-testid="stHeader"] { background: transparent; }

html,body,[class*="css"],.stMarkdown,p,li,label,span,div {
    font-family:'Sora','Segoe UI',system-ui,sans-serif !important;
    color:#18192e;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#1a2550 0%,#0f1635 100%);
    border-right:2px solid #2a3a7a;
    box-shadow:4px 0 28px rgba(0,0,0,.25);
}
[data-testid="stSidebar"] * { color:#ffffff !important; }
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color:#a8c0ff !important; }
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div { color:#ffffff !important; }

/* Sidebar date inputs */
[data-testid="stSidebar"] input[type="text"],
[data-testid="stSidebar"] input[type="date"],
[data-testid="stSidebar"] input {
    background:#1e2d6b !important;
    color:#ffffff !important;
    border:1.5px solid #3a50a0 !important;
    border-radius:10px !important;
    caret-color:#ffffff !important;
}
[data-testid="stSidebar"] input::placeholder { color:#8899cc !important; }

/* Sidebar selectbox */
[data-testid="stSidebar"] .stSelectbox>div>div {
    background:#1e2d6b !important;
    border:1.5px solid #3a50a0 !important;
    color:#ffffff !important;
}
[data-testid="stSidebar"] .stSelectbox>div>div>div { color:#ffffff !important; }
[data-testid="stSidebar"] [data-baseweb="select"] * { color:#ffffff !important; }
[data-testid="stSidebar"] [data-baseweb="select"] [data-baseweb="popover"] {
    background:#1e2d6b !important;
}

/* Sidebar date picker calendar */
[data-testid="stSidebar"] [data-baseweb="calendar"],
[data-testid="stSidebar"] [data-baseweb="datepicker"] { background:#1e2d6b !important; }
[data-testid="stSidebar"] [data-baseweb="calendar"] * { color:#ffffff !important; }
[data-testid="stSidebar"] [data-baseweb="calendar"] button { color:#ffffff !important; background:transparent !important; }
[data-testid="stSidebar"] [data-baseweb="calendar"] [aria-selected="true"] {
    background:#426cff !important; color:#ffffff !important; border-radius:50% !important;
}

/* ── Global Popover / Dropdown menus (ALL selectboxes everywhere) ── */
[data-baseweb="popover"],
[data-baseweb="menu"],
ul[data-baseweb="menu"],
[role="listbox"],
[data-baseweb="select"] [role="listbox"] {
    background:#1e2d6b !important;
    border:1.5px solid #3a50a0 !important;
    border-radius:12px !important;
}
[data-baseweb="popover"] *,
[data-baseweb="menu"] *,
ul[data-baseweb="menu"] li,
[role="listbox"] *,
[role="option"] {
    color:#ffffff !important;
    background:transparent !important;
}
[role="option"]:hover,
[role="option"][aria-selected="true"],
li[role="option"]:hover {
    background:#2e45a0 !important;
    color:#ffffff !important;
}
/* Calendar popup global */
[data-baseweb="calendar"] {
    background:#1e2d6b !important;
    border:1.5px solid #3a50a0 !important;
    border-radius:14px !important;
}
[data-baseweb="calendar"] * { color:#ffffff !important; }
[data-baseweb="calendar"] button {
    color:#ffffff !important;
    background:transparent !important;
}
[data-baseweb="calendar"] [aria-selected="true"] {
    background:#426cff !important;
    color:#ffffff !important;
    border-radius:50% !important;
}
[data-baseweb="calendar"] [data-baseweb="select"] button,
[data-baseweb="calendar"] [data-baseweb="select"] div { color:#ffffff !important; }
/* Month/year header dropdowns inside calendar */
[data-baseweb="calendar"] [data-baseweb="select"] [role="listbox"],
[data-baseweb="calendar"] [data-baseweb="popover"] {
    background:#1e2d6b !important;
}
[data-baseweb="calendar"] [data-baseweb="select"] [role="option"] { color:#ffffff !important; }

/* Sidebar slider */
[data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"],
[data-testid="stSidebar"] .stSlider span { color:#ffffff !important; }

/* Sidebar markdown text */
[data-testid="stSidebar"] .stMarkdown * { color:#ffffff !important; }
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] .stCaption { color:#99aadd !important; }

/* Active filter card — force ALL text black */
.active-filters-card, .active-filters-card *,
.active-filters-card .af-label,
.active-filters-card .af-value,
[data-testid="stSidebar"] .active-filters-card,
[data-testid="stSidebar"] .active-filters-card *,
[data-testid="stSidebar"] .af-label,
[data-testid="stSidebar"] .af-value {
    color:#000000 !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background:rgba(255,255,255,.88);
    border-radius:18px;
    padding:7px;
    gap:5px;
    border:1.5px solid #dde6ff;
    backdrop-filter:blur(12px);
    box-shadow:0 4px 22px rgba(66,108,255,.09);
}
.stTabs [data-baseweb="tab"] {
    background:transparent;
    border-radius:12px;
    color:#3d4a6b !important;
    font-weight:700;
    font-size:13px;
    padding:10px 18px;
    transition:all .22s ease;
    font-family:'Sora',sans-serif !important;
}
.stTabs [aria-selected="true"] {
    background:linear-gradient(135deg,#426cff,#8b5ef5) !important;
    color:#fff !important;
    box-shadow:0 4px 18px rgba(66,108,255,.35);
}
.stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
    background:#eef2ff;
}

/* ── KPI Cards ── */
.kpi-card {
    background:#fff;
    border-radius:20px;
    padding:18px 20px;
    border:1.5px solid #e6eeff;
    box-shadow:0 4px 22px rgba(66,108,255,.09);
    min-height:112px;
    display:flex; flex-direction:column; justify-content:center;
    overflow:hidden; box-sizing:border-box;
    position:relative;
}
.kpi-card::before {
    content:'';
    position:absolute;
    top:0; left:0; right:0;
    height:4px;
    border-radius:20px 20px 0 0;
    background:var(--accent, linear-gradient(90deg,#426cff,#8b5ef5));
}
.kpi-emoji { font-size:20px; margin-bottom:5px; }
.kpi-label { font-size:9.5px; color:#8a96b8; font-weight:700;
    text-transform:uppercase; letter-spacing:1.2px; font-family:'Sora',sans-serif; }
.kpi-value { font-size:22px; color:#18192e; font-weight:800; margin:3px 0 2px;
    white-space:nowrap; overflow:hidden; text-overflow:ellipsis; font-family:'Sora',sans-serif; }
.kpi-delta { font-size:11px; color:#6b7db3; font-weight:600; }

/* ── Section Headers ── */
.section-header {
    display:flex; align-items:center; gap:10px;
    padding:11px 20px;
    background:linear-gradient(135deg,#426cff 0%,#8b5ef5 100%);
    color:#fff !important;
    border-radius:14px;
    font-size:14.5px; font-weight:700;
    margin:22px 0 14px;
    box-shadow:0 6px 22px rgba(66,108,255,.26);
    letter-spacing:.3px;
}

/* ── Recommendation Cards ── */
.rec-card {
    background:linear-gradient(135deg,#fffbea 0%,#fff5cc 100%);
    border:1.5px solid #f0d050;
    border-radius:16px;
    padding:13px 16px;
    margin-bottom:10px;
    box-shadow:0 2px 14px rgba(240,195,50,.13);
    transition:transform .18s ease, box-shadow .18s ease;
}
.rec-card:hover { transform:translateY(-2px); box-shadow:0 6px 20px rgba(240,195,50,.22); }

/* ── Customer Profile Card ── */
.cust-card {
    background:linear-gradient(135deg,#eef2ff 0%,#e8ecff 100%);
    border:1.5px solid #c5d2ff;
    border-radius:20px;
    padding:18px 22px;
    margin-bottom:16px;
    box-shadow:0 4px 18px rgba(66,108,255,.11);
}

/* ── Segment Badges ── */
.seg-badge {
    display:inline-block;
    padding:4px 13px;
    border-radius:20px;
    font-size:11.5px;
    font-weight:700;
    letter-spacing:.25px;
}
.badge-loyal    { background:#d2f5e3; color:#0d7a40; }
.badge-atrisk   { background:#fde4e4; color:#c0392b; }
.badge-new      { background:#e3f0ff; color:#1355c0; }
.badge-sensitive { background:#fff1df; color:#e05900; }
.badge-potential { background:#f3e5ff; color:#6a1b9a; }

/* ── Info Box ── */
.info-box {
    background:linear-gradient(135deg,#eef2ff,#f5f0ff);
    border:1.5px solid #ccd4ff;
    border-radius:16px;
    padding:20px 26px;
    margin:12px 0;
}

/* ── Search / Input ── */
.stTextInput>div>div>input {
    border-radius:12px !important;
    border:2px solid #dde6ff !important;
    padding:10px 16px !important;
    font-family:'Sora',sans-serif !important;
    font-size:13.5px !important;
    background:#fff !important;
    color:#18192e !important;
}
.stTextInput>div>div>input:focus {
    border-color:#426cff !important;
    box-shadow:0 0 0 3px rgba(66,108,255,.13) !important;
}

/* ── Selectbox (main area) ── */
.stSelectbox>div>div {
    border-radius:12px !important;
    border:2px solid #dde6ff !important;
    background:#fff !important;
}
.stSelectbox>div>div>div { color:#18192e !important; }

/* ── DataFrame ── */
[data-testid="stDataFrame"] {
    border-radius:14px !important;
    overflow:hidden;
    border:1.5px solid #e6eeff;
    box-shadow:0 4px 18px rgba(66,108,255,.07);
}

/* ── Download buttons ── */
.stDownloadButton>button {
    background:linear-gradient(135deg,#426cff,#8b5ef5) !important;
    color:#fff !important;
    border:none !important;
    border-radius:12px !important;
    font-weight:700 !important;
    font-size:13px !important;
    padding:10px 20px !important;
    transition:all .2s ease !important;
    font-family:'Sora',sans-serif !important;
    box-shadow:0 4px 16px rgba(66,108,255,.28) !important;
}
.stDownloadButton>button:hover {
    transform:translateY(-2px) !important;
    box-shadow:0 6px 22px rgba(66,108,255,.42) !important;
}

/* ── Misc ── */
hr { border:none; border-top:2px solid #e6eeff; margin:16px 0; }
.stAlert { border-radius:14px !important; }
.stSlider>div>div>div { background:#426cff !important; }
.stSelectbox label,.stSlider label,.stDateInput label,.stMultiSelect label {
    font-weight:700 !important; color:#2b3b74 !important; font-size:12.5px !important;
}
[data-testid="stMetricDelta"] { color:#22c55e !important; }
::-webkit-scrollbar { width:6px; height:6px; }
::-webkit-scrollbar-track { background:#eef2ff; }
::-webkit-scrollbar-thumb { background:#b8c8ff; border-radius:6px; }
::-webkit-scrollbar-thumb:hover { background:#7090ff; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CHART THEME CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
CHART_BG   = "#fefeff"
PAPER_BG   = "#ffffff"
FC         = "#18192e"
GRID       = "#eef2ff"
ACCENT     = ["#426cff","#f59e0b","#10b981","#ef4444","#8b5ef5",
              "#06b6d4","#f97316","#ec4899","#14b8a6","#6366f1"]
SEG_COLORS = {
    "High-Value Loyal Customers": "#10b981",
    "At-Risk Customers":          "#ef4444",
    "New Buyers":                 "#426cff",
    "Price-Sensitive Shoppers":   "#f97316",
    "Potential Loyalists":        "#8b5ef5",
}

def blayout(title="", height=420):
    return dict(
        title=dict(text=title, font=dict(color=FC, size=14, family="Sora"), x=0.01),
        paper_bgcolor=PAPER_BG, plot_bgcolor=CHART_BG,
        font=dict(color=FC, family="Sora"),
        height=height,
        margin=dict(l=55, r=35, t=52, b=55),
        xaxis=dict(gridcolor=GRID, linecolor="#dde3f8",
                   tickfont=dict(color=FC, family="Sora")),
        yaxis=dict(gridcolor=GRID, linecolor="#dde3f8",
                   tickfont=dict(color=FC, family="Sora")),
        legend=dict(bgcolor="rgba(255,255,255,.92)", bordercolor="#dde6ff",
                    borderwidth=1, font=dict(family="Sora")),
    )

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOMER NAME GENERATOR  (deterministic from seed)
# ─────────────────────────────────────────────────────────────────────────────
_FIRSTS = [
    "Aarav","Vivaan","Aditya","Vihaan","Arjun","Reyansh","Ayaan","Krishna","Ishaan","Shaurya",
    "Atharv","Advik","Dhruv","Kabir","Ritvik","Ranveer","Advaith","Rohan","Ananya","Diya",
    "Pihu","Anika","Saanvi","Aarohi","Siya","Riya","Kavya","Isha","Shreya","Nandini",
    "Priya","Meera","Deepa","Pooja","Sunita","Rekha","Geeta","Rahul","Vikram","Nikhil",
    "Amit","Suresh","Raj","Vijay","Sachin","Manish","Simran","Neha","Swati","Divya",
    "Ankita","Tanvi","Jyoti","Komal","Sneha","Pallavi","Karan","Ravi","Arun","Deepak",
    "Naveen","Sanjay","Rajesh","Mohan","Sunil","Harpreet","Gurpreet","Jaspreet","Manpreet","Zara",
    "Faiza","Nadia","Sana","Ayesha","Mehak","Zoya","Alisha","Hina","Taranjit","Kuldeep",
    "Loveleen","Bikram","Aryan","Ishita","Tara","Gaurav","Himanshu","Kartik","Nishant","Varun",
    "Ritika","Sonali","Bharti","Nisha","Usha","Shalini","Puja","Chandni","Preeti","Shweta",
]
_LASTS = [
    "Sharma","Verma","Singh","Patel","Kumar","Gupta","Mehta","Shah","Joshi","Nair",
    "Reddy","Rao","Pillai","Menon","Iyer","Krishnan","Subramanian","Venkatesh","Murthy","Bose",
    "Chatterjee","Mukherjee","Banerjee","Das","Sen","Ghosh","Roy","Dutta","Sarkar","Desai",
    "Jain","Agarwal","Malhotra","Kapoor","Khanna","Arora","Bhatia","Chopra","Dhawan","Srivastava",
    "Pandey","Mishra","Tiwari","Dubey","Yadav","Chauhan","Rajput","Thakur","Saxena","Trivedi",
]

def build_name_map(customer_ids):
    rng = random.Random(42)
    return {cid: f"{rng.choice(_FIRSTS)} {rng.choice(_LASTS)}" for cid in customer_ids}

# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADERS
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = pathlib.Path(__file__).parent
    segments   = pd.read_csv(base / "customer_segments.csv")
    forecast   = pd.read_csv(base / "sales_forecast.csv", parse_dates=["date"])
    cross_sell = pd.read_csv(base / "cross_sell_insights.csv")
    rec_prod   = pd.read_csv(base / "recommended_products.csv")
    cust_feat  = pd.read_csv(base / "customer_features.csv")
    prod_feat  = pd.read_csv(base / "product_features.csv")
    inter_mat  = pd.read_csv(base / "interaction_matrix.csv")

    all_ids  = sorted(segments["customer_id"].unique().tolist())
    name_map = build_name_map(all_ids)
    return segments, forecast, cross_sell, rec_prod, cust_feat, prod_feat, inter_mat, name_map

try:
    segments, forecast, cross_sell, rec_prod, cust_feat, prod_feat, inter_mat, NAME_MAP = load_data()
    DATA_OK = True
except Exception as exc:
    DATA_OK = False
    _ERR = str(exc)

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def inr(v):
    if pd.isna(v): return "N/A"
    if v >= 1e7:   return f"₹{v/1e7:.2f}Cr"
    if v >= 1e5:   return f"₹{v/1e5:.2f}L"
    return f"₹{v:,.0f}"

def get_name(cid):
    return NAME_MAP.get(cid, cid)

def kcard(col, emoji, label, value, delta="", accent="#426cff"):
    col.markdown(
        f"""<div class='kpi-card' style='--accent:linear-gradient(90deg,{accent},{accent}cc);'>
              <div class='kpi-emoji'>{emoji}</div>
              <div class='kpi-label'>{label}</div>
              <div class='kpi-value'>{value}</div>
              <div class='kpi-delta'>{delta}</div>
            </div>""",
        unsafe_allow_html=True,
    )

def sec(text, emoji="📌"):
    st.markdown(
        f"<div class='section-header'><span>{emoji}</span><span>{text}</span></div>",
        unsafe_allow_html=True,
    )

def badge(seg):
    cls_map = {
        "High-Value Loyal Customers": "badge-loyal",
        "At-Risk Customers":          "badge-atrisk",
        "New Buyers":                 "badge-new",
        "Price-Sensitive Shoppers":   "badge-sensitive",
        "Potential Loyalists":        "badge-potential",
    }
    return f"<span class='seg-badge {cls_map.get(seg,'badge-new')}'>{seg}</span>"

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:10px 0 6px;'>
        <div style='font-size:42px;'>📊</div>
        <div style='font-size:17px;font-weight:800;color:#ffffff;margin:6px 0 2px;'>Revenue Analytics</div>
        <div style='font-size:10.5px;color:#99aadd;font-weight:700;letter-spacing:.7px;'>PERSONALIZATION DASHBOARD</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")

    if DATA_OK:
        st.markdown("**🗓️ Forecast Date Range**")
        min_d = forecast["date"].min().date()
        max_d = forecast["date"].max().date()
        date_from = st.date_input("From", value=min_d, min_value=min_d, max_value=max_d, key="fc_from")
        date_to   = st.date_input("To",   value=max_d, min_value=min_d, max_value=max_d, key="fc_to")

        st.markdown("---")
        st.markdown("**👥 Customer Segment**")
        all_segs = ["All"] + sorted(segments["segment"].dropna().unique().tolist())
        sel_seg  = st.selectbox("Filter by Segment", all_segs)

        st.markdown("---")
        st.markdown("**📦 Product Category**")
        all_cats = ["All"] + sorted(prod_feat["category"].dropna().unique().tolist())
        sel_cat  = st.selectbox("Filter by Category", all_cats)

        st.markdown("---")
        st.markdown("**🔮 Extended Forecast**")
        extra_days = st.slider("Extra forecast days", 0, 90, 30, step=10)

        st.markdown("---")
        # Active-filter summary badge block
        filters = [
            ("🗓️ From",    str(date_from)),
            ("🗓️ To",      str(date_to)),
            ("👥 Segment", sel_seg),
            ("📦 Category",sel_cat),
            ("🔮 Extra",   f"+{extra_days} days"),
        ]
        st.markdown("**🔎 Active Filters**")
        html = "<div class='active-filters-card' style='background:#ffffff;border:1.5px solid #dde6ff;border-radius:12px;padding:8px 12px;font-size:12px;'>"
        for i,(k,v) in enumerate(filters):
            bg = "#f6f8ff" if i%2==0 else "#ffffff"
            active = v not in ("All","+0 days")
            bc,bg2 = ("#426cff","#dce8ff") if active else ("#10b981","#d2f5e3")
            html += (f"<div style='display:flex;justify-content:space-between;align-items:center;"
                     f"padding:5px 4px;background:{bg};border-radius:6px;margin-bottom:2px;'>"
                     f"<span class='af-label' style='color:#000000 !important;font-weight:700;font-family:Sora,sans-serif;'>{k}</span>"
                     f"<span class='af-value' style='background:{bg2};color:#000000 !important;padding:2px 10px;"
                     f"border-radius:20px;font-weight:700;font-size:10.5px;font-family:Sora,sans-serif;'>{v}</span></div>")
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("💡 Use filters above to drill into your data.")

# ─────────────────────────────────────────────────────────────────────────────
# MAIN HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding:4px 0 2px;'>
  <h1 style='color:#18192e;font-size:30px;font-weight:800;margin:0;line-height:1.2;
             font-family:Sora,sans-serif;'>
    📊 Revenue Growth & Personalization Dashboard
  </h1>
  <p style='color:#6b7db3;font-size:13.5px;margin:5px 0 0;font-weight:600;'>
    AI-Powered Analytics &nbsp;·&nbsp; Sales Forecasting &nbsp;·&nbsp;
    Customer Intelligence &nbsp;·&nbsp; Product Recommendations
  </p>
</div>""", unsafe_allow_html=True)

if not DATA_OK:
    st.error(f"❌ Could not load data files.\n\nError: {_ERR}")
    st.stop()

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────────────────────────────────────
fc_filt = forecast[
    (forecast["date"].dt.date >= date_from) &
    (forecast["date"].dt.date <= date_to)
].copy()

seg_filt = segments.copy()
if sel_seg != "All":
    seg_filt = seg_filt[seg_filt["segment"] == sel_seg]

prod_filt = prod_feat.copy()
if sel_cat != "All":
    prod_filt = prod_filt[prod_filt["category"] == sel_cat]

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL KPIs
# ─────────────────────────────────────────────────────────────────────────────
total_fc   = fc_filt["forecasted_sales"].sum()
avg_daily  = fc_filt["forecasted_sales"].mean()
n_cust     = seg_filt["customer_id"].nunique()
n_prod     = prod_filt["product_name"].nunique() if "product_name" in prod_filt.columns else prod_feat["product_name"].nunique()
avg_spend  = seg_filt["monetary"].mean()
top_seg    = segments["segment"].value_counts().idxmax()

c1,c2,c3,c4,c5,c6 = st.columns(6)
kcard(c1,"📈","Forecasted Revenue",   inr(total_fc),        "Selected Period",  "#426cff")
kcard(c2,"📅","Avg Daily Forecast",   inr(avg_daily),       "Daily Average",    "#f59e0b")
kcard(c3,"👥","Customers (Filtered)", f"{n_cust:,}",        "Active Customers", "#10b981")
kcard(c4,"📦","Products (Filtered)",  f"{n_prod:,}",        "Product SKUs",     "#8b5ef5")
kcard(c5,"💰","Avg Customer Spend",   inr(avg_spend),       "Lifetime Value",   "#ef4444")
kcard(c6,"🏆","Top Segment",          top_seg.split()[0],   "Largest Group",    "#06b6d4")

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈  Sales Forecast",
    "👥  Customer Segments",
    "🎯  Product Recommendations",
    "🏆  Products & Cross-Sell",
    "📁  Data & Export",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 – SALES FORECAST
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    sec("Sales Forecast Overview", "📈")

    # Optionally extend forecast
    fc_ext = fc_filt.copy()
    if extra_days > 0:
        last_date = fc_filt["date"].max()
        last_val  = fc_filt["forecasted_sales"].iloc[-1]
        x_arr     = np.arange(len(fc_filt))
        slope     = np.polyfit(x_arr, fc_filt["forecasted_sales"].values, 1)[0]
        fut_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=extra_days)
        fut_vals  = [last_val + slope*(i+1) for i in range(extra_days)]
        band_w    = (fc_filt["upper_bound"] - fc_filt["lower_bound"]).mean()
        fut_df    = pd.DataFrame({
            "date":             fut_dates,
            "forecasted_sales": fut_vals,
            "lower_bound":      [v - band_w/2 for v in fut_vals],
            "upper_bound":      [v + band_w/2 for v in fut_vals],
            "is_ext":           True,
        })
        fc_ext["is_ext"] = False
        fc_ext = pd.concat([fc_ext, fut_df], ignore_index=True)
    else:
        fc_ext["is_ext"] = False

    hist = fc_ext[~fc_ext["is_ext"]]
    extp = fc_ext[fc_ext["is_ext"]]

    fig_fc = go.Figure()
    # Confidence band
    fig_fc.add_trace(go.Scatter(x=hist["date"], y=hist["upper_bound"],
        mode="lines", line=dict(width=0), showlegend=False, hoverinfo="skip"))
    fig_fc.add_trace(go.Scatter(x=hist["date"], y=hist["lower_bound"],
        mode="lines", line=dict(width=0), fill="tonexty",
        fillcolor="rgba(66,108,255,.10)", name="Confidence Band"))
    if extra_days > 0:
        fig_fc.add_trace(go.Scatter(x=extp["date"], y=extp["upper_bound"],
            mode="lines", line=dict(width=0), showlegend=False, hoverinfo="skip"))
        fig_fc.add_trace(go.Scatter(x=extp["date"], y=extp["lower_bound"],
            mode="lines", line=dict(width=0), fill="tonexty",
            fillcolor="rgba(245,158,11,.12)", name="Extended Band"))
        fig_fc.add_trace(go.Scatter(x=extp["date"], y=extp["forecasted_sales"],
            name=f"Extended (+{extra_days}d)", mode="lines+markers",
            line=dict(color="#f59e0b", width=2.5, dash="dot"),
            marker=dict(size=5, color="#f59e0b")))
    fig_fc.add_trace(go.Scatter(x=hist["date"], y=hist["forecasted_sales"],
        name="Forecasted Sales", mode="lines+markers",
        line=dict(color="#426cff", width=3), marker=dict(size=6, color="#426cff"),
        hovertemplate="<b>%{x|%d %b %Y}</b><br>₹%{y:,.0f}<extra></extra>"))
    lfc = blayout("Daily Sales Forecast with Confidence Bands", 440)
    lfc["xaxis"]["title"] = "Date"
    lfc["yaxis"]["title"] = "Forecasted Revenue (₹)"
    fig_fc.update_layout(**lfc)
    st.plotly_chart(fig_fc, use_container_width=True)

    # KPI row
    c1f,c2f,c3f,c4f = st.columns(4)
    pk = fc_filt.loc[fc_filt["forecasted_sales"].idxmax()]
    lw = fc_filt.loc[fc_filt["forecasted_sales"].idxmin()]
    kcard(c1f,"📈","Peak Day",        pk["date"].strftime("%d %b %Y"), inr(pk["forecasted_sales"]), "#426cff")
    kcard(c2f,"📉","Low Day",         lw["date"].strftime("%d %b %Y"), inr(lw["forecasted_sales"]), "#ef4444")
    kcard(c3f,"💰","Total Forecast",  inr(total_fc),                   f"{len(fc_filt)} days",      "#10b981")
    kcard(c4f,"📊","Avg Conf. Band",  inr((fc_filt["upper_bound"]-fc_filt["lower_bound"]).mean()), "Uncertainty", "#8b5ef5")

    st.markdown("<br>", unsafe_allow_html=True)
    cA, cB = st.columns(2)

    with cA:
        sec("Weekly Aggregation", "📅")
        fc_w = fc_filt.copy()
        fc_w["week"] = fc_w["date"].dt.to_period("W").astype(str)
        wk = fc_w.groupby("week").agg(total=("forecasted_sales","sum"),
                                       upper=("upper_bound","sum"),
                                       lower=("lower_bound","sum")).reset_index()
        fig_wk = go.Figure()
        fig_wk.add_trace(go.Bar(x=wk["week"], y=wk["total"], name="Weekly Revenue",
            marker=dict(color="#426cff", opacity=.85, line=dict(width=0)),
            text=[inr(v) for v in wk["total"]], textposition="outside",
            textfont=dict(color=FC, size=10),
            hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>"))
        fig_wk.add_trace(go.Scatter(x=wk["week"], y=wk["upper"], mode="lines",
            name="Upper Bound", line=dict(color="#f59e0b", dash="dash", width=1.8)))
        fig_wk.add_trace(go.Scatter(x=wk["week"], y=wk["lower"], mode="lines",
            name="Lower Bound", line=dict(color="#ef4444", dash="dash", width=1.8)))
        lw2 = blayout("Weekly Revenue Forecast", 370)
        lw2["xaxis"]["tickangle"] = -35
        fig_wk.update_layout(**lw2)
        st.plotly_chart(fig_wk, use_container_width=True)

    with cB:
        sec("Monthly Aggregation", "📆")
        fc_m = fc_filt.copy()
        fc_m["month"] = fc_m["date"].dt.to_period("M").astype(str)
        mo = fc_m.groupby("month").agg(total=("forecasted_sales","sum"),
                                        avg=("forecasted_sales","mean")).reset_index()
        fig_mo = go.Figure()
        fig_mo.add_trace(go.Bar(x=mo["month"], y=mo["total"], name="Monthly Total",
            marker=dict(color="#10b981", opacity=.85, line=dict(width=0)),
            text=[inr(v) for v in mo["total"]], textposition="outside",
            textfont=dict(color=FC, size=10),
            hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>"))
        fig_mo.add_trace(go.Scatter(x=mo["month"], y=mo["avg"], mode="lines+markers",
            name="Daily Avg", yaxis="y2",
            line=dict(color="#8b5ef5", width=2.5), marker=dict(size=8, color="#8b5ef5")))
        lm2 = blayout("Monthly Revenue Forecast", 370)
        lm2["xaxis"]["tickangle"] = -22
        lm2["yaxis2"] = dict(title="Daily Avg (₹)", overlaying="y", side="right",
                             tickfont=dict(color=FC), showgrid=False)
        fig_mo.update_layout(**lm2)
        st.plotly_chart(fig_mo, use_container_width=True)

    sec("Forecast Period Breakdown Table", "📋")
    tbl = fc_filt[["date","forecasted_sales","forecast_period","lower_bound","upper_bound"]].copy()
    tbl["date"]             = tbl["date"].dt.strftime("%d %b %Y")
    tbl["forecasted_sales"] = tbl["forecasted_sales"].apply(inr)
    tbl["lower_bound"]      = tbl["lower_bound"].apply(inr)
    tbl["upper_bound"]      = tbl["upper_bound"].apply(inr)
    tbl.columns = ["Date","Forecast","Period","Lower Bound","Upper Bound"]
    st.dataframe(tbl, use_container_width=True, height=280)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 – CUSTOMER SEGMENTS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    sec("Customer Segment Overview", "👥")

    sc = seg_filt["segment"].value_counts().reset_index()
    sc.columns = ["Segment","Customers"]
    sc_colors  = [SEG_COLORS.get(s, ACCENT[0]) for s in sc["Segment"]]

    col1, col2 = st.columns(2)
    with col1:
        fig_bar = go.Figure(go.Bar(
            x=sc["Segment"], y=sc["Customers"],
            marker_color=sc_colors,
            text=sc["Customers"], textposition="outside",
            textfont=dict(color=FC, size=13),
            hovertemplate="<b>%{x}</b><br>%{y} customers<extra></extra>"))
        fig_bar.update_layout(**blayout("Customers per Segment", 390))
        fig_bar.update_xaxes(title_text="Segment", tickangle=-18)
        fig_bar.update_yaxes(title_text="Customers")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        fig_pie = go.Figure(go.Pie(
            labels=sc["Segment"], values=sc["Customers"],
            marker=dict(colors=sc_colors, line=dict(color="#fff", width=2)),
            hole=.46, textinfo="label+percent",
            textfont=dict(color=FC, size=11.5),
            hovertemplate="<b>%{label}</b><br>%{value} customers (%{percent})<extra></extra>"))
        fig_pie.update_layout(paper_bgcolor=PAPER_BG, plot_bgcolor=CHART_BG,
            font=dict(color=FC, family="Sora"), height=390,
            margin=dict(l=10,r=10,t=30,b=10),
            legend=dict(font=dict(color=FC)))
        st.plotly_chart(fig_pie, use_container_width=True)

    sec("RFM Metrics by Segment", "📊")
    c3,c4,c5 = st.columns(3)

    with c3:
        rm = seg_filt.groupby("segment")["monetary"].mean().reset_index()
        fig_r1 = go.Figure(go.Bar(
            x=rm["segment"], y=rm["monetary"],
            marker_color=[SEG_COLORS.get(s,ACCENT[1]) for s in rm["segment"]],
            text=[inr(v) for v in rm["monetary"]], textposition="outside",
            textfont=dict(color=FC, size=10)))
        fig_r1.update_layout(**blayout("Avg Lifetime Spend by Segment", 350))
        fig_r1.update_xaxes(tickangle=-22)
        fig_r1.update_yaxes(title_text="₹ Spend")
        st.plotly_chart(fig_r1, use_container_width=True)

    with c4:
        rf = seg_filt.groupby("segment")["frequency"].mean().reset_index()
        fig_r2 = go.Figure(go.Bar(
            x=rf["segment"], y=rf["frequency"],
            marker_color="#06b6d4",
            text=rf["frequency"].round(1), textposition="outside",
            textfont=dict(color=FC, size=10)))
        fig_r2.update_layout(**blayout("Avg Order Frequency by Segment", 350))
        fig_r2.update_xaxes(tickangle=-22)
        fig_r2.update_yaxes(title_text="Orders")
        st.plotly_chart(fig_r2, use_container_width=True)

    with c5:
        rr = seg_filt.groupby("segment")["recency"].mean().reset_index()
        fig_r3 = go.Figure(go.Bar(
            x=rr["segment"], y=rr["recency"],
            marker_color="#f97316",
            text=rr["recency"].round(0), textposition="outside",
            textfont=dict(color=FC, size=10)))
        fig_r3.update_layout(**blayout("Avg Days Since Last Purchase", 350))
        fig_r3.update_xaxes(tickangle=-22)
        fig_r3.update_yaxes(title_text="Days")
        st.plotly_chart(fig_r3, use_container_width=True)

    sec("RFM Score Distribution", "🎯")
    c6, c7 = st.columns(2)

    with c6:
        fig_h = go.Figure(go.Histogram(x=seg_filt["rfm_score"], nbinsx=12,
            marker=dict(color="#426cff", opacity=.85, line=dict(color="#fff", width=1))))
        fig_h.update_layout(**blayout("Distribution of RFM Scores", 320))
        fig_h.update_xaxes(title_text="RFM Score")
        fig_h.update_yaxes(title_text="Customers")
        st.plotly_chart(fig_h, use_container_width=True)

    with c7:
        sr = seg_filt.groupby("segment")["rfm_score"].mean().reset_index()
        fig_r4 = go.Figure(go.Bar(
            x=sr["segment"], y=sr["rfm_score"].round(1),
            marker_color=[SEG_COLORS.get(s,ACCENT[4]) for s in sr["segment"]],
            text=sr["rfm_score"].round(1), textposition="outside",
            textfont=dict(color=FC, size=11)))
        fig_r4.update_layout(**blayout("Avg RFM Score per Segment", 320))
        fig_r4.update_xaxes(tickangle=-22)
        st.plotly_chart(fig_r4, use_container_width=True)

    sec("Customer Segment Table — ID · Name · Segment · RFM", "📋")

    # Interactive search
    q_seg = st.text_input("🔍 Search by Customer ID or Name",
                           placeholder="e.g. C100005 or Priya Singh", key="seg_search")

    disp = seg_filt[["customer_id","segment","rfm_score","recency","frequency","monetary"]].copy()
    disp.insert(1, "customer_name", disp["customer_id"].map(get_name))
    disp["monetary"] = disp["monetary"].apply(inr)
    disp.columns = ["Customer ID","Customer Name","Segment","RFM Score",
                    "Days Since Purchase","Orders","Total Spend"]

    if q_seg.strip():
        q_lo = q_seg.strip().lower()
        disp = disp[
            disp["Customer ID"].str.lower().str.contains(q_lo) |
            disp["Customer Name"].str.lower().str.contains(q_lo)
        ]
    st.dataframe(disp, use_container_width=True, height=360)
    st.caption(f"Showing {len(disp):,} customers")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 – PRODUCT RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    all_cids     = sorted(rec_prod["user_id"].unique().tolist())
    disp_opts    = [f"{cid}  —  {get_name(cid)}" for cid in all_cids]
    opt_to_cid   = dict(zip(disp_opts, all_cids))

    n_recs = 5

    sel_opt  = st.selectbox("👤 Select Customer (ID — Name):", disp_opts, key="sel_cust")
    sel_cid  = opt_to_cid[sel_opt]
    sel_name = get_name(sel_cid)

    cust_recs     = rec_prod[rec_prod["user_id"] == sel_cid].sort_values("rank").head(n_recs)
    cust_seg_row  = segments[segments["customer_id"] == sel_cid]

    # ── Customer Profile Card ──
    if not cust_seg_row.empty:
        row = cust_seg_row.iloc[0]
        avatar_letter = sel_name[0].upper()
        seg_color = SEG_COLORS.get(row["segment"], "#426cff")

        st.markdown(f"""
        <div class='cust-card'>
          <div style='display:flex;align-items:center;gap:16px;flex-wrap:wrap;'>
            <div style='background:linear-gradient(135deg,#426cff,#8b5ef5);
                 width:58px;height:58px;border-radius:50%;display:flex;align-items:center;
                 justify-content:center;font-size:26px;font-weight:800;color:#fff;
                 flex-shrink:0;font-family:Sora,sans-serif;'>{avatar_letter}</div>
            <div>
              <div style='font-size:21px;font-weight:800;color:#18192e;
                          font-family:Sora,sans-serif;'>{sel_name}</div>
              <div style='font-size:13px;color:#6b7db3;margin-top:3px;font-weight:600;'>
                Customer ID: <b style='color:#426cff;font-family:JetBrains Mono,monospace;
                font-size:12px;'>{sel_cid}</b>
                &nbsp;·&nbsp; {badge(row['segment'])}
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        c1r,c2r,c3r,c4r,c5r = st.columns(5)
        kcard(c1r,"🪪","Customer ID",    sel_cid,                    "",                   "#426cff")
        kcard(c2r,"📊","RFM Score",      str(row["rfm_score"]),      "Score",              "#f59e0b")
        kcard(c3r,"🛒","Total Orders",   str(row["frequency"]),      "Purchases",          "#10b981")
        kcard(c4r,"💰","Lifetime Spend", inr(row["monetary"]),       "Total Spend",        "#ef4444")
        kcard(c5r,"⏱️","Last Purchase",  f"{row['recency']} days ago","Recency",            "#8b5ef5")

    st.markdown("<br>", unsafe_allow_html=True)
    sec(f"Top {n_recs} Recommendations for {sel_name}", "🏅")

    colA, colB = st.columns([1.1, 0.9])

    with colA:
        fig_rec = go.Figure(go.Bar(
            x=cust_recs["recommended_product"],
            y=(cust_recs["rank"].max() + 1 - cust_recs["rank"]),
            marker=dict(color=ACCENT[:len(cust_recs)], opacity=.9, line=dict(width=0)),
            text=["Rank #"+str(r) for r in cust_recs["rank"]],
            textposition="outside", textfont=dict(color=FC, size=12),
            hovertemplate="<b>%{x}</b><br>Rank #%{text}<extra></extra>"))
        lr = blayout(f"Recommended Products — {sel_name} ({sel_cid})", 420)
        lr["xaxis"]["title"] = "Product"
        lr["yaxis"]["title"] = "Relevance Score"
        lr["yaxis"]["showticklabels"] = False
        fig_rec.update_layout(**lr)
        st.plotly_chart(fig_rec, use_container_width=True)

    with colB:
        st.markdown("""<div style='font-size:15px;font-weight:700;color:#18192e;
                    margin-bottom:12px;margin-top:8px;'>🛍️ Personalized Cards</div>""",
                    unsafe_allow_html=True)
        for _, rrow in cust_recs.iterrows():
            pi = prod_feat[prod_feat["product_name"] == rrow["recommended_product"]]
            if not pi.empty:
                p       = pi.iloc[0]
                pop_pct = int(p.get("popularity_score", 0) * 100)
                bw      = max(8, pop_pct)
                st.markdown(f"""
                <div class='rec-card'>
                  <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                    <b style='font-size:14.5px;color:#18192e;'>
                      #{rrow['rank']} &nbsp;{rrow['recommended_product']}
                    </b>
                    <span style='background:#426cff;color:#fff;padding:2px 10px;border-radius:10px;
                           font-size:10.5px;font-weight:700;'>{rrow['recommendation_type'].title()}</span>
                  </div>
                  <div style='margin-top:6px;font-size:12px;color:#555;line-height:1.8;'>
                    👤 For: <b style='color:#426cff;'>{sel_name}</b><br>
                    📂 <b>{p['category']}</b> &nbsp;|&nbsp;
                    💰 <b>{inr(p['avg_price'])}</b> &nbsp;|&nbsp;
                    ⭐ Popularity: <b>{p['popularity']}</b>
                  </div>
                  <div style='margin-top:8px;background:#f0d050;border-radius:6px;height:5px;'>
                    <div style='width:{bw}%;background:linear-gradient(90deg,#f59e0b,#f97316);
                         height:5px;border-radius:6px;'></div>
                  </div>
                  <div style='font-size:9.5px;color:#aaa;margin-top:2px;'>Popularity score: {pop_pct}%</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='rec-card'>
                  <b>#{rrow['rank']} — {rrow['recommended_product']}</b>
                  <div style='font-size:11.5px;color:#666;margin-top:4px;'>
                    👤 For: <b style='color:#426cff;'>{sel_name}</b> &nbsp;|&nbsp;
                    {rrow['recommendation_type'].title()}
                  </div>
                </div>""", unsafe_allow_html=True)

    # Purchase history from interaction matrix
    cust_hist = inter_mat[inter_mat["customer_id"] == sel_cid]
    if not cust_hist.empty:
        sec(f"Purchase History — {sel_name} ({sel_cid})", "🧾")
        hist_d = cust_hist.copy()
        hist_d.columns = [c.replace("_"," ").title() for c in hist_d.columns]
        st.dataframe(hist_d, use_container_width=True, height=180)

    sec("Overall Recommendation Summary", "📊")
    rs = (rec_prod.groupby("recommended_product")
          .agg(Times_Recommended=("user_id","count"), Avg_Rank=("rank","mean"))
          .reset_index().sort_values("Times_Recommended", ascending=False))
    rs["Avg_Rank"] = rs["Avg_Rank"].round(1)

    cx, cy = st.columns(2)
    with cx:
        fig_rs = go.Figure(go.Bar(
            x=rs["recommended_product"], y=rs["Times_Recommended"],
            marker=dict(color=ACCENT[4], opacity=.88, line=dict(width=0)),
            text=rs["Times_Recommended"], textposition="outside",
            textfont=dict(color=FC, size=12)))
        fig_rs.update_layout(**blayout("Most Recommended Products", 370))
        fig_rs.update_xaxes(title_text="Product")
        fig_rs.update_yaxes(title_text="Times Recommended")
        st.plotly_chart(fig_rs, use_container_width=True)

    with cy:
        rs_show = rs.copy()
        rs_show.columns = ["Product","Times Recommended","Avg Rank"]
        st.dataframe(rs_show, use_container_width=True, height=300)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 – PRODUCTS & CROSS-SELL
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    sec("Top Products by Revenue & Popularity", "🏆")

    col1, col2 = st.columns(2)
    with col1:
        tp = prod_filt.nlargest(10, "total_revenue")
        fig_tp = go.Figure(go.Bar(
            y=tp["product_name"], x=tp["total_revenue"], orientation="h",
            marker=dict(color=tp["total_revenue"],
                        colorscale=[[0,"#c5d5ff"],[1,"#426cff"]],
                        showscale=False, line=dict(width=0)),
            text=[inr(v) for v in tp["total_revenue"]],
            textposition="outside", textfont=dict(color=FC, size=11)))
        fig_tp.update_layout(**blayout("Top Products by Revenue", 420))
        fig_tp.update_xaxes(title_text="Total Revenue (₹)")
        st.plotly_chart(fig_tp, use_container_width=True)

    with col2:
        pp = prod_filt.nlargest(10, "popularity")
        fig_pp = go.Figure(go.Bar(
            y=pp["product_name"], x=pp["popularity"], orientation="h",
            marker=dict(color=pp["popularity"],
                        colorscale=[[0,"#d2f5e3"],[1,"#10b981"]],
                        showscale=False, line=dict(width=0)),
            text=pp["popularity"], textposition="outside",
            textfont=dict(color=FC, size=11)))
        fig_pp.update_layout(**blayout("Top Products by Popularity", 420))
        fig_pp.update_xaxes(title_text="Popularity Score")
        st.plotly_chart(fig_pp, use_container_width=True)

    sec("Category Analysis", "📦")
    cat_agg = prod_filt.groupby("category").agg(
        Total_Revenue=("total_revenue","sum"),
        Units_Sold=("total_units_sold","sum"),
        Avg_Price=("avg_price","mean"),
        Products=("product_name","count"),
    ).reset_index()

    col3, col4 = st.columns(2)
    with col3:
        fig_cat = go.Figure()
        fig_cat.add_trace(go.Bar(x=cat_agg["category"], y=cat_agg["Total_Revenue"],
            name="Revenue", marker=dict(color="#10b981", opacity=.88, line=dict(width=0)),
            text=[inr(v) for v in cat_agg["Total_Revenue"]], textposition="outside",
            textfont=dict(color=FC, size=11),
            hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>"))
        fig_cat.add_trace(go.Scatter(x=cat_agg["category"], y=cat_agg["Units_Sold"],
            name="Units Sold", mode="lines+markers", yaxis="y2",
            marker=dict(color="#426cff", size=10), line=dict(color="#426cff", width=2.5)))
        lcat = blayout("Revenue vs Units Sold by Category", 390)
        lcat["yaxis2"] = dict(title="Units Sold", overlaying="y", side="right",
                              tickfont=dict(color=FC), showgrid=False)
        fig_cat.update_layout(**lcat)
        st.plotly_chart(fig_cat, use_container_width=True)

    with col4:
        fig_sc = go.Figure(go.Scatter(
            x=prod_filt["avg_price"], y=prod_filt["total_revenue"],
            mode="markers+text",
            text=prod_filt["product_name"],
            textposition="top center",
            textfont=dict(size=10, color=FC),
            marker=dict(size=prod_filt["popularity"].fillna(1)/8,
                        color="#8b5ef5", opacity=.78,
                        line=dict(color="#fff", width=2))))
        fig_sc.update_layout(**blayout("Price vs Revenue (Bubble = Popularity)", 390))
        fig_sc.update_xaxes(title_text="Avg Price (₹)")
        fig_sc.update_yaxes(title_text="Total Revenue (₹)")
        st.plotly_chart(fig_sc, use_container_width=True)

    sec("Cross-Sell Insights", "🔗")
    st.info("ℹ️ Cross-sell pairs show products frequently bought together — ideal for bundles & upsell campaigns.")

    col5, col6 = st.columns([1.2, 1])
    with col5:
        top_cs   = cross_sell.sort_values("similarity_score", ascending=False).head(15)
        cs_lbls  = [f"{r['product']} ➜ {r['cross_sell_product']}" for _, r in top_cs.iterrows()]
        fig_cs = go.Figure(go.Bar(
            x=cs_lbls, y=top_cs["similarity_score"],
            marker=dict(color=top_cs["similarity_score"],
                        colorscale=[[0,"#fde4e4"],[1,"#ef4444"]],
                        showscale=True, colorbar=dict(title="Score", len=.6),
                        line=dict(width=0)),
            text=top_cs["similarity_score"].round(2), textposition="outside",
            textfont=dict(color=FC, size=11)))
        lcs = blayout("Top Cross-Sell Pairs by Similarity", 430)
        lcs["xaxis"]["tickangle"] = -38
        lcs["xaxis"]["tickfont"] = dict(size=9, color=FC)
        fig_cs.update_layout(**lcs)
        fig_cs.update_yaxes(title_text="Similarity Score", range=[0, 1.15])
        st.plotly_chart(fig_cs, use_container_width=True)

    with col6:
        sec("Cross-Sell Pair Table", "📋")
        cs_d = cross_sell.copy()
        cs_d["similarity_score"] = cs_d["similarity_score"].apply(lambda x: f"{x:.2f}")
        cs_d.columns = ["Product","Pair With","Similarity"]
        st.dataframe(cs_d, use_container_width=True, height=380)

    sec("Product Feature Details", "📋")
    pf_d = prod_filt.copy()
    pf_d["total_revenue"] = pf_d["total_revenue"].apply(inr)
    pf_d["avg_price"]     = pf_d["avg_price"].apply(inr)
    pf_d.columns = ["Product","Category","Popularity Rank","Units Sold","Total Revenue",
                    "Avg Price","Avg Discount %","Price Band","Price Range","Popularity Score"]
    st.dataframe(pf_d, use_container_width=True, height=300)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 – DATA & EXPORT
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    sec("Download Ready Deliverables", "📥")
    st.success("✅ All files are production-ready for CRM, email personalization, and inventory planning.")

    col_d1, col_d2, col_d3 = st.columns(3)

    with col_d1:
        rec_exp = rec_prod.copy()
        rec_exp.insert(1, "customer_name", rec_exp["user_id"].map(get_name))
        st.download_button("⬇️  recommended_products.csv",
            data=rec_exp.to_csv(index=False).encode("utf-8"),
            file_name="recommended_products.csv", mime="text/csv",
            use_container_width=True)
        st.caption("💡 Website recs, email personalization")

    with col_d2:
        seg_exp = segments.copy()
        seg_exp.insert(1, "customer_name", seg_exp["customer_id"].map(get_name))
        st.download_button("⬇️  customer_segments.csv",
            data=seg_exp.to_csv(index=False).encode("utf-8"),
            file_name="customer_segments.csv", mime="text/csv",
            use_container_width=True)
        st.caption("💡 CRM integration, targeted campaigns")

    with col_d3:
        st.download_button("⬇️  sales_forecast.csv",
            data=forecast.to_csv(index=False).encode("utf-8"),
            file_name="sales_forecast.csv", mime="text/csv",
            use_container_width=True)
        st.caption("💡 Inventory planning, revenue projections")

    col_d4, col_d5, col_d6 = st.columns(3)
    with col_d4:
        st.download_button("⬇️  cross_sell_insights.csv",
            data=cross_sell.to_csv(index=False).encode("utf-8"),
            file_name="cross_sell_insights.csv", mime="text/csv",
            use_container_width=True)
        st.caption("💡 Bundle promos, upsell campaigns")
    with col_d5:
        st.download_button("⬇️  product_features.csv",
            data=prod_feat.to_csv(index=False).encode("utf-8"),
            file_name="product_features.csv", mime="text/csv",
            use_container_width=True)
        st.caption("💡 Product intelligence, pricing analysis")
    with col_d6:
        st.download_button("⬇️  customer_features.csv",
            data=cust_feat.to_csv(index=False).encode("utf-8"),
            file_name="customer_features.csv", mime="text/csv",
            use_container_width=True)
        st.caption("💡 ML training, feature engineering")

    sec("Data Preview", "👁️")
    ds_choice = st.selectbox("Choose dataset to preview:", [
        "Sales Forecast",
        "Customer Segments (with Names)",
        "Product Features",
        "Recommended Products (with Names)",
        "Cross-Sell Insights",
        "Customer Features",
        "Interaction Matrix",
    ])

    seg_nm  = segments.copy(); seg_nm.insert(1,"customer_name",seg_nm["customer_id"].map(get_name))
    rec_nm  = rec_prod.copy(); rec_nm.insert(1,"customer_name",rec_nm["user_id"].map(get_name))

    ds_map = {
        "Sales Forecast":                    forecast,
        "Customer Segments (with Names)":    seg_nm,
        "Product Features":                  prod_feat,
        "Recommended Products (with Names)": rec_nm,
        "Cross-Sell Insights":               cross_sell,
        "Customer Features":                 cust_feat,
        "Interaction Matrix":                inter_mat,
    }
    prev = ds_map[ds_choice]
    st.markdown(f"**Rows:** {len(prev):,} &nbsp;|&nbsp; **Columns:** {len(prev.columns)}")
    st.dataframe(prev.head(200), use_container_width=True, height=380)

    sec("API Integration Guide", "🔗")
    st.markdown("""
<div class='info-box'>
<h4 style='color:#1a3a9f;margin-top:0;font-size:15.5px;'>🔗 REST API Endpoints (Developer Integration)</h4>

<b style='color:#333;'>Get Recommendations for a User:</b><br>
<code style='background:#fff;border:1.5px solid #dde6ff;padding:5px 12px;border-radius:8px;
     font-family:JetBrains Mono,monospace;color:#426cff;font-size:13px;'>
GET /recommendations?user_id=C100000</code>

<br><br><b style='color:#333;'>Required Headers:</b><br>
<code style='background:#fff;border:1.5px solid #dde6ff;padding:5px 12px;border-radius:8px;
     font-family:JetBrains Mono,monospace;color:#8b5ef5;font-size:13px;'>
Authorization: Bearer &lt;your_token&gt;</code>

<br><br><b style='color:#333;'>Integration Use Cases:</b>
<ul style='line-height:2;color:#444;'>
  <li>🛍️ <b>Website</b> — Personalized suggestions on homepage &amp; product pages</li>
  <li>📧 <b>Email Marketing</b> — Top-3 recommendations in newsletters</li>
  <li>📋 <b>CRM</b> — Sync customer segments to sales team workflows</li>
  <li>📦 <b>Inventory</b> — Use forecast to plan restocking cycles</li>
  <li>📲 <b>Push Notifications</b> — Cross-sell alerts for at-risk customers</li>
</ul>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    sec("Project Summary", "ℹ️")
    cs1, cs2, cs3 = st.columns(3)
    kcard(cs1,"👥","Total Customers",  f"{segments['customer_id'].nunique():,}", "In dataset",   "#426cff")
    kcard(cs2,"📦","Total Products",   f"{prod_feat['product_name'].nunique():,}", "SKUs tracked","#10b981")
    kcard(cs3,"📅","Forecast Horizon", "90 Days",                                 "Jan–Mar 2024","#8b5ef5")
