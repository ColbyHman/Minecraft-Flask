from flask import Flask, render_template
from mcipc.rcon.je import Client

player_roster = []
players = []
stats_table = []
scoreboard_exists = False
total_death = 0
total_player_kill = 0
total_mob_kill = 0
total_walk = 0
total_ran = 0

app = Flask(__name__)


def setup_scoreboard():
    with Client('127.0.0.1', 25575, passwd='holden') as client:
        client.run("scoreboard", "objectives", "add", "Deaths", "deathCount", "\"Death Count\"")
        client.run("scoreboard", "objectives", "add", "PlayerKills", "playerKillCount", "\"Player Kills\"")
        client.run("scoreboard", "objectives", "add", "MobKills", "minecraft.custom:minecraft.mob_kills", "\"Mob Kills\"")
        client.run("scoreboard", "objectives", "add", "DistanceWalk", "minecraft.custom:minecraft.walk_one_cm", "\"Distanced Walked\"")
        client.run("scoreboard", "objectives", "add", "DistanceRun", "minecraft.custom:minecraft.sprint_one_cm", "\"Distance Ran\"")
        scoreboard_exists = True

def get_count(client_object, player, attribute):
    try:
        return int(
            (client_object.run(
                "scoreboard", "players", "get", player.name, attribute)).split("has ")[1].split(" [")[0])
    except:
        return 0


def get_roster():
    with Client('127.0.0.1', 25575, passwd='holden') as client:
        players = (client.list()).players
        for player in players:
            if ['#27cf32', player.name] not in player_roster:
                player_roster.append(['#27cf32', player.name])


def update_roster():
    with Client('127.0.0.1', 25575, passwd='holden') as client:
        current_players = client.list().players
        current_names = []
        for player in current_players:
            current_names.append(player.name)
        for item in player_roster:
            if item[1] not in current_names and ['#27cf32', item[1]] in player_roster:
                player_roster.remove(['#27cf32', item[1]])
                player_roster.append(['#cf2727', item[1]])
            elif item[1] in current_names and ['#cf2727', item[1]] in player_roster:
                player_roster.remove(['#cf2727', item[1]])
                player_roster.append(['#27cf32', item[1]])

def get_player_info(stats):
    with Client('127.0.0.1', 25575, passwd='holden') as client:
        players = (client.list()).players
        total_death = 0
        total_player_kill = 0
        total_mob_kill = 0
        total_walk = 0
        total_ran = 0
        if len(players) > 0:
            for player in players:
                death_count = get_count(client, player, "Deaths")
                player_kills = get_count(client, player, "PlayerKills")
                mob_kills = get_count(client, player, "MobKills")
                distance_walked = get_count(client, player, "DistanceWalk")/1000
                distance_ran = get_count(client, player, "DistanceRun")/1000
                stats.append([player.name, death_count, player_kills, mob_kills, distance_walked, distance_ran])
                total_death += death_count
                total_player_kill += player_kills
                total_mob_kill += mob_kills
                total_walk += distance_walked
                total_ran += distance_ran
        else:
            return None
        return stats, total_death, total_player_kill, total_mob_kill, total_walk, total_ran


@app.route('/')
def index():
    stats = None
    if not scoreboard_exists:
        setup_scoreboard()
    try:
        stats, total_death, total_player, total_mob, total_walk, total_ran = get_player_info(stats_table)
    except TypeError:
        total_death = total_player = total_mob = total_walk = total_ran = 0
    if len(player_roster) == 0:
        get_roster()
    else:
        update_roster()

    if stats != None:
        return render_template('index.html', stats=stats,
                           roster=player_roster,
                           total_deaths=total_death,
                           total_player_kills=total_player,
                           total_mob_kills=total_mob,
                           total_distance_walked=total_walk,
                           total_distance_ran=total_ran)
    else:
        return render_template('index.html', stats=[['No Players Yet', 0, 0, 0, 0, 0]],
                           roster=player_roster,
                           total_deaths=total_death,
                           total_player_kills=total_player,
                           total_mob_kills=total_mob,
                           total_distance_walked=total_walk,
                           total_distance_ran=total_ran)
