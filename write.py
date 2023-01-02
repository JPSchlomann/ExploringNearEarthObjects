"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.
"""

import csv
import json
import helpers

def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """

    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )
    # Write the results to a CSV file
    with open(filename, 'w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames)
        writer.writeheader()
        if results:
            for result in results:
                dict = {'datetime_utc': result.time, 'distance_au': result.distance,'velocity_km_s': result.velocity,
                'designation': result.neo.designation, 'name': result.neo.name, 'diameter_km': result.neo.diameter, 'potentially_hazardous': result.neo.hazardous}
                writer.writerow(dict)

def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    # prepare results for writing it to a json file
    results_json_format = []

    for result in results:
        results_dic = {
        'datetime_utc': helpers.datetime_to_str(result.time),
        'distance_au': result.distance,
        'velocity_km_s': result.velocity,
        'neo': {
        'designation': result.neo.designation,
        'name': result.neo.name,
        'diameter_km': result.neo.diameter,
        'potentially_hazardous': result.neo.hazardous
        }
        }
        results_json_format.append(results_dic)

    # Write the results to a JSON file
    with open(filename, 'w') as outfile:
        json.dump(results_json_format, outfile, indent=2)
