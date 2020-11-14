import pandas as pd
from model import fit_model, forecast

series = pd.read_csv('../data/dataset.csv', header=0, index_col=0)
X = series.values
num_steps = 5000

model = fit_model(X)
forecast_result = forecast(X, model, num_steps)