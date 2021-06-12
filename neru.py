from classes.coap import CoAP
from classes.mqtt import MQTT
from classes.common import CommonValues
import threading
import json
import datetime, time
import asyncio
import sys
#from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import Process, Pipe, Value, Manager
#from threading import Thread

class MQTTScheduler(MQTT):

    def __init__(self, status, event_list, *args): #, result_queue):
        self.status = status
        self.event_list = event_list
        #self.result_queue = result_queue
        super().__init__(*args)

    def scheduler_update(self, updateInfo):
        #Parse string updateInfo into datetime format
        #TODO: Update to parse json(?)
        print("Scheduling process")
        #print(updateInfo)
        try:
            if updateInfo[0] == "clear": self.event_list.clear()
            else: self.event_list.append(datetime.datetime.strptime(" ".join(updateInfo), "%Y-%m-%d %H:%M:%S.%f"))

        except:
            if updateInfo[0] == "clear": self.event_list.clear()
            else: self.event_list.append(datetime.datetime.strptime(" ".join(updateInfo), "%Y-%m-%d %H:%M:%S"))

        self.event_list.sort()
        #print(self.event_list)
        self.status.value = 1

class NeruHandler(CoAP, Process):

    def __init__(self, task_queue, publish_queue, radius=100, ip="0.0.0.0", port=5683): #task_queue, radius=100, ip="0.0.0.0", port=5683):
        super().__init__(radius, ip, port)
        self.task_queue = task_queue
        self.publish_queue = publish_queue
        #self.scheduler_process = None
        self.event_list = Manager().list()
        #self._mqtt_executor = ThreadPoolExecutor(1)
        self.schedule_status = Value('b', 0)

    def run(self):
        mqttScheduler = MQTTScheduler(self.schedule_status, self.event_list, True)
        #MQTT().__init__()
        #proc_name = self.name
        while True:
            mqttScheduler.dispatchDisturbanceMessage(self.task_queue.recv())
            #next_task = self.task_queue.get()
            '''if next_task is None:
                # Poison pill means shutdown
                print '%s: Exiting' % proc_name
                self.task_queue.task_done()
                break
            print '%s: %s' % (proc_name, next_task)
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)'''
        return

    '''async def mqtt_dispatch(self, disturbance):
        # run blocking function in another thread,
        # and wait for its result:
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
        self.schedule_status.value = True'''

    async def disturbance_scheduler(self):
        #From https://stackoverflow.com/a/54774814
        #print("Scheduling disturbances!")
        def wait_until(end_datetime):
            while True:
                diff = (end_datetime - datetime.datetime.now()).total_seconds()
                if self.schedule_status.value > 0: return False
                if diff < 0: return True       # In case end_datetime was in past to begin with
                if diff > 2: time.sleep(1)
                else: time.sleep(diff/2)
                #print(diff)
                if diff <= 0.0001: return True # Accuracy within 1 ms (approx.)

        for event in self.event_list:
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
                publish_queue.send(disturbance)
                await asyncio.wait_for(self.dispatchDisturbanceMessages(disturbance.encode("utf-8")), timeout=0.3) #, self.mqtt_dispatch(disturbance))

    '''def arrivalFunction(self, data):
        self.arrivalMessage(data)'''


if __name__ == "__main__":

    task_queue, publish_queue = Pipe()


    neruhandler = NeruHandler(task_queue, publish_queue, 4000, port = int(sys.argv[2])) #, ip = "192.168.1.222")


    #mqttQueue = MQTTQueue(task_queue)
    neruhandler.start()

    #coap = CoAP()
    #neruhandler.startServer()

    CommonValues.setNearbyNERUs({sys.argv[1]: [int(sys.argv[2]), 51.36972005698434, -0.07820504197321534]})
    CommonValues.setDeviceID("Newcastle 1")
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

        await asyncio.sleep(0.7)

        disturbance =  json.dumps({
                'Latitude': CommonValues.deviceLat,
                'Longitude': CommonValues.deviceLon,
                'device_id_1': CommonValues.device_id_1,
                'time': str(datetime.datetime.now()),
                'type': 'Other type 1'
        })


        #await asyncio.gather(neruhandler.dispatchDisturbanceMessages(disturbance.encode("utf-8")), neruhandler.mqtt_dispatch(disturbance))
        #p = Thread(target=neruhandler.dispatchDisturbanceMessage, args=(disturbance,))
        #p.start()
        publish_queue.send(disturbance)
        await asyncio.wait_for(neruhandler.dispatchDisturbanceMessages(disturbance.encode("utf-8")), timeout=0.3)
        #await asyncio.gather(neruhandler.dispatchDisturbanceMessages(disturbance.encode("utf-8")))
        #await neruhandler.dispatchDisturbanceMessages(disturbance.encode("utf-8"))
        #p.join()
        #print("Process Joined!")
        while True:
            #print("Hello")
            #neruhandler.connectToBroker()
            if neruhandler.schedule_status.value > 0:
                print("Task scheduled!")
                neruhandler.schedule_status.value = 0
                await neruhandler.disturbance_scheduler()
                print("Task scheduler exited!")

    asyncio.run(main())
