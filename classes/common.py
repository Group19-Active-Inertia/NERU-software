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
