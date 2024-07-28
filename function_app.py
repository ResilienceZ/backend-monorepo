import azure.functions as func
import logging
import datetime
import service.bmkg as bmkg
import service.notifier as notifier
import json
import os
import service.repository as repo
import service.notifier as notifier
import constants
import controller.earthquake_controller as earthquake_controller
import handler.datatype_handler as datatype_handler

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
        
@app.route(route="disaster_demo_trigger")
def listen_disaster_trigger(req: func.HttpRequest) -> func.HttpResponse:
    try:
        demo_data = bmkg.fetch_latest_eq()
        db_data = repo.get_latest_record(1)
        
        return func.HttpResponse(
            db_data.toJSON(),
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
            emergency_contact.toJSON(),
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
    try:
        req_body = req.get_json()
        to = req_body.get('to')
        message = req_body.get('message')
        data = {'message': message}
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

@app.route(route="bmkg/check_for_new_disaster")
def check_for_new_disaster(req: func.HttpRequest) -> func.HttpResponse:
    try:
        new_disaster = earthquake_controller.is_new_disaster()
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

@app.route(route="bmkg/get_disaster")
def get_disaster(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        count = req_body.get('count')
        type = req_body.get('type')

        result = []

        disasters = repo.get_latest_record_with_type(type, count)
        print(f'disasters: {disasters}')

        for disaster in disasters:
            print(f'disaster: {disaster}')
            disaster_json = disaster.toJSON()
            print(f'disaster_json {disaster_json}')
            result.append(disaster_json)

        print(f'result: {result}')

        return func.HttpResponse(
            str(result),
            mimetype="application/json",
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
    new_disaster = earthquake_controller.is_new_disaster()
    if new_disaster == True:
        result_message = earthquake_controller.publish_to_pushy_latest_eq()

    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    # if timer.past_due:
    #     logging.info('The timer is past due!')
    # logging.info('Python timer trigger function ran at %s', utc_timestamp)