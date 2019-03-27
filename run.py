from create_problem import *
from write import write_to_spreadsheet
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-fcl', '--fromcommandline', help="whether the spreadsheet is being created from the command line",
                    action='store_true')
parser.add_argument('-s', '--sheetname', help="the name of the spreadsheet to write data to")
parser.add_argument('-m', '--matchnumber', help="the qualification match number to get team data from")

args = parser.parse_args()

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

"""
Creating spreadsheets from the command line:

python run.py -fcl -s [spreadsheet name] -m [match_number]
ex.) python run.py -fcl  -s "test.xlsx" -m 3
Creates a spreadsheet called "test.xlsx" for qualification match 3

Importing a schedule:
In the get_teams_from_match function below, change 'schedule.json' to be the name of your match_schedule json

"""

if args.fromcommandline:
    blue_teams, red_teams = get_teams_from_match('schedule.json', args.matchnumber)

    create_match_spreadsheet(datafile='clackams_extracted.json', sheetname=args.sheetname, match_num=args.matchnumber,
                             blue_teams=blue_teams, red_teams=red_teams,
                             blue_null_panels='optimal', red_null_panels='optimal', optimize_rocket='auto')
else:
    create_match_spreadsheet(datafile='clackams_extracted.json', sheetname='clackams_QF1.xlsx', match_num=1,
                             blue_teams=['3674', '3673', '3636'], red_teams=['2521', '5085', '1359'],
                             blue_null_panels='optimal', red_null_panels='optimal', optimize_rocket='auto')
