import json

class DisasterReport:
    def __init__(self, id, reporter_uniqueid, longitude, latitude, geohash, type, timestamp):
        self.id = id
        self.reporter_uniqueid = reporter_uniqueid
        self.longitude = longitude
        self.latitude = latitude
        self.geohash = geohash
        self.type = type
        self.timestamp = timestamp

    def __repr__(self):
        return (f"DisasterReport(id={self.id}, reporter_uniqueid={self.reporter_uniqueid}, longitude={self.longitude}, "
                f"latitude={self.latitude}, geohash={self.geohash}, type={self.type}, timestamp={self.timestamp})")
        
    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)

