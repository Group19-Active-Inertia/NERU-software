from classes.coap import CoAP
from classes.mqtt import MQTT
from classes.common import CommonValues
import threading
import json
import datetime
import asyncio

class NeruHandler(MQTT, CoAP):
    def __init__(self):
        super().__init__()

if __name__ == "__main__":

    neruhandler = NeruHandler()

    #coap = CoAP()
    #neruhandler.startServer()

    CommonValues.setNearbyNERUs({"2.31.150.98": [5683, 51, 0]})
    disturbance =  json.dumps({
                'device_id_1': 'E56!w3se',
                'location_1': [51.5476363, 56.6376463],
                'time': str(datetime.datetime.now()),
                'type': 'Frequency event'
            })
    #disturbance = message.encode("utf-8")
    asyncio.run(neruhandler.dispatchDisturbanceMessages(disturbance.encode("utf-8")))
    neruhandler.dispatchDisturbanceMessage(disturbance)
    while True:
        #print("Hello")
        #neruhandler.connectToBroker()
        pass
