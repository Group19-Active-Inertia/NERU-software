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
