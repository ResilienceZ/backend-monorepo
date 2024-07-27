import requests

def fetch():
    response = requests.get("https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json")
    response.raise_for_status()
    data = response.json()
    
    earthquake_obj = data["Infogempa"]["gempa"]
    lat = earthquake_obj["Lintang"]
    long = earthquake_obj["Bujur"]
    mag = earthquake_obj["Magnitude"]
    depth = earthquake_obj["Kedalaman"]
    
    feel_data = earthquake_obj["Dirasakan"].split(" ")
    feel_scale = feel_data[0]
    feel_zone = feel_data[1:len(feel_data)-1].join(" ")
    
    return {
        "lat": lat,
        "long": long,
        "magnitude": mag,
        "depth": depth,
        "feel_scale": feel_scale,
        "feel_zone": feel_zone,
    }