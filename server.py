import socket
from _thread import *
from car import Car
import pickle
from pymongo import MongoClient
import pymongo.errors
import sys
import time
import random


# Mongodb database
password = "pZu532OuO1urq4yV"
connection_string = f"mongodb+srv://m:{password}@cluster0.lm8lset.mongodb.net/?retryWrites=true&w=majority"


client = MongoClient(connection_string)
databaseMain = client.carGame
databaseReplica = client.carGameReplica
databases = [databaseMain, databaseReplica]

# Check database connection
def checkDatabaseConnection():
    global database
    global databases
    try:
        if databaseMain.command('ping')['ok'] == 1:
            print("Successfully connected to MongoDB Main database!")
            database = databaseMain
            databases = [databaseMain]
        elif databaseReplica.command('ping')['ok'] == 1:
            print("Successfully connected to MongoDB Replica database!")
            database = databaseReplica
            databases = [databaseReplica]
        else:
            print("Failed to connect to MongoDB both Main and Replica databases!")
        if databaseMain.command('ping')['ok'] == 1 and databaseReplica.command('ping')['ok'] == 1:
            databases = [databaseMain, databaseReplica]
    except pymongo.errors.ConnectionFailure as e:
        print("Failed to connect to MongoDB databases:", e)
        sys.exit()




# Set active players to 0 at the beginning in both dbs main and replica
forallfields = {}
activePlayersStart = {"$set": {"activePlayers": 0, "score": 0, "name": None, "messages":[]}}
checkDatabaseConnection()
for d in databases:
    d.player.update_many(forallfields, activePlayersStart)




def get_from_db():
    playersInfo = []
    for x in database.player.find({}, {"_id": 0}):
        playersInfo.append(x)
    info = [tuple(playersInfo[0].values()),tuple(playersInfo[1].values()),tuple(playersInfo[2].values()),tuple(playersInfo[3].values()),tuple(playersInfo[4].values())]
    return info

# Get data of players from database
def get_updated_info():
    global infoFromDb
    global info
    infoFromDb = get_from_db()

    # Update the all objects with the updated values from db

    # info[0].playerId = infoFromDb[0][0]
    # info[0].imgID = infoFromDb[0][1]
    # info[0].x = infoFromDb[0][2]
    # info[0].y = infoFromDb[0][3]
    # info[0].activePlayers = infoFromDb[0][4]
    # info[0].score = infoFromDb[0][5]
    # info[0].nickname = infoFromDb[0][6]


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





server = socket.gethostbyname(socket.gethostname())
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(4)
print("Waiting for a connection, Server Started")


# Make infoFromDb in this format [(0, 0, 418, 400, 3, 88, 500), (1, 1, 358, 160, 3, 88, 555), (2, 2, 478, 280, 3, 88, 477), (3, 3, 258, 260, 3, 88, 888)]

infoFromDb = get_from_db()
print(infoFromDb, "ahu da el value bt3 info from db awel ma aad5ol")


obsL_x = [random.randrange(73,188),random.randrange(188,303),random.randrange(73,188),random.randrange(188,303),random.randrange(73,188),random.randrange(188,303),random.randrange(73,188)]
obsR_x = [random.randrange(330,475),random.randrange(475,620),random.randrange(330,475),random.randrange(475,620),random.randrange(330,475),random.randrange(475,620),random.randrange(330,475)]
obsL_img = [0,1,2,3,1,0,2]
obsR_img = [1,2,3,0,3,1,0]

info = [Car(infoFromDb[0][0],infoFromDb[0][1],355,400, obsL_x, obsR_x, obsL_img, obsR_img), Car(infoFromDb[1][0],infoFromDb[1][1],490,400, obsL_x, obsR_x, obsL_img, obsR_img),Car(infoFromDb[2][0],infoFromDb[2][1],215,400, obsL_x, obsR_x, obsL_img, obsR_img),Car(infoFromDb[3][0],infoFromDb[3][1],600,400, obsL_x, obsR_x, obsL_img, obsR_img),Car(infoFromDb[4][0],infoFromDb[4][1],100,400, obsL_x, obsR_x, obsL_img, obsR_img)]


# Player Unique ID
currentPlayer = 0
activePlayers = 0
disconnectedPlayer = 11

startTime = time.time()

def threaded_client(conn, player):
    conn.send(pickle.dumps(info[player]))
    global activePlayers
    global disconnectedPlayer
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
                checkDatabaseConnection()
                # Took data object recieved from client and store it to both databases Main and Replica >> Hnaaaaaaa el store started
                thisPlayer = data
                field = {"id": player}
                newInfo = {"$set": {"xPos": thisPlayer.x, "yPos": thisPlayer.y,"score":thisPlayer.score,"name":thisPlayer.nickname, "activePlayers":thisPlayer.activePlayers, "messages":thisPlayer.messages}}
                for d in databases:
                    d.player.update_many(field, newInfo)

                # To save the messages list in all players at both databases so that when a disconnected player connects again, view the current messages
                for d in databases:
                    for document in d.player.find():
                        d.player.update_one({"_id": document["_id"]},{"$set": {"messages": thisPlayer.messages}})


            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = info[0],info[2],info[3],info[4]
                elif player == 2:
                    reply = info[0], info[1], info[3],info[4]
                elif player == 3:
                    reply = info[0], info[1], info[2],info[4]
                elif player == 4:
                    reply = info[0], info[1], info[2],info[3]
                else:
                    reply = info[1], info[2],info[3],info[4]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Player ",player+1," Disconnected")
    info[player].active = 0
    # Take the id of the disconnected player
    disconnectedPlayer = player
    print(info[player].active,"now i disconnected")
    activePlayers-=1

    # Save all his info to the both DBs
    print(player,"ana roht lel id dah fl db w 3amalt save lel id dah",info[player].playerId)
    checkDatabaseConnection()
    field = {"id": player}
    newInfo = {"$set": {"id":info[player].playerId, "carId":info[player].imgID,"xPos": info[player].x, "yPos": info[player].y, "score": info[player].score, "name": info[player].nickname,"activePlayers": info[player].activePlayers, "messages":info[player].messages}}
    for d in databases:
        d.player.update_many(field, newInfo)
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    # If a player disconnects (disconnected player != 11), then we will check if the player trying to connect new or trying to reconnect from his addr
    # if an old player trying to connect, get his last info from any db
    # checkDatabaseConnection()
    # get_updated_info()

    start_new_thread(threaded_client, (conn, currentPlayer))
    info[currentPlayer].active = 1
    print(info[currentPlayer].active,"now i connected")
    currentPlayer += 1
    allfields = {}
    activePlayers +=1


