from pulp import *
import json

with open('clackams_extracted.json', 'r') as fp:
    scouting_data = json.load(fp)

scoring_locations = ['C_CS', 'C_RL', 'C_RMH', 'P_CS', 'P_RL', 'P_RMH']

# Dictionary associating position names with scouted metric names
locations = dict(C_CS='Cargo in Cargo Ship,Teleop', C_RL='Cargo in low Rocket,Teleop',
                 C_RMH='Cargo in middle/high Rocket,Teleop', P_CS='Panels on Cargo Ship,Teleop',
                 P_RL='Panels on low Rocket,Teleop', P_RMH='Panels on middle/high Rocket,Teleop')


# Util function returning the team number and scoring location of a given position string
def parse_position(position):
    team_num = position.split('-')[0]
    scoring_location = position.split('-')[1]

    return team_num, scoring_location


def create_model(teams):
    # Variable to contain the problem data
    prob = LpProblem("Maximizing Deepspace Scoring Potential", LpMaximize)

    # Creating initial list of scoring positions in format [teamnumber-gamepiece_scoringlocation]
    positions = []
    for scoring_location in scoring_locations:
        for team in teams:
            positions.append('{}-{}'.format(str(team), scoring_location))
    print(positions)

    # Assigning the proper point values to each of the positions
    point_values = {position: 2 if 'P' in position.split('-')[1] else 3 for position in positions}

    # Creating dictionary of positions with keys being original values in positions list and values being
    # the name of the variable in the model
    positions = LpVariable.dicts("position", positions, 0, cat=LpInteger)

    """ 
    =====================================================================================================
                                        OBJECTIVE FUNCTION
    =====================================================================================================
    """
    # Creating the objective function of each position * point value of game piece scored in that position
    prob += lpSum([positions[i] * point_values[i] for i in positions]), "Maximum Game Piece Score"

    """ 
    =====================================================================================================
                                            CONSTRAINTS
    =====================================================================================================
    """

    # Creates constraints based on a team's scouted scoring potential on panels and cargo
    # in the cargo ship, rocket low, and rocket middle high
    for (position, position_model_name) in positions.items():
        # Parse the position string to get the team number and scoring location
        team_num, scoring_location = parse_position(position)

        # Look up the team's scoring potential in a location from the scouting data and add it to the constraints
        prob += lpSum(position_model_name) <= scouting_data[team_num][locations[scoring_location]][
            'max'], 'Team {} scoring potential on {}'.format(team_num, scoring_location)

    # Create constraints based on the total number of panels/cargo on one side of the field
    prob += lpSum(positions[i] for i in positions if 'P' in i) <= 24, "Total Number of Hatch Panels"
    prob += lpSum(positions[i] for i in positions if 'P' not in i) <= 24, "Total Number of Cargo"

    # Create constraints based on available hatches/bays
    prob += lpSum(
        positions[i] for i in positions if 'CS' in i and 'P' in i) <= 8, "Total Number of Hatches on Cargo Ship"
    prob += lpSum(
        positions[i] for i in positions if 'CS' in i and 'P' not in i) <= 8, "Total Number of Bays on Cargo Ship"
    prob += lpSum(
        positions[i] for i in positions if 'RL' in i and 'P' in i) <= 4, "Total Number of Hatches on Low Rockets"
    prob += lpSum(
        positions[i] for i in positions if 'RL' in i and 'P' not in i) <= 4, "Total Number of Bays on Low Rockets"
    prob += lpSum(positions[i] for i in positions if
                  'RMH' in i and 'P' in i) <= 8, "Total Number of Hatches on Middle/High Rockets"
    prob += lpSum(positions[i] for i in positions if
                  'RMH' in i and 'P' not in i) <= 8, "Total Number of Bays on Middle/High Rockets"



    """ 
    =====================================================================================================
                                            SOLVING
    =====================================================================================================
    """

    prob.writeLP('deepspace_optimizer')

    # The problem is solved using PuLP's choice of Solver
    prob.solve()

    # The status of the solution is printed to the screen
    print("Status:", LpStatus[prob.status])

    # Each of the variables is printed with it's resolved optimum value
    for v in prob.variables():
        print(v.name, "=", v.varValue)

    # The optimised objective function value is printed to the screen
    print("MAX", value(prob.objective))


create_model([568, 1359, 1425])
