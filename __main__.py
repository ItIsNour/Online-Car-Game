import socket
import ssl
from _thread import *
from car import Car
import pickle
from pymongo import MongoClient
import pymongo.errors
import sys
import time
import random

password = "pZu532OuO1urq4yV"
connection_string = f"mongodb+srv://m:{password}@cluster0.lm8lset.mongodb.net/?retryWrites=true&w=majority"

replica_connection_string = f"mongodb+srv://asuprojects111:db_m0ng0_repl1ca@cluster0.tgwobdr.mongodb.net/"

client = MongoClient(connection_string)
databaseMain = client.carGame

clientR = MongoClient(replica_connection_string)
databaseReplica = clientR.carGameReplica

databases = [databaseMain, databaseReplica]


# Disconnect Main Database
# client.close()

# Disconnect Replica Database
# clientR.close()

# Check database connection
def checkDatabaseConnection():
    global database
    global databases

    try:
        if databaseMain.command('ping')['ok'] == 1 and databaseReplica.command('ping')['ok'] == 1:
            database = databaseMain
            databases = [databaseMain, databaseReplica]
        print("ALL GOOD")
    except:
        try:
            if databaseMain.command('ping')['ok'] == 1:
                print("Successfully connected to MongoDB Main database!")
                database = databaseMain
                databases = [databaseMain]
        except:
            try:
                if databaseReplica.command('ping')['ok'] == 1:
                    print("Failed to connect to MongoDB Main database!")
                    print("Successfully connected to MongoDB Replica database!")
                    database = databaseReplica
                    databases = [databaseReplica]
            except:
                print("Failed to connect to MongoDB both Main and Replica databases!")
                sys.exit()


# Set active players to 0 at the beginning in both dbs main and replica
forallfields = {}
activePlayersStart = {"$set": {"activePlayers": 0, "score": 0, "name": None, "messages": []}}
checkDatabaseConnection()
for d in databases:
    d.player.update_many(forallfields, activePlayersStart)


def get_from_db():
    playersInfo = []
    for x in database.player.find({}, {"_id": 0}):
        playersInfo.append(x)
    info = [tuple(playersInfo[0].values()), tuple(playersInfo[1].values()), tuple(playersInfo[2].values()),
            tuple(playersInfo[3].values()), tuple(playersInfo[4].values())]
    return info


# Get data of players from database
def get_updated_info(reconnecting_player):
    global prevInfo
    print("get hna")
    for x in database.player.find({"id": reconnecting_player}, {"_id": 0}):
        prevInfo = list(x.values())

    print(prevInfo, "da el infoo el adim bta3eeee")

    # Update the object with the updated values from db

    info[reconnecting_player].playerId = prevInfo[0]
    info[reconnecting_player].imgID = prevInfo[1]
    info[reconnecting_player].x = prevInfo[2]
    info[reconnecting_player].y = prevInfo[3]
    info[reconnecting_player].activePlayers = prevInfo[4]
    info[reconnecting_player].score = prevInfo[5]
    info[reconnecting_player].nickname = prevInfo[6]
    info[reconnecting_player].messages = prevInfo[7]
    info[reconnecting_player].time = prevInfo[8]
    info[reconnecting_player].reconnected = 1

    # info[1].playerId = infoFromDb[1][0]
    # info[1].imgID = infoFromDb[1][1]
    # info[1].x = infoFromDb[1][2]
    # info[1].y = infoFromDb[1][3]
    # info[1].activePlayers = infoFromDb[1][4]
    # info[1].score = infoFromDb[1][5]
    # info[1].nickname = infoFromDb[1][6]

    # info[2].playerId = infoFromDb[2][0]
    # info[2].imgID = infoFromDb[2][1]
    # info[2].x = infoFromDb[2][2]
    # info[2].y = infoFromDb[2][3]
    # info[2].activePlayers = infoFromDb[2][4]
    # info[1].score = infoFromDb[2][5]
    # info[2].nickname = infoFromDb[2][6]

    # info[3].playerId = infoFromDb[3][0]
    # info[3].imgID = infoFromDb[3][1]
    # info[3].x = infoFromDb[3][2]
    # info[3].y = infoFromDb[3][3]
    # info[3].activePlayers = infoFromDb[3][4]
    # info[3].score = infoFromDb[3][5]
    # info[3].nickname = infoFromDb[3][6]

    # info[4].playerId = infoFromDb[4][0]
    # info[4].imgID = infoFromDb[4][1]
    # info[4].x = infoFromDb[4][2]
    # info[4].y = infoFromDb[4][3]
    # info[4].activePlayers = infoFromDb[4][4]
    # info[4].score = infoFromDb[4][5]
    # info[4].nickname = infoFromDb[4][6]


def databaseWrite(data, player):
    checkDatabaseConnection()
    print("Writing in DB")
    # Took data object recieved from client and store it to both databases Main and Replica >> Hnaaaaaaa el store started
    thisPlayer = data
    field = {"id": player}
    newInfo = {
        "$set": {"xPos": thisPlayer.x, "yPos": thisPlayer.y, "score": thisPlayer.score, "name": thisPlayer.nickname,
                 "activePlayers": thisPlayer.activePlayers, "messages": thisPlayer.messages}}
    for d in databases:
        d.player.update_many(field, newInfo)

    # To save the messages list in all players at both databases so that when a disconnected player connects again, view the current messages
    for d in databases:
        for document in d.player.find():
            d.player.update_one({"_id": document["_id"]}, {"$set": {"messages": thisPlayer.messages}})


