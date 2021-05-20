import os
from io import StringIO
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

### -----------------------------------------------------
### -----------------------------------------------------
### -----------       Exceptions    ---------------------
### -----------------------------------------------------
### -----------------------------------------------------


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


class MQTT:
    def __init__(self):
        self.brokerInfo = {}
        self.getBrokerCredentials()

        self.MQTTClient = None
        self.connectToBroker()

        self.subscribeToTopic()

    def getBrokerCredentials(self):
        try:
            self.brokerInfo["qos"] = None
            self.brokerInfo["host"] = None
            self.brokerInfo["port"] = 8883
            self.brokerInfo["rootCA"] = None
            self.brokerInfo["privateKey"] = None
            self.brokerInfo["certificatePath"] = None
            self.brokerInfo["clientId"] = None
            self.brokerInfo["disturbanceTopic"] = "d"
            self.brokerInfo["updateTopic"] = "update"
        except:
            raise MQTTBrokerCredentialException("Broker failed to initialise")

    def connectToBroker(self):
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

    def handleIncomingMessage(self):
        pass

    def dispatchDisturbanceMessage(self):
        pass

    def dispatchDisturbanceMessage(self, publicIp):
        try:
            MQTTClient.publish(
                self.brokerInfo["disturbanceTopic"], 
                publicIp, 
                self.brokerInfo["qosDisturbance"]
            )
        except:
            raise MQTTPublishException