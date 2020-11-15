import time
import flask
import pickle
import model.model as mdl
import threading, queue
from collections import namedtuple

app = flask.Flask(__name__)

# Initialise data and model from file
data = pickle.load(open("model/data.pkl", "rb"))
model = pickle.load(open("model/arima_model.pkl", "rb"))

# Initialise task queue and data
q = queue.Queue()
Task = namedtuple('Task', 'type data id')
task_id = 0

# Initialise flag to indicate if model creation is in progress
on_hold = False

# Initialise hash map to save forecast results
forecast_results = {}

@app.route('/fit_model', methods=['POST'])
def fit_model():
    # Get data from request
    data = flask.request.get_json()['data']

    # Add create model task to queue
    q.put(Task('fit_model', data, None))

    return 'New model is being created\n'

@app.route('/forecast', methods=['POST'])
def forecast():
    # Get number of steps from request
    num_steps = int(flask.request.get_json()['num_steps'])

    # Get new task id and add compute forecast task to queue
    global task_id
    task_id += 1
    q.put(Task('forecast', num_steps, task_id))

    # Return json with task id
    return flask.jsonify( {'task_id': task_id})

@app.route('/forecast_result', methods=['POST'])
def forecast_result():
    # Get number of steps from request
    task_id = int(flask.request.get_json()['task_id'])

    # Return json with forecast result
    return flask.jsonify({'forecast_result': forecast_results[task_id]})

def processing_unit():
    # Use global variables
    global data, model, on_hold, forecast_response

    while True:
        task = q.get()

        # Wait until new model is created
        while on_hold:
            print('Waiting while new model is being created')
            time.sleep(1)

        # Process fit model task
        if task.type == 'fit_model':
            on_hold = True
            data = task.data
            model = mdl.fit_model(data)
            on_hold = False
            print('New model has been created')

        # Process compute forecast task
        elif task.type == 'forecast':
            forecast_result = mdl.forecast(data, model, task.data)
            forecast_results[task.id] = list(forecast_result)
            print('New forecast result has been computed')

        q.task_done()

if __name__ == '__main__':
    # Start n threads of processing unit
    num_threads = 3
    for _ in range(num_threads):
        threading.Thread(target=processing_unit).start()

    # Run flask
    app.run(host='0.0.0.0', port=5000)