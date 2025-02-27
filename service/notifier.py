from service.pushy import PushyAPI

def notify(destination_topic: str, data: str, message: str):
    data = data

    to = '/topics/'+destination_topic

    options = { 
        'notification': {
            'badge': 1,
            'sound': 'ping.aiff',
            'title': 'Test Notification',
            'body': message
        }
    }

    PushyAPI.sendPushNotification(data, to, options)