from math import acos, sin, cos, pi
import requests, os
#from multiprocessing import Array
import requests

# This class is used in common with all other modules
# it is added so information does not have to be passed
# between classes as it would become very muddled
class CommonValues:
    # radius in km
    nearbyNERURadius = 100
    nearbyNERUs = []
    
    # file paths to mqtt certificates, used by multiple modules
    cwd = os.getcwd()
    certificatePaths = {
        "rootCA": os.path.join(cwd,"certs","Amazon-root-CA-1.pem"),
        "privateKey": os.path.join(cwd,"certs","private.pem.key"),
        "certificate": os.path.join(cwd,"certs","device.pem.crt")        
    }

    # local NERU device location. Accuracy depends on distance
    # Within the UK: ± <1km error. Error increases to a few km for >3000km distances
    # Coordinates below are of Imperial's EEE building
    deviceLat, deviceLon = 54.975123382631736, -1.6478403158353487
    device_id_1 = "Newcastle 1"
    symmetric_key = None # = Array('b', 1)
    
    port = None
    ip = None
    
    # calculates euclidean distance from host neru location to point
    def euclideanDistance(lat, lon):
        rlat1, rlon1, rlat2, rlon2 = (
            CommonValues.deviceLat * pi / 180,
            CommonValues.deviceLon * pi / 180,
            lat * pi / 180,
            lon * pi / 180,
        )
        return int(
            6378.388
            * acos(
                sin(rlat1) * sin(rlat2) + cos(rlat1) * cos(rlat2) * cos(rlon2 - rlon1)
            )
        )

    # set device ID
    def setDeviceID(name):
        CommonValues.device_id_1 = name
        
    def getPublicIP():
        return requests.get('https://api.ipify.org').text

    def setKey(key):
        CommonValues.symmetric_key = key

    # calculate nearby nerus from dict of nerus
    # nerus format: {ip: [port, lat, lon]}
    def setNearbyNERUs(nerus):
        CommonValues.nearbyNERUs = [
            (ip, port)
            for (ip, (port, lat, lon)) in nerus.items()
            if CommonValues.euclideanDistance(lat, lon) <= CommonValues.nearbyNERURadius
        ]

    # calculate if neru is nearby enough and add to list
    # info format: [ip, port, lat, lon]
    def addNearbyNERU(info):
        if (
            CommonValues.euclideanDistance(info[2], info[3])
            <= CommonValues.nearbyNERURadius
        ):
            CommonValues.nearbyNERUs.append((info[0], info[1]))

    # remove nearby NERU from list
    # info format: [ip]
    def removeNearbyNERU(info):
        CommonValues.nearbyNERUs = [
            (ip, port) for (ip, port) in CommonValues.nearbyNERUs if ip != info[0]
        ]

    # edit neru ip
    # info format: [oldIp, newIp]
    def editNearbyNERU(info):
        CommonValues.nearbyNERUs = [
            (info[1], port) if ip == info[0] else (ip, port)
            for (ip, port) in CommonValues.nearbyNERUs
        ]
