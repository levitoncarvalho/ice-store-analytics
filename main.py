# main.py
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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
from src.hypothesis_testing import test_xbox_vs_pc, test_action_vs_sports

REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)

def save_and_close(fig, filename):
    path = os.path.join(REPORT_DIR, filename)
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    print(f"   📊 Saved {filename}")

def narrative_section(title):
    print("\n" + "=" * 70)
    print(f"   {title}")
    print("=" * 70)

def main():
    print("▶ Loading and cleaning data...")
    raw = load_data()
    if raw.empty:
        print("❌ data/games.csv not found.")
        return
    df = preprocess_data(raw)
    df_recent = filter_relevant_period(df, start_year=2014)
    print("✅ Data ready.")

    # 1. Historical overview
    narrative_section("1. HISTORICAL OVERVIEW – How many games were launched?")
    fig1 = plot_releases_by_year(df)
    save_and_close(fig1, "01_releases_historical.png")
    peak_year = df.groupby('year_of_release')['name'].count().idxmax()
    peak_count = df.groupby('year_of_release')['name'].count().max()
    print(f"📈 Peak in {peak_year} with {peak_count} titles.")

    # 2. Platform dominance
    narrative_section("2. PLATFORM DOMINANCE (2014-2016)")
    fig2 = plot_total_sales_by_platform(df_recent)
    save_and_close(fig2, "02_platform_sales_recent.png")
    top_platform = df_recent.groupby('platform')['total_sales'].sum().idxmax()
    print(f"🏆 Dominant platform: {top_platform}")

    # 3. Sales distribution
    narrative_section("3. SALES DISTRIBUTION")
    fig3 = plot_sales_distribution(df_recent)
    save_and_close(fig3, "03_sales_distribution.png")
    median_sales = df_recent['total_sales'].median()
    print(f"📦 Median global sale: {median_sales:.2f}M copies.")

    # 4. Regional preferences
    narrative_section("4. REGIONAL PREFERENCES")
    regions = [('na_sales', '05_top5_NA.png'),
               ('eu_sales', '06_top5_EU.png'),
               ('jp_sales', '07_top5_JP.png')]
    for col, fname in regions:
        fig = plot_regional_ranking(df_recent, col)
        save_and_close(fig, fname)
        top_plat = df_recent.groupby('platform')[col].sum().idxmax()
        print(f"🌍 {REGION_LABELS.get(col, col)}: #1 → {top_plat}")

    # 5. Genre profitability
    narrative_section("5. GENRE MEDIAN SALES")
    fig5 = plot_median_sales_by_genre(df_recent, 'total_sales')
    save_and_close(fig5, "08_median_sales_by_genre_global.png")
    top_genre = df_recent.groupby('genre')['total_sales'].median().idxmax()
    print(f"🎮 Top median-sales genre: {top_genre}")

    # 6. Reviews vs sales
    narrative_section("6. REVIEWS vs SALES (PS4)")
    for score_type, func, fname in [
        ('critic', plot_critic_score_vs_sales, "09_critic_impact_ps4.png"),
        ('user', plot_user_score_vs_sales, "10_user_impact_ps4.png")
    ]:
        fig = func(df_recent, platform='PS4')
        save_and_close(fig, fname)
        data = df_recent[df_recent['platform'] == 'PS4'].dropna(subset=[f'{score_type}_score', 'total_sales'])
        if len(data) > 1:
            corr, _ = stats.pearsonr(data[f'{score_type}_score'], data['total_sales'])
            print(f"📈 {score_type} correlation: r = {corr:.3f}")

    # 7. Hypothesis test
    narrative_section("7.1 STATISTICAL TEST – Xbox One vs PC user scores")
    p_val, reject = test_xbox_vs_pc(df_recent, alpha=0.05)

    print(f"🧪 p-value = {p_val:.4e}")
    if reject:
        print("❌ Significant difference.")
    else:
        print("✅ No significant difference.")
    
    narrative_section("7. STATISTICAL TEST – Action vs Sports")
    p_val2, reject2 = test_action_vs_sports(df_recent, alpha=0.5)
    p_val2, reject2 = test_action_vs_sports(df_recent, alpha=0.05)
    print(f"🧪 p-value (Action vs Sports) = {p_val2:.4e}")
    if reject2:
        print("❌ Significant difference.")
    else:
        print("✅ No significant difference.")

    # 8. Final recommendations
    narrative_section("8. FINAL STRATEGY FOR 2017")
    print("""
• Lead platforms: PS4 & Xbox One.
• Genre: Shooters, Sports, Action – higher medians.
• Sales expectation: median ~0.1M units → budget accordingly.
• Reviews matter less than community & marketing.
• Japan requires a separate platform strategy (handhelds).
All plots saved in 'reports/' folder.
""")

if __name__ == "__main__":
    main()