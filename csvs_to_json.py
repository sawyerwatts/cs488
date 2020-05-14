import pandas

print("Loading CSVs.")
print("\tLoading freeway_detectors.csv")
detectors = pandas.read_csv("assets/freeway_detectors.csv")

print("\tLoading highways.csv")
highways = pandas.read_csv("assets/highways.csv")

print("\tLoading freeway_stations.csv")
stations = pandas.read_csv("assets/freeway_stations.csv")

print("\tLoading freeway_loopdata.csv")
loopdata = pandas.read_csv("assets/freeway_loopdata.csv", parse_dates=["starttime"])

print()
print("Starting to process data.")


###############################################################################


def process_row(row, verbose=False):
    def var_print(desc, var):
        if verbose: print("\t", desc, type(var), str(var))

    try:
        det_id = row["detectorid"]
        var_print("detectorid", det_id)

        vol = row["volume"]
        var_print("volume", vol)

        speed = row["speed"]
        var_print("speed", speed)

        datetimerecorded = row["starttime"]
        var_print("datetimerecorded", datetimerecorded)

        stationname = get_stationname(row)
        var_print("stationname", stationname)

        highwayname   = get_highwayname(row)
        var_print("highwayname", highwayname)

        direction     = get_direction(row)
        var_print("direction", direction)

        nextstationname = get_nextstationname(row)
        var_print("nextstationname", nextstationname)

        stationlength = get_stationlength(row)
        var_print("stationlength", stationlength)

        return {
                "location": {
                    "stationname": stationname,
                    "detectorid" : det_id,
                    "highwayname": highwayname,
                    "direction"  : direction,
                    "stationlength"
                                 : stationlength,
                    "nextstationname"
                                 : nextstationname
                    },
                "recorded": {
                    "speed"           : speed,
                    "datetimerecorded": datetimerecorded,
                    "volume"          : vol
                    }
                }

    except IndexError:
        return None


def get_stationname(row):
    global detetectors
    global stations

    detector_row = detectors[detectors["detectorid"] == row["detectorid"]]
    stationid = detector_row["stationid"].iloc[0]
    station_row = stations[stations["stationid"] == stationid]
    return station_row["locationtext"].iloc[0]


def get_highwayname(row):
    global detetectors
    global highways

    detector_row = detectors[detectors["detectorid"] == row["detectorid"]]
    highwayid = detector_row["highwayid"].iloc[0]
    highway_row = highways[highways["highwayid"] == highwayid]
    return highway_row["highwayname"].iloc[0]


def get_direction(row):
    global detetectors
    global highways

    detector_row = detectors[detectors["detectorid"] == row["detectorid"]]
    highwayid = detector_row["highwayid"].iloc[0]
    highway_row = highways[highways["highwayid"] == highwayid]
    return highway_row["shortdirection"].iloc[0]


def get_nextstationname(row):
    global detetectors
    global stations

    detector_row = detectors[detectors["detectorid"] == row["detectorid"]]
    stationid = detector_row["stationid"].iloc[0]
    station_row = stations[stations["stationid"] == stationid]

    downstream_stationid = station_row["downstream"].iloc[0]
    station_row = stations[stations["stationid"] == stationid]
    return station_row["locationtext"].iloc[0]


def get_stationlength(row):
    global detetectors
    global stations

    detector_row = detectors[detectors["detectorid"] == row["detectorid"]]
    stationid = detector_row["stationid"].iloc[0]
    station_row = stations[stations["stationid"] == stationid]
    return station_row["length"].iloc[0]


###############################################################################


# This will cause a Series of NoSQL documents (as dicts); next, convert this
# Series to JSON with pandas.Series.to_json(), and then write this JSON to
# disk. This will allow MongoDB to import that JSON file as a list of
# documents.
results = loopdata.apply(axis=1, func=process_row)
results.dropna(inplace=True)
print()


print("Converting to JSON and writing to disk")
results.to_json("output.json", orient="records")
print()


print("Here is memory usage of the DataFrames (for funsies)")
print("\tThe output JSON has been written, you can kill this process at any point.")
print("detectors")
detectors.info()
print("loopdata")
loopdata.info()
print("stations")
stations.info()
print("highways")
highways.info()
print("results")
results.to_frame().info()

