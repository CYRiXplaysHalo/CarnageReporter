# MCC Carnage Reporter created by CYRiX github.com/CYRiXplaysHalo/CarnageReporter twitch.tv/cyrix - Forked (Updated) and commented by ICoN 6iX (Tested for Halo CE only)

#exe made with py2exe as pyinstaller had issues, I belive due to temp file useage so complied it this way

# The folder should contain:
# * Folder with the exe in the other files just make the exe run
# * EXE file it self - what you press to run
# * Script source - if you want to see how it is made and make tweaks to it (Halo_MCC_Stat_Tracker.py file)
# * Readme file
# * Stats folder - created on first time running and checks for it on everyrun
# * Saved games folder inside of Stats folder - created on first time running and checks for it on everyrun
# * Config.ini - created on first time running and checks for it on everyrun
# * Inside of Stats folder once the script is run the text files for Twitch are created here

# Import all the modules/ libraries
import argparse
import datetime
import glob #If there are files for to delete
import shutil #Copy and paste files
import sys
import time #Pause between actions
import xml.etree.ElementTree as ET #Get data from the XML files
import os
from os import system
from os.path import isfile, join


def cls(): return system('cls')  # Used to clear the screen

print("MCC Carnage Reporter created by CYRiX - Updated by ICoN 6iX")
print("Version 0.8")
time.sleep(2)
cls()

def print_inventory(dct): #Used to print gamertags later as a case/ switch
    for item, amount in dct.items():
        print("{},  {}".format(item, amount))

# determine if application is a script file or frozen exe - if its an exe it needs to find the current directory a different way is all
# Finds the directory which you run this script from and saves it as a variable
if getattr(sys, 'frozen', False):
    dir_path = os.path.dirname(sys.executable)
elif __file__:
    dir_path = str(os.path.dirname(os.path.realpath(__file__)))

# Check if the config file is created, if not creates it and ask for user input for the gamertag
if not os.path.exists(dir_path + "\\" + "config.ini"):
    open("config.ini", "x")  # Creates the a blank file called config.ini
    print("Creating new config\n")  # Let the user know what is happening
    time.sleep(2)

    # Get user input and write to config.ini
    tag = input("Enter gamertag which you want to collect stats for: ").lower().strip()
    f = open(dir_path + "\\" + "config.ini", "w")
    # Adds gamertag to the config so its clear as to what it saves
    f.write("gamertag: " + str(tag))
    print("Loading...")
    time.sleep(3)  # Added encase it wrote to the file slow for some reason
    f.close
    f = open(dir_path + "\\" + "config.ini", "r")
    # Reading the file acts to notify the user of the gamertag used and updates the file, without this the file would not update
    print("\nStats will be collected for " + f.read())
    time.sleep(3)

# If config exits it grabs the gamertag from the file and stores it in a variable
else:
    if not os.stat(dir_path + "\\" + "config.ini").st_size == 0:
        c = open(dir_path + "\\" + "config.ini")
        content = c.readlines()
        config = [x.strip() for x in content]
        for line in config:
            if 'gamertag: ' in line:
                # Opens the file and finds gamertag and then gets the info following that, the gamertag itself
                tag = line[10:].strip()

                # Check with user if gamertag is correct or if they want to change it
                # If its anything other then y keep the original gamertag
                if input("Current gamertag = " + tag + "\nDo you want to make a change (Y/N)? ").lower().strip()[:1] != "y":
                    print("Stats will be collected for gamertag: " + tag)
                    time.sleep(3)

                else:
                    # If y was pressed, get user input and write to config.ini
                    tag = input(
                        "Enter gamertag which you want to collect stats for: ").lower().strip()
                    f = open(dir_path + "\\" + "config.ini", "w")
                    f.write("gamertag: " + str(tag))
                    print("Loading...")
                    time.sleep(3)
                    f.close
                    f = open(dir_path + "\\" + "config.ini", "r")
                    print("\nStats will be collected for " + f.read())
                    time.sleep(3)

    else:
        tag = input("Enter gamertag which you want to collect stats for: ").lower().strip()
        f = open(dir_path + "\\" + "config.ini", "w")
        f.write("gamertag: " + str(tag))
        print("Loading...")
        time.sleep(3)
        f.close
        f = open(dir_path + "\\" + "config.ini", "r")
        print("\nStats will be collected for " + f.read())
        time.sleep(3)

