import sqlite3
import json

conn=sqlite3.connect('round_data_full.sqlite')
cur=conn.cursor()

fh=open('round_data_full.txt')
data=fh.read()
js=json.loads(data)

for item in js:
    if 'allplayers' in item.keys():
        new_dict=item['allplayers']
        for k,v in new_dict.items():
            
            #extracting players, their steam_id, name and team to Players
            if v['team']=='CT':
                team_id='CT'
            else:
                team_id='T'
            cur.execute('INSERT OR IGNORE INTO Players (steam_id, name, team_id) VALUES (?,?,?)', (k, v['name'], team_id))

            #extracting weapons to Weapons
            weapons_dict=v['weapons']
            for key ,value in weapons_dict.items():
                cur.execute('INSERT OR IGNORE INTO Weapons (name, type) VALUES (?,?)', (value['name'], value['type']))
                #extracting weapons per player per timestamp to then add them to the relevant row in Matches
                if key=='weapon_0':
                    cur.execute('SELECT id FROM Weapons WHERE name=?', (value['name'], ))
                    weapon_0_id=cur.fetchone()[0]
                    weapon_0_state=value['state']
                elif key=='weapon_1':
                    cur.execute('SELECT id FROM Weapons WHERE name=?', (value['name'], ))
                    weapon_1_id=cur.fetchone()[0]
                    weapon_1_state=value['state']
                    #initialising the rest of weapon slots which aren't necessarily filled to pass None to the SQL INSERT statement to make Null in the DB
                    weapon_2_id=None
                    weapon_2_state=None
                    weapon_3_id=None
                    weapon_3_state=None
                    weapon_4_id=None
                    weapon_4_state=None
                    weapon_5_id=None
                    weapon_5_state=None
                elif key=='weapon_2':
                    cur.execute('SELECT id FROM Weapons WHERE name=?', (value['name'], ))
                    weapon_2_id=cur.fetchone()[0]
                    weapon_2_state=value['state']
                elif key=='weapon_3':
                    cur.execute('SELECT id FROM Weapons WHERE name=?', (value['name'], ))
                    weapon_3_id=cur.fetchone()[0]
                    weapon_3_state=value['state']
                elif key=='weapon_4':
                    cur.execute('SELECT id FROM Weapons WHERE name=?', (value['name'], ))
                    weapon_4_id=cur.fetchone()[0]
                    weapon_4_state=value['state']
                elif key=='weapon_5':
                    cur.execute('SELECT id FROM Weapons WHERE name=?', (value['name'], ))
                    weapon_5_id=cur.fetchone()[0]
                    weapon_5_state=value['state']

            #extracting 'state' values to then add them to Matches
            health=v['state']['health']
            armor=v['state']['armor']
            helmet=v['state']['helmet']
            flashed=v['state']['flashed']
            burning=v['state']['burning']

            #extracting 'match_stats' values to then add them to Matches    
            kills=v['match_stats']['kills']
            assists=v['match_stats']['assists']
            deaths=v['match_stats']['deaths']
            
            #extracting XYZ positions and directions to Matches as well as match_id, round_id, player_id, {state}, {match_stats} and timestamp
            value_pos=v['position'].split()
            pos_x=value_pos[0].replace(',','')
            pos_y=value_pos[1].replace(',','')
            pos_z=value_pos[2].replace(',','')
            value_forw=v['forward'].split()
            dir_x=value_forw[0].replace(',','')
            dir_y=value_forw[1].replace(',','')
            dir_z=value_forw[2].replace(',','')
            cur.execute('SELECT id FROM Players WHERE steam_id=?', (k, )) #selecting the player_id matching the steam_id which is k of the item in new_dict
            player_id=cur.fetchone()[0] #fetching the id found using the above line
            cur.execute('INSERT INTO Matches (match_id, round_id, player_id, posX, posY, posZ, dirX, dirY, dirZ, health, armour, helmet, flashed, burning, kills, assists, deaths, timestamp, w_0_id, w_0_state, w_1_id, w_1_state, w_2_id, w_2_state, w_3_id, w_3_state, w_4_id, w_4_state, w_5_id, w_5_state) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (1, item['map']['round'], player_id, pos_x, pos_y, pos_z, dir_x, dir_y, dir_z, health, armor, helmet, flashed, burning, kills, assists, deaths, item['provider']['timestamp'], weapon_0_id, weapon_0_state, weapon_1_id, weapon_1_state, weapon_2_id, weapon_2_state, weapon_3_id, weapon_3_state, weapon_4_id, weapon_4_state, weapon_5_id, weapon_5_state))
           

    #extracting grendes to Grenades
    if 'grenades' in item.keys():
        gren_dict=item['grenades']
        for k,v in gren_dict.items():
            gren_num=k
            gren_type=v['type']
            cur.execute('INSERT OR IGNORE INTO Grenades(type, number) VALUES (?,?)', (gren_type, gren_num))
            
            #extracting every grenade's scattering to Scattering. The script throws an error which I dunno how to sort but the INSERT statement works well
            try:
                if v['type']=='smoke':
                    cur.execute('SELECT id FROM Grenades WHERE number=?', (k, ))
                    grenade_id=cur.fetchone()[0]
                    cur.execute('SELECT id FROM Players WHERE steam_id=?', (v['owner'], ))
                    player_id=cur.fetchone()[0]

                    lala=gren_dict.get(k)
                    if lala: 
                        print(lala)
                    else:
                        print('NF')

                    gren_pos=v['position'].split()
                    pos_x=gren_pos[0].replace(',','')
                    pos_y=gren_pos[1].replace(',','')
                    pos_z=gren_pos[2].replace(',','')
                    gren_vel=v['velocity'].split()
                    vel_x=gren_vel[0].replace(',','')
                    vel_y=gren_vel[1].replace(',','')
                    vel_z=gren_vel[2].replace(',','')
                    lifetime=v['lifetime']
                    effect_time=v['effecttime']
                    cur.execute('INSERT INTO Scattering (match_id, round_id, grenade_id, player_id, posX, posY, posZ, velX, velY, velZ, lifetime, effect_time, timestamp) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', (1, item['map']['round'], grenade_id, player_id, pos_x, pos_y, pos_z, vel_x, vel_y, vel_z, lifetime, effect_time, item['provider']['timestamp']))
            except:
                continue

            if v['type']=='flashbang':
                cur.execute('SELECT id FROM Grenades WHERE number=?', (k, ))
                grenade_id=cur.fetchone()[0]
                cur.execute('SELECT id FROM Players WHERE steam_id=?', (v['owner'], ))
                player_id=cur.fetchone()[0] 
                gren_pos=v['position'].split()
                pos_x=gren_pos[0].replace(',','')
                pos_y=gren_pos[1].replace(',','')
                pos_z=gren_pos[2].replace(',','')
                gren_vel=v['velocity'].split()
                vel_x=gren_vel[0].replace(',','')
                vel_y=gren_vel[1].replace(',','')
                vel_z=gren_vel[2].replace(',','')
                lifetime=v['lifetime']
                effect_time=None
                cur.execute('INSERT INTO Scattering (match_id, round_id, grenade_id, player_id, posX, posY, posZ, velX, velY, velZ, lifetime, effect_time, timestamp) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', (1, item['map']['round'], grenade_id, player_id, pos_x, pos_y, pos_z, vel_x, vel_y, vel_z, lifetime, effect_time, item['provider']['timestamp']))
            elif v['type']=='frag':
                cur.execute('SELECT id FROM Grenades WHERE number=?', (k, ))
                grenade_id=cur.fetchone()[0]
                cur.execute('SELECT id FROM Players WHERE steam_id=?', (v['owner'], ))
                player_id=cur.fetchone()[0]
                gren_pos=v['position'].split()
                pos_x=gren_pos[0].replace(',','')
                pos_y=gren_pos[1].replace(',','')
                pos_z=gren_pos[2].replace(',','')
                gren_vel=v['velocity'].split()
                vel_x=gren_vel[0].replace(',','')
                vel_y=gren_vel[1].replace(',','')
                vel_z=gren_vel[2].replace(',','')
                lifetime=v['lifetime']
                effect_time=None
                cur.execute('INSERT INTO Scattering (match_id, round_id, grenade_id, player_id, posX, posY, posZ, velX, velY, velZ, lifetime, effect_time, timestamp) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', (1, item['map']['round'], grenade_id, player_id, pos_x, pos_y, pos_z, vel_x, vel_y, vel_z, lifetime, effect_time, item['provider']['timestamp']))
            elif v['type']=='firebomb':
                cur.execute('SELECT id FROM Grenades WHERE number=?', (k, ))
                grenade_id=cur.fetchone()[0]
                cur.execute('SELECT id FROM Players WHERE steam_id=?', (v['owner'], ))
                player_id=cur.fetchone()[0]
                gren_pos=v['position'].split()
                pos_x=gren_pos[0].replace(',','')
                pos_y=gren_pos[1].replace(',','')
                pos_z=gren_pos[2].replace(',','')
                gren_vel=v['velocity'].split()
                vel_x=gren_vel[0].replace(',','')
                vel_y=gren_vel[1].replace(',','')
                vel_z=gren_vel[2].replace(',','')
                lifetime=v['lifetime']
                effect_time=None
                cur.execute('INSERT INTO Scattering (match_id, round_id, grenade_id, player_id, posX, posY, posZ, velX, velY, velZ, lifetime, effect_time, timestamp) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', (1, item['map']['round'], grenade_id, player_id, pos_x, pos_y, pos_z, vel_x, vel_y, vel_z, lifetime, effect_time, item['provider']['timestamp']))
            elif v['type']=='inferno':
                cur.execute('SELECT id FROM Grenades WHERE number=?', (k, ))
                grenade_id=cur.fetchone()[0]
                cur.execute('SELECT id FROM Players WHERE steam_id=?', (v['owner'], ))
                player_id=cur.fetchone()[0]
                lifetime=v['lifetime']
                cur.execute('INSERT INTO Scattering (match_id, round_id, grenade_id, player_id, posX, posY, posZ, velX, velY, velZ, lifetime, effect_time, timestamp) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', (1, item['map']['round'], grenade_id, player_id, None, None, None, None, None, None, lifetime, None, item['provider']['timestamp']))

print('inserted')
conn.commit()
print('Done')
