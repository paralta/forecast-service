# AI Software Engineer Challenge - Outsystems
## Catarina Paralta

## 1. Description

Build a service to use a forecasting model to make prediction into the future. It should be composed of two microservices:
* A broker to contact with other services. It should expose two REST endpoints: one to create a new model and one to compute the forecast.
* A python processing unit that uses an already existing model to compute predictions and that creates a new model from provided data. Model-related functions are provided.

**Constraints and requirements:**
* One single instance of broker to handle all incoming requests
* At least three instances of the python processing unit to handle incoming requests
* When new forecast request is made, if a new model is being created, the request should be put on hold until the model creation is finished and it should be computed using the new model

# 2. Run

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