# Where stats will be updated - checks if it exist and if not creates it
output_path = dir_path + "\\" + "Stats\\"
if not os.path.exists(output_path):
    os.makedirs(output_path)
    time.sleep(2)

# Where saved game files will be saved - checks if it exist and if not creates it
saved = output_path + "Saved Game Files\\"
if not os.path.exists(saved):
    os.makedirs(saved)
    time.sleep(2)

# Globals
total_game_count = 0
total_wins = 0
total_matchmaking_games = 0
total_custom_games = 0
total_finished_games = 0
gametype_count = []
total_score = 0
total_kills = 0
total_deaths = 0
total_assists = 0
total_betrayals = 0
total_suicides = 0
longest_kill_streak = 0  # This is broke inside of MCC as of season 6
total_weapon_kills = 0
total_grenade_kills = 0
total_melee_kills = 0
total_other_kills = 0
total_double_kills = 0
total_triple_kills = 0
total_killtaculars = 0
total_killing_sprees = 0
total_running_riots = 0
total_sniper_sprees = 0
total_camo_kills = 0

# Medals
total_grenade_sticks = 0
total_headshots = 0

# More medals can be added you just need to work out the medal id and what it corresponds to, more on this later in this script


def getModifiedTimes(mcc_temp_path, fileList, fileModifiedList):
    for file in fileList:
        fileModifiedList.append(time.ctime(
            os.path.getmtime(mcc_temp_path + "\\" + file)))


# Get MCC temp path and get initial list of xml files, not any other files/ folders
# App data is found where ever your users folder is
app_data_path = os.getenv('APPDATA')
# Eg C:\Users\WindowsUserNameGoesHere\AppData - this folder is hidden by default if you wanted to look for it in explore (go to explore, view ribbon and tick hidden items if you want to see these files)
mcc_temp_path = app_data_path.replace(
    'Roaming', 'LocalLow') + r'\MCC\Temporary'
prev_files = [f for f in os.listdir(mcc_temp_path) if (
    isfile(join(mcc_temp_path, f)) and f.endswith('.xml'))]
prev_files_modified_times = []
getModifiedTimes(mcc_temp_path, prev_files, prev_files_modified_times)

# Lastest MCC file - on updates to the game eg seasons this could update so this finds the latest version to use, so to future proof it
list_of_files = glob.glob(mcc_temp_path + '/*.xml')
mcc_max = max(list_of_files, key=os.path.getctime)
latest_mcc = mcc_max[-29:]

# Creates text files where stats will be saved and zero's them out for session start aka when you start your stream they will start all at zero and increment as you play
# W at the end creates a file also x can be used to do the same
f = open(output_path + "total_games.txt", "w")
f.write(str(0))
f.close()
f = open(output_path + "total_kills.txt", "w")
f.write(str(0))
f.close()
f = open(output_path + "total_deaths.txt", "w")
f.write(str(0))
f.close()
f = open(output_path + "total_kdr.txt", "w")
f.write(str(0))
f.close()
f = open(output_path + "total_assists.txt", "w")
f.write(str(0))
f.close()
f = open(output_path + "total_betrayals.txt", "w")
f.write(str(0))
f.close()
f = open(output_path + "total_suicides.txt", "w")
f.write(str(0))
f.close()
f = open(output_path + "total_weapon_kills.txt", "w")
f.write(str(0))
f.close()
f = open(output_path + "win_percentage.txt", "w")
f.write(str('{0:.0%}'.format(1)))
f.close()
f = open(output_path + "total_melee_kills.txt", "w")
f.write(str(0))
f.close()
f = open(output_path + "total_wins.txt", "w")
f.write(str(0))
f.close()
f = open(output_path + "total_losses.txt", "w")
f.write(str(0))
f.close()
f = open(output_path + "total_grenade_sticks.txt", "w")
f.write(str(0))
f.close()
f = open(output_path + "total_headshots.txt", "w")
f.write(str(0))
f.close()

