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

**Prepare database by making dockerfile which launches and ingests green taxi data and zones in to database
    Steps
        1. Download green taxi data from Oct 2019. I downloaded parquet file since I know i can convert, not familliar with unzipping tarball.
        2. create new local directory for green taxi data, make notepad for docker run command new database name ny_gtaxi to not cross wires with my 2024 workthrough and per slack notes using postgres17 from here forward
        3. launch docker pg-database instance
        4. launch jupter notebook, import pandas, download parquet data file (wget in vscode), use pandas to convert to csv, and check things.  Similar to yellow taxi data the pickup time and drop off schema needs to be overriden from text to datetime type.  create engine, establish connection, import headers, create iterator and import whole batch similar to 2024 exersize.
        5. work on new dockerfile and ingestion script that i can use for automating this green trips import as well as zones. -DONE!  had to try / catch errors
        6. data imported to datbase now --> Now ready to use sql to work to answering quesiton 3


Question 3: During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, respectively, happened:

    Up to 1 mile
    In between 1 (exclusive) and 3 miles (inclusive),
    In between 3 (exclusive) and 7 miles (inclusive),
    In between 7 (exclusive) and 10 miles (inclusive),
    Over 10 miles

part A: Select
            COUNT(1)
        FROM green_taxi_data t
        WHERE t.trip_distance < 1.01
        ==>104838
Part B: Select
            COUNT(1)
        FROM green_taxi_data t
        WHERE t.trip_distance > 1.00 AND t.trip_distance <3.01
        ==> 199013
Part C: Select
            COUNT(1)
        FROM green_taxi_data t
        WHERE t.trip_distance > 3.00 AND t.trip_distance <7.01
        ==>109645
Part D: Select
            COUNT(1)
        FROM green_taxi_data t
        WHERE t.trip_distance > 7.00 AND t.trip_distance <10.01
        ==> 27688
Part E: Select
            COUNT(1)
        FROM green_taxi_data t
        WHERE t.trip_distance > 10.00
        ==> 35202
    ANSWER: 104,838, 199,013, 109,645, 27,688, 35,202

Question 4: Question 4. Longest trip (1 point)
    Select
        *
    FROM green_taxi_data
        ORDER BY trip_distance DESC
    LIMIT(1)
    ==>2019-10-31...to 2019-11-01...
    ANSWER: 2019-10-31

Question 5: Which were the top pickup locations with over 13,000 in total_amount (across all trips) for 2019-10-18?

    Consider only lpep_pickup_datetime when filtering by date.
    Select
        SUM(total_amount) AS total,
        zpu."Zone"
    FROM green_taxi_data t,
        zones zpu
        WHERE t."PULocationID" = zpu."LocationID" AND
            t.lpep_pickup_datetime >= '2019-10-18 00:00:01' AND 
        t.lpep_pickup_datetime <= '2019-10-18 23:59:59'
    GROUP BY zpu."Zone"
    ORDER BY total DESC
    LIMIT 5;
    ANSWER==> East Harlem North, East Harlem South, Morningside Heights

Question 6: For the passengers picked up in October 2019 in the zone name "East Harlem North" which was the drop off zone that had the largest tip?   Note: it's tip , not trip   We need the name of the zone, not the ID.

    ANSWER:  ==> I currently cannot figure this one out :(

    

Question 7:
    
