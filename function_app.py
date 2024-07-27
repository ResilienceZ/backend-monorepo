import azure.functions as func
import logging
import datetime
import service.bmkg as bmkg
import service.notifier as notifier
import json
import os
import service.dbservice as repo
import service.notifier as notifier
import constants
import controller.earthquake_controller as earthquake_controller

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
        
@app.route(route="disaster_demo_trigger")
def listen_disaster_trigger(req: func.HttpRequest) -> func.HttpResponse:
    try:
        demo_data = bmkg.fetch_latest_eq()
        
        db_data = repo.exec_select("SELECT * FROM disaster_records ORDER BY timestamp DESC LIMIT 1;")
        
        return func.HttpResponse(
            json.dumps(db_data),
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

@app.route(route="push_notification")
def send_push_notification(req: func.HttpRequest) -> func.HttpResponse:
    print('in send_push_notification')
    try:
        print(f'req {str(req)}')
        req_body = req.get_json()
        to = req_body.get('to')
        message = req_body.get('message')
        data = {'message': message}
        print(f'to {to}, data {data}')
        notifier.notify(to, data, message)

        return func.HttpResponse(
            f"Request done successfully with message {message}", 
            status_code=200
            )
    except Exception as err:
        return func.HttpResponse(
                f"Error. {err}",
                status_code=500
            )

@app.route(route="get_disaster_mapping")
def get_geohash(req: func.HttpRequest) -> func.HttpResponse:
    try:
        return func.HttpResponse(
                str(constants.DISASTER_MAPPING),
                mimetype="application/json",
                status_code=200
                )
    except Exception as err:
        return func.HttpResponse(
                f"Error. {err}",
                status_code=500
            )

@app.route(route="bmkg/alert_last_eq")
def push_disaster_alert(req: func.HttpRequest) -> func.HttpResponse:
        result_message = earthquake_controller.publish_to_pushy_latest_eq()
        # print(f'result_message {result_message}')
        if result_message == 'Success':
            return func.HttpResponse(
                f"Request done successfully with message {result_message}",
                status_code=200
                )
        else:
            return func.HttpResponse(
                    f"Error. {result_message}",
                    status_code=500
                )

@app.route(route="test/checkdb")
def check_for_new_disaster(req: func.HttpRequest) -> func.HttpResponse:
    try:
        print('in check_for_new_disaster')
        new_disaster = earthquake_controller.is_new_disaster()
        print(f'new_disaster: {new_disaster}')
        if new_disaster == False:
            return func.HttpResponse(
                f"No new disaster",
                status_code=200
                )
        else:
            return func.HttpResponse(
                f"New disaster detected",
                status_code=200
                )
    except Exception as err:
        return func.HttpResponse(
                f"Error. {err}",
                status_code=500
            )

@app.function_name(name="get_eq_data_timer")
@app.timer_trigger(schedule="*/5 * * * * *", 
              arg_name="timer",
              run_on_startup=True)
def get_eq_data_timer(timer: func.TimerRequest) -> None:
    print('in get_eq_data_timer')
    new_disaster = earthquake_controller.is_new_disaster()
    print(new_disaster)
    if new_disaster == False:
        print('No new disaster')
    else:
        result_message = earthquake_controller.publish_to_pushy_latest_eq()

    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    if timer.past_due:
        logging.info('The timer is past due!')
    logging.info('Python timer trigger function ran at %s', utc_timestamp)