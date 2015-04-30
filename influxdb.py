#-*-encoding:utf-8-*-

import logging
import time
import random
import threading
from influxdb.influxdb08 import InfluxDBClient
from config import INFLUXDB_PORT_8086_TCP_ADDR,INFLUXDB_PORT_8086_TCP_PORT,INFLUXDB_USERNAME,INFLUXDB_PASSWORD

INFLUXDB_TIMEOUT=30
database='DB'
series_name='taoge_test'
series_columns=['int_time','random_string']

LOG=logging.getLogger(__name__)

def __gen_client():
    u = urlparse(INFLUXDB_URL)
    return InfluxDBClient(host=INFLUXDB_PORT_8086_TCP_ADDR,port=INFLUXDB_PORT_8086_TCP_PORT,
            database=database,username=INFLUXDB_USERNAME,
            password=INFLUXDB_PASSWORD,timeout=INFLUXDB_TIMEOUT)


def __init_db():
	client=__gen_client()
	dbs=[d.get('name') for d in client.get_list_database()]
	if not dbs or database not in dbs:
		if not client.create_database(database):
			raise Exception('INIT DB FAILED.')

def __gen_data(name,columns,points):
	assert len(columns)==len(points)
	return {'name':name,
			'columns':columns,
			"points":points}

def write_data():
	client=__gen_client()
	
	while True:
		points=[int(time.time),'-'.join(random.sample(string.lowercase+string.uppercase+string.digits,5))]
		data=__gen_data(series_name,series_columns,points)
		client.write([data])
		print '<<<',series_name,';'.join(series_columns),';'.join(points)
		time.sleep(1)

def read_data():
	client=__gen_client()
	query="select * from {%s} limit 10"%series_name
	while True:
		data=client.query(query)
		for d in data:
			print '>>>',d["name"],';'.join(d["columns"]),';'.join('|'.join([ p for p in d["points"]])



if __name__=='__main__':
	t1=threading.Thread(target=write_data)
	t2=threading.Thread(target=read_data)
	t1.start()
	t2.start()
