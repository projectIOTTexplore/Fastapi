def Data_Sensor_Entity(item) -> dict:
    return {
        "sensor": item["sensor"],
        "status": item["status"],
        "value": item["value"],
        "timestamp": item["timestamp"]
    }

def Datas_Sensors_Entity(entity) -> list:
    return [Data_Sensor_Entity(item) for item in entity]