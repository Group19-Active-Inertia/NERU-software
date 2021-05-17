#ifndef DISTURBANCE_H
#define DISTURBANCE_H


#include "../CommonTypes.hpp"


class LoginScreen {

    bool isValidUser ();
    std::vector<std::string> getPermittedSites ();
    void fetchCredentialFiles ();
    void saveCredentialFiles ();
    void fetchCoAPNetworkIPs ();

    public:
        void renderLoginScreen ();

};


#endif