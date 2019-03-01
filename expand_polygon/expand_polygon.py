import math
import numpy as np
import logging
import argparse


def get_parallel_at_distance_d(p1, p2, d):
    v = p1 - p2
    v = v/np.linalg.norm(v, ord=2)
    v *= d
    return np.asarray([-v[1], v[0]])


def lines_intersect(p1, p2, p3, p4):
    dx12 = p2[0] - p1[0]
    dy12 = p2[1] - p1[1]
    dx34 = p4[0] - p3[0]
    dy34 = p4[1] - p3[1]

    den = (dy12 * dx34 - dx12 * dy34)
    t1 = ((p1[0] - p3[0])*dy34 + (p3[1] - p1[1]) * dx34)/den;

    if t1 == math.inf:
        l_intersect = False
        seg_intersect = False
        intersection = None
        return l, seg_intersect, intersection
    l_intersect = True
    t2 = ((p3[0] - p1[0]) * dy12 + (p1[1] - p3[1]) * dx12)/-den;
    intersection = [int(p1[0]+dx12*t1), int(p1[1]+dy12*t1)]
    seg_intersect = ((t1>=0) and (t1 <= 1) and (t2 >= 0) and (t2 <=1))
    return l_intersect, seg_intersect, intersection


def expand_polygon(polygon, euc_dist):
    new_poly = []
    num_points = len(polygon)
    for j in range(num_points):
        i = j-1
        if i < 0:
            i+=num_points
        k = (j+1) % num_points

        # unit vector in direction of 1st egde
        # normal to the edge.
        n1 = get_parallel_at_distance_d(polygon[j], polygon[i], distance)

        pij1 = polygon[i] + n1
        pij2 = polygon[j] + n1

        # repeat for second edge
        n2 = get_parallel_at_distance_d(polygon[k], polygon[j], distance)

        pjk1 = polygon[j] + n2
        pjk2 = polygon[k] + n2

        # get point of intersection for the 2 edges parallel to the original
        # edge at distance "euc_dist"
        l_intersect, seg_intersect, intersection = lines_intersect(
            pij1, pij2, pjk1, pjk2
        )
        new_poly.append(intersection)
    #profit.
    return new_poly

def main(polygon):
    args = createargs()
    if args.driver == 1:
        driver()
    else:
        polygon = json.load(open(args.json, 'r'))
        euc_dist = args.distance
        expand_polygon(polygon, euc_dist)

def driver():
    polygon = []
    euc_dist = 10
    return expand_polygon(polygon, euc_dist)

if __name__ == '__main__':
    main()
