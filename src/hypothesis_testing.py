import pandas as pd
from scipy import stats

def test_xbox_vs_pc(df, alpha=0.05):

    xone_scores = df[df['platform'] == 'XOne']['user_score'].dropna()
    pc_scores = df[df['platform'] == 'PC']['user_score'].dropna()
    
    stat, p_value = stats.ttest_ind(xone_scores, pc_scores, equal_var=False)
    reject_null = p_value < alpha
    
    return p_value, reject_null

def test_action_vs_sports(df, alpha=0.05):
    action_scores = df[df['genre'] == 'Action']['user_score'].dropna()
    sports_scores = df[df['genre'] == 'Sports']['user_score'].dropna()
    
    stat, p_value = stats.ttest_ind(action_scores, sports_scores, equal_var=False)
    reject_null = p_value < alpha
    
    return p_value, reject_null