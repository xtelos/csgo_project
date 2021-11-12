import mysql.connector
import dotenv
import os


def connectToMysql():
    dotenv.load_dotenv()

    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    conn = mysql.connector.connect(username=username, password=password, host='localhost')
    cursor = conn.cursor()

    return conn, cursor


def create():
    cursor.execute('CREATE DATABASE IF NOT EXISTS csgo;')
    cursor.execute('USE csgo;')

    cursor.execute('DROP TABLE IF EXISTS players;')
    cursor.execute('DROP TABLE IF EXISTS matches;')
    cursor.execute('DROP TABLE IF EXISTS maps;')
    cursor.execute('DROP TABLE IF EXISTS playerAnalytics;')

    cursor.execute('CREATE TABLE players (name VARCHAR(255), '
                   'team VARCHAR(255), country VARCHAR(255), eventID INT, eventName VARCHAR(255));')
    cursor.execute('CREATE TABLE matches (date DATE, matchID INT, eventID VARCHAR(255), '
                   'team1 VARCHAR(255), team2 VARCHAR(255), bestOf INT, winner VARCHAR(255));')
    cursor.execute('CREATE TABLE maps (mapName VARCHAR(255), pickRate FLOAT, banRate FLOAT, '
                   'totalPicks INT, totalBans INT);')
    cursor.execute('CREATE TABLE playerAnalytics (playerName VARCHAR(255), '
                   'teamName VARCHAR(255), matchID INT, kills INT, deaths INT);')
    conn.commit()


if __name__ == "__main__":
    conn, cursor = connectToMysql()
    create()
