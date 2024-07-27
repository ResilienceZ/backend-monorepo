import json
import urllib2

pushy_api_key = os.environ.get('PUSHY_API_KEY')

class PushyAPI:
    @staticmethod
    def sendPushNotification(data, to, options):

        # Default post data to provided options or empty object
        postData = options or {}
        
        # Set notification payload and recipients
        postData['to'] = to
        postData['data'] = data

        # Set URL to Send Notifications API endpoint
        req = urllib2.Request('https://api.pushy.me/push?api_key=' + pushy_api_key)

        # Set Content-Type header since we're sending JSON
        req.add_header('Content-Type', 'application/json')

        try:
           # Actually send the push
           urllib2.urlopen(req, json.dumps(postData))
        except urllib2.HTTPError as e:
           # Print response errors
           print("Pushy API returned HTTP error " + str(e.code) + ": " + e.read())