import numpy as np
import matplotlib.pyplot as plt

def plot_predictions(series, forecast):
    x_series = np.arange(len(series))
    x_forecast = np.arange(len(series), len(series) + len(forecast))
    plt.plot(x_series, series, 'r', x_forecast, forecast, 'b')
    plt.show()