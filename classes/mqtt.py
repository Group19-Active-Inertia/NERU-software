import os
from io import StringIO
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

### -----------------------------------------------------
### -----------------------------------------------------
### -----------       Exceptions    ---------------------
### -----------------------------------------------------
### -----------------------------------------------------


class MQTTBrokerCredentialException(Exception):
    pass


class MQTTBrokerConnectionException(Exception):
    pass


class MQTTTopicSubscribeException(Exception):
    def __init__(self, topic):
        self.topic = topic
        super().__init__(self.topic)

    def __str__(self):
        return f"Failed to subscribe to topic {self.topic}"


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
            self.MQTTClient.configureOfflinePublishQueueing(
                -1
            )  # Infinite offline Publish queueing
            self.MQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
            self.MQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
            self.MQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
        except:
            raise MQTTBrokerConnectionException("Failed to connect to broker")

    def subscribeToTopic(self):
        try:
            self.MQTTClient.connect()
            self.MQTTClient.subscribe(
                self.brokerInfo["disturbanceTopic"],
                self.brokerInfo["qos"],
                self.incomingMessageHandler,
            )
        except:
            raise MQTTTopicSubscribeException()

    def handleIncomingMessage(self):
        pass

    def dispatchDisturbanceMessage(self):
        pass
