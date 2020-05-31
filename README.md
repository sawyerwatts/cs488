# CS488 Term Project

This is the repo for the term project in CS 488: Cloud and Cluster Data
Management. This project involves denormalizing some relational data to be
stored and used within a MongoDB instance that is running on a Google Cloud
Platform, and then performing some tasks on that NoSQL database.

## Set Up

After cloning this repo, untar `assets.tar.gz`, which contains a collection of
CSVs `csv_to_json.py` will normalize to create the JSON file. Due to the simplicity
of this program, the script will not catch a FileNotFoundError.

    $ tar -xzf assets.tar.gz

Next, it is necessary to install the needed virtual environment. This requires
the Python package Pipenv to be installed. This project uses Python 3.5.

    $ pipenv shell
    (cs488) $ pipenv install

## Denormalization

This process is controlled by `csv_to_json.py`, which reads the needed CSVs
from `assets/` and generates `output.json`, which can then be imported into
MongoDB.  

The general design for the MongoDB document is below. Please keep in mind that
`datetimerecorded` is a poor name and `epoch` would be much better.

    {
        location =
        {
            stationname,
            detectorid,
            highwayname,
            direction,
            stationlength,
            nextstationname
        },
        recorded =
        {
            speed,
            datetimerecorded,
            volume
        }
    }

The mapping of what relation field to the corresponding document attribute
is below, where an arrow indicates that the field is renamed in the document.

    freeway_loopdata(detectorid)
    freeway_loopdata(volume)
    freeway_loopdata(speed)
    freeway_loopdata(starttime)   →  datetimerecorded

    freeway_station(locationtext) →  stationname
    freeway_stations(length)      →  stationlength
    freeway_stations(downstream)  →  nextstationname

    highway(direction)
    highway(highwayname)

## Queries

The various files that follow the syntax regex("query?\.py") are the various
assigned queries for this project. These are described bellow.

1. Count high speeds: Find the number of speeds > 100 in the data set.

2. Volume: Find the total volume for the station Foster NB for Sept 21, 2011.

3. Single-Day Station Travel Times: Find travel time for station Foster NB for
5-minute intervals for Sept 22, 2011. Report travel time in seconds.

4. Peak Period Travel Times: Find the average travel time for 7-9AM and 4-6PM
on September 22, 2011 for station Foster NB. Report travel time in seconds.

5. Peak Period Travel Times: Find the average travel time for 7-9AM and 4-6PM
on September 22, 2011 for the I-205 NB freeway. Report travel time in minutes.

6. Route Finding: Find a route from Johnson Creek to Columbia Blvd on I-205 NB
using the upstream and downstream fields.

