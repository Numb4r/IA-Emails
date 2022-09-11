import matplotlib.pyplot as plt
import json
import pandas as pd

dictionary = json.load(open('export.json', 'r'))
string = ""
while len(string) == 0:
    op = int(input("1.SPAM\n2.HAM\n"))
    if op == 1:
        string = "SPAM"
    elif op == 2:
        string = "HAM"

boxplot = False
while True:
    op = int(input("1.Grafico barra\n2.Boxplot\n"))
    if op == 1:
        break
    elif op == 2:
        boxplot = True
        break


dicToListSorted = sorted(dictionary[string].items(), key=lambda x: x[1])

if not boxplot:
    # print(dicToListSorted[-6:])
    sortdict = dict(dicToListSorted[-6:])
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
    print(dicToListSorted)
    df = pd.DataFrame(
        [value for _, value in dict(dicToListSorted).items()], columns=['A1'])
    boxplot = df.boxplot(column=['A1'], grid=True)
    boxplot.get_figure().savefig(string+"boxplot")
else:
    cemMelhores = dict(dicToListSorted[-6:])
    p = [value for _, value in cemMelhores.items()]
    print(p)
    plt.boxplot(p)
    # plt.ylim([0, 0.005])
    plt.savefig(string+"boxplot")
