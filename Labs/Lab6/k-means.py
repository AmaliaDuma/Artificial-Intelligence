import csv
import random
from math import sqrt

from matplotlib import pyplot


def readPoints():
    points = dict()
    with open('dataset.csv') as csv_file:
        csv_file.readline()
        while line := csv_file.readline()[:-1]:
            tokens = line.split(",")
            # tokens[0] -> {A,B,C,D} : label
            # tokens[1], tokens[2] -> val1, val2
            points[(float(tokens[1]), float(tokens[2]))] = tokens[0]
    return points


def dist(x, y):
    # The distance we need to get the nearest centroid
    return (x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2


def nearestCentroid(centroids, point):
    # Nearest centroid for a point.
    # We want to take the centroid such that: dist between the point and the centroid is minimum
    centroid_sol = centroids[0]
    for centroid in centroids[1:]:
        if dist(centroid, point) < dist(centroid_sol, point):
            centroid_sol = centroid
    return centroid_sol


def newCentroids(points, k):
    # We want to re-compute the centroids by moving them in the means of instances associated to it
    # How to recompute:
    #    points prev assigned -> take their vectors and avg them (add them and divide by the nr)
    minX = min([point[0] for point in points])
    maxX = max([point[0] for point in points])
    minY = min([point[1] for point in points])
    maxY = max([point[1] for point in points])
    centroids = [[0, 0] for _ in range(k)]
    centroidsCount = [0 for _ in range(k)]
    for point in points:
        centroidsCount[points[point]] += 1
        centroid = centroids[points[point]]
        centroid[0] += point[0]
        centroid[1] += point[1]
    returnC = []
    for i, centroid in enumerate(centroids):
        if centroidsCount[i] != 0:
            returnC.append((centroid[0] / centroidsCount[i], centroid[1] / centroidsCount[i]))
        else:
            returnC.append((random.random() * (maxX-minX) + minX, random.random() * (maxY-minY) + minY))
    return returnC


def solve(points, k):
    solution = dict()
    minX = min([point[0] for point in points])
    maxX = max([point[0] for point in points])
    minY = min([point[1] for point in points])
    maxY = max([point[1] for point in points])
    centroids = []

    for _ in range(k):
        centroids.append((random.random() * (maxX - minX) + minX, random.random() * (maxY - minY) + minY))

    iterations = 100
    for i in range(iterations):
        for point in points:
            centroid = nearestCentroid(centroids, point)
            solution[point] = centroids.index(centroid)
        if i != iterations-1:
            centroids = newCentroids(solution, k)
    return solution, centroids


def getStats(initialPoints, computedPoints, k):
    stat = [dict() for _ in range(k)]
    for point in initialPoints:
        if initialPoints[point] not in stat[computedPoints[point]]:
            stat[computedPoints[point]][initialPoints[point]] = 0
        stat[computedPoints[point]][initialPoints[point]] += 1
    return stat


def main():
    initialPoints = readPoints()
    colors = ["red", "purple", "blue", "yellow"]
    k = 4
    points, centroids = solve(initialPoints, k)
    stats = getStats(initialPoints, points, k)
    accuracy = sum([max(stat.values()) for stat in stats]) / len(initialPoints)
    print(stats)
    print("Accuracy: ", accuracy)

    for point in points:
        pyplot.scatter(point[0], point[1], color=colors[points[point]])
    for point in centroids:
        pyplot.scatter(point[0], point[1], color="black")
    pyplot.show()


if __name__ == "__main__":
    main()

