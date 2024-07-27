import azure.functions as func
import logging
import service.bmkg as bmkg
import service.notifier as notifier
import json
import os

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
        
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

@app.route(route="get-emergency-contact")
def get_emergency_contact(req: func.HttpRequest) -> func.HttpResponse:
    try: 
        # emergency_contact = postgre.fetch("select * from emergency_contact")
        emergency_contact = ''

        return func.HttpResponse(
            json.dumps(emergency_contact),
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