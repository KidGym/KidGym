
from enum import IntEnum


# Fixed Path

IMG_BASE_PATH = './imgs'
OBJ_ID_IMG_PATH = './imgs/id/obj_numbers'
BAG_ID_IMG_PATH = './imgs/id/bag_letters'
AGENT_IMG_PATH = './imgs/agent/agent.png'
AGENT_DIR_IMG_PATH = './imgs/agent/direction'

TEMPLATE_JSON_PATH = './jsons/template.json'

TILE_PIXEL = 64
ID_IMG_PIXEL = 16

RESOLUTION = (576, 576)

GRID_SIZE = 5

BAG_SIZE = 4
BAG_IMG_OFFSET = (10, 0)
BAG_IMG_PADDING = 12
BAG_IDS = "ABCD"

MAX_STEP = 10

JSON_PATH = './jsons'

NUMBER_TO_LETTER = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
}

LETTER_TO_NUMBER = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
}

DIR_TO_POS = {
    0: (0, 1), # down
    1: (1, 0),  # right
    2: (0, -1),  # up
    3: (-1, 0), # left
}

POS_TO_DIR = {
    (0, 1): 0, # down
    (1, 0): 1, # right
    (0, -1): 2, # up
    (-1, 0): 3 # left
}


class ACTION(IntEnum):
    # down/right/up/left
    DOWN = 0
    RIGHT = 1
    UP = 2
    LEFT = 3
    # rotate clockwise
    ROTATE = 4
    # pick
    PICK = 5
    # drop A/B/C/D
    DROP_A = 6
    DROP_B = 7
    DROP_C = 8
    DROP_D = 9
    

TYPES = ['animal', 'fruit', 'food', 'toy']
COUNTING_TYPES = ['fruit', 'food']
SEQUENCE_TYPE = "maze"
DECODE_TYPE = "mixed"
PUZZLE_TYPE = "figure"
FILLING_TYPE = "figure"

ORIENTATION_4 = ["north", "south", "west", "east"]
ORIENTATION_8 = ["north", "south", "west", "east", "northwest", "northeast", "southwest", "southeast"]
DIRECTION = ["clockwise", "anticlockwise"]

RESOURCE = {
    "animal": {"resources": ["cat", "chick", "cow", "dog", "elephant", 
                             "giraffe", "horse", "monkey", "mouse", "pig", 
                             "rabbit", "sheep", "snail", "tortoise"],
               "pieces": [["cat_1", "cat_2", "cat_3", "cat_4"],
                          ["chick_1", "chick_2", "chick_3", "chick_4"],
                          ["cow_1", "cow_2", "cow_3", "cow_4"],
                          ["dog_1", "dog_2", "dog_3", "dog_4"],
                          ["elephant_1", "elephant_2", "elephant_3", "elephant_4"],
                        #   ["griaffe_1", "griaffe_2", "griaffe_3", "griaffe_4"],
                          ["goldfish_1", "goldfish_2", "goldfish_3", "goldfish_4"],
                        #   ["hourse_1", "hourse_2", "hourse_3", "hourse_4"],
                          ["monkey_1", "monkey_2", "monkey_3", "monkey_4"],
                          ["pig_1", "pig_2", "pig_3", "pig_4"],
                        #   ["rabbit_1", "rabbit_2", "rabbit_3", "rabbit_4"],
                          ["sheep_1", "sheep_2", "sheep_3", "sheep_4"],
                          ["tortoise_1", "tortoise_2", "tortoise_3", "tortoise_4"]],
               "all_pieces": ["cat_1", "cat_2", "cat_3", "cat_4", "chick_1", "chick_2", "chick_3", "chick_4", "cow_1", "cow_2", "cow_3", "cow_4", "dog_1", "dog_2", "dog_3", "dog_4", "elephant_1", "elephant_2", "elephant_3", "elephant_4", "goldfish_1", "goldfish_2", "goldfish_3", "goldfish_4", "monkey_1", "monkey_2", "monkey_3", "monkey_4", "pig_1", "pig_2", "pig_3", "pig_4", "sheep_1", "sheep_2", "sheep_3", "sheep_4", "tortoise_1", "tortoise_2", "tortoise_3", "tortoise_4"],
               "background": "farm"},
    
    "fruit": {"resources": ["apple", "banana", "cherry", "grape", "kiwifruit",
                            "lemon", "orange", "peach", "pineapple", "strawberry",
                            "watermelon"],
              "counting_resourses": ["apple", "lemon", "orange", "strawberry", "watermelon"],
              "background": "shop"},
              
    "food": {"resources": ["cake", "chicken_leg", "egg", "hamburger", "hotdog",
                           "pizza", "sandwich", "sushi"],
             "counting_resourses": ["cake", "egg", "hamburger", "pizza", "sushi"],
             "background": "canteen"},

    "toy": {"resources": ["badminton", "balloon", "basketball", "diamond", "doll",
                          "football", "kite", "toy_ball", "toy_bear", "toy_car",
                          "toy_plane", "toy_train"],
            "background": "toy_house"},
    
    "tool": {"basket": ["blue", "green", "red", "yellow"],
             "door": ["blue", "red", "yellow"],
             "key": ["blue", "red", "yellow"],
             "puzzle": ["puzzle_piece_r_1", "puzzle_piece_r_2", "puzzle_piece_r_3", "puzzle_piece_r_4"]},
    
    "mixed": {"background": "park"},
    "figure": {"background": "gallery"},
    "maze": {"resources": "wall",
             "background": "maze"},
    "roman": {"resources": ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]}
    }
