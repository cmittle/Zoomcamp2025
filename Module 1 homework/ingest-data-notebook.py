#!/usr/bin/env python
# coding: utf-8

####
#this is my jupyter notebook from testing.  I've exported to script and cleaned it up
#but reviewed and pasted results in to ingest_green.py file
###
import pandas as pd

import os
from sqlalchemy import create_engine
from time import time

df=pd.read_parquet('green_tripdata_2019-10.parquet')

df.to_csv('green_tripdata_2019-10.csv')

df = pd.read_csv('green_tripdata_2019-10.csv', nrows=100)

engine = create_engine('postgresql://root:root@localhost:5432/ny_gtaxi')
engine.connect()


#print(pd.io.sql.get_schema(df, name="green_taxi_data", con=engine))

df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

df_iter = pd.read_csv('green_tripdata_2019-10.csv', iterator=True, chunksize=100000)

df = next(df_iter)
df.head(n=0).to_sql(name='green_taxi_data', con=engine, if_exists='replace')
df.to_sql(name='green_taxi_data', con=engine, if_exists='append') 
#ingestion loop for green taxi data
try:
    while True:
        start_time = time()
        df = next(df_iter)
        #cast to datetime types
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
        df.to_sql(name='green_taxi_data', con=engine, if_exists='append') 
        end_time = time()
        print('inserted another chunk... took %.3f second' % (end_time - start_time))
except StopIteration:
    pass

de = pd.read_csv('taxi_zone_lookup.csv', nrows=100)

de_iter = pd.read_csv('taxi_zone_lookup.csv', iterator=True, chunksize=100)

de = next(de_iter)

de.head(n=0).to_sql(name='zones', con=engine, if_exists='replace')

de.to_sql(name='zones', con=engine, if_exists='append') 

try:
    while True:
        start_time = time()
        de = next(de_iter)
        de.to_sql(name='zones', con=engine, if_exists='append') 
        end_time = time()
        print('inserted another chunk... took %.3f second' % (end_time - start_time))
except StopIteration:
    pass