# server = "192.168.1.14"
# port = 5555
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# try:
#     s.bind((server, port))
# except socket.error as e:
#     str(e)
#
# s.listen(5)

hostname = 'www.python.org'
# PROTOCOL_TLS_CLIENT requires valid cert chain and hostname
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations('path/to/cabundle.pem')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
with s as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        print(ssock.version())






print("Waiting for a connection, Server Started")

# Make infoFromDb in this format [(0, 0, 418, 400, 3, 88, 500), (1, 1, 358, 160, 3, 88, 555), (2, 2, 478, 280, 3, 88, 477), (3, 3, 258, 260, 3, 88, 888)]

infoFromDb = get_from_db()
print(infoFromDb, "ahu da el value bt3 info from db awel ma aad5ol")

obsL_x = [random.randrange(73, 188), random.randrange(188, 303), random.randrange(73, 188), random.randrange(188, 303),
          random.randrange(73, 188), random.randrange(188, 303), random.randrange(73, 188)]
obsR_x = [random.randrange(330, 475), random.randrange(475, 620), random.randrange(330, 475),
          random.randrange(475, 620), random.randrange(330, 475), random.randrange(475, 620),
          random.randrange(330, 475)]
obsL_img = [0, 1, 2, 3, 1, 0, 2]
obsR_img = [1, 2, 3, 0, 3, 1, 0]

info = [Car(infoFromDb[0][0], infoFromDb[0][1], 355, 400, obsL_x, obsR_x, obsL_img, obsR_img),
        Car(infoFromDb[1][0], infoFromDb[1][1], 490, 400, obsL_x, obsR_x, obsL_img, obsR_img),
        Car(infoFromDb[2][0], infoFromDb[2][1], 215, 400, obsL_x, obsR_x, obsL_img, obsR_img),
        Car(infoFromDb[3][0], infoFromDb[3][1], 600, 400, obsL_x, obsR_x, obsL_img, obsR_img),
        Car(infoFromDb[4][0], infoFromDb[4][1], 100, 400, obsL_x, obsR_x, obsL_img, obsR_img)]

# Player Unique ID
currentPlayer = 0
activePlayers = 0
disconnectedPlayers = {}
prevInfo = []

startTime = time.time()


def threaded_client(conn, player, playerIp):
    global activePlayers
    global disconnectedPlayers
    global prevInfo

    car_object = info[player]
    print(info[player], "da el kont bab3ato")

    print("i senttttttttttttttttttttt", info[player].playerId,
          info[player].imgID,
          info[player].x,
          info[player].y,
          info[player].activePlayers,
          info[player].score,
          info[player].nickname,
          info[player].messages, )

    conn.send(pickle.dumps(car_object))

    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            print(infoFromDb, "first in while")

            info[player] = data

            for x in range(len(info)):
                info[x].activePlayers = activePlayers

            sec = round(time.time() - startTime)
            print(sec)
            if sec % 5 == 0:
                start_new_thread(databaseWrite, (data, player))

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = info[0], info[2], info[3], info[4]
                elif player == 2:
                    reply = info[0], info[1], info[3], info[4]
                elif player == 3:
                    reply = info[0], info[1], info[2], info[4]
                elif player == 4:
                    reply = info[0], info[1], info[2], info[3]
                else:
                    reply = info[1], info[2], info[3], info[4]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Player ", player + 1, " Disconnected")
    info[player].active = 0
    # Take the id of the disconnected player
    disconnectedPlayers[player] = playerIp
    print(info[player].active, "now i disconnected and this is the dict of all disconnected playersssssss",
          disconnectedPlayers)
    activePlayers -= 1

    # Save all his info to the both DBs
    print(player, "ana roht lel id dah fl db w 3amalt save lel id dah", info[player].playerId)
    checkDatabaseConnection()
    field = {"id": player}
    newInfo = {"$set": {"id": info[player].playerId, "carId": info[player].imgID, "xPos": info[player].x,
                        "yPos": info[player].y, "score": info[player].score, "name": info[player].nickname,
                        "activePlayers": info[player].activePlayers, "messages": info[player].messages,
                        "time": info[player].time}}
    for d in databases:
        d.player.update_many(field, newInfo)
    conn.close()


def startServer():
    global currentPlayer
    global activePlayers
    while True:

        conn, addr = s.accept()
        print("Connected to:", addr)

        # Get the IP address of the conencted player
        playerIp = addr[0].split(':')[0]

        # flag = False

        for key, value in disconnectedPlayers.items():
            if playerIp == value:
                currentPlayer = key
                get_updated_info(key)

        start_new_thread(threaded_client, (conn, currentPlayer, playerIp))
        info[currentPlayer].active = 1
        print(info[currentPlayer].active, "now i connected")
        currentPlayer += 1
        for value in disconnectedPlayers.values():
            if playerIp == value:
                currentPlayer -= 1
        allfields = {}
        activePlayers += 1


if __name__ == '__main__':
    startServer()