from pulp import *
import json

with open('clackams_extracted.json', 'r') as fp:
    scouting_data = json.load(fp)

scoring_locations = ['C_CS', 'C_RL', 'C_RMH', 'P_CS', 'P_RL', 'P_RMH']

locations = dict(C_CS='Cargo in Cargo Ship,Teleop', C_RL='Cargo in low Rocket,Teleop',
                 C_RMH='Cargo in middle/high Rocket,Teleop, Teleop', P_CS='Panels on Cargo Ship,Teleop',
                 P_RL='Panels on low Rocket,Teleop', P_RMH='Panels on middle/high Rocket,Teleop')


def create_model(teams):
    # Variable to contain the problem data
    prob = LpProblem("Maximizing Deepspace Scoring Potential", LpMaximize)

    positions = []
    for scoring_location in scoring_locations:
        for team in teams:
            positions.append('{}-{}'.format(str(team), scoring_location))
    print(positions)

    point_values = {position: 2 if 'P' in position.split('-')[1] else 3 for position in positions}

    positions = LpVariable.dicts("position", positions, 0)
    print(positions)


create_model([568, 1359, 1425])
