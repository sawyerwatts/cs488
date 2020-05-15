# CS488 Term Project

This is the repo for the term project in CS 488: Cloud and Cluster Data
Management. This project involves denormalizing some relational data to be
stored and used within a MongoDB instance that is running on a Google Cloud
Platform, and then performing some tasks on that NoSQL database.

## Set Up

After cloning this repo, untar `assets.tar.gz`, which contains a collection of
CSVs this script will normalize to create the JSON file. Due to the simplicity
of this program, the script will not catch a FileNotFoundError.

    $ tar -xzf assets.tar.gz

Next, it is necessary to install the needed virtual environment. This requires
the Python package Pipenv to be installed. This project uses Python 3.6.

    $ pipenv shell
    (cs488) $ pipenv install

## Denormalization

This process is controlled by `csv_to_json.py`, which reads the needed CSVs
from `assets/` and generates `output.json`, which can then be imported into
MongoDB.  

The general design for the MongoDB document is below.

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
    freeway_stations(downstream)  →  next

    highway(direction)
    highway(highwayname)

