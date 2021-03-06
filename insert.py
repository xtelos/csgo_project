from create_db import connectToMysql
from create_db import create
import csv


def insertIntoPlayers():
    cursor.execute('USE csgo;')
    with open('csgo_data/players.csv') as csvFile:
        csvFile.readline()
        reader = csv.reader(csvFile)
        career_total_kills = {}
        career_total_deaths = {}
        for row in reader:
            playerName = row[1]
            team = row[2]
            country = row[4]
            eventID = row[7]
            eventName = row[8]
            matchID = row[6]
            match_total_kills = checkIfEmpty(row[13])
            match_total_deaths = checkIfEmpty(row[15])

            addToKDDict(playerName, career_total_kills, match_total_kills)
            addToKDDict(playerName, career_total_deaths, match_total_deaths)

            cursor.execute('INSERT INTO playerAnalyticsPerMatch VALUES("{}", "{}", "{}", "{}");'.format(playerName, matchID, match_total_kills, match_total_deaths))
            if eventName not in eventSet:
                eventSet.add(eventName)
                cursor.execute('INSERT INTO events VALUES("{}", "{}");'.format(eventID, eventName))
            cursor.execute('INSERT INTO players VALUES("{}","{}","{}","{}");'.format(playerName, team, country, eventID))
        insertIntoOverallAnalytics(career_total_kills, career_total_deaths)

        conn.commit()


def insertIntoMatches():
    cursor.execute('USE csgo;')
    with open('csgo_data/results.csv') as csvFile:
        csvFile.readline()
        reader = csv.reader(csvFile)
        for row in reader:
            date = row[0]
            matchID = row[13]
            eventID = row[12]
            team1 = row[1]
            team2 = row[2]
            if int(row[16]) + int(row[17]) <= 5:
                bestOf = int(row[16]) + int(row[17])
            else:
                bestOf = 1
            if int(row[16]) > int(row[17]):
                winner = 'team1'
            else:
                winner = 'team2'
            cursor.execute('INSERT INTO matches VALUES("{}","{}","{}","{}","{}", "{}", "{}");'.format(date, matchID, eventID, team1, team2, bestOf, winner))
        conn.commit()


def addToDict(name, dict):
    if name in dict:
        dict[name] += 1
    else:
        dict[name] = 1


def addToKDDict(name, dict, value):
    if name in dict:
        dict[name] += value
    else:
        dict[name] = value


def addToInvalidList(invalid_list, map_dict):
    for key, value in map_dict.items():
        if key == '0.0':
            invalid_list.append(key)
        if value < 5:
            invalid_list.append(key)


def insertIntoMaps():
    cursor.execute('USE csgo;')
    with open('csgo_data/picks.csv') as csvFile:
        csvFile.readline()
        reader = csv.reader(csvFile)
        banned_mapsDict = {}
        picked_mapsDict = {}
        invalidMaps = []
        invalid_banned_maps = []
        for row in reader:
            t1_ban_1 = row[8]
            t1_ban_2 = row[9]
            t1_ban_3 = row[10]
            t2_ban_1 = row[11]
            t2_ban_2 = row[12]
            t2_ban_3 = row[13]
            bans_list = [t1_ban_1, t1_ban_2, t1_ban_3, t2_ban_1, t2_ban_2, t2_ban_3]
            t1_picked = row[14]
            t2_picked = row[15]
            pick_list = [t1_picked, t2_picked]

            for map_ban in bans_list:
                addToDict(map_ban, banned_mapsDict)
            for map_pick in pick_list:
                addToDict(map_pick, picked_mapsDict)

        addToInvalidList(invalid_banned_maps, banned_mapsDict)
        addToInvalidList(invalidMaps, picked_mapsDict)

        for invalid_map in invalid_banned_maps:
            del banned_mapsDict[invalid_map]

        for invalid_map in invalidMaps:
            del picked_mapsDict[invalid_map]

        total_count_picked = sum(picked_mapsDict.values())
        total_count_banned = sum(banned_mapsDict.values())

        pickRate = {}
        for mapName in picked_mapsDict:
            pickRate[mapName] = round((picked_mapsDict[mapName] / total_count_picked), 3)

        banRate = {}
        for mapName in banned_mapsDict:
            banRate[mapName] = round((banned_mapsDict[mapName] / total_count_banned), 3)

        for mapName in picked_mapsDict:
            cursor.execute('INSERT INTO maps VALUES("{}",{},{},{},{});'.format(
                mapName, pickRate[mapName], banRate[mapName], picked_mapsDict[mapName], banned_mapsDict[mapName]))

        conn.commit()


def checkIfEmpty(value):
    if value == '':
        return 0
    return int(float(value))


def insertIntoOverallAnalytics(career_total_kills, career_total_deaths):
    for name in career_total_kills.keys():
        totalMatchKills = career_total_kills[name]
        totalMatchDeaths = career_total_deaths[name]
        averageKD = totalMatchKills / totalMatchDeaths
        cursor.execute('INSERT INTO playerAnalyticsOverall VALUES("{}", "{}")'.format(name, averageKD))
    conn.commit()


if __name__ == '__main__':
    conn, cursor = connectToMysql()
    create(conn, cursor)
    eventSet = set()
    insertIntoPlayers()
    insertIntoMatches()
    insertIntoMaps()
