# app.py
import streamlit as st
import matplotlib.pyplot as plt
from scipy import stats

from src.data_loader import load_data
from src.preprocessing import preprocess_data
from src.analysis import filter_relevant_period
from src.visualization import (
    plot_releases_by_year,
    plot_total_sales_by_platform,
    plot_sales_distribution,
    plot_regional_ranking,
    plot_median_sales_by_genre,
    plot_critic_score_vs_sales,
    plot_user_score_vs_sales,
    REGION_LABELS,
)
from src.hypothesis_testing import test_xbox_vs_pc, test_action_vs_sports  # <-- added test_action_vs_sports

# ---------- PAGE CONFIG & STYLING ----------
st.set_page_config(
    page_title="ICE Store | Video Game Sales Strategy",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
div[data-testid="stMetric"] {
    background-color: #ffffff;
    padding: 15px;
    border-radius: 8px;
    border-left: 5px solid #1f77b4;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}
.stAlert { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# ---------- CACHED DATA LOADING ----------
@st.cache_data
def get_analysis_data():
    """Load, clean, and prepare all computed values needed across sections."""
    raw = load_data()
    if raw.empty:
        return None, None, None, None
    df = preprocess_data(raw)
    df_recent = filter_relevant_period(df, start_year=2014)

    # Top-level metrics
    peak_year = df.groupby('year_of_release')['name'].count().idxmax()
    peak_count = df.groupby('year_of_release')['name'].count().max()
    top_platform = df_recent.groupby('platform')['total_sales'].sum().idxmax()
    top_platform_sales = df_recent.groupby('platform')['total_sales'].sum().max()
    median_sales_global = df_recent['total_sales'].median()
    top_genre = df_recent.groupby('genre')['total_sales'].median().idxmax()
    top_genre_median = df_recent.groupby('genre')['total_sales'].median().max()

    # Regional top platforms
    regional_tops = {}
    for col, label in REGION_LABELS.items():
        if col in df_recent.columns:
            top = df_recent.groupby('platform')[col].sum().idxmax()
            regional_tops[label] = top

    # Correlations (PS4 as default for display)
    ps4_data = df_recent[df_recent['platform'] == 'PS4']
    critic_corr = 0
    user_corr = 0
    if not ps4_data.empty:
        critic_clean = ps4_data.dropna(subset=['critic_score', 'total_sales'])
        user_clean = ps4_data.dropna(subset=['user_score', 'total_sales'])
        if len(critic_clean) > 1:
            critic_corr, _ = stats.pearsonr(critic_clean['critic_score'], critic_clean['total_sales'])
        if len(user_clean) > 1:
            user_corr, _ = stats.pearsonr(user_clean['user_score'], user_clean['total_sales'])

    # Hypothesis tests
    p_val, reject = test_xbox_vs_pc(df_recent, alpha=0.05)
    p_val2, reject2 = test_action_vs_sports(df_recent, alpha=0.05) 

    return (df, df_recent, {
        "peak_year": peak_year,
        "peak_count": peak_count,
        "top_platform": top_platform,
        "top_platform_sales": top_platform_sales,
        "median_sales_global": median_sales_global,
        "top_genre": top_genre,
        "top_genre_median": top_genre_median,
        "regional_tops": regional_tops,
        "critic_corr": critic_corr,
        "user_corr": user_corr,
        "p_value": p_val,
        "reject_h0": reject,
        "p_value2": p_val2,     
        "reject_h0_2": reject2,  
    })


with st.spinner("Loading historical sales data and preparing analysis..."):
    df_hist, df_recent, metrics = get_analysis_data()

if df_hist is None or df_recent is None:
    st.error("❌ data/games.csv not found. Please add the file to the 'data' folder.")
    st.stop()

# ---------- SIDEBAR NAVIGATION ----------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3081/3081648.png", width=80)
    st.title("ICE Store Analytics")
    st.markdown("Use the navigation below to explore the data story.")

    nav_option = st.radio(
        "Navigation",
        [
            "1. Business Context",
            "2. Market Trends & Platforms",
            "3. Regional & Genre Strategy",
            "4. Reviews & Player Satisfaction",
            "5. Final Recommendation",
        ],
    )

# ---------- FOOTER (fixed) ----------
footer = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #f8f9fa;
    color: #6c757d;
    text-align: center;
    padding: 10px 0;
    font-size: 14px;
    border-top: 1px solid #e9ecef;
    z-index: 999;
}
.block-container {
    padding-bottom: 80px;
}
</style>
<div class="footer">
    Developed by Leviton Lima Carvalho as a portfolio project | Data source: ICE Video game sales (1980‑2016)
</div>
"""
st.markdown(footer, unsafe_allow_html=True)

# ---------- MAIN CONTENT ----------
st.title("🎮 ICE Store — Video Game Sales Strategy for 2017")

# ==================== 1. BUSINESS CONTEXT ====================
if nav_option == "1. Business Context":
    st.header("1. The Business Question")
    st.markdown("""
    You are an analyst at **ICE Store**, a global video game retailer.  
    It's early **2017** and the company is planning a major campaign to boost sales.
    
    The CEO asks three key questions:
    1. **Which platforms** should we focus on?  
    2. **Which genres** offer the safest return on investment?  
    3. **Do critic / user reviews** significantly drive sales, or should we rely on other marketing channels?
    
    We have historical sales data from **1980 to 2016** across multiple regions and platforms.
    The goal is to **use data to back every strategic decision** and minimize risk.
    """)

    st.info("""
    **Note on the data:** The dataset contains over 16,000 game titles with regional sales (NA, EU, JP, Other),
    critic scores, user scores, and genres. All monetary values are in **millions of USD**.
    """)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Games in Dataset", f"{len(df_hist):,}")
    col2.metric("Years Covered", "1980 – 2016")
    col3.metric("Regions Analyzed", "NA, EU, JP, Global")

# ==================== 2. MARKET TRENDS & PLATFORMS ====================
elif nav_option == "2. Market Trends & Platforms":
    st.header("2. Historical Releases & Platform Dominance")

    # 2a. Releases by year
    st.subheader("📈 How Many Games Were Launched?")
    col1, col2 = st.columns([2, 1])
    with col1:
        fig1 = plot_releases_by_year(df_hist)
        st.pyplot(fig1)
    with col2:
        st.metric("Peak Year", metrics["peak_year"])
        st.metric("Max Titles", f"{metrics['peak_count']:,}")

    st.success(
        f"The industry peaked in **{metrics['peak_year']}** with **{metrics['peak_count']:,}** new games. "
        "After that, releases declined – likely due to console generation transitions and the rise of mobile platforms."
    )

    # 2b. Platform dominance (recent period)
    st.subheader("🕹️ Which Platforms Lead the Current Market (2014‑2016)?")
    fig2 = plot_total_sales_by_platform(df_recent)
    st.pyplot(fig2)

    col1, col2 = st.columns(2)
    col1.metric("Top Platform", metrics["top_platform"])
    col2.metric("Total Sales (Millions USD)", f"${metrics['top_platform_sales']:.0f}M")

    st.success(
        f"**{metrics['top_platform']}** dominates global sales in the recent period, "
        "with PS4 and Xbox One forming the core of the current console generation. "
        "Older platforms (PS3, X360) still appear but are clearly fading. "
        "A 2017 campaign **must include PS4 and Xbox One** as primary targets."
    )

    # 2c. Sales distribution
    st.subheader("📊 The Blockbuster Reality")
    fig3 = plot_sales_distribution(df_recent)
    st.pyplot(fig3)

    st.metric("Median Global Sale per Title", f"{metrics['median_sales_global']:.2f} M copies")

    st.success(
        f"The median game sells only **{metrics['median_sales_global']:.2f} million** copies. "
        "A tiny fraction of titles become blockbusters and earn most of the revenue. "
        "For financial planning, assume a **median performance**, not a mega‑hit."
    )

# ==================== 3. REGIONAL & GENRE STRATEGY ====================
elif nav_option == "3. Regional & Genre Strategy":
    st.header("3. Where and What to Sell")

    # 3a. Regional platforms
    st.subheader("🌍 Regional Platform Preferences")
    for col, label in REGION_LABELS.items():
        if col in df_recent.columns:
            fig = plot_regional_ranking(df_recent, col)
            st.pyplot(fig)
            top = metrics["regional_tops"].get(label, "N/A")
            st.caption(f"**{label}** → #1 platform: `{top}`")

    st.success(
        "North America and Europe follow a similar pattern (PS4 > XOne > X360). "
        "**Japan is an outlier** — handhelds (3DS) and local consoles dominate. "
        "A global campaign must adapt platform choice to each region, especially Japan."
    )

    # 3b. Genre median sales
    st.subheader("🎮 Which Genres Are the Safest Bet?")
    fig5 = plot_median_sales_by_genre(df_recent, 'total_sales')
    st.pyplot(fig5)

    col1, col2 = st.columns(2)
    col1.metric("Top Genre (Median Sales)", metrics["top_genre"])
    col2.metric("Median Sales (Millions USD)", f"${metrics['top_genre_median']:.2f}M")

    st.success(
        f"**{metrics['top_genre']}** leads with a median sale of {metrics['top_genre_median']:.2f}M. "
        "Shooter, Sports, and Platform games consistently show above‑average medians. "
        "Focusing on these genres reduces the risk of under‑performance."
    )

# ==================== 4. REVIEWS & PLAYER SATISFACTION ====================
elif nav_option == "4. Reviews & Player Satisfaction":
    st.header("4. Do Scores Predict Sales?")

    platform_choice = st.selectbox(
        "Pick a platform for the scatter plots:",
        ["PS4", "XOne", "PC", "3DS", "WiiU"],
        index=0,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Critic Score vs Sales")
        fig_critic = plot_critic_score_vs_sales(df_recent, platform=platform_choice)
        st.pyplot(fig_critic)
    with col2:
        st.subheader("User Score vs Sales")
        fig_user = plot_user_score_vs_sales(df_recent, platform=platform_choice)
        st.pyplot(fig_user)

    # Correlations for selected platform (recompute for interactivity)
    plat_df = df_recent[df_recent['platform'] == platform_choice]
    corr_critic, corr_user = 0, 0
    if not plat_df.empty:
        critic_clean = plat_df.dropna(subset=['critic_score', 'total_sales'])
        user_clean = plat_df.dropna(subset=['user_score', 'total_sales'])
        if len(critic_clean) > 1:
            corr_critic, _ = stats.pearsonr(critic_clean['critic_score'], critic_clean['total_sales'])
        if len(user_clean) > 1:
            corr_user, _ = stats.pearsonr(user_clean['user_score'], user_clean['total_sales'])

    col1, col2 = st.columns(2)
    col1.metric("Critic ↔ Sales (r)", f"{corr_critic:.3f}")
    col2.metric("User ↔ Sales (r)", f"{corr_user:.3f}")

    st.success(
        f"Critic scores show a moderate positive correlation with sales (r = {corr_critic:.3f}), "
        "suggesting that critically acclaimed titles tend to perform better commercially. "
        f"User scores, on the other hand, show negligible correlation (r = {corr_user:.3f}) — "
        "marketing campaigns should leverage professional accolades rather than community ratings."
    )

    # ── Hypothesis Test 1: XOne vs PC ──
    st.subheader("🔬 Hypothesis 1: Are Xbox One and PC Players Equally Satisfied?")
    st.markdown("""
    - **H0:** Average user ratings for Xbox One and PC are the same.  
    - **H1:** Average user ratings for Xbox One and PC are different.
    """)

    p_val, reject = test_xbox_vs_pc(df_recent, alpha=0.05)
    st.metric("Welch's t‑test p‑value (XOne vs PC)", f"{p_val:.4e}")

    if reject:
        st.success(
            f"p = {p_val:.4e} **< 0.05** → We reject H0. "
            "There is a statistically significant difference in average user scores between Xbox One and PC."
        )
    else:
        st.success(
            f"p = {p_val:.4e} **> 0.05** → We cannot reject H0. "
            "No significant difference in average user scores was found between Xbox One and PC — "
            "both platforms appear equally satisfying to players."
        )

    # ── Hypothesis Test 2: Action vs Sports ──
    st.subheader("🔬 Hypothesis 2: Do Action and Sports Players Rate Games Differently?")
    st.markdown("""
    - **H0:** Average user ratings for Action and Sports genres are the same.  
    - **H1:** Average user ratings for Action and Sports genres are different.
    """)

    p_val2, reject2 = test_action_vs_sports(df_recent, alpha=0.05)
    st.metric("Welch's t‑test p‑value (Action vs Sports)", f"{p_val2:.4e}")

    if reject2:
        st.success(
            f"p = {p_val2:.4e} **< 0.05** → We reject H0. "
            "There is a statistically significant difference in average user scores between Action and Sports games."
        )
    else:
        st.success(
            f"p = {p_val2:.4e} **> 0.05** → We cannot reject H0. "
            "No significant difference in average user scores was found between Action and Sports games."
        )

# ==================== 5. FINAL RECOMMENDATION ====================
elif nav_option == "5. Final Recommendation":
    st.header("5. Strategic Recommendations for the 2017 Campaign")

    st.success("""
    ### ✅ Final Strategy: How to Maximize the Campaign's Success
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Primary Platforms", "PS4, Xbox One")
        st.metric("Secondary (Japan)", "3DS, PS4")
    with col2:
        st.metric("Safe Genres", f"{metrics['top_genre']}, Shooter, Sports")
        st.metric("Median Sales Benchmark", f"~{metrics['median_sales_global']:.2f}M copies")

    st.markdown("""
    **Summary of the data‑backed logic:**
    1. **Platform choice:** PS4 and Xbox One dominate global sales; Japan requires a separate handheld strategy (3DS + RPG focus).
    2. **Genre selection:** Shooters, Sports, and Action/Adventure have the highest median sales – lower risk per title released.
    3. **Financial planning:** Budget for the median (~0.1M copies); treat a blockbuster as a bonus, not a baseline.
    4. **Marketing focus:** Critic scores show a moderate positive correlation with sales — leverage professional accolades. User scores have negligible impact and should not drive campaign decisions.
    5. **Regional nuance:** Keep North America/Europe unified (Shooter/Action, rated M); create a tailored Japanese release with handheld support and RPG catalog.

    All decisions are grounded in historical data up to 2016, simulating exactly what we would know in early 2017.
    """)