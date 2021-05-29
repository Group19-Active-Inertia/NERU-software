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
        self.scheduler_process = None
        self.event_list = None

    def scheduler_update(self, updateInfo):
        #Kill old process (in case event to be scheduled occurs earlier)
        if self.scheduler_process != None:
            '''while True:
                try:'''
            self.scheduler_process.terminate()
            self.scheduler_process.close()
                '''except: #ValueError:
                    pass'''
        #Parse string updateInfo into datetime format
        #TODO: Update to parse json(?)
        event_list.append(datetime.datetime.strptime(" ".join(updateInfo), "%Y-%m-%d %H:%M:%S.%f"))
        event_list.sort()

        self.scheduler_process = Process(target=self.disturbance_scheduler, arg=(event_list,)).start()

   def disturbance_scheduler(date)
       #From https://stackoverflow.com/a/54774814
       def wait_until(end_datetime):
           while True:
               diff = (end_datetime - datetime.datetime.now()).total_seconds()
               if diff < 0: return       # In case end_datetime was in past to begin with
                   time.sleep(diff/2)
               if diff <= 0.001: return # Accuracy within 1 ms (approx.)

       for event in event_list:
           wait_until(event)
           disturbance =  json.dumps({
                'device_id_1': 'E56!w3se',
                'location_1': [51.5476363, 56.6376463],
                'time': str(datetime.datetime.now()),
                'type': 'Frequency event'
           })

           coap_task = asyncio.create_task(self.dispatchDisturbanceMessages(disturbance.encode("utf-8")))
           mqtt_task = asyncio.creat_task(self.dispatchDisturbanceMessage(disturbance))
           loop = asyncio.get_event_loop().run_until_complete()

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
    coap_task = asyncio.create_task(self.dispatchDisturbanceMessages(disturbance.encode("utf-8")))
    mqtt_task = asyncio.creat_task(self.dispatchDisturbanceMessage(disturbance))
    loop = asyncio.get_event_loop().run_until_complete()
    '''asyncio.run(neruhandler.dispatchDisturbanceMessages(disturbance.encode("utf-8")))
    neruhandler.dispatchDisturbanceMessage(disturbance)'''

    while True:
        #print("Hello")
        #neruhandler.connectToBroker()
        pass
