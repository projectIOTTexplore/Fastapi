from fastapi import FastAPI
from routes.sensor_route import sensor
app = FastAPI()

app.include_router(sensor)
