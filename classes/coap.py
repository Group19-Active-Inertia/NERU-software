

class CoAP:
    
    def __init__ (self, radius:int):
        self.nearbyNERURadius = radius
        self.nearbyNERUs = []
    
    def startServer (self):
        pass
    
    def handleIncomingMessage (self):
        pass
    
    def dispatchDisturbanceMessage (self):
        pass
    
    # calculate nearby nerus from list of nerus
    def setNearbyNERUs (self, nerus:dict):
        pass
    
    # calculate if neru is nearby enough and add to list
    def addNearbyNERU (self, neru:dict):
        pass
    
    # remove nearby NERU from list
    def removeNearbyNERU (self, neru:str):
        pass
    