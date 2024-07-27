import bmkg as bmkg
import notifier as notifier
import json

def get_eq_geohash(details):
	geohash = bmkg.get_geohash(details["lat"], details["long"], "earthquake")
	return geohash

def publish_to_pushy_latest_eq():
	try:
		latest_eq = bmkg.fetch_latest_eq()
		latest_geohash = get_eq_geohash(latest_eq)

		data = {}

		message = 'Earthquake Alert in your area!'
		data['message'] = message
		data['data'] = latest_eq

		data_json = json.dumps(data)
		print(f'data_json: {data_json}')
		notifier.notify(latest_geohash, data, message)
		notifier.notify('jakarta', data, message)
		return 'Success'
	except Exception as err:
		return err