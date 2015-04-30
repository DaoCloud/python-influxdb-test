#-*-encoding:utf-8-*-

import logging
import time
import random
import threading
import string
from influxdb.influxdb08 import InfluxDBClient
from config import INFLUXDB_PORT_8086_TCP_ADDR,INFLUXDB_PORT_8086_TCP_PORT,INFLUXDB_USERNAME,INFLUXDB_PASSWORD

INFLUXDB_TIMEOUT=30
database='DB'
series_name='taoge_test'
series_columns=['int_time','random_string']

LOG=logging.getLogger(__name__)

def __gen_client():
    return InfluxDBClient(host=INFLUXDB_PORT_8086_TCP_ADDR,port=INFLUXDB_PORT_8086_TCP_PORT,database=database,username=INFLUXDB_USERNAME,password=INFLUXDB_PASSWORD,timeout=INFLUXDB_TIMEOUT)


def __init_db():
    client=__gen_client()
    dbs=[d.get('name') for d in client.get_list_database()]
    print 'DBS:',' , '.join(dbs)
    if not dbs or database not in dbs:
        if not client.create_database(database):
            print 'err create db.'
            raise Exception('CAN NOT CREATE DB.')


def __gen_data(name,columns,points):
    assert len(columns)==len(points[0])
    return {'name':name,
        'columns':columns,
        "points":points}

def write_data():
    client=__gen_client()
    while True:
        points=[[int(time.time()),'-'.join(random.sample(string.lowercase+string.uppercase+string.digits,5))]]
        data=__gen_data(series_name,series_columns,points)
        client.write_points([data])
        print '<--',','.join([str(p) for p in points[0]])
        time.sleep(1)

def read_data():
    client=__gen_client()
    query="select * from %s limit 5"%series_name
    while True:
        data=client.query(query)
        for d in data:
            for ps in d['points']:
                print '-->',' | '.join([str(i) for i in ps])
        time.sleep(1)


if __name__=='__main__':
    __init_db()
    print 'COLUMNS :',' , '.join(series_columns)
    t1=threading.Thread(target=write_data)
    t2=threading.Thread(target=read_data)
    t1.start()
    t2.start()
    print 'END'
