#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os
from time import time
from sqlalchemy import create_engine
import argparse

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    zones_table_name = params.zones_table_name
    urlg = params.urlg #green taxi data url
    urlz = params.urlz #taxi zones data url
    parquet_name='output.parquet' #parquet download of green taxi data
    gcsv_name = 'goutput.csv' #green taxi data csv file (after converted)
    zcsv_name = 'zoutput.csv' #zone csv as downloaded

    #download the parquet in the system 'command line' by using wget
    #https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-10.parquet
    os.system(f'wget {urlg} -O {parquet_name}') #download green taxi parquet data
    os.system(f'wget {urlz} -O {zcsv_name}') #download zones data

    #read parquet file and convert to csv file
    df = pd.read_parquet(parquet_name)
    df.to_csv(gcsv_name)

    #engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    #engine.connect()
    df_iter = pd.read_csv(gcsv_name, iterator=True, chunksize=100000)
    #why is this needed?? If I delete i miss the first 100,000, not sure i get how iter works
    df = next(df_iter)

    #on initial inspection we found these load as text but we need to cast 
    # them to timestampe data types when importing to our database
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    #first only look at the headers (line 0)
    #create (or overwrite) table in the database that loads the headers
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    #this is the first 100,000 lines
    df.to_sql(name=table_name, con=engine, if_exists='append')
    #loop through the remaining in 100,000 line iterations appending them 
    # to the previusly created (or replaced) table
#    while True:
#        start_time = time()
#        df = next(df_iter)
#        #cast to datetime type before uploading
#        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
#        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
#        #connect and add
#        df.to_sql(name=table_name, con=engine, if_exists='append') 
#        end_time = time()
#        print('inserted another chunk... took %.3f second' % (end_time - start_time))
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

    print("I am leaving the first import and moving to the second for zones")

    #zones_table_name
    #de = pd.read_csv('taxi_zone_lookup.csv', nrows=100)
    de = pd.read_csv(zcsv_name, nrows=100)
    #de_iter = pd.read_csv('taxi_zone_lookup.csv', iterator=True, chunksize=100)
    de_iter = pd.read_csv(zcsv_name, iterator=True, chunksize=100)

    de = next(de_iter)

    de.head(n=0).to_sql(name=zones_table_name, con=engine, if_exists='replace')

    de.to_sql(name=zones_table_name, con=engine, if_exists='append') 

    try:
        while True:
            start_time = time()
            de = next(de_iter)
            de.to_sql(name=zones_table_name, con=engine, if_exists='append') 
            end_time = time()
            print('inserted another chunk... took %.3f second' % (end_time - start_time))
    except StopIteration:
        pass

#I think i can leave this alone as the main fuction at the bottom.

if __name__=='__main__':

    parser = argparse.ArgumentParser(description="Ingest parquet file, convert to csv, upload data file to postgres")

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password name for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the green table we will add to the db')
    parser.add_argument('--zones_table_name', help='name of the zone table we will add to the db')
    parser.add_argument('--urlg', help='url of parquet green taxi data file')
    parser.add_argument('--urlz', help='url of zones csv file')

    args = parser.parse_args()

    main(args)