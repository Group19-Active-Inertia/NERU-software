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
    
    def __init__(self):
        self.sites = None
        self.idToken = None
        self.refreshToken = None
        self.tokenDuration = None

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
                    print(f"Configuring NERU for {self.sites[siteIndex]}...")
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
            self.saveMQTTSecretsToFile(req.json())
            
        else:
            print("Error configuring site.")
            print(req.json())
            
            raise SystemExit
    
    def saveMQTTSecretsToFile(self, data):
        with open(CommonValues.certificatePaths["certificate"], "w") as file:
            file.write(data["certificatePem"])
            
        with open(CommonValues.certificatePaths["rootCA"], "w") as file:
            file.write(data["amazonRootCA1"])
            
        with open(CommonValues.certificatePaths["privateKey"], "w") as file:
            file.write(data["privateKey"])
    
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

    def getNeruIPs(self):
        req = requests.get(Session.nerusUrl.format(self.idToken))
        return req.json()