# Checks if you want to delete the contents of saved games folder as this folder can get big fast
old = glob.glob(saved + '/*', recursive=True)

files_deleted = False

if input("Clear old save games files (Y/ N)? ").lower().strip()[:1] != "y":
    print("Keep old saved game files")
    time.sleep(3)
    print("\nAfter a Halo game is complete stats will be updated, if this program is running")
    print("To reset the stat counters to zero, you must restart this program")
    time.sleep(5)
    cls()
    print("Session started " +
          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' - ' + tag
          + "\nWaiting for game stats...")

else:
    if os.listdir(saved) == []:
        print("No saved games files to delete")
        time.sleep(3)
        print("\nAfter a Halo game is complete stats will be updated, if this program is running")
        print("To reset the stat counters to zero, you must restart this program")
        time.sleep(5)
        cls()
        print("Session started " +
              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' - ' + tag
              + "\nWaiting for game stats...")
    else:
        for o in old:
            try:
                os.remove(o)
                print("Deleteing files please wait")
                files_deleted = True

            except OSError as e:
                print("Error: %s : %s" % (f, e.strerror))

if files_deleted == True:
    print("All old saved games files deleted")
    time.sleep(3)
    print("\nAfter a Halo game is complete stats will be updated, if this program is running")
    print("To reset the stat counters to zero, you must restart this program")
    time.sleep(7)
    cls()

    print("Session started " +
          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' - ' + tag
          + "\nWaiting for game stats...")

