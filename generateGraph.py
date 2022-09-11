import matplotlib.pyplot as plt
import json

dictionary = json.load(open('export.json', 'r'))
string = ""
while len(string) == 0:
    op = int(input("1.SPAM\n2.HAM\n"))
    if op == 1:
        string = "SPAM"
    elif op == 2:
        string = "HAM"

dicToListSorted = sorted(dictionary[string].items(), key=lambda x: x[1])
print(dicToListSorted[-6:-1])
sortdict = dict(dicToListSorted[-6:-1])


xAxis = [key for key, value in sortdict.items()]
yAxis = [value for key, value in sortdict.items()]
# xAxis = [key for key, value in simple.items()]
# yAxis = [value for key, value in simple.items()]
plt.grid(True)

## LINE GRAPH ##
plt.plot(xAxis, yAxis, color='maroon', marker='o')
plt.xlabel('Termos')
plt.ylabel('Ocorrencias')

## BAR GRAPH ##
fig = plt.figure()
plt.bar(xAxis, yAxis, color='maroon')
plt.xlabel('variable')
plt.ylabel('value')

plt.show()
plt.savefig(string)
