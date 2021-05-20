from common import CommonValues

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
    async def render_get(self, request):
        # handle incoming disturbance
        # e.g.
        #
        # if not_prepared_for_disturbance:
        #    prepare_for_disturbance()
        return


### -----------------------------------------------------
### -----------------------------------------------------
### ---------------    CoAP Class    --------------------
### -----------------------------------------------------
### -----------------------------------------------------


class CoAP:
    def __init__(self, radius: int):

        self.protocol = Context.create_client_context()

        # Need to use multiprocessing because it makes the server non-blocking
        self.server = Process(target=self.startServer).start()

    def startServer(self):
        server = resource.Site()
        server.add_resource(["d"], CoAPDisturbance())

        context = Context.create_server_context(server)
        asyncio.Task(context)

        asyncio.get_event_loop().run_forever()

    def dispatchDisturbanceMessages(self, disturbance):
        async def dispatchMessage(ip, port):
            msg = Message(
                code=POST, mtype=NON, payload=disturbance, uri=f"coap://{ip}:{port}/d"
            )
            self.protocol.request(msg)

        for (ip, port) in CommonValues.nearbyNERUs:
            dispatchMessage(ip, port)
