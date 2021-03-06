from .common import CommonValues
from multiprocessing import Value, Manager

import os, sys
from io import StringIO
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import datetime
import json
### -----------------------------------------------------
### -----------------------------------------------------
### -----------       Exceptions    ---------------------
### -----------------------------------------------------
### -----------------------------------------------------

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class MQTTBrokerCredentialException(Exception):
    def __str__(self):
        return "Broker failed to initialise"


class MQTTBrokerConfigurationException(Exception):
    def __str__(self):
        return "Failed to set broker configuration"


class MQTTBrokerConnectionException(Exception):
    def __str__(self):
        return "Failed to connect to broker"


class MQTTTopicSubscribeException(Exception):
    def __init__(self, topic):
        self.topic = topic
        super().__init__(self.topic)

    def __str__(self):
        return f"Failed to subscribe to topic {self.topic}"


class MQTTPublishException(Exception):
    def __str__(self):
        return "Failed to publish message"


class MQTTInvalidUpdateMessage(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Invalid update message received: {self.message}"


### -----------------------------------------------------
### -----------------------------------------------------
### -----------       MQTT Class    ---------------------
### -----------------------------------------------------
### -----------------------------------------------------


class MQTT():
    def __init__(self, subscriber=False, *args):
        print("Init MQTT!")
        self.brokerInfo = {}
        self.MQTTClient = None
        self.getBrokerCredentials()
        self.setBrokerConfiguration()

        self.connectToBroker()

        if subscriber:
            self.subscribeToTopic()

        super().__init__(*args)

    def getBrokerCredentials(self):
        try:
            self.brokerInfo["host"] = "a3ccusvtjpdwda-ats.iot.eu-west-2.amazonaws.com"
            self.brokerInfo["port"] = 8883
            self.brokerInfo["rootCA"] = CommonValues.certificatePaths["rootCA"]
            self.brokerInfo["privateKey"] = CommonValues.certificatePaths["privateKey"]
            self.brokerInfo["certificate"] = CommonValues.certificatePaths["certificate"]
            self.brokerInfo["clientId"] = ""
            self.brokerInfo["disturbanceTopic"] = "iot/topic"
            self.brokerInfo["qosDisturbance"] = 0
            self.brokerInfo["updateTopic"] = "update"
            self.brokerInfo["qosUpdate"] = 0
            self.brokerInfo["arriveTopic"] = "firebase"
            self.brokerInfo["qosArrive"] = 0
        except:
            raise MQTTBrokerCredentialException

    def setBrokerConfiguration(self):
        try:
            # Init AWSIoTMQTTClient
            self.MQTTClient = AWSIoTMQTTClient(self.brokerInfo["clientId"])
            self.MQTTClient.configureEndpoint(
                self.brokerInfo["host"], self.brokerInfo["port"]
            )
            self.MQTTClient.configureCredentials(
                self.brokerInfo["rootCA"],
                self.brokerInfo["privateKey"],
                self.brokerInfo["certificate"],
            )

            # AWSIoTMQTTClient connection configuration
            self.MQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
            self.MQTTClient.configureOfflinePublishQueueing(-1)
            self.MQTTClient.configureDrainingFrequency(2)
            self.MQTTClient.configureConnectDisconnectTimeout(10)
            self.MQTTClient.configureMQTTOperationTimeout(5)
        except:
            raise MQTTBrokerConfigurationException

    def connectToBroker(self):
        try:
            self.MQTTClient.connect()
        except:
            raise MQTTBrokerConnectionException

    def subscribeToTopic(self):
        for (topic, qos, handler) in [
            ("disturbanceTopic", "qosDisturbance", self.disturbanceMessageHandler),
            ("updateTopic", "qosUpdate", self.updateMessageHandler),
        ]:
            try:
                self.MQTTClient.subscribe(
                    self.brokerInfo[topic],
                    self.brokerInfo[qos],
                    handler,
                )
            except:
                raise MQTTTopicSubscribeException(self.brokerInfo[topic])

    def disturbanceMessageHandler(self, client, userdata, message):
        date = datetime.datetime.now()
        msgRecv = json.loads(message.payload.decode("utf-8"))
        print(bcolors.WARNING + "-----------------------------------------------------------------------------------------------",
              "\nMQTT Message Received:", message.payload.decode("utf-8"),
              "\nAt Time:", date,
              "\nDelay:", str(date - datetime.datetime.strptime(msgRecv["time"], "%Y-%m-%d %H:%M:%S.%f")),
              "\n-----------------------------------------------------------------------------------------------" + bcolors.ENDC)

        data = json.dumps({
                    "device_id_1": CommonValues.device_id_1,
                    "message received": msgRecv,
                    "message type": "MQTT",
                    "delay":  str(date - datetime.datetime.strptime(msgRecv["time"], "%Y-%m-%d %H:%M:%S.%f")),
                    "time": str(date)
                })

        self.arrivalMessage(data)
        #pass

    def updateMessageHandler(self, client, userdata, message):
        #TODO: Change format of messages received to assume they are json(?)
        msg = message.payload.decode("utf-8")
        msgSplit = msg.split(" ")
        updateType = msgSplit[0]
        updateInfo = msgSplit[1:]

        date = datetime.datetime.now()

        print("MQTT Message Received:", msg)
        print("At Time:", date)

        if updateType == "add":
            CommonValues.addNearbyNERU(updateInfo)
        elif updateType == "edit":
            CommonValues.editNearbyNERUs(updateInfo)
        elif updateType == "del":
            CommonValues.removeNearbyNERU(updateInfo)
        elif updateType == "sched":
            self.scheduler_update(updateInfo)
        else:
            raise MQTTInvalidUpdateMessage(msg)

        #print("MQTT Message Received:", msg)
        #sys.stdout.flush()

    def scheduler_update(self, updateInfo):
        pass

    def dispatchDisturbanceMessage(self, disturbance):
        try:
            self.MQTTClient.publish(
                self.brokerInfo["disturbanceTopic"],
                disturbance,
                self.brokerInfo["qosDisturbance"],
            )
        except:
            raise MQTTPublishException
        date = datetime.datetime.now()
        #print("MQTT Message Published:", disturbance)
        #print("At Time:", date)
        #sys.stdout.flush()

    def arrivalMessage(self, data):
        try:
            self.MQTTClient.publish(
                self.brokerInfo["arriveTopic"],
                data,
                self.brokerInfo["qosArrive"],
            )
        except:
            raise MQTTPublishException
            
            
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
            elif len(updateInfo[1]) == 10: self.event_list.append(datetime.datetime.strptime(" ".join(updateInfo), "%Y-%m-%d %H:%M:%S.%f"))
            elif len(updateInfo[1]) == 8: self.event_list.append(datetime.datetime.strptime(" ".join(updateInfo), "%Y-%m-%d %H:%M:%S"))
            #else: self.event_list.append(datetime.datetime.strptime(" ".join(updateInfo), "%Y-%m-%d %H:%M:%S"))

        except:
            pass

        self.event_list.sort()
        #print(self.event_list)
        self.status.value = 1

