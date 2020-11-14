import flask
import pickle
from deploy.utils import convert_str_to_list
import model.model as mdl

app = flask.Flask(__name__)

@app.route('/fit_model', methods=['POST'])
def fit_model():
    data = flask.request.get_json(force=True)['data']
    pickle.dump(data, open("deploy/data.pkl", "wb"))

    model = mdl.fit_model(data)
    pickle.dump(model, open("deploy/arima_model.pkl", "wb"))

    return 'OK\n'

@app.route('/forecast', methods=['POST'])
def forecast():
    num_steps = flask.request.get_json(force=True)['num_steps']
    num_steps = int(num_steps)

    data = pickle.load(open("deploy/data.pkl", "rb"))
    model = pickle.load(open("deploy/arima_model.pkl", "rb"))
    forecast_result = mdl.forecast(data, model, num_steps)
    response = {'forecast_result': list(forecast_result)}

    return flask.jsonify(response)

if __name__ == '__main__':
    app.run()