import pandas as pd
import numpy as np

def zscore_anomalies(df, threshold=2):
    yearly = df.groupby('Year').size().reset_index(name='Count')
    mean = yearly['Count'].mean()
    std = yearly['Count'].std()
    yearly['Z'] = (yearly['Count'] - mean) / std
    anomalies = yearly[yearly['Z'].abs() > threshold]
    print(anomalies)
    return anomalies