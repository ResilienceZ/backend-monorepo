import azure.functions as func
import logging
import requests

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
url_source = "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json"


@app.route(route="/disaster-listener/earthquake-bmkg")
def listenDisaster(req: func.HttpRequest) -> func.HttpResponse:
    try:
        response = requests.get(url_source)

        # Raise an exception if the request was unsuccessful
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()
        
        earthquake_obj = data["Infogempa"]["gempa"]
        lat = earthquake_obj["Lintang"]
        long = earthquake_obj["Bujur"]
        mag = earthquake_obj["Magnitude"]
        depth = earthquake_obj["Kedalaman"]
        
        feel_data = earthquake_obj["Dirasakan"].split(" ")
        feel_scale, feel_zone = feel_data[0], feel_data[0:len(feel_data-1)].join(" ")
        
        demo_data = {
            "lat": lat,
            "long": long,
            "magnitude": mag,
            "depth": depth,
            "feel_scale": feel_scale,
            "feel_zone": feel_zone,
        }
        
    except requests.exceptions.HTTPError as http_err:
        return func.HttpResponse(demo_data, status_code=200)
    except Exception as err:
        return func.HttpResponse(status_code=500)
