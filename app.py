import flask
import pickle
import model.model as mdl

app = flask.Flask(__name__)
data = pickle.load(open("deploy/data.pkl", "rb"))
model = pickle.load(open("deploy/arima_model.pkl", "rb"))

@app.route('/fit_model', methods=['POST'])
def fit_model():
    data = flask.request.get_json()['data']
    model = mdl.fit_model(data)

    return 'New model created\n'

@app.route('/forecast', methods=['POST'])
def forecast():
    num_steps = flask.request.get_json()['num_steps']
    num_steps = int(num_steps)

    forecast_result = mdl.forecast(data, model, num_steps)
    response = {'forecast_result': list(forecast_result)}

    return flask.jsonify(response)

if __name__ == '__main__':
    app.run()