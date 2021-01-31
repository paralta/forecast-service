# Forecast service

Allows the user to create of a new forecasting model from data provided and to make predictions into the future given the number of steps provided.

## Run

```bash
# Start compose and run app
docker-compose up

# Send requests to http://localhost:5000/
# (Example requests)
curl -X POST http://localhost:5000/fit_model -H 'Content-Type: application/json' -d '{"data": [<insert data>]}'
curl -X POST http://localhost:5000/forecast -H 'Content-Type: application/json' -d '{"num_steps": <insert number of steps>}'
```
