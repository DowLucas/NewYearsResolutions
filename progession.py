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

def get_sums(x, y):
    xSum = np.sum(x)
    ySum = np.sum(y)
    xySum = np.sum(x*y)
    x2Sum = np.sum(np.power(x, 2))
    return xSum, ySum, xySum, x2Sum

def increaseFunction(x, y, A):
    m, b = line_best_fit(x, y)
    K, T, L, B = get_sums(x, y)
    n = len(x)+1
    S = x[-1]+1
    numerator = (A * m * n * S**2) + (A * m * B * n) - (A * m * S**2) - (2 * A * m * S * K) - (A * m * K**2) - (L * n) + (S * T) + (T * K)
    denom = (n * S - S - K)
    newY = numerator/denom
    return newY


def num_push_ups_tomorrow(x, y, increase_factor=1):
    newY = increaseFunction(x, y, increase_factor)
    return newY


def tryLineBestFit_next_day(x, y, newValue):
    x = np.append(x, x[-1]+1)
    y = np.append(y, newValue)

    line_best_fit(x, y)
    newY = num_push_ups_tomorrow(x, y, 2)
    tryLineBestFit_next_day(x, y, newY)



def line_best_fit(x, y):
    xSum, ySum, xySum, x2Sum = get_sums(x, y)

    b = (ySum*x2Sum - xSum*xySum) / (len(x)*x2Sum - xSum**2)
    m = (len(x)*xySum - xSum*ySum) / (len(x)*x2Sum - xSum**2)

    return m, b

def graph_increase_options(x, y):
    plt.clf()
    As = np.arange(1, 3, 1/100)
    
    Ys = [increaseFunction(x, y, A) for A in As]
    
    plt.plot(As, Ys)
    plt.text(As[0], Ys[-1], f"Minimum to keep positive slope going: {int(Ys[0])}")
    plt.show()


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


    Xs = np.arange(len(arr))
    num_push_ups_tomorrow(Xs, arr, increase_factor=2)
    #tryLineBestFit_next_day(time, arr, 96)
    graph_increase_options(Xs, arr)


data = load()
prog, dates = get_progession("Max Sit-ups", data)


graph_progression(prog, dates, True)

