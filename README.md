# 🎮 ICE Store — Video Game Sales Strategy
*Data-driven campaign planning for a global video game retailer*

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Wrangling-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-Bootstrap-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live%20App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://ice-store-analytics-levitoncarvalho.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)

<br>

**[🚀 Try the Live App](https://ice-store-analytics-levitoncarvalho.streamlit.app/)** &nbsp;|&nbsp; **[📓 View Full Notebook](https://github.com/levitoncarvalho/ice-store-analytics/blob/main/notebook/exploration_v1.ipynb)**


</div>


> ⚠️ **Disclaimer:** ICE Store is a **fictional video game retailer** created exclusively for academic and portfolio purposes. This project was developed to demonstrate technical skills in exploratory data analysis, statistical hypothesis testing, and data-driven strategy. The dataset covers video game sales from 1980 to 2016. All monetary values are in **millions of USD**. No real company or business relationship is represented here.

---

## 🧩 Business Problem

> *"It's early 2017. ICE Store, a global video game retailer, needs to plan its annual campaign. Which platforms should we bet on? Which genres are the safest investment? Do review scores actually drive sales?"*

The goal is to use historical sales data to answer these questions and back every strategic decision with data — minimizing risk and maximizing ROI for the 2017 campaign.

| Risk Area | Without Data | With This Analysis |
|---|---|---|
| 🔴 Platform selection | Guesswork across 30+ platforms | Focus on PS4 & Xbox One (proven dominance) |
| 🟡 Genre investment | Equal budget across all genres | Prioritize Shooter, Sports & Action (highest median) |
| 🟢 Regional strategy | One-size-fits-all campaign | Separate strategies for West vs Japan |

---

## 📊 Results & Key Findings

| Question | Finding |
|---|---|
| 🏆 Top global platform (2014–2016) | **PS4** |
| 🎯 Top genre by median sales | **Shooter** |
| 📦 Median sales per title | **~0.11M copies** |
| 🌍 Japan outlier | **3DS dominates**, not PS4/XOne |
| 🎬 Critic score vs sales | **Moderate positive correlation** |
| 👤 User score vs sales | **Negligible correlation** |
| 🧪 XOne vs PC user ratings (t-test) | p = 0.1160 → **Cannot reject H0** |
| 🧪 Action vs Sports user ratings (t-test) | p ≈ 1.83e-14 → **Reject H0** |

---

## 🔄 Project Pipeline

```
games.csv
    │
    ▼
[ data_loader.py ]  →  Load raw CSV
    │
    ▼
[ preprocessing.py ]  →  Clean columns, fix types, create total_sales
    │
    ▼
[ analysis.py ]  →  Filter 2014–2016 relevant period
    │
    ├──▶ [ visualization.py ]  →  Generate all charts
    │
    ├──▶ [ hypothesis_testing.py ]  →  Welch's t-tests
    │
    ▼
[ main.py ]  →  CLI pipeline (saves reports/ PNGs)
[ app.py ]   →  Streamlit interactive dashboard
```

---

## 📁 1. Project Structure

```
ice-store-analytics/
│
├── 📂 data/
│   └── games.csv                  # Raw dataset (1980–2016)
│
├── 📂 notebook/
│   └── exploration_v1.ipynb       # Full EDA & analysis notebook
│
├── 📂 reports/                    # Auto-generated chart exports (main.py)
│   ├── 01_releases_historical.png
│   ├── 02_platform_sales_recent.png
│   ├── 03_sales_distribution.png
│   ├── 05_top5_NA.png
│   ├── 06_top5_EU.png
│   ├── 07_top5_JP.png
│   ├── 08_median_sales_by_genre_global.png
│   ├── 09_critic_impact_ps4.png
│   └── 10_user_impact_ps4.png
│
├── 📂 src/                        # Modular source code
│   ├── __init__.py
│   ├── data_loader.py             # CSV loading
│   ├── preprocessing.py           # Data cleaning & feature engineering
│   ├── analysis.py                # Filtering & aggregations
│   ├── visualization.py           # All matplotlib/seaborn charts
│   └── hypothesis_testing.py      # Welch's t-tests
│
├── app.py                         # Streamlit dashboard
├── main.py                        # CLI pipeline entry point
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 🔍 2. Exploratory Data Analysis

The notebook covers the full EDA journey:

- Distribution of game releases per year (peak: 2008–2009)
- Platform lifecycle analysis — which platforms are rising, peaking, or fading
- Regional sales breakdown across North America, Europe, and Japan
- Genre profitability by median sales (not mean, to avoid blockbuster distortion)
- Critic and user score distributions and their relationship with sales

---

## 🕹️ 3. Platform & Regional Analysis

| Region | #1 Platform | #2 Platform | Notable Pattern |
|---|---|---|---|
| 🌎 North America | PS4 | Xbox One | Shooter/Action dominant |
| 🌍 Europe | PS4 | Xbox One | Similar to NA |
| 🗾 Japan | 3DS | PS4 | Handhelds + RPG preferred |
| 🌐 Global | PS4 | Xbox One | 8th gen consoles lead |

---

## 🎮 4. Genre Strategy

Median sales were used instead of mean to measure consistent ROI per title — avoiding the distortion caused by rare blockbuster hits.

| Genre | Median Sales | Risk Level |
|---|---|---|
| Shooter | Highest | 🟢 Low |
| Sports | High | 🟢 Low |
| Action | High (volume) | 🟡 Medium |
| RPG | Moderate | 🟡 Medium (JP-specific) |
| Strategy | Low | 🔴 High |

---

## 🧪 5. Statistical Hypothesis Testing

Two independent Welch's t-tests were conducted at α = 0.05.

**Hypothesis 1 — Platforms (XOne vs PC):**
- H₀: Average user ratings for Xbox One and PC are the same.
- H₁: Average user ratings for Xbox One and PC are different.
- Result: p = 0.1160 → **Cannot reject H₀.** Both platforms are equally satisfying to players.

**Hypothesis 2 — Genres (Action vs Sports):**
- H₀: Average user ratings for Action and Sports are the same.
- H₁: Average user ratings for Action and Sports are different.
- Result: p ≈ 1.83e-14 → **Reject H₀.** User satisfaction differs significantly between genres.

---

## 🚀 6. Setup & Usage

```bash
# 1. Clone the repository
git clone https://github.com/your-username/ice-store-analytics.git
cd ice-store-analytics

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add the dataset
# Place games.csv inside the data/ folder

# 5a. Run the CLI pipeline (saves charts to reports/)
python main.py

# 5b. Run the Streamlit dashboard
streamlit run app.py
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Core language |
| Pandas | Data loading, cleaning & aggregation |
| NumPy | Numerical operations |
| Matplotlib & Seaborn | Data visualization |
| SciPy | Statistical hypothesis testing |
| Streamlit | Interactive web dashboard |

---

## 💡 Key Takeaways

1. **PS4 and Xbox One** are the undisputed platforms for a Western-focused 2017 campaign.
2. **Japan is a separate market** — handhelds and RPGs require a dedicated strategy.
3. **Shooter and Sports** genres offer the most consistent median sales with lower investment risk.
4. **Critic scores** have a moderate positive correlation with sales — leverage professional accolades in marketing. **User scores** have negligible impact.
5. **Budget for the median (~0.11M copies)** — blockbusters are outliers, not the baseline.

---

## 👨‍💻 Author

<div align="center">

**Leviton Lima Carvalho**
*Data Scientist | Machine Learning | Python*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-levitoncarvalho-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/levitoncarvalho/)
[![GitHub](https://img.shields.io/badge/GitHub-levitoncarvalho-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/levitoncarvalho)
[![Email](https://img.shields.io/badge/Email-levitoncarvalho@icloud.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:levitoncarvalho@icloud.com)

</div>

---

## 📄 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for more details.
