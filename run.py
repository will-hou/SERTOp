from create_problem import *
from write import write_to_spreadsheet
import argparse

# TODO: Implement argparse and create spreadsheets from just match number
"""
Main function to create a spreadsheet of optimum position values

Parameters:
--------------------------------------------------------
datafile: str = the JSON file containing the formatted RS data
sheetname: str = the spreadsheet to write data to ex.) 'Q1_Optimized.xlsx'
match_num: int = the match number to write to the spreadsheet
blue teams: list = list of team strings on the blue alliance ex.) ['2521', '254', '2471']
red teams: list = list of team strings on the red alliance
blue_null_panels: string or int = Number of null panels used in the constraints to calculate optimal score
                                 default='optimal' automatically uses value that results in the greatest optimal score
red_null_panels: string or int = same as blue_null_panels but for red teams
optimize_rocket: string or boolean = whether to force the lp problem creator to ensure a rocket in constraints instead of
                                 calculating its feasibility. Default: 'auto' 
                                 WARNING: CAN LEAD TO AN IMPOSSIBLE SOLUTION.
"""


def create_match_spreadsheet(datafile, sheetname, match_num, blue_teams, red_teams, blue_null_panels='optimal',
                             red_null_panels='optimal', optimize_rocket='auto'):
    b_optimal_positions = find_optimal_null(datafile, blue_teams,
                                            optimize_rocket) if blue_null_panels == 'optimal' else create_problem(
        datafile, blue_teams,
        blue_null_panels, optimize_rocket)
    r_optimal_positions = find_optimal_null(datafile, red_teams,
                                            optimize_rocket) if red_null_panels == 'optimal' else create_problem(
        datafile, red_teams,
        red_null_panels, optimize_rocket)

    write_to_spreadsheet(b_optimal_positions, 'default', sheetname, match_num, 'blue')
    write_to_spreadsheet(r_optimal_positions, sheetname, sheetname, match_num, 'red')

    print("Blue teams: {}      Red teams: {}".format(blue_teams, red_teams))
    print("Created {} for match {}".format(sheetname, match_num))


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                        PLEASE DON'T TOUCH ANYTHING ABOVE THIS LINE
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

create_match_spreadsheet(datafile='clackams_extracted.json', sheetname='clackams_QF1.xlsx', match_num=1,
                         blue_teams=['3674', '3673', '3636'], red_teams=['2521', '5085', '1359'],
                         blue_null_panels='optimal', red_null_panels='optimal', optimize_rocket='auto')
