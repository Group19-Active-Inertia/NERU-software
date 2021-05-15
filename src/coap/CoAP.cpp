

//
//  This file contains classes to receive and send CoAP messages
//  

#include "CoAP.hpp"

void CoAPReceiver::startServer() {;}; // start coap server and wait for messages
void CoAPReceiver::receiveMessage() {;}; // call this function for received messages

void CoAPSender::updateNearbyIPs() {;}; // take list of ips and lat,lon and filter ips inside CoAPRadius
void CoAPSender::sendDisturbance() {;}; // send messages to list of nearby ips