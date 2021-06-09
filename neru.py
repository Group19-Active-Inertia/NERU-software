from classes.coap import CoAP
from classes.mqtt import MQTT
from classes.common import CommonValues
import threading
import json
import datetime, time
import asyncio
import sys
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import Process

class NeruHandler(CoAP, MQTT):

    def __init__(self, radius=100, ip="0.0.0.0", port=5683):
        super().__init__(radius, ip, port)
        #self.scheduler_process = None
        self.event_list = []
        self._mqtt_executor = ThreadPoolExecutor(1)
        self.schedule_status = False

    async def mqtt_dispatch(self, disturbance):
        # run blocking function in another thread,
        # and wait for it's result:
        await asyncio.get_event_loop().run_in_executor(self._mqtt_executor, self.dispatchDisturbanceMessage, disturbance)
        #await p = Process(target=mqtt_publish, args=( , ))
        #p.start()
        #p.join()
    def scheduler_update(self, updateInfo):
        #Parse string updateInfo into datetime format
        #TODO: Update to parse json(?)
        print("Scheduling process")
        #print(updateInfo)
        if updateInfo[0] == "clear": self.event_list.clear()
        else: self.event_list.append(datetime.datetime.strptime(" ".join(updateInfo), "%Y-%m-%d %H:%M:%S.%f"))
        self.event_list.sort()
        #print(self.event_list)
        self.schedule_status = True

    async def disturbance_scheduler(self):
        #From https://stackoverflow.com/a/54774814
        #print("Scheduling disturbances!")
        def wait_until(end_datetime):
            while True:
                diff = (end_datetime - datetime.datetime.now()).total_seconds()
                if self.schedule_status: return False
                if diff < 0: return True       # In case end_datetime was in past to begin with
                if diff > 2: time.sleep(1)
                else: time.sleep(diff/2)
                #print(diff)
                if diff <= 0.0001: return True # Accuracy within 1 ms (approx.)

        for event in self.event_list.copy():
            #loop = asyncio.new_event_loop()
            #asyncio.set_event_loop(loop)
            if wait_until(event):
                self.event_list.pop(0)
                disturbance =  json.dumps({
                    'Latitude': CommonValues.deviceLat,
                    'Longitude': CommonValues.deviceLon,
                    'device_id_1': CommonValues.device_id_1,
                    'time': str(datetime.datetime.now()),
                    'type': 'Other type 1'
                })
                '''disturbance =  json.dumps({
                     'CurrentIP': self._ip,
                     'ID': 'E56!w3se',
                     'Latitude': CommonValues.deviceLat,
                     'Longitude': CommonValues.deviceLon,
                     'Time': str(datetime.datetime.now()),
                     'Type': 'Frequency event',
                     'Name': 'Newcastle',
                     'Online': 'True',
                     'Port': self._port'''
                #asyncio.get_event_loop().run_until_complete(asyncio.gather(self.dispatchDisturbanceMessages(disturbance.encode("utf-8")), self.mqtt_dispatch(disturbance)))
                #self.dispatchDisturbanceMessage(disturbance)
                await asyncio.gather(self.dispatchDisturbanceMessages(disturbance.encode("utf-8")), self.mqtt_dispatch(disturbance))

    def arrivalFunction(self, data):
        self.arrivalMessage(data)

if __name__ == "__main__":

    neruhandler = NeruHandler(500, port = int(sys.argv[2])) #, ip = "192.168.1.222")

    #coap = CoAP()
    #neruhandler.startServer()

    CommonValues.setNearbyNERUs({sys.argv[1]: [int(sys.argv[2]), 54.975123382631736, -1.6478403158353487]})
    CommonValues.setDeviceID("London 2")
    '''CurrentIP': neruhandler._ip,
    'ID': 'E56!w3se',
    'Latitude': CommonValues.deviceLat,
    'Longitude': CommonValues.deviceLon,
    'Time': str(datetime.datetime.now()),
    'Type': 'Frequency event',
    'Name': 'Newcastle',
    'Online': True,
    'Port': neruhandler._port'''
    #disturbance = message.encode("utf-8")
    #asyncio.get_event_loop().run_until_complete(asyncio.gather(neruhandler.dispatchDisturbanceMessages(disturbance.encode("utf-8")), neruhandler.mqtt_dispatch(disturbance)))
    #asyncio.run(neruhandler.dispatchDisturbanceMessages(disturbance.encode("utf-8")))
    #neruhandler.dispatchDisturbanceMessage(disturbance)


    async def main():

        await neruhandler.init_Client()

        disturbance =  json.dumps({
                'Latitude': CommonValues.deviceLat,
                'Longitude': CommonValues.deviceLon,
                'device_id_1': CommonValues.device_id_1,
                'time': str(datetime.datetime.now()),
                'type': 'Other type 1'
            })

        await asyncio.gather(neruhandler.dispatchDisturbanceMessages(disturbance.encode("utf-8")), neruhandler.mqtt_dispatch(disturbance))

        while True:
            #print("Hello")
            #neruhandler.connectToBroker()
            if neruhandler.schedule_status == True:
                print("Task scheduled!")
                neruhandler.schedule_status = False
                await neruhandler.disturbance_scheduler()
                print("Task scheduler exited!")

    asyncio.run(main())
