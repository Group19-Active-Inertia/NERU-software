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
    pass
class MQTT:
    def __init__(self):
        pass

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
        pass

    def subscribeToTopic(self):
        pass

    def handleIncomingMessage(self):
        pass

    def dispatchDisturbanceMessage(self):
        pass
