import argparse
import datetime
import os
from os.path import isfile, join
import shutil
import sys
import time
import xml.etree.ElementTree as ET

#Globals
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
longest_kill_streak = 0
total_weapon_kills = 0
total_grenade_kills = 0
total_melee_kills = 0
total_other_kills = 0
total_double_kills = 0
total_triple_kills = 0
total_headshots = 0
total_killtaculars = 0
total_killing_sprees = 0
total_running_riots = 0
total_grenade_sticks = 0
total_sniper_sprees = 0
total_camo_kills = 0

def getModifiedTimes(mcc_temp_path, fileList, fileModifiedList):
    for file in fileList:
        fileModifiedList.append(time.ctime(os.path.getmtime(mcc_temp_path + "\\" + file)))
        
def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

#Read in config.ini
tag = ''
output_path = ''
track_h1 = True
track_h2 = True

with open('config.ini') as f:
    content = f.readlines()
config = [x.strip() for x in content]
for line in config:
    if 'output_dir=' in line:
        output_path = line[11:].strip()
    if 'gamer_tag=' in line:
        tag = line[10:].strip()
    if 'track_h1=' in line:
        track_h1 = str2bool(line[9:].strip())
    if 'track_h2=' in line:
        track_h2 = str2bool(line[9:].strip())
        
if tag == '' or output_path == '':
    print("Error: Config file not properly set up. Closing in 5 seconds")
    sleep(10)
    sys.exit()

#Do some error correcting/checking with config.ini
if output_path.endswith("\\") == False:
    output_path = output_path + "\\"

try:
    if not os.path.exists(output_path):
        os.makedirs(output_path)
except:
    print("Directory does not exst: " + str(output_path))
    print("Attempted to create one and failed. Please create the directory and restart the applicaton.")
    sleep(60)
    sys.exit()
    
try:
    if not os.path.exists(output_path + "Saved Game Files\\"):
        os.makedirs(output_path + "Saved Game Files\\")
except:
    print("Could not create Saved Game Files directory. Please create it inside: " + str(output_path))
    print("and restart the application.")
    sleep(60)
    sys.exit()

#Get MCC temp path and get initial list of xml files
app_data_path = os.getenv('APPDATA')
mcc_temp_path = app_data_path.replace('Roaming','LocalLow') + r'\MCC\Temporary'
prev_files = [f for f in os.listdir(mcc_temp_path) if (isfile(join(mcc_temp_path, f)) and f.endswith('.xml'))]
prev_files_modified_times = []
getModifiedTimes(mcc_temp_path, prev_files, prev_files_modified_times)

#Zero out for session
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

print("MCC Carnage Reporter v 0.3 beta now running.")
print("Created by CYRiX.")
print("github.com/CYRiXplaysHalo/CarnageReporter")
print("twitch.tv/cyrix")
print("_______________________________________________")
print("")

