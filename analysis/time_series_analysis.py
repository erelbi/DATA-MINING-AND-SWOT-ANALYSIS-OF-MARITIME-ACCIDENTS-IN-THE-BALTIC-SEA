import pandas as pd
import matplotlib.pyplot as plt

def plot_annual_accidents(df):
    summary = df.groupby('Year').size()
    summary.plot(kind='line', marker='o', title='Annual Accidents')
    plt.xlabel('Year')
    plt.ylabel('Number of Accidents')
    plt.show()