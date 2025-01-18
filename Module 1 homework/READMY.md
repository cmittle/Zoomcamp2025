Question 1: Run docker with the python:3.12.8 image in an interactive mode, use the entrypoint bash.

What's the version of pip in the image?

Steps: 
    1 Build docker file to launch with python 3.12.8 in to entry point bash
    2 create pipcheck.sh shell script which runs 'pip --version'
    3 add working directory to dockerfile and copy pipcheck.sh in during launch
    4 create entry point in docker file which launches in 'bash' and executes the pipcheck.sh

    Answer = from terminal output ==>pip 24.3.1

Question 2:Given the following docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?
    Inspection:
        database and pgadmin are launched together within services which means they are on the same network = *localhost*
        The database port will be *5432* unless overridden, the yaml file for compose uses 5433:5432 which is formated as host computer : database connection.
        THere fore *localhost:5432* is what pgadmin shall connect on.

    Answer = localhost:5432

Question 3: