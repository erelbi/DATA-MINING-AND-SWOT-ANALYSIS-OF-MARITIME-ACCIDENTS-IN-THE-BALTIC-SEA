import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

def run_rules(df):
    onehot = pd.get_dummies(df['Acc_Type'])
    freq_items = apriori(onehot, min_support=0.1, use_colnames=True)
    rules = association_rules(freq_items, metric='confidence', min_threshold=0.6)
    print(rules[['antecedents', 'consequents', 'support', 'confidence']])
    return rules