from .classes.coap import CoAP
from .classes.mqtt import MQTT

import threading

if __name__ == "__init__":
    
    mqtt = MQTT()
    
    coap = CoAP()
    coap.startServer()
    
    while True:
        MQTT.connectToBroker()