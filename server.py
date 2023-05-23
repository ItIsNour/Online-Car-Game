import os
import pprint
from pymongo import MongoClient
import re
import time
import socket
from _thread import *
import sys



# Database
password = "***"
connection_string = f"mongodb+srv://nour:{password}@cluster0.lm8lset.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)

database = client.carGame


# Set active players to 0 at the beginning
forallfields = {}
activePlayersStart = {"$set": {"activePlayers": 0}}

database.player.update_many(forallfields, activePlayersStart)


# Get data of players initial info from database
initialPosition = []

for x in database.server.find({},{"_id":0}):
    initialPosition.append(x)
print("from data base",initialPosition)



# Read info from DB and put it in list of tuples
def read_info_from_database(str):
    list=[]
    tup0 = ()
    tup1 = ()
    tup2 = ()
    tup3 = ()
    str = re.findall(r'\{.*?\}', str)
    for i in range(len(str)):
        # print(str[i].split(","))
        el = str[i]
        el_len = len(el)
        f_b = el[0]
        fb_removed = el.replace(f_b, "", 1)
        l_b = fb_removed[len(fb_removed) - 1]
        b_removed = fb_removed.replace(l_b, "", 1)
        fin = b_removed.split(",")
        # print(fin)
        for x in range(len(fin)):
            field = fin[x].split(":")
            # print(field)
            if i == 0:
                tup0 = tup0 + (int(field[1]),)
            # print("ana tuple client 0", tup0)
            if i == 1:
                tup1 = tup1 + (int(field[1]),)
            # print("ana tuple client 1", tup1)
            if i == 2:
                tup2 = tup2 + (int(field[1]),)
            if i == 3:
                tup3 = tup3 + (int(field[1]),)

    list.append(tup0)
    list.append(tup1)
    list.append(tup2)
    list.append(tup3)
    return list



server = "YOURIPADDRESS"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")


# Reads the current player info received
def read_info(str):
    str = str.split(",")
    return int(str[0]), int(str[1]), int(str[2]), int(str[3]), int(str[4])

# Returns a string to the client --- Sends the initial position if input is tuple and all the info list if input is a list
def make_info(info):
    return str(info[0]) + "," + str(info[1])+ "," + str(info[2])+ "," + str(info[3])



# Get data of players info from database
def get_from_db():
    playersInfo = []
    for x in database.player.find({}, {"_id": 0}):
        playersInfo.append(x)
    return playersInfo
# playersInfo = get_from_db()
info = read_info_from_database(make_info(get_from_db()))

print(info, "First reading from DB")

# Get data of players info updated from database every x seconds
def get_updated_info():
    global info
    info = read_info_from_database(make_info(get_from_db()))


# Player Unique ID
currentPlayer = 0




# Reading initial positions from DB and put them in a list of tuples
initPos = read_info_from_database(make_info(initialPosition))
startTime = time.time()

def threaded_client(conn, player):
    conn.send(str.encode(make_info(initPos[player])))
    reply = ""
    while True:
        try:
            # Reads the tuple sent by current client
            data = read_info(conn.recv(2048).decode())
            print(info, "before update")

            sec = round(time.time()-startTime)
            print(sec)
            if sec % 5 == 0:
                # Took data recieved from client and store it to database
                info[(data[0])] = data
                field = {"id": player}
                newInfo = {"$set": {"xPos": info[player][2], "yPos": info[player][3]}}
                database.player.update_many(field, newInfo)

                get_updated_info()
                print(info, "updated now")


            if not data:
                print("Disconnected")
                break
            else:
                reply = info
                print("Received: ", data)
                print("Sending : ", reply)

            conn.send(str.encode(make_info(reply)))
        except:
            break

    print("Lost connection")
    conn.close()





while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
    allfields = {}
    numOfActivePlayers = {"$set": {"activePlayers": currentPlayer}}

    database.player.update_many(allfields, numOfActivePlayers)


