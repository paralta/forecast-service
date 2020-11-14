import pandas as pd
from model import fit_model, forecast
from utils import plot_predictions

series = pd.read_csv('../data/dataset.csv', header=0, index_col=0)
X = series.values
num_steps = 10

model = fit_model(X)
forecast_result = forecast(X, model, num_steps)
plot_predictions(X, forecast_result)