# Copies the latest Halo stats xml to stats folder and updates the indivual text files with last game info
while(True):
    try:
        files = [f for f in os.listdir(mcc_temp_path) if (
            isfile(join(mcc_temp_path, f)) and f.endswith('.xml'))]
        files_modified_times = []
        getModifiedTimes(mcc_temp_path, files, files_modified_times)
        file_count = 0
        if prev_files_modified_times != files_modified_times:
            date_time_now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            for file in files:
                if prev_files_modified_times[file_count] != files_modified_times[file_count]:
                    print("\nNew saved gamefile found " + date_time_now)

                    try:
                        shutil.copyfile(
                            mcc_temp_path + "\\" + file, saved + tag + "-" + date_time_now + "-" + file)
                        if latest_mcc in file:
                            root = ET.parse(
                                saved + tag + "-" + date_time_now + "-" + file).getroot()

                        else:
                            continue

                        # Checks the xml file from the last game and gets the information
                        if latest_mcc in file:
                            # root[4] in the xml is the 5th key inside of the xml carnage report, line 8
                            if root[4].get('mLastMatchIncomplete') == 'false':
                                total_game_count += 1
                                if root[1].get('IsMatchmaking') == 'true':
                                    total_matchmaking_games += 1
                                else:
                                    total_custom_games += 1

                            #If gamertag does not match any from the record game it will check with you if you want to change it to someone in the last game
                            gamertags = []

                            for d in range(0, len(root[10])):
                                gamertags.append(root[10][d].get('mGamertagText').lower())

                            if tag not in gamertags:
                                print("\nCurrent gamertag: " + tag + " - not found in last game\n")

                                gtag_nums = []
                                for x in range(len(gamertags)):
                                    gtag_nums.append(x)

                                switch = {}
                                for value in gtag_nums:
                                    for tags in gamertags:
                                        switch[value] = tags
                                        gamertags.remove(tags)
                                        break

                                print_inventory(switch)

                                gt_choice = int(input("\nPlease pick a gamertag from the list above using the corrensponding number: "))
                                while gt_choice not in gtag_nums:
                                    cls()
                                    print("Incorrect value entered, please try again")
                                    print_inventory(switch)
                                    gt_choice = int(input("\nPlease pick a gamertag from the list above using the corrensponding number: "))
                                    continue

                                else:
                                    tag = str(switch[gt_choice]).lower().strip()
                                    f = open(dir_path + "\\" + "config.ini", "w")
                                    f.write("gamertag: " + str(tag))
                                    print("Loading...")
                                    time.sleep(3)  # Added encase it wrote to the file slow for some reason
                                    f.close
                                    f = open(dir_path + "\\" + "config.ini", "r")
                                    # Reading the file acts to notify the user of the gamertag used and updates the file, without this the file would not update
                                    print("\nStats will be collected for " + f.read())
                                    time.sleep(5)
                                    cls()

                            # This interates through root[10] players key and if it finds aka .get it stores the info to a variable
                            for i in range(0, len(root[10])):
                                if root[10][i].get('mGamertagText').lower() == tag:
                                    team_id = int(
                                        root[10][i].get('mTeamId'))
                                    current_score = int(
                                        root[10][i].get('Score'))
                                    total_score += int(root[10]
                                                        [i].get('Score'))
                                    total_kills += int(root[10]
                                                        [i].get('mKills'))
                                    total_deaths += int(root[10]
                                                        [i].get('mDeaths'))
                                    total_assists += int(root[10]
                                                            [i].get('mAssists'))
                                    total_betrayals += int(
                                        root[10][i].get('mBetrayals'))
                                    total_suicides += int(root[10]
                                                            [i].get('mSuicides'))
                                    # broke in mcc itself - as of season 6
                                    if int(root[10][i].get('mMostKillsInARow')) > longest_kill_streak:
                                        longest_kill_streak = int(
                                            root[10][i].get('mMostKillsInARow'))
                                    total_weapon_kills += int(
                                        root[10][i].get('mKillsWeapon'))
                                    total_grenade_kills += int(
                                        root[10][i].get('mKillsGrenade'))
                                    total_melee_kills += int(
                                        root[10][i].get('mKillsMelee'))
                                    total_other_kills += int(
                                        root[10][i].get('mKillsOther'))

                                    # Medals info requires going deeper into the file
                                    medals = []

                                    for child in root[10][i].find('.//MedalsCount'):
                                        medals.append(child.attrib)

                                    # From the xml <Medal mId="115" mCount="8"/>  medal id 115 = headshots, medal count 8 means you got 8 headshots
                                    total_grenade_sticks += int(
                                        medals[115].get('mCount'))

                                    # You can add more medals this way just need to work out by playing to find out which ones are which
                                    total_headshots += int(
                                        medals[111].get('mCount'))

                                    # Writes medal info to stat text files which OBS/ Streamlabs read and display
                                    f = open(
                                        output_path + "total_grenade_sticks.txt", "w")
                                    f.write(str(total_grenade_sticks))
                                    f.close()
                                    f = open(output_path +
                                                "total_headshots.txt", "w")
                                    f.write(str(total_headshots))
                                    f.close()

                                    # Writes all none medals in the same fashion
                                    f = open(output_path +
                                                "total_melee_kills.txt", "w")
                                    f.write(str(total_melee_kills))
                                    f.close()
                                    f = open(output_path +
                                                "total_games.txt", "w")
                                    f.write(str(total_game_count))
                                    f.close()
                                    f = open(output_path +
                                                "total_kills.txt", "w")
                                    f.write(str(total_kills))
                                    f.close()
                                    f = open(output_path +
                                                "total_deaths.txt", "w")
                                    f.write(str(total_deaths))
                                    f.close()
                                    f = open(output_path +
                                                "total_kdr.txt", "w")
                                    if total_deaths > 0:
                                        f.write(
                                            str(round(total_kills/total_deaths, 2)))
                                    elif total_deaths == 0 and total_kills == 0:
                                        f.write("")
                                    else:
                                        f.write("∞")
                                    f.close()
                                    f = open(output_path +
                                                "total_assists.txt", "w")
                                    f.write(str(total_assists))
                                    f.close()
                                    f = open(output_path +
                                                "total_betrayals.txt", "w")
                                    f.write(str(total_betrayals))
                                    f.close()
                                    f = open(output_path +
                                                "total_suicides.txt", "w")
                                    f.write(str(total_suicides))
                                    f.close()
                                    f = open(output_path +
                                                "total_weapon_kills.txt", "w")
                                    f.write(str(total_weapon_kills))
                                    f.close()

                                    f = open(
                                        output_path + "total_grenade_kills.txt", "w")
                                    f.write(str(total_grenade_kills))
                                    f.close()

                            # Assumes there is only ever two teams or ffa.
                            if root[5].get('IsTeamsEnabled') == 'true':
                                team_score = 0
                                opponent_score = 0
                                for i in range(0, len(root[10])):
                                    if team_id == int(root[10][i].get('mTeamId')):
                                        team_score += int(root[10]
                                                            [i].get('Score'))
                                    else:
                                        opponent_score += int(
                                            root[10][i].get('Score'))
                                if team_score > opponent_score:
                                    total_wins += 1
                            elif root[5].get('IsTeamsEnabled') == 'false':
                                best_opp_score = 0
                                for i in range(0, len(root[10])):
                                    if root[10][i].get('mGamertagText') != tag and best_opp_score < int(root[10][i].get('Score')):
                                        best_opp_score = int(
                                            root[10][i].get('Score'))
                                if best_opp_score < current_score:
                                    total_wins += 1

                            f = open(output_path +
                                        "win_percentage.txt", "w")
                            f.write(str('{0:.1%}'.format(
                                total_wins/total_game_count)))
                            f.close()
                            f = open(output_path + "total_wins.txt", "w")
                            f.write(str(total_wins))
                            f.close()
                            f = open(output_path + "total_losses.txt", "w")
                            f.write(str(total_game_count-total_wins))
                            f.close()

                            # Prints stats in the python itself, just so you can see it is working
                            if team_id == 0:
                                team = "Red Team: "
                            else:
                                team = "Blue Team: "

                            if team_id == 1:
                                op_team = " Red Team: "
                            else:
                                op_team = " Blue Team: "

                            print("\nLast Game Played - " +
                                    root[8].get('GameTypeName'))

                            if int(team_score) > int(opponent_score):
                                print("You won :D\n")
                            elif int(team_score) == int(opponent_score):
                                print("Draw game :|\n")
                            else:
                                print("You lost :(\n")

                            for x in range(0, len(root[10])):
                                if root[10][x].get('mGamertagText').lower() == tag:

                                    print(team + str(team_score) +
                                            op_team + str(opponent_score))
                                    print("Score: " +
                                            str(root[10][x].get('Score')))

                                    if int(root[10][x].get('mDeaths')) > 0 and int(root[10][x].get('mKills')) > 0:
                                        print(
                                            "KD: " + str(round(int(root[10][x].get('mKills')) / int(root[10][x].get('mDeaths')), 2)))
                                    else:
                                        print("")
                                    print("Kills: " +
                                            str(root[10][x].get('mKills')))
                                    print("Deaths: " +
                                            str(root[10][x].get('mDeaths')))
                                    print("Assists: " +
                                            str(root[10][x].get('mAssists')))
                                    print("Stickies: " +
                                            str(medals[115].get('mCount')))
                                    print("Headshots: " +
                                            str(medals[111].get('mCount')))

                                    # Overall stats are just accumulated from start of session
                                    print("\nOveral Stats")
                                    if total_deaths > 0 and total_kills > 0:
                                        print(
                                            "KD: " + str(round(total_kills / total_deaths, 2)))
                                    else:
                                        print("")
                                    print("Kills: " + str(total_kills))
                                    print("Deaths: " + str(total_deaths))
                                    print("Assists: " + str(total_assists))
                                    print("Wins: " + str(total_wins))
                                    print("Losses: " +
                                            str(total_game_count-total_wins))
                                    print("Stickies: " +
                                            str(total_grenade_sticks))
                                    print("Headshots: " +
                                            str(total_headshots))
                                    print("\nWaiting for next game stats...")

                    except:
                        print("Error saving file - check gamertag is correct")
                        time.sleep(10)
                        sys.exit()

                file_count += 1

        prev_files = files
        prev_files_modified_times = files_modified_times

        time.sleep(30)
    except:
        print("Unknown Error. Automatically closing in 10 seconds.")
        time.sleep(10)
        sys.exit()
