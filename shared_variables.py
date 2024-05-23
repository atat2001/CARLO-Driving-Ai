dt = 5  # Time step multiplier (1s real time is dt seconds in simulation)
TIMESTEP  = dt/3000
SIDE_TURN = 0.5
dif_via   = 5.5 # Length diferença entre vias 

MINIMUM_SPEED = -1.5
MAXIMUM_SPEED = 6
THROTTLE      = 6

BREAK_TIME_SQUARED = (MAXIMUM_SPEED*MAXIMUM_SPEED)/(THROTTLE*THROTTLE)

# To make sure it allways has time to break
INTERSECTION_DISTANCE = 900  ## distance to the intersection to start slowing down (consider it squared so 900=30, 400 = 20)
intersections = dict()
roads_to_cars = dict()

# List of Roads
roads = {
    "0": [[20 + dif_via, 3], [20 + dif_via, 48]],
    "1": [[31, 53], [104, 53]],
    "2": [[104, 53 + dif_via], [31, 53 + dif_via]],
    "3": [[20 + dif_via, 64], [20 + dif_via, 117]],
    "4": [[20, 117], [20, 64]],
    "5": [[15, 53 + dif_via], [5, 53 + dif_via]],
    "6": [[1, 53], [15, 53]],
    "7": [[20, 48], [20, 3]],
    "8": [[109.5 + dif_via, 64], [109.5 + dif_via, 111]],
    "9": [[109.5, 111], [109.5, 64]],
    "10": [[31, 122.5], [104, 122.5]],
    "11": [[104, 122.5 + dif_via], [31, 122.5 + dif_via]],
    "12": [[20 + dif_via, 134], [20 + dif_via, 160]],
    "13": [[20, 160], [20, 134]],
    "14": [[31, 166], [104, 166]],
    "15": [[104, 166 + dif_via], [31, 166 + dif_via]],
    "16": [[109.5 + dif_via, 140], [109.5 + dif_via, 160]],
    "17": [[109.5, 160], [109.5, 140]],
    "18": [[172, 112 + dif_via * 4], [121, 112 + dif_via * 4]],
    "19": [[172, 112 + dif_via * 3], [121, 112 + dif_via * 3]],
    "20": [[121, 112 + dif_via * 2], [172, 112 + dif_via * 2]],
    "21": [[121, 112 + dif_via * 1], [172, 112 + dif_via * 1]],
    "22": [[172.5 + dif_via, 111], [172.5 + dif_via, 48]],
    "23": [[172.5 + dif_via * 2, 111], [172.5 + dif_via * 2, 48]],
    "24": [[172.5 + dif_via * 3, 48], [172.5 + dif_via * 3, 111]],
    "25": [[172.5 + dif_via * 4, 48], [172.5 + dif_via * 4, 111]],
    "26": [[200.5, 112 + dif_via], [251.5, 112 + dif_via]],
    "27": [[200.5, 112 + dif_via * 2], [251.5, 112 + dif_via * 2]],
    "28": [[251.5, 112 + dif_via * 3], [200.5, 112 + dif_via * 3]],
    "29": [[251.5, 112 + dif_via * 4], [200.5, 112 + dif_via * 4]],
    "30": [[172.5 + dif_via * 4, 140], [172.5 + dif_via * 4, 155]],
    "31": [[172.5 + dif_via * 3, 140], [172.5 + dif_via * 3, 155]],
    "32": [[172.5 + dif_via * 2, 155], [172.5 + dif_via * 2, 140]],
    "33": [[172.5 + dif_via, 155], [172.5 + dif_via, 140]],
    "34": [[200.5, 156 + dif_via], [251.5, 156 + dif_via]],
    "35": [[200.5, 156 + dif_via * 2], [251.5, 156 + dif_via * 2]],
    "36": [[251.5, 156 + dif_via * 3], [200.5, 156 + dif_via * 3]],
    "37": [[251.5, 156 + dif_via * 4], [200.5, 156 + dif_via * 4]],
    "38": [[252.5 + dif_via, 155], [252.5 + dif_via, 140]],
    "39": [[252.5 + dif_via * 2, 155], [252.5 + dif_via * 2, 140]],
    "40": [[252.5 + dif_via * 3, 140], [252.5 + dif_via * 3, 155]],
    "41": [[252.5 + dif_via * 4, 140], [252.5 + dif_via * 4, 155]],
    "42": [[252.5 + dif_via, 111], [252.5 + dif_via, 48]],
    "43": [[252.5 + dif_via * 2, 111], [252.5 + dif_via * 2, 48]],
    "44": [[252.5 + dif_via * 3, 48], [252.5 + dif_via * 3, 111]],
    "45": [[252.5 + dif_via * 4, 48], [252.5 + dif_via * 4, 111]],
    "46": [[251.5, 19.5 + dif_via * 4], [200.5, 19.5 + dif_via * 4]],
    "47": [[251.5, 19.5 + dif_via * 3], [200.5, 19.5 + dif_via * 3]],
    "48": [[200.5, 19.5 + dif_via * 2], [251.5, 19.5 + dif_via * 2]],
    "49": [[200.5, 19.5 + dif_via], [251.5, 19.5 + dif_via]],
}

