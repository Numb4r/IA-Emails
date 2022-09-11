import json
import os
import threading
from classes import *


folder = "./limpos/"
os.chdir(folder)

folder = os.getcwd()

typeEmail = os.listdir()
typeEmail.sort()
mapCountWords = {"SPAM": {}, "HAM": {}}
globalCountWords = {"SPAM": 0, "HAM": 0}

lock = threading.Lock()


def updateMapCountWords(typeEmail, values: dict):
    global globalCountWords
    global mapCountWords
    valuesInKey = mapCountWords[typeEmail]
    for k in values.keys():
        globalCountWords[typeEmail] += values.get(k)
        if not valuesInKey.get(k):
            valuesInKey[k] = values.get(k)
        else:
            valuesInKey[k] += values.get(k)
    mapCountWords[typeEmail].update(valuesInKey)


def thread_task(lock, key, values):
    # lock.acquire()
    updateMapCountWords(key, values)
    # lock.release()


def discoveryForTypeEmail(path, typeEmail, lock):
    listFiles = os.listdir(path+"/"+typeEmail)
    for j in listFiles:
        with open(path+"/"+typeEmail+"/"+j, 'r', encoding="utf8", errors='ignore') as f:
            t = f.read()
        mapWords = getBody(t)
        thread_task(lock, typeEmail[:-1].upper(), mapWords)
        f.close()


def discoveryWords(path, typeEmail, lock):
    # vetThreads = []
    for i in typeEmail:
        discoveryForTypeEmail(path, i, lock)
        # vetThreads.append(threading.Thread(
        #     target=discoveryForTypeEmail, args=(path, i, lock)))
        # vetThreads[len(vetThreads)-1].start()
        # vetThreads[len(vetThreads)-1].join()


def removingIrrelevantValues(mapWords, key):
    mapCountWords[key] = {key: val for key,
                          val in mapCountWords[key].items() if val > 1}
    print(list(mapCountWords[key])[0])


def removeApproximateValues(mapWords, x: float, y: float):
    auxMap = mapCountWords["SPAM"].copy()
    for key, val in auxMap.items():
        if mapCountWords["HAM"].get(key) and float(val) >= x*float(mapCountWords["HAM"].get(key)) and float(val) < y*float(mapCountWords["HAM"].get(key)):
            print("Removing "+key+" : ",
                  float(mapCountWords["HAM"].get(key)) / float(mapCountWords["SPAM"].get(key)))
            mapCountWords["HAM"].pop(key)
            mapCountWords["SPAM"].pop(key)


def normalizeClass(mapCountWords, globalCountWords, key):

    valuesInKey = mapCountWords[key]
    for x, y in valuesInKey.items():
        valuesInKey[x] = valuesInKey[x]/globalCountWords[key]
    # valuesInKey.update({print(valuesInKey.get(x))
    #                    for x, y in valuesInKey.items()})
    mapCountWords[key] = valuesInKey


discoveryWords(folder, typeEmail, lock)
removingIrrelevantValues(mapCountWords, "SPAM")
removingIrrelevantValues(mapCountWords, "HAM")
removeApproximateValues(mapCountWords, 0.7, 1.3)
normalizeClass(mapCountWords, globalCountWords, "SPAM")
normalizeClass(mapCountWords, globalCountWords, "HAM")


os.chdir("/mnt/c/Users/Yuri/Documents/projetos/Ia/Email/")
export = open("export.json", 'w')
json_obj = json.dumps(mapCountWords, indent=4)
export.write(json_obj)
export.close()
