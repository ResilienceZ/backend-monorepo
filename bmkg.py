import requests
import constants
from geohash import GeoHash

def fetch_latest_eq():
    response = requests.get("https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json")
    response.raise_for_status()
    data = response.json()
    
    earthquake_obj = data["Infogempa"]["gempa"]
    lat = float(earthquake_obj["Lintang"].split(" ")[0])
    long = float(earthquake_obj["Bujur"].split(" ")[0])
    mag = earthquake_obj["Magnitude"]
    depth = earthquake_obj["Kedalaman"]

    feel_data = earthquake_obj["Dirasakan"].split(" ")
    feel_scale = feel_data[0]
    feel_zone = feel_data[1:len(feel_data)-1]

    return {
        "lat": lat,
        "long": long,
        "magnitude": mag,
        "depth": depth,
        "feel_scale": feel_scale,
        "feel_zone": feel_zone,
    }

def fetch_latest_15_eq():
    response = requests.get("https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json")
    response.raise_for_status()
    data = response.json()

    earthquake_obj = data["Infogempa"]["gempa"]
    lat = earthquake_obj["Lintang"]
    long = earthquake_obj["Bujur"]
    mag = earthquake_obj["Magnitude"]
    depth = earthquake_obj["Kedalaman"]

    feel_data = earthquake_obj["Dirasakan"].split(" ")
    feel_scale = feel_data[0]
    feel_zone = feel_data[1:len(feel_data)-1]

    return {
        "lat": lat,
        "long": long,
        "magnitude": mag,
        "depth": depth,
        "feel_scale": feel_scale,
        "feel_zone": feel_zone,
    }

def fetch_latest_15_felt_eq():
    response = requests.get("https://data.bmkg.go.id/DataMKG/TEWS/gempadirasakan.json")
    response.raise_for_status()
    data = response.json()

    earthquake_obj = data["Infogempa"]["gempa"]
    lat = earthquake_obj["Lintang"]
    long = earthquake_obj["Bujur"]
    mag = earthquake_obj["Magnitude"]
    depth = earthquake_obj["Kedalaman"]
    
    feel_data = earthquake_obj["Dirasakan"].split(" ")
    feel_scale = feel_data[0]
    feel_zone = feel_data[1:len(feel_data)-1]
    
    return {
        "lat": lat,
        "long": long,
        "magnitude": mag,
        "depth": depth,
        "feel_scale": feel_scale,
        "feel_zone": feel_zone,
    }


def get_geohash(latitude, longitude, type):
    precision = constants.DISASTER_MAPPING[type]
    return GeoHash.encode(latitude, longitude, precision)
