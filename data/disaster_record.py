import json

class DisasterRecord:
    def __init__(self, id, description, severity, scale, longitude, latitude, type, timestamp):
        self.id = id
        self.description = description
        self.severity = severity
        self.scale = scale
        self.longitude = longitude
        self.latitude = latitude
        self.type = type
        self.timestamp = timestamp

    def __repr__(self):
        return (f"DisasterRecord(id={self.id}, description={self.description}, severity={self.severity}, "
                f"scale={self.scale}, longitude={self.longitude}, latitude={self.latitude}, "
                f"type={self.type}, timestamp={self.timestamp})")

    def toJSON(self):
            return json.dumps(
                self,
                default=lambda o: o.__dict__, 
                sort_keys=True,
                indent=4)
