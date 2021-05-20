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
        pass

    def connectToBroker(self):
        pass

    def subscribeToTopic(self):
        pass

    def handleIncomingMessage(self):
        pass

    def dispatchDisturbanceMessage(self):
        pass
