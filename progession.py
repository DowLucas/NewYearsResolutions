import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style
style.use("ggplot")


json_path = "JSON/main.json"


def load():
    return json.load(open(json_path, "r"))

def get_progession(property, data):

    data = data["Entries"]
    dates = []
    progression = {property: []}

    for item in data.items():
        dates.append(item[0][:-5])
        itemData = item[1]

        if property in itemData.keys():
            value = itemData[property]
        else:
            continue

        try:
            value = int(value)
        except:
            if value == "no":
                value = 0
            elif value == "yes":
                value = 1
            else:
                value = 0
        progression[property].append(value)



    
    return progression, dates

def line_best_fit(x, y):
    print(x, y)

    xHat = sum(x)/len(x)
    yHat = sum(y)/len(y)

    numertator = sum((x-xHat)*(y-yHat))
    denom = np.sum(np.power(x-xHat, 2))

    m = numertator/denom
    b = yHat - m*xHat


    print(m, b)

    return m, b

def graph_progression(progression_dict, dates, see_future = False):

    property = list(progression_dict.keys())[0]
    arr = np.array(progression_dict[property])

    time = np.arange(len(arr))
    plt.scatter(time, arr)
    plt.xlabel("Date")
    plt.ylabel(property)


    m, b = line_best_fit(time, arr)


    if see_future:
        time = np.arange(len(time)+30)
        plt.plot(time, [m*x + b for x in time], c="k", label="line of best fit")
        extra = ['' for x in range(30)]
        dates.extend(extra)
        plt.xticks(time, dates, rotation=90)
        plt.title("Displaying progress and predicted results after 30 days")
    else:
        plt.plot(time, [m*x + b for x in time], c="k", label="line of best fit")
        plt.xticks(time, dates, rotation=90)
        plt.title("Progress since start and general trend")

    plt.show()
    

data = load()
prog, dates = get_progession("Sit-ups", data)


graph_progression(prog, dates, True)

