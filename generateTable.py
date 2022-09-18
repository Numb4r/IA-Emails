from classes import *
import os
import json
import csv
import pandas as pd


def openJsonFile(file):
    j = open(file, 'r')

    return json.load(j)


def concatSumListWords(listWords):
    words = listWords["SPAM"]
    for i in listWords["HAM"]:
        if words.get(i) == None:
            # print("Add ", i)
            words[i] = listWords["HAM"].get(i)
        else:
            # print("Concat ", i)
            words[i] += listWords["HAM"].get(i)
    lista = sorted(words.items(), key=lambda x: x[1])
    return lista


listWords = dict(openJsonFile("export.json"))
words = [i[0] for i in concatSumListWords(listWords)[-500:]]
words.append("!_CLASS_EMAIL")
# bestWords = []


folder = "./limpos/"
os.chdir(folder)

folder = os.getcwd()

typeEmail = os.listdir()
typeEmail.sort()

table = []
# table.append(('!_CLASS_EMAIL', []))
# table = pd.DataFrame(table)


# rowstable = []


def insertInTable(body, table):
    global words
    row = {i: 0 for i in words}
    # print(row)

    for word in body.listWords:
        if body.mapCountWords.get(word) and word in words:
            row[word] = body.mapCountWords.get(word)
            # row[words.index(word)] = body.mapCountWords.get(word)
    return row


def discoveryForTypeEmail(path, typeEmail, table):
    listFiles = os.listdir(path+"/"+typeEmail)
    for j in listFiles:
        # print(path+"/"+typeEmail+"/"+j)
        with open(path+"/"+typeEmail+"/"+j, "r", encoding="utf8", errors='ignore') as f:
            t = f.read()
        body = getBody(t, table)
        row = insertInTable(body, table)

        row["!_CLASS_EMAIL"] = 0 if typeEmail[:-1].upper() == "SPAM" else 1
        table.append(row)
        #
        # row.append()

        # tablewrite.writerow(row)
        f.close()


# fileWrite = open("table.table", 'w')
# tablewrite = table.writer(fileWrite)
# tablewrite.writerow(words)


def discoveryWords(path, typeEmail, table):
    print("Init discovery words")
    for i in typeEmail:
        discoveryForTypeEmail(path, i, table)
    print("Finish discovery words")


discoveryWords(folder, typeEmail, table)

os.chdir("..")
with open('table.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=words)
    writer.writeheader()
    writer.writerows(table)
# fileWrite = open("table.csv", "w")


# fileWrite.write(str(csv))
