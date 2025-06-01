import pandas as pd
import statsmodels.api as sm

def regression_accidents(df):
    yearly = df.groupby('Year').size().reset_index(name='Count')
    X = sm.add_constant(yearly['Year'])
    y = yearly['Count']
    model = sm.OLS(y, X).fit()
    print(model.summary())
    return model