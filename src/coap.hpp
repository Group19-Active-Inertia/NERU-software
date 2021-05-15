

//
//  This file contains classes to receive and send CoAP messages
//  


#include <iostream>
#include <vector>
#include <string>
#include "disturbance.hpp"

// CoAP radius in km
#define CoAPRadius 10

struct ipPort {
    std::string ip;
    int port;
};

class CoAPReceiver {

    disturbanceHandler dst;

    void startServer () {
        ; // start server and wait for messages
    }

    void receiveMessage () {
        ; // handle received message
    }

};


class CoAPSender {

    std::vector<ipPort> nearbyIPs;

    void updateNearbyIPs () {
        ; // take list of IPs and coordinates and filter which is within CoAPRadius
    }

    void sendDisturbance () {
        ; // send disturbance message over CoAP to nearby NERUs
    }

};