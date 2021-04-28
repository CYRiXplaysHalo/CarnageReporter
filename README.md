# Carnage Reporter by CYRiX - Updated by ICoN 6iX

![Image of Carnage Reporter stream overlay](https://raw.githubusercontent.com/CYRiXplaysHalo/CarnageReporter/b755295ff99c067f6ac80f18b0a4116294b6d5a1/image.png)

## Download and use just - Halo MCC Stat Tracker.exe

### Changes from original

* All the information needed to run is collected from the user directly or from the app itself
* Creates all folders needed itself
* Checks with the user if they want to delete old game saves
* Checks correct gamertag is used
* Saves some medal data
* Does not save stats to halo1hub
* Stats show on the app itself
* Improved ux

### Stat tracker

Run the .exe or if you want to run it from source you need to have python install and then just double click or open and run module (you can download python from the windows store)

When it runs it will ask prompt you for input, and the app will tell you what to press aka 'y' key or 'n' key, enter a gamertag or enter a number. After adding your response to any question press 'Enter' to confirm
 
Now play a game and the tracker will show you the last game stats and overall stats
if you play another the overal stats will update to be an total of the last two games and any following games

In the stats folder after a game is complete the indiviual stats text files will update if you have got, say some kills

### Using this with OBS/ Streamlabs 

Add a new source as text file, find Stats Tracker folder and then stats folder
In here you will see all the stats, eg total_kills.txt

open this and move the text on obs where you want it, and maybe add other text source to say total kills or an custom image which can sit below this

If you have a two PC setup to and want to use this you run this on the gaming PC and then on the stream PC either have it networked and look for these files
Or use Google drive app which you can setup to look at the stats folder and this again is what OBS/ Streamlabs will look for, just these text files 
