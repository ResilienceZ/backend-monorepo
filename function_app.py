import azure.functions as func
import logging
import requests
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
        )
        
        
@app.route(route="listen_disaster_trigger")
def listen_disaster_trigger(req: func.HttpRequest) -> func.HttpResponse:
    try:
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
        
        demo_data = {
            "lat": lat,
            "long": long,
            "magnitude": mag,
            "depth": depth,
            "feel_scale": feel_scale,
            "feel_zone": feel_zone,
        }
        return func.HttpResponse(
            json.dumps(demo_data),
            mimetype="application/json",
            status_code=200
        )
    except Exception as err:
        return func.HttpResponse(
            f"Error. {err}",
            status_code=500
        )