# Roads per intersection
road_to_intersection = {
    "0": "1",
    "1": "2",
    "2": "1",
    "3": "3",
    "4": "1",
    "5": "0",
    "6": "1",
    "7": "0",
    "8": "4",
    "9": "2",
    "10": "4",
    "11": "3",
    "12": "5",
    "13": "3",
    "14": "6",
    "15": "5",
    "16": "6",
    "17": "4",
    "18": "4",
    "19": "4",
    "20": "9",
    "21": "9",
    "22": "11",
    "23": "11",
    "24": "9",
    "25": "9",
    "26": "10",
    "27": "10",
    "28": "9",
    "29": "9",
    "30": "7",
    "31": "7",
    "32": "9",
    "33": "9",
    "34": "8",
    "35": "8",
    "36": "7",
    "37": "7",
    "38": "10",
    "39": "10",
    "40": "8",
    "41": "8",
    "42": "12",
    "43": "12",
    "44": "10",
    "45": "10",
    "46": "11",
    "47": "11",
    "48": "12",
    "49": "12",
}

intersection_roads = {
    "1": ["4", "3", "2", "1", "0", "7", "6", "5"],
    "2": ["9", "8", "1", "2"],
    "3": ["13", "12", "11", "10", "3", "4"],
    "4": ["17", "16", "18", "19", "20", "21", "8", "9", "10", "11"],
    "5": ["15", "14", "12", "13"],
    "6": ["16", "17", "14", "15"],
    "7": ["37", "36", "35", "34", "30", "31", "32", "33"],
    "8": ["41", "40", "39", "38", "34", "35", "36", "37"],
    "9": ["33", "32", "31", "30", "29", "28", "27", "26", "25", "24", "23", "22", "21", "20", "19", "18"],
    "10": ["38", "39", "40", "41", "45", "44", "43", "42", "26", "27", "28", "29"],
    "11": ["22", "23", "24", "25", "46", "47", "48", "49"],
    "12": ["42", "43", "44", "45", "49", "48", "47", "46"],
}

intersection_phases = {
    "1": {
        1: [(1, 6), (5, 2), (1, 8), (5, 4)],
        2: [(3, 8), (3, 2), (7, 4), (7, 6)],
        3: [(1, 8), (3, 2), (5, 4), (7, 6)],
        4: [(1, 8), (7, 2), (7, 6)],
        5: [(3, 2), (1, 4), (1, 8)],
        6: [(5, 4), (3, 6), (3, 2)],
        7: [(7, 6), (5, 8), (5, 4)],
        8: [(1, 6), (3, 2), (5, 4)],
        9: [(3, 8), (5, 4), (7, 6)],
        10: [(5, 2), (7, 6), (1, 8)],
        11: [(7, 4), (1, 8), (3, 2)],
    },
    "2": {},
    "3": {
        1: [(1, 6), (5, 2), (5, 4)],
        2: [(1, 6), (3, 2), (5, 4)],
        3: [(1, 6), (1, 4), (3, 2)],
        4: [(3, 6), (5, 4)],
    },
    "4": {
        1: [(1, 10), (1, 8), (1, 5), (3, 2), (7, 6)],
        2: [(3, 2), (4, 10), (7, 6), (9, 8), (9, 5)],
        3: [(1, 10), (3, 2), (7, 6), (9, 8), (9, 5)],
        4: [(1, 10), (7, 6), (9, 8), (9, 5), (9, 2)],
        5: [(1, 10), (3, 2), (7, 6), (9, 8), (9, 5)],
        6: [(1, 10), (1, 8), (7, 6), (7, 2)],
        7: [(3, 2), (4, 10), (4, 8), (7, 6)],
        8: [(7, 6), (7, 2), (7, 10), (9, 8)],
        9: [(1, 10), (7, 6), (7, 2), (9, 8)],
        10: [(1, 10), (1, 8), (3, 2), (7, 6)],
    },
    "5": {},
    "6": {},
    "7": {},
    "8": {},
    "9": {
        1: [(1, 16), (1, 12), (2, 11), (10, 3), (9, 4), (9, 8)],
        2: [(5, 4), (5, 16), (6, 15), (14, 7), (13, 8), (13, 12)],
        3: [(1, 16), (2, 11), (5, 4), (9, 8), (10, 3), (13, 12)],
        4: [(1, 16), (5, 4), (6, 15), (9, 8), (13, 12), (14, 7)],
        5: [(13, 12), (10, 15), (10, 3), (9, 4), (9, 8)],
        6: [(9, 8), (6, 15), (6, 11), (5, 16), (5, 4)],
        7: [(5, 4), (2, 11), (2, 7), (1, 12), (1, 16)],
        8: [(1, 16), (14, 3), (14, 7), (13, 8), (13, 12)],
        9: [(1, 16), (1, 12), (9, 4), (9, 8)],
        10: [(5, 4), (5, 16), (13, 12), (13, 8)],
        11: [(1, 16), (1, 12), (5, 4), (9, 8)],
        12: [(5, 4), (5, 16), (9, 8), (13, 12)],
        13: [(9, 8), (9, 4), (13, 12), (1, 16)],
        14: [(13, 12), (13, 8), (1, 16), (5, 4)],
    },
    "10": {
        1: [(1, 12), (2, 11), (2, 7), (9, 8), (6, 3), (5, 4)],
        2: [(1, 12), (2, 11), (5, 4), (9, 8), (10, 3)],
        3: [(1, 12), (5, 4), (6, 3), (9, 8), (6, 11)],
    },
    "11": {},
    "12": {},
}


paths = [["15", "13", "4", "1"], 
         ["0", "3", "10", "20", "27"], 
         ["17", "9", "2", "3", "12"], 
         ["19","11","12", "14", "17", "19"], 
         ["10","20", "27", "40"], 
         ["8","16", "15", "13", "10", "20", "27"]]

