import json
import urllib
import requests
import os
import handler.datatype_handler as datatype_handler

api_key = os.environ.get('PUSHY_API_KEY')

class PushyAPI:
   @staticmethod
   def sendPushNotification(data, to, options):
      # Default post data to provided options or empty object
      postData = options or {}

      # Set notification payload and recipients
      postData['to'] = to
      postData['data'] = data

      # Set URL to Send Notifications API endpoint
      url = 'https://api.pushy.me/push?api_key=' + api_key
      headers = {
         'Content-Type': 'application/json'
      }

      # print(f'in pushyAPI {json.dumps(postData)}')
      try:
         # Actually send the push
         response = requests.post(url, headers=headers, data=json.dumps(postData, indent=4, sort_keys=True, default=datatype_handler.datetime_handler))
         response.raise_for_status()  # Raise an HTTPError if the response was an HTTP error
         return response
      except requests.exceptions.HTTPError as e:
         # Print response errors
         print("Pushy API returned HTTP error " + str(response.status_code) + ": " + response.text)
      except requests.exceptions.RequestException as e:
         # Print other request errors
         print(f"Pushy API request failed: {e}")