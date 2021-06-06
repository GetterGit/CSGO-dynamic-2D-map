import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Used to convert Dataset positions to positions on the radar
def pointx_to_resolutionx(xinput, startX=-2486, endX=2127, resX=1024):
    sizeX=endX-startX
    if startX<0:
        xinput+=startX *(-1.0)
    else:
        xinput+=startX
    xoutput=float((xinput/abs(sizeX))*resX)
    return xoutput

def pointy_to_resolutiony(yinput, startY=-1150, endY=3455, resY=1024):
    sizeY=endY-startY
    if startY<0:
        yinput+=startY*(-1.0)
    else:
        yinput+=startY
    youtput=float((yinput/abs(sizeY))*resY)
    return resY-youtput



#importing the map image and declaring its dimensions
im=plt.imread('dust2.png')
plt.figure(figsize=(20,20))
twod_map=plt.imshow(im)

#Importing the data from csv
data_teams=pd.read_csv(r'round_data_full_csv/Teams.csv')
data_players=pd.read_csv(r'round_data_full_csv/Players.csv')
data_grenades=pd.read_csv(r'round_data_full_csv/Grenades.csv')
data_weapons=pd.read_csv(r'round_data_full_csv/Weapons.csv')
data_matches=pd.read_csv(r'round_data_full_csv/Matches.csv')
data_scattering=pd.read_csv(r'round_data_full_csv/Scattering.csv')

#Joining Matches and Players by player_id
df_matches_players=data_matches.join(data_players.set_index('id'), on='player_id', how='left')

#Converting the positional data to radar positions
df_matches_players['player_mapX'] = df_matches_players['posX'].apply(pointx_to_resolutionx)
df_matches_players['player_mapY'] = df_matches_players['posY'].apply(pointy_to_resolutiony)

#Converting the directions data to radar directions with the crosshair in the middle
df_matches_players['player_dirX']=df_matches_players['dirX'].apply(pointx_to_resolutionx)
df_matches_players['player_dirY']=df_matches_players['dirY'].apply(pointy_to_resolutiony)

#reshaping df_matches_players to entail only 1 player state per 1 timestamp instead of current 3 player states per 1 timestamp
#filtering out (player_id + timestamp) duplicates 
df_matches_players=df_matches_players.drop_duplicates(subset=['player_id','timestamp'])
#J!!!UST FOR THIS MATCH: filtering out player_id=16873 cuz he swapped the teams during the round
df_matches_players=df_matches_players[df_matches_players['player_id'] != 16873]



#Joining Scattering and Players by player_id, joining Scattering and Grenades by grenade_id
df_scattering_joint=data_scattering.join(data_players.set_index('id'), on='player_id', how='left')
df_scattering_joint=df_scattering_joint.join(data_grenades.set_index('id'), on='grenade_id', how='left')

#Converting the nades positional data to radar positions
df_scattering_joint['nade_mapX'] = df_scattering_joint['posX'].apply(pointx_to_resolutionx)
df_scattering_joint['nade_mapY'] = df_scattering_joint['posY'].apply(pointy_to_resolutiony)

#reshaping df_scattering_joint to entail only 1 grenade state per 1 timestamp instead of current 3 grenade states per 1 timestamp
df_scattering_joint=df_scattering_joint.drop_duplicates(subset=['grenade_id', 'player_id', 'timestamp'])



#creating the lists of player_ids to then print the map per player per team
#then creating a list of timestamps to make the dynamic 2D map
tuples=[tuple(x) for x in df_matches_players.values]
lst_ct=list()
lst_t=list()
lst_times=list()

for t in tuples:
    if t[3] in lst_ct:
        continue
    elif t[3] in lst_t:
        continue
    else:
        if 'CT' in t:
            lst_ct.append(t[3])
        else:
            lst_t.append(t[3])
            
for t in tuples:
    if t[18] in lst_times:
        continue
    else:
        lst_times.append(t[18])



#creating script to identify Who killed Who and When
state_df=df_matches_players
deaths=list()
kills=list()
times=list()

#the order of appending the lists is equal to the order of kills in the round which gives me an opportunity to match the list elements by their numbers in the lists so that deaths[0]:kills[0] etc.]
for player in state_df.values:
    if player[10]==0:
        killed=player[32]
        state_d=state_df[state_df['player_id'] != player[3]]
        if killed not in deaths:
            deaths.append(killed)
            times.append(player[18])
    kills_num=player[15]
    state_prev_df=state_df[state_df.timestamp==player[18]-1]
    for player_prev in state_prev_df.values:
        if player_prev[3]==player[3]:
            kills_prev=player_prev[15]
            if kills_prev<kills_num:
                killer=player[32]
                kills.append(killer)

