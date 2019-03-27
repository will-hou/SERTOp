# Util function returning the team number and scoring location of a given position string
def parse_position(position):
    team_num = position.split('-')[0]
    scoring_location = position.split('-')[1]

    return team_num, scoring_location


"""
Given dictionary of scouting data and array of teams, returns True if scouting data suggests that a complete rocket is 
possible.

Parameters:
----------------------------------------------
This parameter may become a dictionary rather than just an int for greater flexibility
max_contribution: the maximum number of game pieces a team can contribute to completing a rocket
TODO: Find recommended value for this parameter
acceptable_deviation: the number of missing game pieces an alliance can have on the rocket but still have it 
considered to be complete 
"""


def evaluate_possible_rocket(scouting_data, teams, max_contribution, acceptable_deviation, verbose=False):
    max_contributions = dict((team, max_contribution) for team in teams)
    position_values = {'P_RL': 0, 'P_RMH': 0, 'C_RL': 0, 'C_RMH': 0}

    # Dictionary containing team numbers as keys. Values are a nested dictionary with keys:
    # ('P_RL, 'C_RL', 'P_RMH', 'C_RMH')containing the scouted maximums
    # for panels, cargo on rocket low and rocket middle/high for both Teleop and Sandstorm
    teams_scouting_data = {}
    for team in teams:
        teams_scouting_data[team] = {}
        teams_scouting_data[team]['P_RL'] = scouting_data[team]['Panels on low Rocket,Teleop']['max'] + \
                                            scouting_data[team][
                                                'Panels on low Rocket,Sandstorm']['max']
        teams_scouting_data[team]['C_RL'] = scouting_data[team]['Cargo in low Rocket,Teleop']['max'] + \
                                            scouting_data[team][
                                                'Cargo in low Rocket,Sandstorm']['max']
        teams_scouting_data[team]['P_RMH'] = scouting_data[team]['Panels on middle/high Rocket,Teleop']['max'] + \
                                             scouting_data[team]['Panels on middle/high Rocket,Sandstorm']['max']
        teams_scouting_data[team]['C_RMH'] = scouting_data[team]['Cargo in middle/high Rocket,Teleop']['max'] + \
                                             scouting_data[team]['Cargo in middle/high Rocket,Sandstorm']['max']

    if verbose:
        print(teams_scouting_data)

    filled_rocket = False
    trial = 1
    # The maximum filled rocket slots from all three trials
    max_rocket_slots = 0
    while filled_rocket is False:
        # The max value for a position as indicated by scouting data
        remaining_potential = teams_scouting_data.copy()
        # How many more game pieces a team can contribute to rocket completion
        remaining_contribution = max_contributions.copy()
        position_values = {'P_RL': 0, 'P_RMH': 0, 'C_RL': 0, 'C_RMH': 0}
        # As long as all the available slots in a position haven't been filled,
        # the team still hasn't contributed more than their allowed contribution,
        # and scoring the game piece still remains possible in respects to their scoring potential,
        # increment the values in the scoring position by 1
        for team in teams:
            while position_values['P_RMH'] < 4 and remaining_potential[team]['P_RMH'] > 0 and remaining_contribution[
                team] > 0:
                position_values['P_RMH'] += 1
                remaining_potential[team]['P_RMH'] -= 1
                remaining_contribution[team] -= 1
            while position_values['C_RMH'] < 4 and remaining_potential[team]['C_RMH'] > 0 and remaining_contribution[
                team] > 0:
                position_values['C_RMH'] += 1
                remaining_potential[team]['C_RMH'] -= 1
                remaining_contribution[team] -= 1
            while position_values['P_RL'] < 2 and remaining_potential[team]['P_RL'] > 0 and remaining_contribution[
                team] > 0:
                position_values['P_RL'] += 1
                remaining_potential[team]['P_RL'] -= 1
                remaining_contribution[team] -= 1
            while position_values['C_RL'] < 2 and remaining_potential[team]['C_RL'] > 0 and remaining_contribution[
                team] > 0:
                position_values['C_RL'] += 1
                remaining_potential[team]['C_RL'] -= 1
                remaining_contribution[team] -= 1

        if verbose:
            print(teams_scouting_data)
            print(trial, teams)
            print(trial, position_values)
            print(trial, remaining_potential)
            print(trial, remaining_contribution)

        filled_rocket_slots = sum([i for i in position_values.values()])

        max_rocket_slots = filled_rocket_slots if filled_rocket_slots > max_rocket_slots else max_rocket_slots

        if trial == 3 and max_rocket_slots >= 12 - acceptable_deviation:
            filled_rocket = True
            break
        # Try and find the max number of rocket slots three times by changing the order rocket slots are calculated
        # (in respects to team)
        elif trial != 3:
            trial += 1
            # First team in list becomes last, last become first, etc.
            teams = teams[-1:] + teams[:-1]
        else:
            filled_rocket = False
            break

    print("The maximum filled rocket slots found was: " + str(max_rocket_slots))
    if filled_rocket:
        print("{} is within the range of the given acceptable deviation of {}".format(
            max_rocket_slots, acceptable_deviation))
        return True
    else:
        return False
