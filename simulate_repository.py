import repository as repo

print(repo.get_latest_record(1))
print(repo.get_latest_report(2))
print(repo.get_latest_report_by_geohash("somegeo","2024-07-27T19:32:00UTC",1))