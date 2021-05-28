from classes.coap import CoAP
from classes.mqtt import MQTT
from classes.common import CommonValues
import threading
import json
import datetime
import asyncio
import sys

class NeruHandler(CoAP, MQTT):
    def __init__(self, radius=100, ip="0.0.0.0", port=5683):
        super().__init__(radius, ip, port)

if __name__ == "__main__":

    neruhandler = NeruHandler(port = int(sys.argv[2]))

    #coap = CoAP()
    #neruhandler.startServer()

    CommonValues.setNearbyNERUs({sys.argv[1]: [int(sys.argv[2]), 51, 0]})
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
