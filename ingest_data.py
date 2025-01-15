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
    url = params.url
    parquet_name='output.parquet'
    csv_name = 'output.csv'

    #download the parquet in the system 'command line' by using wget
    #https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet
    os.system(f'wget {url} -O {parquet_name}')

    #read parquet file and convert to csv file
    df = pd.read_parquet(parquet_name)
    df.to_csv(csv_name)

    #engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    #engine.connect()
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    #why is this needed?? can i delete?
    df = next(df_iter)

    #on initial inspection we found these load as text but we need to cast 
    # them to timestampe data types when importing to our database
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    #first only look at the headers (line 0)
    #create (or overwrite) table in the database that loads the headers
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    #this is the first 100,000 lines
    df.to_sql(name=table_name, con=engine, if_exists='append')
    #loop through the remaining in 100,000 line iterations appending them 
    # to the previusly created (or replaced) table
    while True:
        start_time = time()
        df = next(df_iter)

        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append') 
        end_time = time()
        print('inserted another chunk... took %.3f second' % (end_time - start_time))


if __name__=='__main__':

    parser = argparse.ArgumentParser(description="Ingest parquet file, convert to csv, upload data file to postgres")

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password name for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table we will add to the db')
    parser.add_argument('--url', help='url of parquet data file')

    args = parser.parse_args()

    main(args)