# CarnageReporter

![Image of Carnage Reporter stream overlay](https://raw.githubusercontent.com/CYRiXplaysHalo/CarnageReporter/master/image.png)

### What is Carnage Reporter?

This is currently a simple python script that will save off your Halo 1 MCC PC carnage report files into a non-temporary directory to preserve them since the game simply overwrites this file in its temporary directory after a new game is completed. Doing this allows you to have in-game session level stats for your stream as well as help report Halo 1 MCC PC stats to halo1hub.com where there will (eventually) be more in-depth stats than what you can get on Halo Waypoint.

### I don't stream, why should I still use this?

With this application we can create a database of in-depth stats for each game that will allow us to better understand Halo 1 MCC PC. So in addition to being able to track yourself throughout your career on MCC PC, we can better understand trends in the game itself like: what exactly is the distribution of maps selected for each playlist? are the maps balanced? are the maps balanced any different than OG? Additionally, as long as one person per game submits stats, we will be able to record stats for all players in that game.

### How does it work?

Halo 1 MCC PC generates an XML file after each multiplayer game. These files give you every statistic and medal for each player and team. This script simply monitors the folder this file is created in, and copies it over to another folder where we can save it off, use it for streams and send it to halo1hub.com

### How do I install it?

While the code is open source, in order to submit stats to halo1hub.com you must use the compiled release version. 

### How do I configure it to work on my machine?

You must edit the config.ini file that comes with the release, and edit the "output_dir" and "gamer_tag" values to point to an output folder you want it to use and the gamertag you use to log on and play. Without the values being set properly, the application will not work.
