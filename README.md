# CSGO-dynamic-2D-map
Parses live data from your csgo match and recreates it in the 2D view.

The machine we want to parse the data from is required to have a game_state_integrator config pre-installed: 
https://www.reddit.com/r/GlobalOffensive/comments/cjhcpy/game_state_integration_a_very_large_and_indepth/

- data_cleaning.py - cleans inconsistencies in the raw data supplied by the config, so that the data can be represented in the json format
- round_data_to_db.py - after cleaning the data, fetching and putting real-time player coordinates and view angles to the db; putting additional round data to the db, i.e. player names, weapons, nades and their locations 
- round_data_vis.py - visualising the 2D view of the match using timestamps whic the config also supplies

![alt text](https://github.com/GetterGit/CSGO-dynamic-2D-map/blob/main/2d_screenshot.png?raw=true)
