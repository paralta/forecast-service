import json, pika, time, flask

app = flask.Flask(__name__)

# Initialise task id and forecast results
task_id = 0
forecast_results = {}

@app.route('/fit_model', methods=['POST'])
def fit_model():
    # Get data from request
    data = flask.request.get_json()['data']
    task = {'type': 'fit_model', 'data': data}

    # Add create model task to queue
    channel.basic_publish(exchange='', routing_key='task', body=json.dumps(task))
    return 'New model is being created\n'

@app.route('/forecast', methods=['POST'])
def forecast():
    # Get number of steps from request
    num_steps = int(flask.request.get_json()['num_steps'])

    # Get new task id and add compute forecast task to queue
    global task_id
    task_id += 1
    task = {'type': 'forecast', 'id': task_id, 'num_steps': num_steps}
    channel.basic_publish(exchange='', routing_key='task', body=json.dumps(task))

    while str(task_id) not in forecast_results:
        print('Waiting while forecast result is being computed')
        time.sleep(1)

    # Return json with forecast result
    return flask.jsonify( {'forecast_result': forecast_results[str(task_id)]})

@app.route('/forecast_result', methods=['POST'])
def forecast_result():
    # Get forecast result from request and add it to hashmap
    r = flask.request.get_json()
    forecast_results[str(r['id'])] = r['forecast_result']
    return 'OK'

if __name__ == '__main__':
    # Set upconnection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Create a task queue
    channel.queue_declare(queue='task')

    # Run flask
    app.run(threaded=True, host='0.0.0.0', port=5000)