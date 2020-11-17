import os
import sys
import json
import pika
import time
import pickle
import threading
import model.model as mdl

# Initialise data and model from file
data = pickle.load(open("model/data.pkl", "rb"))
model = pickle.load(open("model/arima_model.pkl", "rb"))

# Initialise flag to indicate if model creation is in progress
on_hold = False

forecast_results = {}

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task')

    def callback(ch, method, properties, body):
        global data, model, on_hold, forecast_results

        while on_hold:
            print('Waiting while new model is being created')
            time.sleep(1)

        print(f"Received {body}")
        task = json.loads(body)

        # Process fit model task
        if task['type'] == 'fit_model':
            on_hold = True
            data = task['data']
            model = mdl.fit_model(data)
            on_hold = False
            print('New model has been created')

        # Process compute forecast task
        elif task['type'] == 'forecast':
            forecast_result = mdl.forecast(data, model, task['num_steps'])
            forecast_results[int(task['id'])] = list(forecast_result)
            print('New forecast result has been computed')

    channel.basic_consume(queue='task', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages')
    channel.start_consuming()

if __name__ == '__main__':
    # Start n threads of processing unit
    num_threads = 3
    for _ in range(num_threads):
        threading.Thread(target=main).start()

