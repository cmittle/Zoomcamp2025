FROM python:3.9
#run docker container of python 3.9

#tell it to install pandas
RUN pip install pandas

#what directory to start in
WORKDIR /app
#copy file from host machine int to docker
COPY pipeline.py pipeline.py

#even though we're running python docker 
#container we can force to enter at bash(ubuntu)
ENTRYPOINT [ "python", "pipeline.py" ]