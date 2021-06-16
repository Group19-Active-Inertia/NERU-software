from .common import CommonValues

import json
import requests
from getpass import getpass
import time
import threading

class Session:
    endpointNames = {
        "nerus": "items"
    }
    
    loginUrl = "https://www.neru-api.herokuapp.com/nerulogin"
    chooseSiteUrl = "https://www.neru-api.herokuapp.com/choosesite"
    
    apiKey = "AIzaSyBkpEDGlj06SVpYzIbNr2KCIGfYhXBGysE"
    projectId = "create-active-inertia"
    refreshTokenUrl = f"https://securetoken.googleapis.com/v1/token?key={apiKey}"
    nerusUrl = f"https://create-active-inertia-default-rtdb.europe-west1.firebasedatabase.app/{endpointNames['nerus']}.json?auth={self.idToken}"
    
    def __init__(self):
        self.sites = None
        self.idToken = None
        self.refreshToken = None
        self.tokenDuration = None

    def attemptLogin(self):
        while True:
            data = {
                "email": input("Email: "),
                "password": getpass("Password: ")
            }
        
            req = requests.post(Session.loginUrl, data=data)
            
            if req.status_code == 200:
                print("Login successful.")
                break
            else:
                print("Wrong credentials. Try again.")

        reqJson = req.json()
        
        self.sites = reqJson["sites"]
        self.idToken = reqJson['idToken']
        self.refreshToken = reqJson["refreshToken"]
        self.tokenDuration = reqJson["tokenExpiresIn"]
        
        sitesPrintFormat = ""
        
        for index, site in zip( range(len(reqJson["sites"])), reqJson["sites"] ):
            sitesPrintFormat += f"[ {index} ] {site}"
                        
        print(sitesPrintFormat)
    
    def chooseSite(self):
        
        while True:
            siteIndex = input("Choose a site number: ")
        
            if siteIndex >= 0 and siteIndex < len(self.sites):
                break
            
            print("Number entered was out of bounds. Try again.")
        
        data = {
            "token": self.idToken,
            "site": self.sites[siteIndex],
            "lat": CommonValues.deviceLat,
            "lon": CommonValues.deviceLon,
            "ip": CommonValues.getPublicIP(),
        }
        
        req = requests.post(Session.chooseSiteUrl, data=data)
        
        if req.status_code == 200:
            print("Initialisation successful. Starting NERU Software..")
        else:
            print("Error choosing site")
            raise SystemExit
    
    def refreshIdToken(self):

        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refreshToken,
        }
        
        req = requests.post(refreshTokenUrl, data=data)
        reqJson = req.json()
        
        self.idToken = reqJson['id_token']
        self.refreshToken = reqJson["refresh_token"]
        self.tokenDuration = reqJson["expires_in"]

    def getNeruIPs(self):
        req = requests.get(Session.nerusUrl)
        return req.json()

    def getNeruDetails(self):
        pass

