import service.bmkg as bmkg
import service.notifier as notifier
import json
import service.repository as repo
from data.disaster_report import DisasterReport
from data.disaster_record import DisasterRecord
import handler.datatype_handler as datatype_handler

def get_eq_geohash(details):
	geohash = bmkg.get_geohash(details["latitude"], details["longitude"], details["type"])
	return geohash

def publish_to_pushy_latest_eq():
	try:
		latest_eq = bmkg.fetch_latest_eq()
		latest_geohash = get_eq_geohash(latest_eq)

		data = {}

		message = 'Earthquake Alert in your area!'
		data['message'] = message
		data['data'] = latest_eq

		data_json = json.dumps(data, default=datatype_handler.datetime_handler)
		print(f'data_json: {data_json}')
		notifier.notify(latest_geohash, data, message)
		notifier.notify('jakarta', data, message)
		return 'Success'
	except Exception as err:
		return err

def is_new_disaster():

	latest_eq = bmkg.fetch_latest_eq()
	latest_eq_timestamp = latest_eq['timestamp']

	is_new = True

	last_record = repo.get_latest_record()
	if len(last_record) > 0:
		last_timestamp = getattr(last_record[0], 'timestamp')
		if latest_eq_timestamp == last_timestamp:
			is_new = False
			return False

	if is_new:
		repo.insert_record(DisasterRecord(**latest_eq))
