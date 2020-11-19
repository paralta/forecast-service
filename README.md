# Forecast service

Allows the user to create of a new forecasting model from data provided and to make predictions into the future given the number of steps provided.

## Requirements

```bash
pip3 install -r requirements.txt
```

## Run

```bash
# Start RabbitMQ server
service rabbitmq-server start

# Start model server
cd model
python3 model_app.py

# Start broker app
python3 app.py

# Start processing units
python3 processing_unit.py

# Send requests to http://localhost:5000/
# (Example requests)
curl -X POST http://localhost:5000/fit_model -H 'Content-Type: application/json' -d '{"data": [<insert data>]}'
curl -X POST http://localhost:5000/forecast -H 'Content-Type: application/json' -d '{"num_steps": <insert number of steps>}'
```
