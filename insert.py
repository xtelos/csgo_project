from create_db import connectToMysql
import csv


def insertIntoPlayers():
    cursor.execute('USE csgo;')
    with open('csgo_data/players.csv') as csvFile:
        csvFile.readline()
        reader = csv.reader(csvFile)
        for row in reader:
            playerName = row[1]
            team = row[2]
            country = row[4]
            eventID = row[7]
            eventName = row[8]
            cursor.execute('INSERT INTO players VALUES("{}","{}","{}","{}","{}");'.format(playerName, team, country, eventID, eventName))
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


def insertIntoMaps():
    cursor.execute('USE csgo;')
    with open('csgo_data/picks.csv') as csvFile:
        csvFile.readline()
        reader = csv.reader(csvFile)
        mapDictionary = {}
        invalidMaps = []
        for row in reader:
            map = row[16]
            if map in mapDictionary:
                mapDictionary[map] += 1
            else:
                mapDictionary[map] = 1

        for key, value in mapDictionary.items():
            if value < 5:
                invalidMaps.append(key)

        for x in invalidMaps:
            del mapDictionary[x]

        for mapName in mapDictionary:
                cursor.execute('INSERT INTO maps VALUES("{}",{},{});'.format(mapName, mapDictionary[mapName], 0))

        conn.commit()

def insertIntoPlayerAnalytics():
    cursor.execute('USE csgo;')


if __name__ == '__main__':
    conn, cursor = connectToMysql()
    insertIntoPlayers()
    insertIntoMatches()
    insertIntoMaps()

