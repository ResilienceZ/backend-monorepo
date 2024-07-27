import json
import urllib
import requests
import os

api_key = os.environ.get('PUSHY_API_KEY')

class PushyAPI:
   @staticmethod
   def sendPushNotification(data, to, options):
      # Default post data to provided options or empty object
      postData = {}

      # Set notification payload and recipients
      postData['to'] = to
      postData['data'] = data

      # Set URL to Send Notifications API endpoint
      print(f'api_key {api_key}')
      url = 'https://api.pushy.me/push?api_key=' + api_key
      print(f'url {url}')
      headers = {
         'Content-Type': 'application/json'
      }

      print(f'in pushyAPI {str(postData)}')
      try:
         # Actually send the push
         response = requests.post(url, headers=headers, data=json.dumps(postData))
         response.raise_for_status()  # Raise an HTTPError if the response was an HTTP error
         return response
      except requests.exceptions.HTTPError as e:
         # Print response errors
         print("Pushy API returned HTTP error " + str(response.status_code) + ": " + response.text)
      except requests.exceptions.RequestException as e:
         # Print other request errors
         print(f"Pushy API request failed: {e}")