while(True):
    try:
        files = [f for f in os.listdir(mcc_temp_path) if (isfile(join(mcc_temp_path, f)) and f.endswith('.xml'))]
        files_modified_times = []
        getModifiedTimes(mcc_temp_path, files, files_modified_times)
        file_count = 0
        if prev_files_modified_times != files_modified_times:
            date_time_now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            for file in files:
                if prev_files_modified_times[file_count] != files_modified_times[file_count]:
                        print("New file found at " + date_time_now)
                        try:
                            shutil.copyfile(mcc_temp_path + "\\" + file, output_path + tag + "-" + date_time_now + "-" + file)
                            if 'mpcarnagereport1_1389' in file:
                                root = ET.parse(output_path + tag + "-" + date_time_now + "-" + file).getroot()
                                
                            elif 'mpcarnagereport1_1477' in file:
                                root = ET.parse(output_path + tag + "-" + date_time_now + "-" + file).getroot()

                            else:
                                continue
                                                       
                            if ('mpcarnagereport1_1389' in file and track_h1 == True) or ('mpcarnagereport1_1477' in file and track_h2 == True):
                                if root[4].get('mLastMatchIncomplete') == 'false':
                                    total_game_count += 1
                                    if root[1].get('IsMatchmaking') == 'true':
                                        total_matchmaking_games += 1
                                    else:
                                        total_custom_games += 1

                                    for i in range(0,len(root[10])):
                                        if root[10][i].get('mGamertagText') == tag:
                                            team_id = int(root[10][i].get('mTeamId'))
                                            current_score = int(root[10][i].get('Score'))
                                            total_score += int(root[10][i].get('Score'))
                                            total_kills += int(root[10][i].get('mKills'))
                                            total_deaths += int(root[10][i].get('mDeaths'))
                                            total_assists += int(root[10][i].get('mAssists'))
                                            total_betrayals += int(root[10][i].get('mBetrayals'))
                                            total_suicides += int(root[10][i].get('mSuicides'))
                                            if int(root[10][i].get('mMostKillsInARow')) > longest_kill_streak:
                                                longest_kill_streak = int(root[10][i].get('mMostKillsInARow'))
                                            total_weapon_kills += int(root[10][i].get('mKillsWeapon'))
                                            total_grenade_kills += int(root[10][i].get('mKillsGrenade'))
                                            total_melee_kills += int(root[10][i].get('mKillsMelee'))
                                            total_other_kills += int(root[10][i].get('mKillsOther'))

                                            f = open(output_path + "total_melee_kills.txt", "w")
                                            f.write(str(total_melee_kills))
                                            f.close()
                                            f = open(output_path + "total_games.txt", "w")
                                            f.write(str(total_game_count))
                                            f.close()
                                            f = open(output_path + "total_kills.txt", "w")
                                            f.write(str(total_kills))
                                            f.close()
                                            f = open(output_path + "total_deaths.txt", "w")
                                            f.write(str(total_deaths))
                                            f.close()
                                            f = open(output_path + "total_kdr.txt", "w")
                                            if total_deaths > 0:
                                                f.write(str(round(total_kills/total_deaths,2)))
                                            elif total_deaths == 0 and total_kills == 0:
                                                f.write("")
                                            else:
                                                f.write("∞")
                                            f.close()
                                            f = open(output_path + "total_assists.txt", "w")
                                            f.write(str(total_assists))
                                            f.close()
                                            f = open(output_path + "total_betrayals.txt", "w")
                                            f.write(str(total_betrayals))
                                            f.close()   
                                            f = open(output_path + "total_suicides.txt", "w")
                                            f.write(str(total_suicides))
                                            f.close()
                                            f = open(output_path + "total_weapon_kills.txt", "w")
                                            f.write(str(total_weapon_kills))
                                            f.close()
                                            f = open(output_path + "total_grenade_kills.txt", "w")
                                            f.write(str(total_grenade_kills))
                                            f.close() 

                                    #Assumes there is only ever two teams or ffa.
                                    if root[5].get('IsTeamsEnabled') == 'true':
                                        team_score = 0
                                        opponent_score = 0
                                        for i in range(0,len(root[10])):
                                            if team_id == int(root[10][i].get('mTeamId')):
                                                team_score += int(root[10][i].get('Score'))
                                            else:
                                                opponent_score += int(root[10][i].get('Score'))
                                        if team_score > opponent_score:
                                            total_wins += 1
                                    elif root[5].get('IsTeamsEnabled') == 'false':
                                        best_opp_score = 0
                                        for i in range(0,len(root[10])):
                                            if root[10][i].get('mGamertagText') != tag and best_opp_score < int(root[10][i].get('Score')):
                                                best_opp_score = int(root[10][i].get('Score'))
                                        if best_opp_score < current_score:
                                            total_wins += 1
                                              
                                    f = open(output_path + "win_percentage.txt", "w")
                                    f.write(str('{0:.1%}'.format(total_wins/total_game_count)))
                                    f.close()
                                    f = open(output_path + "total_wins.txt", "w")
                                    f.write(str(total_wins))
                                    f.close()
                                    f = open(output_path + "total_losses.txt", "w")
                                    f.write(str(total_game_count-total_wins))
                                    f.close()
                        except:
                            print("Error saving file.")
                file_count += 1
                    
        prev_files = files
        prev_files_modified_times = files_modified_times
        
        time.sleep(30)
    except:
        print("Unknown Error. Automatically closing in 60 seconds.")
        time.sleep(60)
        sys.exit()