del kills[3] #deleting a kill made on a player who I deleted becacuse he changed the teams - gotta be more careful next time
deathnote=list(zip(deaths, kills, times)) #getting the dict where each key (killed player) has a value of the killer  

#printint Who killed Who and When
for note in deathnote:
    print(note[1], ' killed ', note[0], ' at ', note[2])



#printing the dynamic 2D map, timestamp by timestamp
for time_num in lst_times: 
    
    #creating df's for specific time_num + !!! round_id=6 for the sake of the demo when required
    ct_df=df_matches_players[(df_matches_players.team_id=='CT') & (df_matches_players.timestamp==time_num)]
    t_df=df_matches_players[(df_matches_players.team_id=='T') & (df_matches_players.timestamp==time_num)]
   
    #printing the empty map
    plt.figure(figsize=(20,20))
    twod_map=plt.imshow(im)
    plt.title(time_num)
   
    #printing ct movement + accouting for killed ct's by renewing ct_df of a given time_num
    for ct in ct_df.values:
        if ct[10]==0:
            ct_df_killed=ct_df[ct_df['player_id'] == ct[3]]
            twod_map=plt.scatter(ct_df_killed['player_mapX'], ct_df_killed['player_mapY'], s=300, marker='x', alpha=1, c='blue') 
            plt.annotate(ct[32], (ct_df_killed['player_mapX'], ct_df_killed['player_mapY']), c='white') #annotating a name of the killed player           
            ct_df=ct_df[ct_df['player_id'] != ct[3]] #updating ct_df for this time_num to excluded the killed player
            
        #doing else to annotate the player's name if he is still alive
        else:
            ct_df_annotate=ct_df[ct_df['player_id'] == ct[3]]
            plt.annotate(ct[32], (ct_df_annotate['player_mapX'], ct_df_annotate['player_mapY']), c='white')
            
        #printing the ct directions adjusted to the resolution
        print(time_num, ct[32], ct[36], ct[37])
        
    twod_map=plt.scatter(ct_df['player_mapX'], ct_df['player_mapY'], s=300, alpha=1, c='blue')
    
    #printing ct movement + accouting for killed t's t_df of a given time_num
    for t in t_df.values:
        if t[10]==0:
            t_df_killed=t_df[t_df['player_id'] == t[3]]
            twod_map=plt.scatter(t_df_killed['player_mapX'], t_df_killed['player_mapY'], s=300, marker='x', alpha=1, c='yellow') 
            plt.annotate(t[32], (t_df_killed['player_mapX'], t_df_killed['player_mapY']), c='white') #annotating a name of the killed player
            t_df=t_df[t_df['player_id'] != t[3]]
            
       #doing else to annotate the player's name if he is still alive
        else:
            t_df_annotate=t_df[t_df['player_id'] == t[3]]
            plt.annotate(t[32], (t_df_annotate['player_mapX'], t_df_annotate['player_mapY']), c='white') 
            
        #printing the t directions adjusted to the resolution
        print(time_num, t[32], t[36], t[37])
        
    twod_map=plt.scatter(t_df['player_mapX'], t_df['player_mapY'], s=300, alpha=1, c='yellow')
    
    
    #let's display the nades for a given time_num 
    #creating df's for specific time_num 
    df_sj_time=df_scattering_joint[df_scattering_joint.timestamp==time_num]
    
    for nade in df_sj_time.values:
        if nade[17]=='smoke':
            df_smoke=df_sj_time[df_sj_time.type=='smoke']
            twod_map=plt.scatter(df_smoke['nade_mapX'], df_smoke['nade_mapY'], s=300, marker='d', alpha=1, c='silver')
            
        elif nade[17]=='flashbang':
            df_flash=df_sj_time[df_sj_time.type=='flashbang']
            twod_map=plt.scatter(df_flash['nade_mapX'], df_flash['nade_mapY'], s=300,  marker='d', alpha=1, c='white')
    
        elif nade[17]=='firebomb':
            df_firebomb=df_sj_time[df_sj_time.type=='firebomb']
            twod_map=plt.scatter(df_firebomb['nade_mapX'], df_firebomb['nade_mapY'], s=300,  marker='d', alpha=1, c='orangered')
            #I won't be displaying inferno type for now as I think it's the second state of firebomb beginning when it explodes


  
