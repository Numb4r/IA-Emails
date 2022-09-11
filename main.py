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

lock = threading.Lock()


def updateMapCountWords(typeEmail, values: dict):
    # if (typeEmail == "ham"):
    #     global mapCountWordsHam
    #     mapTypeEmail = mapCountWordsHam
    # else:
    #     global mapCountWordsSpam
    global mapCountWords
    valuesInKey = mapCountWords[typeEmail]
    for k in values.keys():
        if not valuesInKey.get(k):
            valuesInKey[k] = values.get(k)
        else:
            valuesInKey[k] += values.get(k)
    mapCountWords[typeEmail].update(valuesInKey)


def thread_task(lock, key, values):
    # lock.acquire()
    updateMapCountWords(key, values)
    # lock.release()


string = ""


def discoveryForTypeEmail(path, typeEmail, lock):
    # lock.acquire()
    global string
    os.chdir(path+"/"+typeEmail)
    listFiles = os.listdir()
    # lock.release()
    for j in listFiles:

        # print(path+"/"+typeEmail+"/",end='')
        # print(j)
        with open(path+"/"+typeEmail+"/"+j, 'r', encoding="utf8", errors='ignore') as f:
            t = f.read()
        mapWords = getBody(t)
        # string=" ".join(mapWords)
        thread_task(lock, typeEmail[:-1].upper(), mapWords)
        f.close()


def discoveryWords(path, typeEmail, lock):
    vetThreads = []
    for i in typeEmail:
        # print(path+"/"+i)
        discoveryForTypeEmail(path, i, lock)
        # vetThreads.append(threading.Thread(target=discoveryForTypeEmail, args=(path,i,lock)))
        # vetThreads[len(vetThreads)-1].start()
        # vetThreads[len(vetThreads)-1].join()


discoveryWords(folder, typeEmail, lock)
# Removendo valores irrelevantes
mapCountWords["SPAM"] = {key: val for key,
                         val in mapCountWords["SPAM"].items() if val > 1}
mapCountWords["HAM"] = {key: val for key,
                        val in mapCountWords["HAM"].items() if val > 1}
keysToRemove = []
values = {}
# Removendo valores muito aproximados (entre 1 vez e 1.5 vezes)
for key, val in mapCountWords["SPAM"].items():
    if mapCountWords["HAM"].get(key) and float(val) >= 0.7*float(mapCountWords["HAM"].get(key)) and float(val) < 1.3*float(mapCountWords["HAM"].get(key)):
        keysToRemove.append(key)
        values[key] = (mapCountWords["HAM"].get(
            key), mapCountWords["SPAM"].get(key))
print(values)
for key in keysToRemove:
    mapCountWords["HAM"].pop(key)
    mapCountWords["SPAM"].pop(key)
os.chdir("/mnt/c/Users/Yuri/Documents/projetos/Ia/Email/")
export = open("export.json", 'w')
json_obj = json.dumps(mapCountWords, indent=4)
export.write(json_obj)
export.close()
