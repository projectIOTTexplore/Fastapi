from datetime import date
from pydantic import BaseModel
from datetime import datetime, date

class Datasensor(BaseModel):
    timestamp = datetime.now()
    sensor: str
    status: str
    value: float