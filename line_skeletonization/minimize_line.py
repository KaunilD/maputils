import numpy as np
import math
import sys
import json
import cv2
import argparse
import logging

EPSILON = 0.5

def createargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', required = False, type=str)
    parser.add_argument('--driver', required = False, type=int)
    args = parser.parse_args()
    return args

def preparelogger():
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)

def dist(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def perpendicular_distance(point, p1, p2):
    point = [point[0], point[1]]
    p1 = [p1[0], p1[1]]
    p2 = [p2[0], p2[1]]
    if (p1 == p2):
        return dist(point, p1)
    else:
        n = abs((p2[0] - p1[0]) * (p1[1] - point[1]) - (p1[0] - point[0]) * (p2[1] - p1[1]))
        d = math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
        return n / d

""" stupid stact overflow """
def minimize_line_iter(line, eps, mask):
    stack = []
    stack.append([0, len(line)-1])
    while(stack):
        start, end = stack.pop()
        dmax = 0.0
        index = start
        for idx in range(index+1, end):
            d = perpendicular_distance(line[idx], line[start], line[end])
            if d > dmax:
                dmax = d
                index = idx
        if dmax >= eps:
            stack.append((start, index))
            stack.append((index, end))
    # always include line endpoints
    mask[start] = 1
    mask[end] = 1

def minimize(points, eps):
    mask = np.zeros((len(points)), dtype=np.uint8)
    minimize_line_iter(points, eps, mask)
    return [points[idx] for idx, ival in enumerate(mask) if mask[idx] > 0]

def prepareimage(width, height):
    return np.zeros((width, height))

def main():
    args = createargs()
    if args.driver == 1:
        driver()
    else:
        preparelogger()
        logging.info('Reading JSON')
        data = json.load(open(args.json, 'r'))
        roads = data[1]
        newroads = {}
        for i in roads:
            road = roads[i]
            newroads[i] = minimize(road, epsilon)
        data[1] = newroads
        json.dump(data, open("minified.json", 'w'))
        return data

def driver():
    line = [[1, 1], [2, 2], [3, 3], [4, 4]]
    print(minimize(line, EPSILON))


if __name__ == '__main__':
  main()
