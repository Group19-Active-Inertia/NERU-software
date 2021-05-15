
#ifndef COAP_H
#define COAP_H

#include "../disturbance/Disturbance.hpp"
#include "../CommonTypes.hpp"

class CoAPReceiver {
    disturbanceHandler dst;
    void startServer ();
    void receiveMessage ();
};

class CoAPSender {
    std::vector<ipPort> nearbyIPs;
    void updateNearbyIPs ();
    void sendDisturbance ();
};

#endif