import json, time, flask, pickle

app = flask.Flask(__name__)

# Initialise task id, on hold flag and forecast results
data = pickle.load(open("data.pkl", "rb"))
model = pickle.load(open("arima_model.pkl", "rb"))
model_timestamp = time.time()

@app.route('/post_data', methods=['POST'])
def post_data():
    global data
    print(flask.request.data)
    data = pickle.loads(flask.request.data)
    return 'OK'

@app.route('/post_model', methods=['POST'])
def post_model():
    global model, model_timestamp
    model = pickle.loads(flask.request.data)
    model_timestamp = time.time()
    return 'OK'

@app.route('/get_model_timestamp')
def foreget_model_timestampcast():
    return flask.jsonify({'model_timestamp': model_timestamp})

@app.route('/get_data')
def get_data():
    return pickle.dumps(data)

@app.route('/get_model')
def get_model():
    return pickle.dumps(model)

if __name__ == '__main__':
    # Run flask
    app.run(threaded=True, host='0.0.0.0', port=5001)