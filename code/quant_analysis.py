import pandas as pd
import os
import statsmodels.api as sm

IN_PATH = os.path.join("data", "clean", "imdb_clean.csv")
OUTPUT_DIR = "quantitative analysis"
REVENUE_OLS_PATH = os.path.join(OUTPUT_DIR, "revenue_ols_regression.csv")
IMDB_OLS_PATH = os.path.join(OUTPUT_DIR, "imdb_ols_regression.csv")
METASCORE_OLS_PATH = os.path.join(OUTPUT_DIR, "metascore_ols_regression.csv")
SUMMARY_PATH = os.path.join(OUTPUT_DIR, "decade_analysis.csv")

df = pd.read_csv(IN_PATH)
dummy_cols = df.columns[10:-1]

def decade_summary(out_path):
    '''Group data by decade and convert summary statistics to csv'''   
    
    (
    df.assign(Decade=lambda df: (df["ReleaseYear"]//10)*10)
    .drop("ReleaseYear", axis=1)
    .groupby("Decade")
    .describe()
    .round(decimals=2)
    .to_csv(SUMMARY_PATH)
    )


def revenue_ols_regression(out_path):
    '''Perform OLS regression of movie Revenue on IMBD Rating, Metascore, Release Year, and genre dummies and create csv'''
    
    x_cols = ["IMDBRating", "Metascore", "ReleaseYear"]
    for col in dummy_cols:
        x_cols.append(col)

    x = df[x_cols]
    y = df["GrossRevenue"]
    model = sm.OLS(y, sm.add_constant(x))
    model_fit = model.fit()
    model_fit_summary = model_fit.summary()

    model_as_html = model_fit_summary.tables[1].as_html()
    pd.read_html(model_as_html, header=0, index_col=0)[0].to_csv(out_path)

def imdb_ols_regression(out_path):
    '''Perform OLS regression of IMBD Rating on genre dummies and create csv'''
    
    x = df[dummy_cols]
    y = df["IMDBRating"]
    model = sm.OLS(y, sm.add_constant(x))
    model_fit = model.fit()
    model_fit_summary = model_fit.summary()

    model_as_html = model_fit_summary.tables[1].as_html()
    pd.read_html(model_as_html, header=0, index_col=0)[0].to_csv(out_path)
    
def metascore_ols_regression(out_path):
    '''Perform OLS regression of Metascore on genre dummies and create csv'''
    
    x = df[dummy_cols]
    y = df["Metascore"]
    model = sm.OLS(y, sm.add_constant(x))
    model_fit = model.fit()
    model_fit_summary = model_fit.summary()

    model_as_html = model_fit_summary.tables[1].as_html()
    pd.read_html(model_as_html, header=0, index_col=0)[0].to_csv(out_path)


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    decade_summary(SUMMARY_PATH)
    revenue_ols_regression(REVENUE_OLS_PATH)
    imdb_ols_regression(IMDB_OLS_PATH)
    metascore_ols_regression(METASCORE_OLS_PATH)