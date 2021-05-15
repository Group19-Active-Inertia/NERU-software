

//
//  This file contains classes to receive and send MQTT messages
//  


#include <iostream>
#include <vector>
#include <string>
#include "disturbance.hpp"


class MQTTReceiver {

    disturbanceHandler dst;

    void connectToBroker () {
        ; // connects to MQTT broker
    }

    void subscribeToTopic () {
        ; // subscribe to MQTT topics
    }

    void receiveMessage () {
        ; // handle incoming messages
    }

};

class MQTTSender {

    void publishToTopic () {
        ; // publish msg to given topic
    }

};