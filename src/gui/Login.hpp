#ifndef DISTURBANCE_H
#define DISTURBANCE_H


#include "../CommonTypes.hpp"


class LoginScreen {

    void renderLoginScreen ();
    bool isValidUser ();
    std::vector<std::string> getPermittedSites ();
    void fetchCredentialFiles ();
    void saveCredentialFiles ();
    void fetchCoAPNetworkIPs ();

};


#endif