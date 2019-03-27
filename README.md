# SERT DeepSpace Scoring Optimizer
[![Team 2521][team-img]][team-url]

[team-img]: https://img.shields.io/badge/team-2521-7d26cd.svg?style=flat-square
[team-url]: https://sert2521.org

### Inspired by this [presentation](https://www.chiefdelphi.com/t/score-optimization-with-linear-programming/351314) created by FRC team 8 (Paly Robotics)

### Create beautiful spreadsheets to optimize scoring in DeepSpace with scouting data collected with [Robot Scouter](https://github.com/SUPERCILEX/Robot-Scouter)

![Score Optimization Template Spreadsheet](https://user-images.githubusercontent.com/23201789/55105011-c1e07d80-5088-11e9-84f1-e0c5e7f50705.png)

## Usage

Make sure Python is installed on your computer and use `pip install -r requirements.txt` to install the needed packages

### Preparing Scouting Data
The optimizer can only work with [Robot Scouter](https://github.com/SUPERCILEX/Robot-Scouter) data in a specific format
#### Using rs_extract to prepare Robot Scouter JSON files:
1. In the program directory, enter and run `python rs_extract.py -s [savename]` where the name of the file you want the formatted data saved to goes in the place of the brackets
   ex. `python rs_extract.py -s event_scouts.json`
2. A file selector with pop up on the screen. Select the Robot Scouter JSON export file that you want to reformat
3. The program will reformat the file and save it to the file you specified in the command line. You're ready for the fun part!


### Creating the Spreadsheet

Kinda hard to use for now... will be improved soon!

1. Use any text editor/IDE of your choice and access the run.py file
2. Below the 'Do Not Touch' line, modify the parameters in the create_match_spreadsheet function to suit your needs. Read the green text at the top of the file for help interpreting the parameter names. The existing parameters inside the function can help serve as a guide for what to do.
3. In the command line, enter and run `python run.py`
4. The program will find the optimal score for your alliance based on the given scouting data and values will be written to an excel spreadsheet of the name specified in the `sheetname` parameter


### Happy Optimizing! :D

#### Note
This program is highly experimental and was designed specifically for usage by SERT(2521).

Although teams/individuals interested in this program are more than welcome to use it, many features are not optimized (haha) for general usability. Additionally, reliability of the program is also not guaranteed -- extensive testing has not been performed and small bugs are likely to exist.

That being said, please feel free to submit an issue if bugs are found, you have suggestons, or if you would like some assistance!
