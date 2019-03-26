import json
from statistics import mean, stdev
from collections import defaultdict

import argparse
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# This script creates a JSON file in a format readable by the LP model creator
# See clackams_extracted.json for example of structure

Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--savename', help="the name of the file to score the formatted data to")
args = parser.parse_args()

# Opens a file selector window for a user to choose the RS JSON file they want to format
file_path = askopenfilename(
    filetypes=[("JSON files", '*.json')])  # show an "Open" dialog box and return the path to the selected file

with open(file_path, 'r') as file_path:
    json_data = json.load(file_path)

calculation_map = {'max': max, 'min': min, 'avg': mean}


# This function extracts minimums/maxes/averages (for each team)
# from each numerical metric in a robot scouter JSON export file
def rs_convert(savename):
    extracted_data = dict()
    for (team_num, team_scouts) in json_data['teams'].items():
        # Make sure that there is data for a team
        if len(team_scouts) > 0:
            extracted_data[team_num] = {}
            team_data = defaultdict(list)
            # For each team, create a dictionary of keys corresponding to metric_names and values corresponding
            # to an array of all scouted values for that metric
            for scout in team_scouts:
                for metric in scout['metrics'].values():
                    if type(metric['value']) == int:
                        team_data[metric['name'].strip() + ',' + metric['category']].append(metric['value'])
            # In the extracted_data dictionary, keys are team numbers and values are nested dictionaries
            # Level one is the name of the scouted metric. Level two is name of the calculation type
            # Final value is either min/max/avg of all a team's scouted data for a metric
            for (metric_name, scouted_values) in team_data.items():
                extracted_data[team_num][metric_name] = dict()
                for calculation_type in ['max', 'min']:
                    extracted_data[team_num][metric_name].update(
                        {calculation_type: calculation_map[calculation_type](scouted_values)})
        else:
            continue

    with open(savename, 'w') as fp:
        json.dump(extracted_data, fp)


rs_convert(args.savename)
