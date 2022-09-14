from classes import *
import os
import json
import csv


def openJsonFile(file):
    j = open(file, 'r')

    return json.load(j)


listWords = dict(openJsonFile("export.json"))
folder = "./limpos/"
os.chdir(folder)

folder = os.getcwd()

typeEmail = os.listdir()
typeEmail.sort()


words = list(listWords["SPAM"].keys())
rowscsv = []


def insertInTable(body, typeEmail):
    global words
    row = [0 for _ in words]
    for word in body.listWords:
        if body.mapCountWords.get(word) and word in words:
            row[words.index(word)] = body.mapCountWords.get(word)
    return row


def discoveryForTypeEmail(path, typeEmail, fileWrite):
    listFiles = os.listdir(path+"/"+typeEmail)
    for j in listFiles:
        print(path+"/"+typeEmail+"/"+j)
        with open(path+"/"+typeEmail+"/"+j, "r", encoding="utf8", errors='ignore') as f:
            t = f.read()
        body = getBody(t)
        row = insertInTable(body, typeEmail[:-1].upper())
        row.append(0 if typeEmail[:-1].upper() == "SPAM" else 1)
        csvwrite.writerow(row)
        f.close()


os.chdir("..")
fileWrite = open("table.csv", 'w')
csvwrite = csv.writer(fileWrite)
csvwrite.writerow(words)


def discoveryWords(path, typeEmail, fileWrite):
    print("Init discovery words")
    for i in typeEmail:
        discoveryForTypeEmail(path, i, fileWrite)
    print("Finish discovery words")


discoveryWords(folder, typeEmail, csvwrite)
