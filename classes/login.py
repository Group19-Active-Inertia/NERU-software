from .common import CommonValues

import json
import requests
from getpass import getpass
import time
import threading

# This class handles all communication where a Firebase ID Token is necessary.
class Session:
    
    loginUrl = "https://neru-api.herokuapp.com/nerulogin"
    chooseSiteUrl = "https://neru-api.herokuapp.com/choosesite"
    
    apiKey = "AIzaSyBkpEDGlj06SVpYzIbNr2KCIGfYhXBGysE"
    projectId = "create-active-inertia"
    refreshTokenUrl = f"https://securetoken.googleapis.com/v1/token?key={apiKey}"
    nerusUrl = "https://create-active-inertia-default-rtdb.europe-west1.firebasedatabase.app/nerus.json?auth={}"
    
    localNeruUrl = "https://create-active-inertia-default-rtdb.europe-west1.firebasedatabase.app/nerus/{}.json?auth={}"
    
    def __init__(self):
        self.sites = None
        self.idToken = None
        self.refreshToken = None
        self.tokenDuration = None
        self.localSite = None
        self.coapPort = None

    def attemptLogin(self):
        while True:
            
            email = input("Email: ")
            password = getpass("Password: ")
        
            data = {
                "email": email,
                "password": password
            }
            
            dataToPost = json.dumps(data)
        
            req = requests.post(Session.loginUrl, data=dataToPost)
            
            if req.status_code == 200:
                print("Login successful.")
                break
            
            else:
                print("Wrong credentials. Try again.")

        reqJson = req.json()
        
        self.sites = reqJson["sites"]
        self.idToken = reqJson['idToken']
        self.refreshToken = reqJson["refreshToken"]
        self.tokenDuration = int(reqJson["tokenExpiresIn"])
        
        # Initialise string
        sitesPrintFormat = ""
        
        for index, site in zip( range(len(reqJson["sites"])), reqJson["sites"] ):
            sitesPrintFormat += f"[ {index} ] {site}\n"
                        
        # prints on purpose
        print(sitesPrintFormat)
    
    def chooseSite(self):
        
        while True:
            try:
                siteIndex = int(input("Choose a site number: "))
                
                if siteIndex >= 0 and siteIndex < len(self.sites):
                    self.localSite = self.sites[siteIndex]
                    
                    print(f"Configuring NERU for {self.localSite}...")
                    break
                
                else:
                    print("Number entered was out of bounds. Try again.")
                    
            except:
                print("Please enter a number.")
        
        data = {
            "token": self.idToken,
            "site": self.sites[siteIndex],
            "lat": CommonValues.deviceLat,
            "lon": CommonValues.deviceLon,
            "ip": CommonValues.getPublicIP(),
        }
        
        dataToSend = json.dumps(data)
        
        req = requests.post(Session.chooseSiteUrl, data=dataToSend)
        
        if req.status_code == 200:
            print("Configuration was successful.")
            data = req.json()
            self.saveMQTTSecretsToFile(data)
            self.continuouslyRefreshIdToken()
            self.coapPort = getLocalNeruPort()
            CommonValues.setKey(data["aesKey"])
            
        else:
            print("Error configuring site.")
            print(req.json())
            
            raise SystemExit
        
    # Saves certificates and key into files
    def saveMQTTSecretsToFile(self, data):
        with open(CommonValues.certificatePaths["certificate"], "w") as file:
            file.write(data["certificatePem"])
            
        with open(CommonValues.certificatePaths["rootCA"], "w") as file:
            file.write(data["amazonRootCA1"])
            
        with open(CommonValues.certificatePaths["privateKey"], "w") as file:
            file.write(data["privateKey"])
    
    # Gets the port of the chosen neru from firebase
    def getLocalNeruPort(self):
        req = requests.get(Session.nerusUrl.format(self.localSitem, self.idToken)).json()
        return req["Port"]
    
    # continuously refreshes the firebase idToken
    def continuouslyRefreshIdToken(self):
        def refreshIdToken():
            time.sleep(self.tokenDuration-5)
            
            data = {
                "grant_type": "refresh_token",
                "refresh_token": self.refreshToken,
            }
            
            req = requests.post(refreshTokenUrl, data=data)
            reqJson = req.json()
            
            self.idToken = reqJson['id_token']
            self.refreshToken = reqJson["refresh_token"]
            self.tokenDuration = int(reqJson["expires_in"])
            
        threading.Thread(target=refreshIdToken).start()

    # gets list of all NERUs from firebase as a dictionary
    # format:
    # {
    #    "Aberdeen": {
    #       "CurrentIP": "57.129.89.99"
    #       "Latitude": 51.52453425
    #       "Longitude": -7.0234756
    #       "Name": "Aberdeen"
    #       "Online": true
    #       "Port": 5836
    #    }
    #    "Nottingham": {
    #       "CurrentIP": "27.99.80.208"
    #       "Latitude": 53.57213385
    #       "Longitude": -6.22028973
    #       "Name": "Nottingham"
    #       "Online": true
    #       "Port": 8893
    #    }
    #    ...
    # }
    def getNeruList(self):
        req = requests.get(Session.nerusUrl.format(self.idToken))
        return req.json()