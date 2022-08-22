from fastapi import APIRouter
from fastapi_utils.tasks import repeat_every
from models.data_sensor_model import Datasensor
from schemas.data_sensor_schemas import Data_Sensor_Entity , Datas_Sensors_Entity
from config.db import connect
import datetime
import time
import random

from threading import Thread, Event
from typing import Callable

sensor = APIRouter()
Path = connect.WASTETREATMENT.data_sensor
Path_DO = connect.WASTETREATMENT.data_sensor_DO
Path_kWh = connect.WASTETREATMENT.data_sensor_kWh
Path_sensor_count = connect.WASTETREATMENT.sensor_count

class TimedCalls(Thread):
    """Call function again every `interval` time duration after it's first run."""
    def __init__(self, func: Callable, interval: datetime.timedelta) -> None:
        super().__init__()
        self.func = func
        self.interval = interval
        self.stopped = Event()

    def cancel(self):
        self.stopped.set()

    def run(self):
        next_call = time.time()
        while not self.stopped.is_set():
            self.func()  # Target activity.
            next_call = next_call + self.interval
            # Block until beginning of next interval (unless canceled).
            self.stopped.wait(next_call - time.time())
            
def my_function():
    # sensors = [1,2,3,4,5,6,7,8,9,10]
    sensors = ['1','2','3','4','5','6','7','8','9','10']
    for ss in sensors:
        value = round(random.uniform(-10,10),4)
        if value < 0:
            Path.insert_one({"sensor":ss,"status":"bad","value": value,"timestamp": datetime.datetime.now()})
        else:
            Path.insert_one({"sensor":ss,"status":"good","value": value,"timestamp": datetime.datetime.now()})


@sensor.post('/add-data-json')
async def post_time():
    # Start test a few secs from now.
    start_time = datetime.datetime.now() + datetime.timedelta(seconds=5)
    run_time = datetime.timedelta(minutes=2)  # How long to iterate function.
    end_time = start_time + run_time

    assert start_time > datetime.datetime.now(), 'Start time must be in future'

    timed_calls = TimedCalls(my_function, 10)  # Thread to call function every 10 secs.

    # print(f'waiting until {start_time.strftime("%H:%M:%S")} to begin...')
    wait_time = start_time - datetime.datetime.now()
    time.sleep(wait_time.total_seconds())

    print('starting')
    timed_calls.start()  # Start thread.
    while datetime.datetime.now() < end_time:
        time.sleep(1)  # Twiddle thumbs while waiting.
    print('done')
    timed_calls.cancel()
    return {
        "message":"success"
    }

@sensor.post('/add-sensor')
async def add_sensor(sensor:int):
    add_ = Path_sensor_count.insert({"sensor":sensor})
    if add_ : 
        return {
            "success"
        }
    else :
        {
            "faild"
        }

@sensor.get('/timestamp')
async def timestamp():
    time_now = datetime.now()
    m = time.time()
    end_time = 60*5
    # print(datetime.now())
    while True:
        current_time = time.time()
        i = 1
        if (current_time - m) == 60:
            print(i)
            m = current_time
        if i == 3:
            print(i) 
            break
    # print(m)
    return datetime.now()


@sensor.get('/find-by-id-sensor')
async def find_by_id_sensor(id:int):
    find_ = Path.find({"sensor":id})
    if find_ :
        return Datas_Sensors_Entity(find_)
    else :
        return{
            "message":"sensor not found!"
        }

@sensor.post('/del-sensor')
async def del_sensor(id:int):
    del_ = Path.delete_many({"sensor":id})
    if del_ :
        return {
            "success!"
        }
    else :
        return {
            "faild!"
        }

@sensor.on_event("startup")
@repeat_every(seconds=60,wait_first=True)
async def add():
    sensors = [1,2,3,4,5,6,7,8,9,10]
    for ss in sensors:
        if ss >= 1 and ss <= 4:
            ph_value = round(random.uniform(-2,16),1)
            if ph_value < 1 or ph_value > 14:
                Path.insert_one({"sensor":ss,"value": ph_value,"timestamp": datetime.datetime.now(),"sensor_flag":1})
            else :
                Path.insert_one({"sensor":ss,"value": ph_value,"timestamp": datetime.datetime.now(),"sensor_flag":0})
        elif ss >= 5 and ss <= 7:
            do_value = round(random.uniform(-2,10),1)
            if do_value < 1 or do_value > 8:
                Path_DO.insert_one({"sensor":ss,"value": do_value,"timestamp": datetime.datetime.now(),"sensor_flag":1})
            else :
                Path_DO.insert_one({"sensor":ss,"value": do_value,"timestamp": datetime.datetime.now(),"sensor_flag":0})
        else :
            kWh_value = round(random.uniform(-2,460),1)
            if kWh_value < 1 or kWh_value > 458:
                Path_kWh.insert_one({"sensor":ss,"value": kWh_value,"timestamp": datetime.datetime.now(),"sensor_flag":1})
            else :
                Path_kWh.insert_one({"sensor":ss,"value": kWh_value,"timestamp": datetime.datetime.now(),"sensor_flag":0})
