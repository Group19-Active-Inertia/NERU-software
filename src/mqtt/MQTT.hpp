

//
//  This file contains classes to receive and send MQTT messages
// 


#ifndef MQTT_H
#define MQTT_H

#include "../disturbance/Disturbance.hpp"
#include "../CommonTypes.hpp"


class MQTTReceiver {

    disturbanceHandler dst;

    void connectToBroker ();
    void subscribeToTopic ();
    void receiveMessage ();

};

class MQTTSender {

    void publishToTopic ();

};

#endif