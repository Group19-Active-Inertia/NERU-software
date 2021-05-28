from .common import CommonValues

import aiocoap.resource as resource
from aiocoap import *
import asyncio
from multiprocessing import Process

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
    #def __init__(self):
    #        super().__init__()

    async def render_post(self, request):
        # handle incoming disturbance
        # e.g.
        print("POST request received: %s" % request.payload.decode("utf-8") )
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
        self.protocol = Context.create_client_context()
        #time.sleep(2)
        #self.protocol = None
        self._ip = ip
        self._port = port

        # Need to use multiprocessing because it makes the server non-blocking
        self.server = Process(target=self.startServer).start()

        #asyncio.run(self.startClient())

        super().__init__(*args)

    def startServer(self):
        server = resource.Site()
        server.add_resource(["d"], CoAPDisturbance())

        context = Context.create_server_context(server, (self._ip, self._port))
        asyncio.Task(context)

        asyncio.get_event_loop().run_forever()

    '''async def startClient(self):
        self.protocol = await Context.create_client_context()'''

    async def dispatchDisturbanceMessages(self, disturbance):
        #Error arises if self.protocol used, so handle used as a workaround
        #TODO: Allow direct reference to self.protocol
        handle = await Context.create_client_context()
        async def dispatchMessage(ip, port):
            msg = Message(
                code=POST, mtype=NON, payload=disturbance, uri=f"coap://{ip}:{port}/d"
            )
            response = await handle.request(msg).response
            #response = await self.protocol.request(msg).response
            print(response)
        await asyncio.gather(*(dispatchMessage(ip, port) for (ip, port) in CommonValues.nearbyNERUs))
