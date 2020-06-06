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
the Python package Pipenv to be installed. This project uses Python 3.5 as that is
the version of Python3 on the Google Cloud Platform (GCP) MongoDB used.

    $ pipenv shell
    (cs488) $ pipenv install

### GCP Set Up

To use the project on GCP as it was during development, set up a GCP project and
create a virtual machine (VM). SSH into the VM. 

Install Mongo on the VM. These are the commands we used:

	sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10

	echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list

	sudo apt-get update

	sudo apt-get install mongodb

### Load Data into Database
Start Mongo and create a database for the freeway data:

	mongo
	use freewaydata
	quit()
	
Now that you have a database for your data, load it:

	mongoimport --jsonArray --db freewaydata --collection allData --file output.json

### Install Python MongoDB Driver

If pip isn't installed (which is most likely the case on GCP), you will need to
install it.

	curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
	python3 get-pip.py
	
Next, you will need to install Pipenv.

	python3 -m pip install pipenv

## Denormalization

This process is controlled by `csv_to_json.py`, which reads the needed CSVs
from `assets/` and generates `output.json`, which can then be imported into
MongoDB.  

The general design for the MongoDB document is below. Please keep in mind that
`datetimerecorded` is a poor name and `epoch` would be much better as it stores
the *milliseconds* since Epoch.

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

The various files that follow the syntax regex(query[1-6]\.py) are the various
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

These queries all use `query_setup.py`, which will determine which dataset to
work with. If any arguments are supplied, `query_setup.py` will have the query
script use the test dataset (one hour data from 2011 Sept 15). Otherwise, the
full dataset is used.

## Visualizations

The various files that follow the syntax regex(pre_visualize[1-6]\.py) are
visualization scripts that go into more detail about the corresponding query.

The various file(s) that follow the syntax regex(pre_visualize[1-6]\.py) are
used to generate a CSV that can be visualized by file(s) with syntax
regex(visualize[1-6]\.py). The pregenerated files live in
visualizations.tar.gz, along with output HTML files for ease of reuse.

1. This visualization will take the entries with a speed greater than 100 MPH
and plot the time by the station to display the frequency of this high speed,
scrubbed down to the hour. There will be a plot for each day.

## `epoch_converter.py`

This contains `convert_epoch()`.

### `convert_epoch(seconds, type="datetime")`

This will convert `seconds`, which is seconds since 1 Jan 1970, and convert it
to the current time. The data type of the return value is set by `type`, which
can be `"datetime"` or `"string"`, and will thrown an exception for any other
value.

