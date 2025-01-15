FROM python:3.9
#run docker container of python 3.9

#tell it to install pandas for csv/parquet files
#also psycopg2 pyarrow and fastparquet for conversion from pq to csv
RUN pip install pandas sqlalchemy psycopg2 pyarrow fastparquet
#install wget for download
RUN apt-get install wget

#what directory to start in
WORKDIR /app
#copy file from host machine int to docker
COPY ingest_data.py ingest_data.py

#even though we're running python docker 
#container we can force to enter at bash(ubuntu)
ENTRYPOINT [ "python", "ingest_data.py" ]