import json, pika, time, pickle, requests, threading
import model as mdl

broker_url = 'http://0.0.0.0:5000/'
model_url = 'http://0.0.0.0:5001/'

# Initialise data and model from file
data = None
model = None
model_timestamp = time.time()

def callback(ch, method, properties, body):
    global model_timestamp, data, model

    print(f"Received {body}")
    task = json.loads(body)

    # Process fit model task
    if task['type'] == 'fit_model':
        # Fit model
        data = task['data']
        model = mdl.fit_model(data)

        # Load model to server
        requests.post(model_url + 'post_data', data=pickle.dumps(data))
        requests.post(model_url + 'post_model', data=pickle.dumps(model))

        # Announce that fit model task is complete
        requests.post(broker_url + 'fit_model_complete')
        print('New model has been created')

    # Process compute forecast task
    elif task['type'] == 'forecast':
        # Check if latest model is loaded. If not, get it from server
        latest_model_timestamp = requests.get(model_url + 'get_model_timestamp').json()['model_timestamp']
        if data == None or latest_model_timestamp != model_timestamp:
            data = pickle.loads(requests.get(model_url + 'get_data').content)
            model = pickle.loads(requests.get(model_url + 'get_model').content)
            model_timestamp = latest_model_timestamp

        # Calculate forecast
        forecast_result = mdl.forecast(data, model, task['num_steps'])
        forecast_result = {'id': task['id'], 'forecast_result': list(forecast_result)}

        # Send forecast result
        requests.post(broker_url + 'forecast_result', json=forecast_result)
        print(f'New forecast result has been computed {forecast_result}')

def processing_unit():
    # Set upconnection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('0.0.0.0'))
    channel = connection.channel()

    # Create a task queue
    channel.queue_declare(queue='task')

    # Subscribe callback function to queue
    channel.basic_consume(queue='task', on_message_callback=callback, auto_ack=True)

    # Wait for tasks in queue
    print('Waiting for tasks')
    channel.start_consuming()

if __name__ == '__main__':
    # Start n threads of processing unit
    num_threads = 3
    for _ in range(num_threads):
        threading.Thread(target=processing_unit).start()