import dbservice as db
from disaster_report import DisasterReport
from disaster_record import DisasterRecord

# Diaster Record
def get_latest_record(limit: int = 1):
    query = "SELECT * FROM disaster_records ORDER BY timestamp DESC LIMIT %s;"
    query_result = db.exec_select(query, (limit,))
    
    result = []
    for res in query_result:
        result.append(DisasterRecord(*res))
    return result

def get_latest_record_with_type(dtype: str, limit: int = 1):
    query = "SELECT * FROM disaster_records WHERE type=%s ORDER BY timestamp DESC LIMIT %s;"
    query_result = db.exec_select(query, (dtype, limit,))
    
    result = []
    for res in query_result:
        result.append(DisasterRecord(*res))
    return result

def insert_record(record: DisasterRecord):
    query = """
        INSERT INTO public.disaster_records (description, severity, scale, longitude, latitude, type, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        record.description, record.severity, record.scale, 
        record.longitude, record.latitude, record.type, record.timestamp
    )
    db.exec_commit(query, values)
    
def get_latest_report(limit: int = 1):
    query = "SELECT * FROM disaster_reports ORDER BY timestamp DESC LIMIT %s;"
    query_result = db.exec_select(query, (limit,))
    
    result = []
    for res in query_result:
        result.append(DisasterReport(*res))
    return result
    
    
# Report
def get_latest_report_by_geohash(geohash: str, max_timestamp: str, limit: int = 1):
    query = "SELECT * FROM disaster_reports WHERE geohash=%s AND timestamp>%s ORDER BY timestamp DESC LIMIT %s;"
    query_result = db.exec_select(query, (geohash, max_timestamp, limit,))
    
    result = []
    for res in query_result:
        result.append(DisasterReport(*res))
    return result

def insert_report(report: DisasterReport):
    query = """
        INSERT INTO public.disaster_reports (reporter_uniqueid, longitude, latitude, geohash, type, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (
        report.reporter_uniqueid, report.longitude, report.latitude, 
        report.geohash, report.type, report.timestamp
    )
    db.exec_commit(query, values)
