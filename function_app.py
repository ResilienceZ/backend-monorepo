import azure.functions as func
import logging
import service.bmkg as bmkg
import service.notifier as notifier
import json
import os

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
pushy_api_key = os.environ.get('PUSHY_API_KEY')

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
        
@app.route(route="disaster_demo_trigger")
def listen_disaster_trigger(req: func.HttpRequest) -> func.HttpResponse:
    try:
        demo_data = bmkg.fetch()
        
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

@app.schedule(schedule="0 * * * * *", arg_name="req", run_on_startup=True, use_monitor=False) 
def timer_trigger(req: func.TimerRequest) -> None:
    if req.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')