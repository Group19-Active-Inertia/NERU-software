from .common import CommonValues
#import .mqtt
import aiocoap.resource as resource
from aiocoap import *
import asyncio
from multiprocessing import Process
import sys
import datetime
import json

### -----------------------------------------------------
### -----------------------------------------------------
### -----------       Exceptions    ---------------------
### -----------------------------------------------------
### -----------------------------------------------------


### -----------------------------------------------------
### -----------------------------------------------------
### -----------      CoAP Resources    ------------------
### -----------------------------------------------------
### -----------------------------------------------------

# handles incoming disturbances from CoAP
class CoAPDisturbance(resource.Resource):
    def __init__(self): #, Handler, function):
        #self.arrival_func = function
        #self.Handler = Handler
        super().__init__()

    async def render_post(self, request):
        # handle incoming disturbance
        # e.g.
        date = datetime.datetime.now()
        print("POST request received: %s" % request.payload.decode("utf-8") )
        print("At time:", date)

        '''msg = json.loads(request.payload.decode("utf-8"))

        msgRecv = json.dumps({
                    "device_id_1": CommonValues.device_id_1,
                    "message received": msg,
                    "message type": "MQTT",
                    "duration":  str(date - datetime.datetime.strptime(msg["time"], "%Y-%m-%d %H:%M:%S.%f")),
                    "time": str(date)
                  })

        try:
            self.MQTTClient.publish(
                self.brokerInfo["arriveTopic"],
                json.dumps({
                    "device_id_1": CommonValues.device_id_1,
                    "message received": msg,
                    "message type": "MQTT",
                    "duration":  str(date - datetime.datetime.strptime(msg["time"], "%Y-%m-%d %H:%M:%S.%f")),
                    "time": str(date)
                }),
                self.brokerInfo["qosArrive"],
            )
        except:
            raise Error #MQTTPublishException'''

        #self.arrival_func(self.Handler, msgRecv)
        #sys.stdout.flush()
        #
        # if not_prepared_for_disturbance:
        #    prepare_for_disturbance()
        return Message()


### -----------------------------------------------------
### -----------------------------------------------------
### ---------------    CoAP Class    --------------------
### -----------------------------------------------------
### -----------------------------------------------------


class CoAP():
    def __init__(self, radius: int = 100, ip: str = "0.0.0.0", port: int = 5683, *args):
        print("Init CoAP!")
        CommonValues.nearbyNERURadius = radius
        #asyncio.get_event_loop().run_until_complete(asyncio.gather(self.init_Client()))
        #time.sleep(2)
        #self.protocol = Context.create_client_context()
        self._ip = ip
        self._port = port

        print("IP: ", ip, "Port:", port)
        # Need to use multiprocessing because it makes the server non-blocking
        self.server = Process(target=self.startServer).start()

        #asyncio.run(self.startClient())

        super().__init__(*args)

    async def init_Client(self):
        self.protocol =  await Context.create_client_context()

    def arrivalFunction(self, data):
        print("base arrivalFunction executed!")
        self.arrivalMessage(data)
        pass

    def startServer(self):
        server = resource.Site()
        server.add_resource(["d"], CoAPDisturbance()) #self, CoAP.arrivalFunction)) #self.MQTTClient))

        context = Context.create_server_context(server, (self._ip, self._port))
        asyncio.Task(context)

        asyncio.get_event_loop().run_forever()

    async def dispatchDisturbanceMessages(self, disturbance):
        #Error arises if self.protocol used without running function in main event loop
        #handle = await Context.create_client_context()
        async def dispatchMessage(ip, port):
            msg = Message(
                code=POST, mtype=NON, payload=disturbance, uri=f"coap://{ip}:{port}/d"
            )
            #response = await handle.request(msg).response
            response = await self.protocol.request(msg).response
            #date = datetime.datetime.now()
            #print(response)
            #print("At time:", date)

        await asyncio.gather(*(dispatchMessage(ip, port) for (ip, port) in CommonValues.nearbyNERUs))
