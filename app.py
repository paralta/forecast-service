import json, pika, time, flask

app = flask.Flask(__name__)

# Initialise task id, on hold flag and forecast results
task_id = 0
on_hold = False
forecast_results = {}

@app.route('/fit_model', methods=['POST'])
def fit_model():
    global on_hold

    # Wait if model creation is in progress
    while on_hold:
        print('Waiting while new model is being created')
        time.sleep(1)

    # Get data from request
    data = flask.request.get_json()['data']

    # Block other tasks from being added to queue
    on_hold = True

    # Add create model task to queue
    task = {'type': 'fit_model', 'data': data}
    channel.basic_publish(exchange='', routing_key='task', body=json.dumps(task))

    print('New model is being created\n')
    return 'OK'

@app.route('/forecast', methods=['POST'])
def forecast():
    global task_id, on_hold

    # Get number of steps from request
    num_steps = int(flask.request.get_json()['num_steps'])

    # Get new task id
    task_id += 1

    # Wait if model creation is in progress
    while on_hold:
        print('Waiting while new model is being created')
        time.sleep(1)

    # Add compute forecast task to queue
    task = {'type': 'forecast', 'id': task_id, 'num_steps': num_steps}
    channel.basic_publish(exchange='', routing_key='task', body=json.dumps(task))

    # Wait while forecast result calculation is in progress
    while str(task_id) not in forecast_results:
        print('Waiting while forecast result is being computed')
        time.sleep(1)

    # Return json with forecast result
    return flask.jsonify( {'forecast_result': forecast_results[str(task_id)]})

@app.route('/fit_model_complete', methods=['POST'])
def fit_model_complete():
    # Resume adding tasks to queue
    global on_hold
    on_hold = False
    return 'OK'

@app.route('/forecast_result', methods=['POST'])
def forecast_result():
    # Get forecast result from request and add it to hashmap
    r = flask.request.get_json()
    forecast_results[str(r['id'])] = r['forecast_result']
    return 'OK'

if __name__ == '__main__':
    # Set upconnection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit', port='5672'))
    channel = connection.channel()

    # Create a task queue
    channel.queue_declare(queue='task')

    # Run flask
    app.run(threaded=True, host='0.0.0.0', port=5000)