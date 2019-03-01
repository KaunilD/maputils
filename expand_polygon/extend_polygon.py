import math
import numpy as np
import logging
import argparse

def get_intersection(l1, l2):
    raise NotImplementedError()

def extend_polygon(polygon, euc_dist):
    raise NotImplementedError()

def main(polygon):
    args = createargs()
    if args.driver == 1:
        driver()
    else:
        polygon = json.load(open(args.json, 'r'))
        euc_dist = args.distance
        extend_polygon(polygon, euc_dist)

def driver():
    polygon = []
    euc_dist = 10
    return extend_polygon(polygon, euc_dist)

if __name__ == '__main__':
    main()
