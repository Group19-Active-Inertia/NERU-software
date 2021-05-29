import json
import requests
from getpass import getpass
import time
import threading

class Session:
    endpointNames = {
        "nerus": "items"
    }
    
    apiKey = "AIzaSyBkpEDGlj06SVpYzIbNr2KCIGfYhXBGysE"
    projectId = "create-active-inertia"
    loginUrl = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={apiKey}"
    refreshTokenUrl = f"https://securetoken.googleapis.com/v1/token?key={apiKey}"
    nerusUrl = f"https://create-active-inertia-default-rtdb.europe-west1.firebasedatabase.app/{endpointNames['nerus']}.json"
    
    def __init__(self):
        self.tokenId = None
        self.refreshToken = None
        self.uid = None
        self.tokenDuration = None

    def attemptLogin(self):
        while True:
            data = {
                "email": input("Email: "),
                "password": getpass("Password: "),
                "returnSecureToken": "true"
            }
        
            req = requests.post(Session.loginUrl,data=data)
            
            if req.status_code == 200:
                print("Login successful.")
                break
            else:
                print("Wrong credentials. Try again.")

        reqJson = req.json()
        
        self.idToken = reqJson['idToken']
        self.refreshToken = reqJson["refreshToken"]
        self.uid = reqJson["localId"]
        self.tokenDuration = reqJson["expiresIn"]
        
        
    def refreshIdToken(self):

        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refreshToken,
        }
        
        req = requests.post(refreshTokenUrl, data=data)
        reqJson = req.json()
        
        self.idToken = reqJson['id_token']
        self.refreshToken = reqJson["refresh_token"]
        self.uid = reqJson["localId"]
        self.tokenDuration = reqJson["expires_in"]
        
        
    def getAllowedSites(self):
        pass

    def updateLocalSiteIP(self):
        pass

    def getMQTTFiles(self):
        pass

    def getNeruIPs(self):
        req = requests.get(Session.nerusUrl)
        return req.json()

    def getNeruDetails(self):
        pass
