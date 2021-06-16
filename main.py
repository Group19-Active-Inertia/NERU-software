from classes.common import CommonValues

#TODO: set the key using the API
CommonValues.setKey(b"OjJ_mLzQdA2tR-rjjjhh3XTFtTqPRZWfY49v96cOOIo=")

def getInput(val: float, bounds = 90, prompt = "Please enter: ", error = "Insert a correct value!", type = "float"):
    while True:
        consoleInput = raw_input(prompt)
        try:
            if type == "float":
                val = float(consoleInput)
                if val > bound or val < -1 * bound:
                    raise ValueError
            elif type == "str":
                val = consoleInput
            elif type == "int":
                val = int(consoleInput)
                if val < 0 or val > 65535: val = None
            break
            
        except ValueError:
            if type == "int": val = None
            else: print(error)
            
getInput(CommonValues.deviceLat, 90, "Please enter the device Latitude co-ordinate: ", "Insert a valid floating point number from -90 to 90!")
getInput(CommonValues.deviceLat, 180, "Please enter the device Latitude co-ordinate: ", "Insert a valid floating point number from -90 to 90!")
getInput(CommonValues.device_id_1, 0, "Please enter the device ID: ", "Please enter a valid string for the device ID!", "str")
getInput(CommonValues.Port, 0, "Please enter a port number to bind to the CoAP server (default 5683): ", "Please enter a valid port number!", "int")

from classes.login import Session

s = Session()

s.attemptLogin()
s.chooseSite()

for neru_node in s.neruList():
    CommonValues.setNearbyNERUs(neru_node)

#Test neru added to nearby NERU list for now
CommonValues.setNearbyNERUs({CommonValues.getPublicIP(): [CommonValues.port, CommonValues.deviceLat, CommonValues.deviceLon]})

from classes.neru import NeruHandler
import json
import datetime
import asyncio
from multiprocessing import Pipe, Value

if __name__ == "__main__":

    task_queue, publish_queue = Pipe()


    if CommonValues.Port == None: neruhandler = NeruHandler(task_queue, publish_queue, 100)
    else: neruhandler = NeruHandler(task_queue, publish_queue, 100, CommonValues.port)
    
    neruhandler.start()

    
    #CommonValues.setDeviceID("Newcastle 1")
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

        '''disturbance =  json.dumps({
                'Latitude': CommonValues.deviceLat,
                'Longitude': CommonValues.deviceLon,
                'device_id_1': CommonValues.device_id_1,
                'time': str(datetime.datetime.now()),
                'type': 'Phase shift'
        })


        #await asyncio.gather(neruhandler.dispatchDisturbanceMessages(disturbance.encode("utf-8")), neruhandler.mqtt_dispatch(disturbance))
        #p = Thread(target=neruhandler.dispatchDisturbanceMessage, args=(disturbance,))
        #p.start()
        publish_queue.send(disturbance)
        try: await asyncio.wait_for(neruhandler.dispatchDisturbanceMessages(disturbance.encode("utf-8")), timeout=0.3)
        except: pass'''
        #await asyncio.gather(neruhandler.dispatchDisturbanceMessages(disturbance.encode("utf-8")))
        #await neruhandler.dispatchDisturbanceMessages(disturbance.encode("utf-8"))
        #p.join()
        print("Ready to receive messages!")
        while True:
            #print("Hello")
            #neruhandler.connectToBroker()
            if neruhandler.schedule_status.value > 0:
                print("Task scheduled!")
                neruhandler.schedule_status.value = 0
                await neruhandler.disturbance_scheduler()
                print("Task scheduler exited!")

    asyncio.run(main())
