import matplotlib.pyplot as plt
import seaborn as sns

# Mapping for cleaner chart labels
REGION_LABELS = {
    'na_sales': 'North America',
    'eu_sales': 'Europe',
    'jp_sales': 'Japan',
    'total_sales': 'Global'
}

def plot_releases_by_year(df):
    #Line plot showing the number of game releases per year.
    releases = df.groupby('year_of_release')['name'].count()
    fig, ax = plt.subplots(figsize=(5.6, 2.8))
    releases.plot(kind='line', marker='o', color='#1f77b4', ax=ax)
    
    ax.set_title('Game Releases per Year (Historical)', fontsize=14)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Number of Titles', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.5)
    return fig

def plot_total_sales_by_platform(df):
    #Bar plot of total global sales by platform (2014-2016).
    platform_sales = df.groupby('platform')['total_sales'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8.4, 4.2))
    sns.barplot(x=platform_sales.index, y=platform_sales.values,
                hue=platform_sales.index, palette='magma', ax=ax, legend=False)
    
    ax.set_title('Total Sales by Platform (2014-2016)', fontsize=14)
    ax.set_xlabel('Platform', fontsize=12)
    ax.set_ylabel('Total Sales (Millions USD)', fontsize=12)
    return fig

def plot_sales_distribution(df):
    # Box plot of global sales distribution by platform.
    fig, ax = plt.subplots(figsize=(8.4, 4.9))
    sns.boxplot(data=df, x='platform', y='total_sales', ax=ax)
    
    ax.set_ylim(0, 2)
    ax.set_title('Global Sales Distribution by Platform', fontsize=14)
    ax.set_xlabel('Platform', fontsize=12)
    ax.set_ylabel('Global Sales (Millions USD)', fontsize=12)
    return fig

def plot_regional_ranking(df, region_col):
    """Bar plot of the top 5 platforms by sales in a specific region."""
    top_platforms = df.groupby('platform')[region_col].sum().sort_values(ascending=False).head(5)
    fig, ax = plt.subplots(figsize=(5.6, 3.5))
    label = REGION_LABELS.get(region_col, region_col)
    sns.barplot(x=top_platforms.index, y=top_platforms.values,
                hue=top_platforms.index, palette='Blues_r', ax=ax, legend=False)
    
    ax.set_title(f'Top 5 Platforms in {label}', fontsize=13)
    ax.set_ylabel('Total Sales (Millions USD)', fontsize=11)
    ax.set_xlabel('Platform', fontsize=11)
    return fig

def plot_median_sales_by_genre(df, sales_col='total_sales'):
    # Bar plot of median sales by genre, filtering out non-positive medians.
    genre_data = df.groupby('genre')[sales_col].median().sort_values(ascending=False)
    genre_data = genre_data[genre_data > 0]
    
    fig, ax = plt.subplots(figsize=(7, 3.5))
    label = REGION_LABELS.get(sales_col, sales_col)
    sns.barplot(x=genre_data.index, y=genre_data.values,
                hue=genre_data.index, palette='viridis', ax=ax, legend=False)
    
    ax.set_title(f'Median Sales by Genre: {label}', fontsize=13)
    ax.set_ylabel('Median Sales (Millions USD)', fontsize=11)
    ax.set_xlabel('Genre', fontsize=11)
    plt.xticks(rotation=45)
    return fig

def plot_critic_score_vs_sales(df, platform='PS4'):
    # Scatter plot of critic score vs. total sales for a given platform.
    data = df[df['platform'] == platform]
    fig, ax = plt.subplots(figsize=(5.6, 3.5))
    sns.scatterplot(data=data, x='critic_score', y='total_sales', alpha=0.6, ax=ax)
    
    ax.set_title(f'Critic Score vs Sales ({platform})', fontsize=13)
    ax.set_xlabel('Score (0-100)', fontsize=11)
    ax.set_ylabel('Sales (Millions USD)', fontsize=11)
    return fig

def plot_user_score_vs_sales(df, platform='PS4'):
    # Scatter plot of user score vs. total sales for a given platform.
    data = df[df['platform'] == platform]
    fig, ax = plt.subplots(figsize=(5.6, 3.5))
    sns.scatterplot(data=data, x='user_score', y='total_sales', alpha=0.5, ax=ax, color='orange')
    
    ax.set_title(f'User Score vs Sales ({platform})', fontsize=13)
    ax.set_xlabel('Score (0-10)', fontsize=11)
    ax.set_ylabel('Sales (Millions USD)', fontsize=11)
    return fig