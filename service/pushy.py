import json
import urllib
import os

class PushyAPI:
    @staticmethod
    def sendPushNotification(data, to, options):

        # Default post data to provided options or empty object
        postData = options or {}
        
        # Set notification payload and recipients
        postData['to'] = to
        postData['data'] = data

        # Set URL to Send Notifications API endpoint
        req = urllib.Request('https://api.pushy.me/push?api_key=' + os.environ.get('PUSHY_API_KEY'))

        # Set Content-Type header since we're sending JSON
        req.add_header('Content-Type', 'application/json')

        try:
           # Actually send the push
           urllib.urlopen(req, json.dumps(postData))
        except urllib.HTTPError as e:
           # Print response errors
           print("Pushy API returned HTTP error " + str(e.code) + ": " + e.read())