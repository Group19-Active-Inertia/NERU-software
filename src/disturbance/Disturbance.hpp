
#ifndef DISTURBANCE_H
#define DISTURBANCE_H

#include "../CommonTypes.hpp"

class disturbanceHandler {
    void parseCoAPMessage ();
    void parseMQTTMessage ();
    void handleDisturbance ();
};

#endif