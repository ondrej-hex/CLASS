# ////////////////////////////////////////////////////////////////////////
# ███████▀▀█   █▀▀█           ████████████    █████████████████████▀▀█
# ██    █▄▄█   █▄▄█           ██        ██    ██            ██    █▄▄█
# ██            ██            ██        ██    ██            ██
# ██            ██            ████████████    ██████████    ██████████
# ██            ██            ██        ██            ██            ██
# ██            ██            ██        ██            ██    █▀▀█    ██
# ██████████████████████████████        ████████████████    █▄▄███████
# CIRCUIT ///// LEARNING /// AND //////////// SIMULATION //// SOFTWARE ///

import msvcrt, os, time, random

# for base app
DEFAULT_WINDOW_WIDTH = 120

# for game in app
DEF_VIEW_X = 100 #-40     
DEF_VIEW_Y = 30  #-10
BFS_PATHFINDING = True



############### Base app classes ###############

class Proposition_complex:
    # each complex proposition is made of other propositions (simple or complex) and a single symbol
    def __init__(self, propositions, symbol): # (a or b or c); (b and c and d); ...
        self.propositions = propositions
        self.symbol = symbol

    # returns a string of this complex proposition, including all under it
    def str(self):
        string = "("

        # handle Negation   (the only unary operation, which also has its symbol in front not in between)
        if(self.symbol == '¬'):
            string += '¬'

            for prop in self.propositions:
                if(type(prop) == str):
                    string += prop
                elif(type(prop) == Proposition_complex):
                    string += prop.str()
                else:
                    print("failed to stringify...")
            string += ')'
            return string
            
        # handle the rest of the operations
        for prop in self.propositions:

            # varibale or value (A, B, C, true, false, ...)
            if(type(prop) == str):
                string += prop + ' ' + self.symbol + ' '

            # deeper proposition (handled recursively)
            elif(type(prop) == Proposition_complex):
                string += prop.str() + ' ' + self.symbol + ' '
                
            else:
                print("failed to stringify...")
        
        string = string[:-3] + ')'
        return string

    # returns a single list of all used variables in this complex proposition and all under it
    def variables(self):
        variables = []
        for prop in self.propositions:
            if(type(prop) == str):
                if(not(prop in variables)):
                    variables.append(prop)
            elif(type(prop) == Proposition_complex):
                prop_vars = prop.variables()
                for var in prop_vars:
                    if(not(var in variables)):
                        variables.append(var)
            else:
                print("failed to retrieve variables...")
        return(variables)
    

class Button:
    # each complex proposition is made of other propositions (simple or complex) and a single symbol
    def __init__(self, text, length = 0): # (a or b or c); (b and c and d); ...
        if(length <= 0):
            self.length = len(text)
        else:
            self.length = length

        self.text = text

    def str(self, lit = False):
        if(lit):
            char = '█'
        else:
            char = '░'

        button_str_arr = [char*(self.length + 4)]
        button_str_arr.append(char + " "*(self.length + 2) + char)
        button_str_arr.append(char + " "*int((self.length + 2 - len(self.text)) / 2 + 0.5) + self.text + " "*int((self.length + 2 - len(self.text)) / 2) + char)
        button_str_arr.append(char + " "*(self.length + 2) + char)
        button_str_arr.append(char*(self.length + 4))

        return(button_str_arr)



############### Game classes ###############

class Player:
    def __init__(self, x, y): # (a or b or c); (b and c and d); ...
        self.x = x
        self.y = y

        self.max_hp = 10
        self.hp = self.max_hp
        self.max_stamina = 100
        self.stamina = self.max_stamina

        self.falling = False
        self.upping = False
        
        self.texture_frame = 0
        self.texture = [
            [
            " ▄▄▄ ",
            "█▀█▀█",
            "██▀██",
            " █▀█ ",
            " █ █ "
            ],[
            " ▄▄▄ ",
            "█▀█▀█",
            "██▀██",
            "  ██ ",
            "  ▀█ "
            ],[
            " ▄▄▄ ",
            "█▀█▀█",
            "██▀██",
            "  ██ ",
            "  █▀ "
            ],[
            " ▄▄▄ ",
            "█▀█▀█",
            "██▀██",
            " █▀█ ",
            " █ █ "
            ]]
        
        self.texture_roll = [
            [
            "▄███▄",
            "█▄█▄█",
            "▀█▄█▀"
            ],[
            "▄█▀█▄",
            "█▀█▀█",
            "▀███▀"
            ]
        ]

        self.texture_up = [
            [
            " ▄▄▄ ",
            "█▀█▀█",
            "██▀██",
            " █▀█ ",
            "█  █ "
            ],[
            " ▄▄▄ ",
            "█▀█▀█",
            "██▀██",
            "  ██ ",
            "  █ █"
            ],[
            " ▄▄▄ ",
            "█▀█▀█",
            "██▀██",
            "  ██ ",
            "  ██ "
            ],[
            " ▄▄▄ ",
            "█▀█▀█",
            "██▀██",
            " █▀█ ",
            " ██  "
            ]]
        
        self.texture_down = [
            [
            " █  █",
            " █▄█ ",
            "██▄██",
            "█▄█▄█",
            " ▀▀▀ "
            ],[
            "█ █  ",
            " ██  ",
            "██▄██",
            "█▄█▄█",
            " ▀▀▀ "
            ],[
            " ██  ",
            " ██  ",
            "██▄██",
            "█▄█▄█",
            " ▀▀▀ "
            ],[
            " █ █ ",
            " █▄█ ",
            "██▄██",
            "█▄█▄█",
            " ▀▀▀ "
            ]]

        self.texture_crouch = [
        "▄███▄",
        "█████",
        "▀███▀"
        ]

        self.texture_shadows = [
            [
            " ███ ",
            "█████",
            " ███ "
            ],[
            " ▓▓▓ ",
            "▓▓▓▓▓",
            " ▓▓▓ "
            ],[
            " ▒▒▒ ",
            "▒▒▒▒▒",
            " ▒▒▒ "
            ],[
            " ░░░ ",
            "░░░░░",
            " ░░░ "
            ]]


        self.view_x = DEF_VIEW_X
        self.view_y = DEF_VIEW_Y

        self.g_vel = 0

        self.roll_steps = 0
        self.last_x_dir = 0

        self.last_step_ts = 0

        self.last_blink_ts = 0
        self.blink = False

        self.crouch = True

        self.inventory = {"0":20, "1":20, "True":2, "False":2, "Rune":4}

        self.fly = False

        self.nightmare_vision = False


class Breakable:
    def __init__(self, x, y, texture, items):
        self.x = x
        self.y = y
        self.texture = texture
        self.items = items
        self.present = True
        self.frame = 0
        self.anim_timer = 0

class Unbreakable:
    def __init__(self, x, y, texture, items):
        self.x = x
        self.y = y
        self.texture = texture
        self.items = items
        self.present = True
        self.frame = 0
        self.anim_timer = 0


class NPC:
    def __init__(self, x, y, texture, texture_walk, dialoges):
        self.x = x
        self.y = y
        self.texture = texture
        self.texture_walk = texture_walk
        self.texture_frame = 0

        self.dialoges = dialoges
        self.dialog = random.choice(dialoges)
        self.dialoge_part = -1
        self.dialoge_charnum = 0

        self.following = False
        self.moving = False
        self.stop_dist = 10 + random.randint(0, 15)

        self.g_vel = 0
        self.g_timer = time.perf_counter()

        self.bfs_path = []
        self.bfs_reload_timer = time.perf_counter()


class Interactable:
    def __init__(self, x, y, texture, price, reward, minigame):
        self.x = x
        self.y = y
        self.texture = texture
        self.texture_frame = 0

        self.price = price
        self.reward = reward
        self.minigame = minigame# can be None

class Effect:
    def __init__(self, x, y, texture, death_ts):
        self.x = x
        self.y = y
        self.texture = texture
        self.texture_frame = 0
        self.death_ts = death_ts
        self.dir_x = random.randint(0, 1)*2-1

class Enemy:
    def __init__(self, x, y, texture, texture_walk, texture_ragdoll, texture_crouch, hp):
        self.x = x
        self.y = y
        self.texture = texture
        self.texture_walk = texture_walk
        self.texture_frame = 0
        self.hp = 100

        self.following = False
        self.moving = False
        self.stop_dist = -1

        self.g_vel = 0
        self.g_timer = time.perf_counter()

        self.texture_ragdoll = texture_ragdoll
        self.texture_crouch = texture_crouch
        self.ragdoll_frame = 0
        self.knockout_frame = 0
        self.ragdoll_dir = 1
        self.hp = hp

        self.bfs_path = []
        self.bfs_reload_timer = time.perf_counter()

class BFS_node:
    def __init__(self, x, y, parent = None):
        self.x = x
        self.y = y
        self.parent = parent

class Dungeon_tile:
    def __init__(self, x, y, type): # (a or b or c); (b and c and d); ...
        self.x = x # before precalculating to actual coords => row, column (x: 1 per tile; y: 1 per floor)
        self.y = y
        self.type = type 
        self.exits = {
            "left":False,
            "right":False,
            "top_left":False,
            "top_center":False,
            "top_right":False,
            "bottom_left":False,
            "bottom_center":False,
            "bottom_right":False
        }
        self.revealed = False

class Control_object:
    def __init__(self, x, y):
        self.x = x
        self.y = y



############### Base assets ###############

logo_anim = [
"////////////////////////////////////////////////////////////////////////",
"░░░░░░█▀▀█   █▀▀█           ░░░░░░░░░░░░    ░░░░░░░░░░░░░░░░░░░░█▀▀█    ",
"░░    █▄▄█   █▄▄█           ░░        ░░    ░░            ░░    █▄▄█    ",
"░░            ░░            ░░        ░░    ░░            ░░            ",
"░░            ░░            ░░░░░░░░░░░░    ░░░░░░░░░░    ░░░░░░░░░░    ",
"░░            ░░            ░░        ░░            ░░            ░░    ",
"░░            ░░            ░░        ░░            ░░    █▀▀█    ░░    ",
"░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░        ░░░░░░░░░░░░░░░░    █▄▄█░░░░░░    ",
"CIRCUIT ///// LEARNING //////// AND /////// SIMULATION //// SOFTWARE ///"
]

#guidebook context
guidebook = {
    
    "Propositions":
    [
        "(To turn pages in the guidebook, use left and right arrowkeys)",
        "(To scroll through a page in the guidebook, use up and down arrowkeys)",
        "----------------------------------------------------------------------",
        "",
        "",
        "",
        "",
        "Foreword",
        "========",
        "Logic is the study of formal reasoning.",
        "It allows us to take complex ideas and break them down into simple, mathematical structures to see if they make sense.",
        "In this app, we use 'Propositional Logic - the foundation of computer science and more.",
        "",
        "",
        "",
        "",
        "Propositions",
        "============",
        "What is a Proposition?",
        "A proposition is a statement that is either True or False. It cannot be both, and it cannot be neither.",
        "In computer science, where we talk about binary logic, we use propositions aswell.",
        "In this system, we use Binary to represent these values:",
        " - True is represented by the number 1 (High/On).",
        " - False is represented by the number 0 (Low/Off).",
        "",
        "",
        "Examples of Propositions:",
        " - ''Ada Lovelace was the worlds first programmer'' (True)",
        " - ''Python is my favourite programming language'' (False)",
        "",
        "",
        "Some additional terms: ",
        "Tautology: A statement which is always True, regardless of input.",
        "Contradiction: A statement which is always False, regardless of input.",
        "",
        "",
        "",
        "",
        "Variables",
        "=========",
        "In logic, we use letters like 'a', 'b', or 'p' to represent these propositions.",
        "By using letters instead of words, we can focus on the structure of the argument rather than the specific topic.",
        "This is called 'Abstraction'.",
        "",
        "",
        "Examples: ",
        " - ''I am hungry and thirsty''  becomes  (a ∧ b).",
        " - ''If it rains, then the ground is wet''  becomes  (a → b).",
        " - ''The sun is rising, or there was an atomic blast.''  becomes  (a ∨ b).",
        "",
        "",
        "",
        "",
        "Operators",
        "=========",
        "To connect these variables into compound propositions, we use operators.",
        "Simmilar to mathematics but working with binary logic",
        "",
        "",
        " - NOT (¬): Negation 'flips' the value such that True becomes False and vice versa.",
        " - AND (∧): Conjunction is True only when ALL propositions are True.",
        " - OR  (∨): Disjunction is True if at least ONE proposition is True.",
        " - XOR (⊻): Exclusive Or is True when exactly one proposition is True.",
        " - Implication (→) can only be False if the first proposition is True, but the second one is False.",
        " - Biconditional implication (↔) is True if both sides have the same value",
        "",
        " - Logical equivalence (≡) is used when two compound propositions are equivalent."
        "",
        "",
        "Order of Operations (Precedence):",
        "Just like math, logic has an order: Parentheses first, then NOT, AND, OR, XOR, Implications and finally Biconditionals.",
        "Examples with brackets in the same order as natural precedence: ",
        " - (a ∨ (b ∧ c))"
        " - (a ∨ (¬ b) ∨ (¬ c))"
        " - (a ∨ (b ∧ (¬ c)))"
    ],

    "Equations":
    [
        "Equations",
        "=========",
        "An equation is a string of variables and operators.",
        "To solve an equation, we replace the variables with True or False.",
        "",
        "",
        "Evaluation Process:",
        "Step 1: Assign values to variables (e.g., a = True, b = False).",
        "Step 2: Follow the Precedence rules (Parentheses first, etc.).",
        "Step 3: Calculate the final result (True or False).",
        "",
        "",
        "Examples: ",
        "(a = True, b = False, c = True)"
        " - (a ∨ (b ∧ c))  =>  (True ∨ (False ∧ True))  ≡  (True ∨ False)  ≡  True",
        " - (a ∨ (¬ b) ∨ (¬ c))  =>  (True ∨ (¬ False) ∨ (¬ True))  ≡  (True ∨ True ∨ False)  ≡ True",
        " - (a → b)  =>  (True → False)  ≡  False",
        "",
        "",
        "",
        "",
        "",
        "",
        "Simplification:",
        "===============",
        "Before we even start solving more complex equations, there are some laws (rules) which we can use to simplify them."
        "",
        "",
        "",
        "",
        "Basic laws",
        "----------",
        "Double negation Law: (¬(¬A)) ≡ A",
        "",
        "Idempotency Law: (A ∨ A) ≡ A",
        "                 (A ∧ A) ≡ A",
        "",
        "Inverse (Complement) Laws: (A ∨ ¬A) ≡ True",
        "                           (A ∧ ¬A) ≡ False",
        "",
        "",
        "",
        "",
        "Null and Identity laws",
        "----------------------",
        "Identity Laws: (A ∨ False) ≡ A",
        "               (A ∧ True) ≡ A",
        "",
        "Null (domination) laws: (A ∨ True) ≡ True",
        "                        (A ∧ False) ≡ False",
        "",
        "",
        "",
        "",
        "Grouping and Distribution Laws",
        "------------------------------",
        "Associative Laws: (A ∨ (B ∨ C)) ≡ (A ∨ B ∨ C)",
        "                  (A ∧ (B ∧ C)) ≡ (A ∧ B ∧ C)",
        "",
        "Distributive Laws: A ∧ (B ∨ C) ≡ (A ∧ B) ∨ (A ∧ C)",
        "                   A ∨ (B ∧ C) ≡ (A ∨ B) ∧ (A ∨ C)",
        "",
        "Absorption Laws: A ∨ (A ∧ B) ≡ A",
        "                 A ∧ (A ∨ B) ≡ A",
        "",
        "",
        "",
        "",
        "De Morgan's Laws",
        "----------------",
        "Negation of AND: ¬(A ∧ B) ≡ (¬A ∨ ¬B)",
        "Negation of OR:  ¬(A ∨ B) ≡ (¬A ∧ ¬B)",
        "",
        "",
        "",
        "",
        "Rewriting rules",
        "---------------",
        "Implication Law: (a → b) ≡ (¬a ∨ b)",
        "",
        "Biconditional Law: (a ↔ b) ≡ (a ∧ b) ∨ (¬a ∧ ¬b)",
        "",
        "XOR Definition: (a ⊻ b) ≡ (a ∨ b) ∧ (¬a ∨ ¬b)"
    ],

    "Truth Tables":
    [
        "Truth Tables",
        "============",
        "A Truth Table is a mathematical table used to determine if a compound proposition is True or False for all possible input values.",
        "It acts as a 'Logic Map' for an equation.",
        "",
        "",
        "How to read a Truth Table:",
        " - The left columns show every possible combination of True (1) and False (0) for given variables.",
        " - The rightmost column shows the final result of the equation for that specific row.",
        "",
        "",
        "Table Size:",
        "The number of rows is determined by the number of variables (n).",
        "The number of rows = 2^n",
        " - 1 Variable (a): 2 rows",
        " - 2 Variables (a, b): 4 rows",
        " - 3 Variables (a, b, c): 8 rows",
        "",
        "",
        "Basic Truth Table Examples:",
        "",
        "AND (∧) Table:        OR (∨) Table:",
        "| a | b | Result |    | a | b | Result |",
        "|---|---|--------|    |---|---|--------|",
        "| 0 | 0 |   0    |    | 0 | 0 |   0    |",
        "| 0 | 1 |   0    |    | 0 | 1 |   1    |",
        "| 1 | 0 |   0    |    | 1 | 0 |   1    |",
        "| 1 | 1 |   1    |    | 1 | 1 |   1    |",
        "",
        ""
    ],

    "Logic gates":
    [
        "TBD..."
    ],
}



############### Game assets ###############

# game map as a single string. /n marks a different y coord. all values will be dynamically changed to account for a map of any size and structure etc...  Objects will be marked with "[P]" - P = player
game_map_preset = '''













             
             
             
             
             
             
             
             
             
             
                                                                                                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               [B]                             
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           ▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓    
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               ▓▓  ▓▓                 ▒▒ ▓▓▓   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ▓▓ ▓▓                ▒▒  ▓▓▓▓  
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 ▓▓▓▓               ▒▒   ▓▓▓▓▓ 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  ▓▓▓              ▒▒    ▓▓▓▓▓▓
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   ▓▓             ▒▒     ▓▓▓▓▓▓▓
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   ▓▓            ▒▒      ▓▓▓▓▓▓▓▓
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   ▓▓           ▒▒       ▓▓▓▓▓▓▓▓▓
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   ▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   ▓▓ ▒▒                 ▓▓▓▓▓▓▓▓▓▓▓  
▓                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  ▓▓  ▒▒                ▓▓▓▓▓▓▓▓▓▓▓▓    
▓                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  ▓▓   ▒▒               ▓▓▓▓▓▓▓▓▓▓▓▓▓    
▓                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  ▓▓    ▒▒              ▓▓▓▓▓▓▓▓▓▓▓▓▓▓    
▓                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  ▓▓     ▒▒             ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                                                                      ▓▓▒▒▒▒▒▒                                                          
▓                                                                                                                                                                                                                                                                                                                                                                                                                                           ▓▓                                                                                                     ▓▓      ▒▒            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                                                                     ▓▓ ▒▒▒▒
▓                                                                                                                                                                                                                                                                                                                                                                                                                                           ▓▓             [B]                                                                                     ▓▓       ▒▒           ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                 [2]                                                ▓▓  ▒▒                                                          [3]
▓                                                                                                                                                                                                                                                                                                                                                                                                                                           ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓                                                    ▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ▒▒                          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓                                                                                                                                                                                                                                                                                                                                                                                                                                           ▓▓                                             ▓▓▓▓                                                    ▓▓                 ▒▒ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ▒▒                          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓                                                                                                                                                                                                                                                                                                                                                                                                                                           ▓▓                                            ▓▓▓▓▓                                                    ▓▓                ▒▒  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ▒▒▒▒                         ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        ▓▓▓▓▓▓                                                                     ▒▒   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ▒▒                          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       ▓▓▓▓▓▓▓▓▓                                                                  ▒▒    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ▒▒
▓                                                                                                                                                                                                                                                                                                                                                                                                                  ▓▓▓                                                                 ▓▓▓▓▓▓▓▓▓▓                                                                 ▒▒     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ▒▒
▓                                                                                                                                                                                                                                                                                                                                                                                                                  ▓▓▓                                                                ▓▓▓▓▓▓▓▓▓▓▓                                                                ▒▒      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ▒▒▒▒
▓                      [B]            [B]               [B]                                                      [4]                                                        [B]                                                                 [1]                                                                                                                                            [B]                 ▓▓▓                                                               ▓▓▓▓▓▓▓▓▓▓▓▓                                        [B]                    ▒▒       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ▒▒
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓             [P]                                                                                             ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ▒▒
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                             [B]                                  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ▒▒
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ▒▒▒▒
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ▒▒
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ▒▒
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ▒▒
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ▒▒▒▒
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ▒▒
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ▒▒
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ▒▒
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ▒▒▒▒
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ▒▒
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ▒▒
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ▒▒
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ▒▒▒▒
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ▒▒
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ▒▒
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ▒▒
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ▒▒▒▒
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ▒▒
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    
'''

Dungeon_map_presets = {
"basic":
'''
▓▓▓▓▓▓????????????▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓????????????▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓????????????▓▓▓▓▓▓
▓▓▓▓▓▓                                                                                                                    ▓▓▓▓▓▓
▓▓▓▓▓▓                                                                                                                    ▓▓▓▓▓▓
▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒                                        ▒▒▒▒▒▒▒▒▒▒▒▒                                        ▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓
▓▓▓▓▓▓                                                                                                                    ▓▓▓▓▓▓
▓▓▓▓▓▓                                                                                                                    ▓▓▓▓▓▓
▓▓▓▓▓▓▒▒▒▒                                                    ▒▒▒▒                                                    ▒▒▒▒▓▓▓▓▓▓
▓▓▓▓▓▓                                                                                                                    ▓▓▓▓▓▓
▓▓▓▓▓▓                             [B]                                          [B]               [B]                     ▓▓▓▓▓▓
▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓
▓▓                                                                                                                            ▓▓
?                                                                                                                              ?
?                                                                                                                              ?
?                                 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                                 ?
?                             ▒▒▒▒▒▒                                                        ▒▒▒▒▒▒                             ?
?                         ▒▒▒▒▒▒                                                                ▒▒▒▒▒▒                         ?
?                     ▒▒▒▒▒▒                                                                        ▒▒▒▒▒▒                     ?
?       [B]       ▒▒▒▒▒▒                                                                                ▒▒▒▒▒▒                 ?
▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓
▓▓▓▓▓▓            ▒▒                 ▒▒                 ▒▒            ▒▒                  ▒▒                ▒▒            ▓▓▓▓▓▓
▓▓▓▓▓▓            ▒▒                 ▒▒                 ▒▒            ▒▒                  ▒▒                ▒▒            ▓▓▓▓▓▓
▓▓▓▓▓▓????????????▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓????????????▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓????????????▓▓▓▓▓▓
''',

"hallway_1":
'''
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
?                                                                                                                              ?
?                                                                                                                              ?
?                                                                                                                              ?
?                                                                                                                              ?
?                                                                                                                              ?
?                                                                                                                              ?
?                                                                                                                              ?
?                            [B]                                       [B]               [B]                                   ?
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
''',

"hallway_2":
'''
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     [B]                   [B]         [B]      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
?                                                                                                                              ?
?                                                                                                                              ?
?                                                              ▒▒▒▒▒▒                                                          ?
?                                                                                                                              ?
?                                                                                                                              ?
?                                                          ▒▒▒▒▒▒                                                              ?
?                                                                                                                              ?
?                            [B]                                                         [B]                                   ?
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
''',

"T_1":
'''
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
?                                                                                                                              ?
?                                                                                                                              ?
?                                                                                                                              ?
?                                                                                                                              ?
?                                                                                                                              ?
?                                                                                                                              ?
?                                                                                                                              ?
?             [B]                                                                                           [B]                ?
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                               ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓????????????▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
''',

"hell_1":
'''
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓????????????▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    ▒▒▒▒    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    ▒▒▒▒    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    ▒▒▒▒    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    ▒▒▒▒    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    ▒▒▒▒    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓????????????▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
''',

"hell_2":
'''
▓▓▓▓▓▓????????????▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓    ▒▒▒▒    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓    ▒▒▒▒    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓    ▒▒▒▒    ▓▓                                                     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓     ▒▒                                                            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓     ▒▒                                                            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓     ▒▒                                                            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓    ▒▒▒▒                                                           ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓     ▒▒                                                            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓     ▒▒                                                            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓     ▒▒                   [B]                       [B]            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓    ▒▒▒▒   ▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓????????????▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
''',

"hell_3":
'''
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓????????????▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    ▒▒▒▒    ▓▓▓▓▓▓
▓▓▓▓                            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                    ▓▓     ▒▒     ▓▓▓▓▓▓
▓▓▓▓                                                                                                               ▒▒     ▓▓▓▓▓▓
▓▓▓▓                                                                                                               ▒▒     ▓▓▓▓▓▓
▓▓▓▓                                                                                                              ▒▒▒▒    ▓▓▓▓▓▓
▓▓▓▓                                                                                                               ▒▒     ▓▓▓▓▓▓
▓▓▓▓                                                                                                               ▒▒     ▓▓▓▓▓▓
▓▓▓▓                                                                                                               ▒▒     ▓▓▓▓▓▓
▓▓▓▓         [B]                                                                          [B]                     ▒▒▒▒    ▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                    ▓▓     ▒▒     ▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                          ▒▒▒▒    ▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                           ▒▒     ▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                           ▒▒     ▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                           ▒▒     ▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                          ▒▒▒▒    ▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                           ▒▒     ▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓         [B]               [B]                                    ▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓            ▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓????????????▓▓▓▓▓▓
''',

"corn":
'''
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓????????????▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓            ▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                    ▒▒▒▒▒▒▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                                ▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                                      ▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                                      ▒▒▒▒▒▒▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                                                  ▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                                                        ▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓            ▓▓▓▓▓▓
?                                                               ▓▓▓▓▓▓▓▓▓▓                                  ▓▓▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓
?                                                         ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                  ▓▓            ▓▓▓▓▓▓
?                                                   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                ▓▓▓▓▓▓
?                                             ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                ▓▓▓▓▓▓
?                                       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                          ▒▒▒▒▒▒▓▓▓▓▓▓
?                                 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                ▓▓▓▓▓▓
?                           ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                ▓▓▓▓▓▓
?                     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓         [B]            [B]                     ▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
''',

"T_2":
'''
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓????????????▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓            ▓▓                  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒                          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒                          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                     [B]        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
?                                                                                                                              ?
?                                                                                                                              ?
?                                                         ▒▒▒▒▒▒                                                               ?
?                                                                                                                              ?
?                                                                                                                              ?
?                                                         ▒▒▒▒▒▒                                                               ?
?                                                                                                                              ?
?             [B]                                                                                           [B]                ?
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
''',

"Arena_1":
'''
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                                ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                                              ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                                                        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                                                                ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓                                                                                                      ▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓                                                                                                            ▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓                                                                                                                ▓▓▓▓▓▓▓▓
▓▓▓▓▓▓                                                                                                                    ▓▓▓▓▓▓
▓▓▓▓▓                                        [E]                                  [C]                                      ▓▓▓▓▓
▓▓▓▓                                ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                                ▓▓▓▓
?                                                                                                                              ?
?                                                                                                                              ?
?                     [B]                                     [B]                                                              ?
?                ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                  ?
?                                                                                                                              ?
?                                                                                                                              ?
?[G]  [T]                                                                       [E]                                    [T]  [G]?
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                                                      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                                          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
''',

"Arena_2":
'''
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓        ▓▓                                                          ▓▓        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                                                        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                                                                ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓                                                                                                      ▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓                                                                                                            ▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓                                   [E]                 [C]                                                      ▓▓▓▓▓▓▓▓
▓▓▓▓▓▓                   ▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒                   ▓▓▓▓▓▓
▓▓▓▓▓                                                                                                                      ▓▓▓▓▓
▓▓▓▓                                                                                                                        ▓▓▓▓
?                                                                                                                              ?
?                        ▒▒▒▒▒▒▒▒                                                              ▒▒▒▒▒▒▒▒                        ?
?                                                                                                                              ?
?                                          ▓▓                                    ▓▓                                            ?
?                        ▒▒▒▒▒▒▒▒          ▓▓                                    ▓▓            ▒▒▒▒▒▒▒▒                        ?
?                                          ▓▓                                    ▓▓                                            ?
?[G]  [T]                                  ▓▓       [B]            [E]           ▓▓     [B]                            [T]  [G]?
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
''',

"Arena_3":
'''
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                                              ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                                                          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                                                                ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                                                                    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                [C]                                                 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                                        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓          [B]            [B]     [E]       ▒▒          ▒▒              [B]                          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓                                            ▓▓                           ▓▓                                             ▓▓▓▓
?                                               ▓▓                           ▓▓                                                ?
?                 ▒▒▒▒▒▒▒▒                      ▓▓                           ▓▓                       ▒▒▒▒▒▒▒▒                 ?
?                                                                                                                              ?
?                                                                                                                              ?
?                 ▒▒▒▒▒▒▒▒        ▓▓                           ▓▓                           ▓▓        ▒▒▒▒▒▒▒▒                 ?
?                                 ▓▓                           ▓▓                           ▓▓                                 ?
?[G]  [T]                         ▓▓                     [E]   ▓▓   [E]                     ▓▓                         [T]  [G]?
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
''',

"hell_room":
'''
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓????????????▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                              ▒▒▒▒                              ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                      ▒▒                                      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                           ▒▒                                           ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                               ▒▒                                               ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓                                                 ▒▒▒▒                                                 ▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓                                                     ▒▒                                                     ▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓                                                       ▒▒                                                       ▓▓▓▓▓▓▓▓
▓▓▓▓▓▓                                                         ▒▒                                                         ▓▓▓▓▓▓
▓▓▓▓▓                [B]                                      ▒▒▒▒                                                         ▓▓▓▓▓
▓▓▓▓       ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                                ▒▒                                                           ▓▓▓▓
▓▓▓                                                            ▒▒                                                            ▓▓▓
▓▓▓                                                            ▒▒                                                            ▓▓▓
▓▓                                                            ▒▒▒▒                                                            ▓▓
▓▓                                                             ▒▒                                                             ▓▓
▓▓                              [B]                            ▒▒                                [B]                          ▓▓
▓▓                  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                       ▒▒                        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                 ▓▓
▓▓                                                                                                                            ▓▓
▓▓                                                                                                                            ▓▓
▓▓       [B]                                                               [B]                                                ▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓????????????▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
''',

"L_1":
'''
▓▓▓▓▓▓????????????▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓    ▒▒▒▒    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓    ▒▒▒▒    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓      ▒▒▒▒      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓        ▒▒        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
?          ▒▒         ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
?          ▒▒         ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
?         ▒▒▒▒        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
?          ▒▒         ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
?                     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
?                     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
?                     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
''',

"L_2":
'''
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓????????????▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    ▒▒▒▒    ▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    ▒▒▒▒    ▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     ▒▒     ▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓      ▒▒▒▒      ▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓        ▒▒        ▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓         ▒▒          ?
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓         ▒▒          ?
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓        ▒▒▒▒         ?
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓         ▒▒          ?
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                     ?
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                     ?
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                     ?
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
''',

"Tunnel_1":
'''
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓????????????▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓????????????▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                 ▓▓▓▓▓▓▓▓▓▓▓▓▓                  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                 ▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                  ▒▒▒▒▒▒▒▒▒▒▒▒                                        ▒▒▒▒▒▒▒▒▒▒▒▒   ▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                                                                     ▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                                                                     ▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                                                                     ▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                  ▒▒▒▒▒▒▒▒▒▒▒▒                                        ▒▒▒▒▒▒▒▒▒▒▒▒   ▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓         [B]                                                     [B]                                 ▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓       ▒▒▒▒       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓        ▒▒        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                 ▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓         ▒▒         ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                   ▓▓▓
?                               ▒▒                                                                                           ▓▓▓
?                              ▒▒▒▒                                                                                          ▓▓▓
?                               ▒▒                                                                                           ▓▓▓
?                               ▒▒                                                                                           ▓▓▓
?                               ▒▒                                                                                           ▓▓▓
?                                                         [B]                                                      [B]       ▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
''',

"Tunnel_2":
'''
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓????????????▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                 ▓▓▓▓
▓▓▓▓▓                                                                                                         ▒▒▒▒▒▒▒▒▒▒▒▒   ▓▓▓
▓▓▓                                                                                                                          ▓▓▓
▓▓▓                                                                                                                          ▓▓▓
▓▓▓                                                                                                           ▒▒▒▒▒▒▒▒▒▒▒▒   ▓▓▓
▓▓▓                                                                                                                          ▓▓▓
▓▓▓                              [B]                       [B]                           [B]                                 ▓▓▓
▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓       ▒▒▒▒       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓       ▒▒▒▒       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓        ▒▒        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓        ▒▒        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓         ▒▒         ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓         ▒▒         ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓         ▒▒         ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓          ▒▒                               ?
▓▓        ▒▒▒▒        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓         ▒▒▒▒                              ?
▓▓         ▒▒         ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓          ▒▒                               ?
▓▓         ▒▒         ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓          ▒▒                               ?
▓▓         ▒▒         ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                           ?
▓▓        ▒▒▒▒        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                               [B]         ?
▓▓         ▒▒         ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓         ▒▒         ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓                    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓????????????▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
''',

}

npc_textures = {
'1': [ # FU*K_HEAD
        [
        " ▄▄▄ ",
        "██▄██",
        "█▄█▄█",
        " █▀█ ",
        " █ █ "
        ],[
        " ▄▄▄ ",
        "██▄██",
        "█████",
        " █▀█ ",
        " █ █ "
        ]
    ]
}

npc_textures_ragdoll = {
'1': [ 
        [
            "▄███▄",
            "█▄█▄█",
            "▀█▄█▀"
        ],[
            "▄█▀█▄",
            "█▀█▀█",
            "▀███▀"
        ]]
}

npc_textures_crouch = {
'1':[
        "▄███▄",
        "█████",
        "▀███▀"
    ]
}

npc_textures_walk = {
'1': [
        [
        " ▄▄▄ ",
        "██▄██",
        "█▄█▄█",
        " █▀█ ",
        " █ █ "
        ],[
        " ▄▄▄ ",
        "██▄██",
        "█▄█▄█",
        "  ██ ",
        "  ▀█ "
        ],[
        " ▄▄▄ ",
        "██▄██",
        "█▄█▄█",
        "  ██ ",
        "  █▀ "
        ],[
        " ▄▄▄ ",
        "██▄██",
        "█▄█▄█",
        " █▀█ ",
        " █ █ "
    ]]
}

npc_dialoges = {
'1':[
        [
        "I hate Procreation!",
        "And Women!",
        "And Men!",
        "And YOU!",
        "FUCK YOU!"
        ],[
        "Did you know...",
        "You can get me to follow you...",
        "By pressing [F]"
        ],[
        "Did you know...",
        "You can get me to follow you...",
        "By pressing [F]"
        ],[
        "In October 2018...",
        "In Haddington, Scotland...",
        "A 22 year old man...",
        "Had his cock bitten off...",
        "By a bulldog named Biggie."
        ]
    ]
}

interactable_textures = {
'2': [
        [
        "                                    # # ",
        "                                 # #   #",
        "                               # #  ##  ",
        "                              ##  # # # ",
        "                            ## # # ##   ",
        "                           ## # ##      ",
        "                          #### #        ",
        "                         ## #           ",
        "                        ### #           ",
        "                        ####            ",
        "                      ████████          ",
        "                       ██████           ",
        "                     ▄████████▄         ",
        "                   ▄██▀▀    ▀▀██▄       ",
        "                  ██▀          ▀██      ",
        "    ▄▄▄▄▄▄▄      ███            ███     ",
        "▀▀████████▀      ████▀▀▀▀▀▀▀▀▀▀████     ",
        "    ████         ███            ███     ",
        "  ▄██▀▀██▄       ████▄▄▄▄▄▄▄▄▄▄████     "
        ],[
        "                                 #   # #",
        "                               # # # ## ",
        "                              # # # ##  ",
        "                            ## ##  ##   ",
        "                           ## ## #      ",
        "                          # ## #        ",
        "                          # # #         ",
        "                        ### #           ",
        "                       ### #            ",
        "                        ###             ",
        "                      ████████          ",
        "                       ██████           ",
        "                     ▄████████▄         ",
        "                   ▄██▀▀    ▀▀██▄       ",
        "                  ██▀          ▀██      ",
        "    ▄▄▄▄▄▄▄      ███            ███     ",
        "▀▀████████▀      ████▀▀▀▀▀▀▀▀▀▀████     ",
        "    ████         ███            ███     ",
        "  ▄██▀▀██▄       ████▄▄▄▄▄▄▄▄▄▄████     "
    ]],
'3': [
        [
        "                           ",
        "                     1010  ",
        "   1100                    ",
        "              1001         ",
        "     0101                  ",
        "                   1010    ",
        "   ████████████████████    ",
        "0100110101110001101110█    ",
        "   █100011101110011100█    ",
        "   █1010010111111000101011 ",
        "  10100011100111011011█    ",
        "   ████████████████████    ",
        "   ██            ██  ██    ",
        "   ████████████████████    ",
        ],[
        "                   1010    ",
        "     1100       1001       ",
        "                           ",
        "          0101        1010 ",
        "                           ",
        "               0110        ",
        "   ████████████████████    ",
        " 010011010111000110111█    ",
        "   █010001110111001110█    ",
        "   █11010010111111000101011",
        " 111010001110011101101█    ",
        "   ████████████████████    ",
        "   ██            ██  ██    ",
        "   ████████████████████    ",
    ]],
'4': [
        [
        "      O     o       O        O                 ",
        "          ▓▓▓▓▓▓▓      o                       ",
        "   O     ▓▓     ▓▓▓▓▓▓▓▓▓▓▓▓▓    O             ",
        "       ░▒▒▒░  o        o    ▓▓                 ",
        "     ░░▒▒▒▒▒░░            ░▒▒▒▒░               ",
        "   ░░▒▒▒▒▒▒▒▒▒░░          ░▒▒▒▒░               ",
        "   ░░▒▒▒▒▒▒▒▒▒░░ #    ▄   ░▒▒▒▒░               ",
        "    ░#▒▒▒▒▒▒#░░       ▓▓▓▓▓▒▒▒▒░               ",
        " #   #░▒▒▒#▒░░# #     ▓   ░▒▒▒▒░          ▄▄   ", 
        "   ███#██##█████ ▄      ██████████    ▄   ▒▒   ",
        "   #█ ## ## # ██ ▒      ██      ██    ▒  ▒▒▒▒  ",
        "   ██# ###### ██ ▒      ██      ██    ▒  ▒▒▒▒  "
        ],[
        "                 o                 O           ",
        "        O ▓▓▓▓▓▓▓      o                       ",
        "    o    ▓▓ o   ▓▓▓▓▓▓▓▓▓▓▓▓▓   o              ",
        "       ░▒▒▒░        o       ▓▓                 ",
        "     ░░▒▒▒▒▒░░            ░▒▒▒▒░               ",
        "   ░░▒▒▒▒▒▒▒▒▒░░ #        ░▒▒▒▒░               ",
        "   ░░▒▒▒▒▒▒▒#▒░░      ▄   ░▒▒▒▒░               ",
        "#   ░#▒▒▒▒▒##░░ #     ▓▓▓▓▓▒▒▒▒░               ",
        "     #░▒▒▒▒▒░░        ▓   ░▒▒▒▒░          ▄▄   ", 
        "   ███████#███#█ ▄      ██████████    ▄   ▒▒   ",
        "   ██## ## # #██ ▒      ██      ██    ▒  ▒▒▒▒  ",
        "   ██ ## ### #██ ▒      ██      ██    ▒  ▒▒▒▒  "
    ]]
}

chest_texture = [
    [   
        "▄▄██████████▄▄",
        "█▓▓█▓▓██▓▓█▓▓█",
        "█▓▓█▓▓▓▓▓▓█▓▓█",
        "██████████████"
    ],[   
        "▄▄██████████▄▄",
        "█▒▒█▒▒██▒▒█▒▒█",
        "█▓▓█▓▓▓▓▓▓█▓▓█",
        "█▓▓█▓▓▓▓▓▓█▓▓█",
        "██████████████"
    ],[   
        "▄▄██████████▄▄",
        "█▒▒▒▒▒██▒▒▒▒▒█",
        "█▒▒▒▒▒▒▒▒▒▒▒▒█",
        "█▓▓█▓▓▓▓▓▓█▓▓█",
        "██████████████"
    ]
]

breakable_textrues = [
    [
        [
            "██████",
            "█▓▓▓▓█",
            "█▓▓▓▓█",
            "██████",
        ],[
            "  ██ ███  ",
            "  █▓▓ ▓█  ",
            "  █▓  ▓█  ",
            "  █ ██ █  ",
        ],[
            " ██   ███ ",
            " █▓▓   ▓█ ",
            " █▓    ▓█ ",
            " █  ██  █ ",
        ],[
            "██▓   ▓██ ",
            "█▓▓    ▓█ ",
            "█▓      ▓█",
            " █  ██   █",
        ],[
            " █▓ ▓▓█   ",
            " █▓▓  ▓█  ",
            "█▓▓    ▓██",
            "█▓  ██  ▓█",
        ],[
            "  █ █     ",
            "█▓▓▓▓ ▓▓█ ",
            "█▓▓ ██ ▓▓█",
        ],[
            " ██ ▓█▓█  ",
            "█▓ ▓ █▓▓▓█",
        ],
    ],[
        [
            "  ██  ",
            " ████ ",
            "██▓▓██",
            "█▓▓▓▓█",
            "█▓▓▓▓█",
            "██████",
        ],[
            "  ██  ",
            " █ ██ ",
            "██ ▓ █",
            "█▓▓ ▓█",
            "█▓▓ ▓█",
            "████ █",
        ],[
            "███   ",
            " █  ██",
            "   ▓ █",
            "█▓  ▓█",
            "█▓█ ▓█",
            "██████",
        ],[
            "██  ██",
            "█ ▓ ██",
            "     ▓",
            "█▓    ",
            "█▓█ ▓█",
            "██████",
        ],[
            "██  ██",
            "█▓  ██",
            "     ▓",
            "█▓    ",
            "█▓█ ▓█",
            "██████",
        ],[
            "██   █",
            "█▓  ██",
            "█▓ ▓ █",
            "█▓█ ▓█",
            "██████",
        ],[
            "█▓   █",
            "█▓█ ▓█",
            "██████",
        ]
    ],[
        [
            " ▄     ",
            " ▒     ",
            "▒▒▒  █ ",
            "▒▒▒ ▒▒▒",
            "▒▒▒ ▒▒▒",
        ],[
            "  ▄    ",
            "  ▒    ",
            " ▒▒▒ █ ",
            "▒▒▒▒▒▒▒",
            "▒▒▒ ▒▒▒",
        ],[
            "   ▄   ",
            "   ▒   ",
            " ░▒▒ █ ",
            "▒▒░▒░▒▒",
            "░░▒ ▒▒░",
        ],[
            "     ▄ ",
            " ░ ▒▒█ ",
            "▒ ░▒ ▒ ",
            "░░▒ ▒▒░",
        ],[
            "   ░▒  ",
            "▒░░▒░█▄",
            "░░▒░▒▒░",
        ],[
            "    ▒  ",
            " ░▒▄ ▒▄",
            "░░▒▒▒█░",
        ],[
            "  ▄▄▒▒▄",
            "░░▒▒▒█░",
        ]
    ]
]

effect_textures = {
    "rift":
    [
        [
            "       1001010101                          100010     ",
            "                                                      ",
            "                      10001010101010                  ",
            "            10101010101010101            1010101011110",
            "                                                      ",
            " 101010101010101              1011111100010101        ",
            "                  1000111001                          "
        ],[
            "    10101011011                         0110101   ",
            "                                                  ",
            "                         10101100111001           ",
            "        101010010101011110            111001101   ",
            "                                                  ",
            "         101010111001     1000110111110001        ",
            "                      11100110011101              "
        ],[
            " 10010111100                         11100110     ",
            "                                                  ",
            "                            1001111100010         ",
            "     10101101101011100             100011100      ",
            "                        10                        ",
            "            111110010011001110101011100           ",
            "                          1011011101011           "
        ],[
            "100110110                         111011001              ",
            "                                                         ",
            "111100                  0      1111011000110             ",
            "    010010101100110     1       100110111       101001111",
            "                        10                               ",
            "            111110010011001110101011100                  ",
            "                         11   1011101000110              "
        ],[
            "001100                         010001110          ",
            "                                                  ",
            "01010111100           110          1010011110110  ",
            "  01001110010110        0   1010101011   101111001",
            "                        10                        ",
            "                0011101001111001010               ",
            "                         101      100001111010    "
        ],[
            "011101101                       1001011101                    ",
            "                                                              ",
            "        10001010101010        0              00111001100101010",
            "  100011110011101             1 100010110101010101010101      ",
            "                            1000 110                          ",
            "   01011                 1101 001 101                 01111001",
            "                            10001  10       10111000110110    "
        ],[
            "                    10010110001                          ",
            "                                                         ",
            "        00111100110000  0  1                 110010010000",
            "010011                0 1 110101010101010101             ",
            "                    10 0 0   1 0                         ",
            "    1011100011     111 1  001 1  1            00101001001",
            "                    10 010 0 010 10         100100       "
        ],[
            "                   110010101101                    100101    ",
            "                                                             ",
            "                101100100011101                    1100111001",
            "110000111                 01110001100111011          1011110 ",
            "                          1    0     0    0                  ",
            "         110001101       1 110 10      1  0101100110011010   ",
            "                          10001     0  0                     "
        ]
    ]
}



############### Base variables ###############

operation_order = ('¬', '∧', '⊻', '∨', '→', '↔') # operation symbol priority from left ot right
operands = ('¬', '∧', '⊻', '∨', '→', '↔')

# main menu
menu_buttons_str = ["FIDGET", "GUIDE", "CLASS", "PRACTICE", "GAME MODE", "DEBUG MODE", "EXIT"]
menu_buttons = []



############### Game variables ###############

game_map = []

view = []
view_blindness = 0

debug_info = False

bfs_explored = []
bfs_queue = []
debug_bfs_considered = []
bfs_energy = 800 +100 # (prevents recursion limit crashes in bfs algorithm) BEST TESTED: 800
bfs_closest_node = None
bfs_closest_node_dist = 99999999

dungeon_doors_lock = False
dungeon_y = game_map_preset.count('\n')

dungeon_tiles = []
dungeon_tile_width = 128
dungeon_tile_height = 22
dungeon_width = 20
dungeon_height = 10

triggers = []
gates = []
enemies = []
    
game_map_width = 0
game_map_height = 0

chests = []

game_map = []
player = None
breakables = []
npcs = []
interactables = []
effects = []

minigame_graphics = []

# timers

g_timer = time.perf_counter()
roll_timer = time.perf_counter()
destructable_timer = time.perf_counter()
anim_timer = time.perf_counter()
text_anim_timer = time.perf_counter()
interactable_anim_timer = time.perf_counter()
view_blindness_timer = time.perf_counter()
player_wiggle_timer = time.perf_counter()
rift_anim_timer = time.perf_counter()
npc_mov_timer = time.perf_counter()
npc_rag_timer = time.perf_counter()
stamina_timer = time.perf_counter()
last_roll_ts = time.perf_counter()



############### Base code blocks ###############

# former version, now converted to a string version
def propositionify_str(equation, op_num = len(operation_order)-1):
    split = equation.split(operation_order[op_num]) # split to arrays by symbol

    string = "("
    if(op_num > 0):
        if(len(split) > 1):
            for part in split:
                string += propositionify_str(part, op_num-1) + operation_order[op_num]
            string = string[:-1] + ")"
        else:
            string = propositionify_str(equation, op_num-1)
        return string
        
    else:
        return equation
    
# newer version, converting equations into complex propositions
def propositionify(equation, op_num = len(operation_order)-1):
    split = equation.split(operation_order[op_num]) # split to arrays by symbol

    new_proposition = Proposition_complex([], operation_order[op_num])
    if(op_num > 0):
        if(len(split) > 1):
            for part in split:
                new_proposition.propositions.append(propositionify(part, op_num-1))
            return new_proposition
        else:
            return propositionify(equation, op_num-1)
        
    else:
        return equation
    
# get the deepest brackets
def count_bracket_depth(equation):
    deepest_bracket = 0
    bracket_count = 0
    for char in equation:
        if char == '(':
            bracket_count+=1
        elif char == ')':
            bracket_count-=1
        
        if bracket_count > deepest_bracket:
            deepest_bracket = bracket_count

    return deepest_bracket

# checks if an equation is fully within a bracket pair
def is_shelled(equation):
    try:
        if((equation[0] == '(') and (equation[-1] == ')')):
            bracket_count = 0
            for char in equation[1:-1]:
                if char == '(':
                    bracket_count+=1
                elif char == ')':
                    bracket_count-=1
                    if(bracket_count < 0):
                        return False
            return True
        else:
            return False
        
    # bc of double negation
    except:
        return False

# newer version, converting equations into complex propositions recursively
def propositionify_prioritized(equation, op_num = len(operation_order)-1):
    
    # handle shelled equations immedietly
    if(is_shelled(equation)):
        return(propositionify_prioritized(equation[1:-1]))

    # handle the unary operation: Negation
    if(equation[0] == '¬'):
        return Proposition_complex([propositionify_prioritized(equation[1:], op_num = op_num)], '¬')
        
    # split the equation by the current operand while accounting for brackets
    split = []
    if('(' in equation): # split around brackets
        sub_equation = ""
        bracket_count = 0
        for char in equation:
            if char == '(':
                bracket_count+=1
            elif char == ')':
                bracket_count-=1
            
            if((char == operation_order[op_num]) and (bracket_count == 0)):
                split.append(sub_equation)
                sub_equation = ""
            else:
                sub_equation += char
        split.append(sub_equation)

    # simple split
    else:
        split = equation.split(operation_order[op_num]) # split to arrays by symbol

    new_proposition = Proposition_complex([], operation_order[op_num])

    if(op_num >= 0):
        if(len(split) > 1):
            if(split[0] == ''): # checks for empty split caused by the unary NOT operation, passes only the second proposition/variable
                split = split[1:]
            for part in split:
                if(is_shelled(part)):
                    new_proposition.propositions.append(propositionify_prioritized(part))
                else:
                    new_proposition.propositions.append(propositionify_prioritized(part, op_num-1))
        else:
            new_proposition = propositionify_prioritized(equation, op_num-1)
        return new_proposition

    else:
        if(('(' in equation) or (')' in equation)):
            raise ValueError("failed to propositionify (invalid variables of propositions or brackets)")
        return equation
    


def standardize(equation):
    #format
    equation = equation.lower()

    equation = equation.replace(' ', '')

    equation = equation.replace("ifandonlyif", '↔')
    equation = equation.replace("iff", '↔')

    equation = equation.replace("not", '¬')
    equation = equation.replace("xor", '⊻') # ⊕
    equation = equation.replace("or", '∨')
    equation = equation.replace("and", '∧')
    equation = equation.replace("if", '(')
    equation = equation.replace("then", ')→')
    equation = equation.replace("implies", '→')

    # check if every bracket has a partner
    bracket_count = 0
    for char in equation:
        if(char == "("):
            bracket_count += 1
        elif(char == ")"):
            bracket_count -= 1

    if(not(bracket_count == 0)):
        raise ValueError("Invalid brackets")

    # turn into a proposition
    return propositionify_prioritized(equation)


# applies basic rules and laws to try and simplify the equation
def simplify(proposition_complex, main = True):
    # already too simple
    if(type(proposition_complex) == str):
        return(proposition_complex)
    
    # called once
    if(main):
        not_simplified = proposition_complex
        simple = False
        while(not(simple)):
            # simplify
            simplified = simplify(not_simplified, main = False) 

            # simple proposition
            if(type(simplified) == str):
                return(simplified)
            
            # same complexity as before (cant be simplified more)
            if(simplified.str() == not_simplified.str()):
                simple = True
            
            # reset
            not_simplified = simplified

        return(simplified)

    # called recursively and repeatedly
    else:
        new_proposition = Proposition_complex([], proposition_complex.symbol)

        propositions_str = []
        for prop in proposition_complex.propositions:
            if(type(prop) == str):
                propositions_str.append(prop)
            else:
                propositions_str.append(prop.str())

        # rewrite more complex operations
        if(proposition_complex.symbol == '→'):
            
            # (A → B)   =>   ((¬A) ∨ B)
            new_proposition.symbol = '∨'
            new_proposition.propositions.append(Proposition_complex([proposition_complex.propositions[0]], symbol='¬'))
            new_proposition.propositions.append(proposition_complex.propositions[1])

            return(simplify(new_proposition))
        
        elif(proposition_complex.symbol == '↔'):
            
            # (A ↔ B)   =>   (A ∧ B) ∨ (¬A ∧ ¬B)
            left_proposition = Proposition_complex([
                proposition_complex.propositions[0], 
                proposition_complex.propositions[1]], 
                symbol='∧')
            
            right_proposition = Proposition_complex([
                Proposition_complex([proposition_complex.propositions[0]], symbol='¬'), 
                Proposition_complex([proposition_complex.propositions[1]], symbol='¬')
                ], symbol='∧')

            new_proposition.symbol = '∨'
            new_proposition.propositions.append(left_proposition)
            new_proposition.propositions.append(right_proposition)

            return(simplify(new_proposition))
        
        elif(proposition_complex.symbol == '⊻'):
            
            # (A ⊻ B)   =>   (A ∨ B) ∧ (¬A ∨ ¬B)
            left_proposition = Proposition_complex([
                proposition_complex.propositions[0], 
                proposition_complex.propositions[1]], 
                symbol='∨')
            
            right_proposition = Proposition_complex([
                Proposition_complex([proposition_complex.propositions[0]], symbol='¬'), 
                Proposition_complex([proposition_complex.propositions[1]], symbol='¬')
                ], symbol='∨')

            new_proposition.symbol = '∧'
            new_proposition.propositions.append(left_proposition)
            new_proposition.propositions.append(right_proposition)

            return(simplify(new_proposition))
            
        #simplify or solve if possible
        for prop in proposition_complex.propositions:

            # simple Negation
            if(proposition_complex.symbol == '¬'):
                if(type(prop) == str):
                    if(prop == "false"):
                        return("true")
                    elif(prop == "true"):
                        return("false")

            # Inverse
            prop_not = Proposition_complex([prop], symbol='¬')
            if(prop_not.str() in propositions_str):
                if(proposition_complex.symbol == '∨'):
                    return("true")
                elif(proposition_complex.symbol == '∧'):
                    return("false")
                
            #Dunno what this law is called
            if(proposition_complex.symbol in ('∨', '∧')): # (A or B)
                if(type(prop) == Proposition_complex): # (A or (B))
                    if(prop.symbol == proposition_complex.symbol): # (A or (B or C))
                        for prop_ in prop.propositions:
                            new_proposition.propositions.append(simplify(prop_))
                        continue # (A or B or C)

                

            #simple proposition
            if(type(prop) == str):

                # Identity; Null; Idempotency
                if(proposition_complex.symbol == '∨'):
                    if(prop == "true"):
                        return("true")
                    elif(prop == "false"):
                        # return("false")
                        pass # itself without this proposition
                    else:
                        if(prop not in new_proposition.propositions): # Idempotency law
                            new_proposition.propositions.append(prop)

                elif(proposition_complex.symbol == '∧'):
                    if(prop == "true"):     
                        # return("true")
                        pass # itself without this proposition
                    elif(prop == "false"):
                        return("false")
                    else: 
                        if(prop not in new_proposition.propositions): # Idempotency law
                            new_proposition.propositions.append(prop)
                
                # no laws apliccable
                else:
                    new_proposition.propositions.append(prop)

            # complex proposition
            elif(type(prop) == Proposition_complex): # complex proposition
                # Double negation
                if((proposition_complex.symbol == '¬') and (prop.symbol == '¬')):
                    return(prop.propositions[0])
                
                # De morgans laws
                if(proposition_complex.symbol == '¬'):
                    prop = proposition_complex.propositions[0]
                    if(prop.symbol in ('∧', '∨')):
                        # flip proposition operand
                        if(prop.symbol == '∧'):
                            new_proposition.symbol = '∨'
                        else:
                            new_proposition.symbol = '∧'

                        for prop_ in prop.propositions: # negate all its propositions
                            new_proposition.propositions.append(Proposition_complex([simplify(prop_)], symbol='¬'))

                        return(new_proposition)
                    
                # Absorption laws
                absorbed = False
                if(((proposition_complex.symbol == '∨') and (prop.symbol == '∧')) or ((proposition_complex.symbol == '∧') and (prop.symbol == '∨'))):

                    for outer_prop in proposition_complex.propositions:
                        for inner_prop in prop.propositions:

                            if(type(outer_prop) == Proposition_complex):
                                if(type(inner_prop) == Proposition_complex):
                                    if(outer_prop.str() == inner_prop.str()):
                                        absorbed = True

                                else:
                                    if(type(outer_prop) == str):
                                        if(outer_prop == inner_prop):
                                            absorbed = True
                            
                            else:
                                if(type(inner_prop) == Proposition_complex):
                                    if(outer_prop == inner_prop.str()):
                                        absorbed = True

                                else:
                                    if(type(outer_prop) == str):
                                        if(outer_prop == inner_prop):
                                            absorbed = True


                if(not(absorbed)):
                    # complex Idempotency
                    if(proposition_complex.symbol in ('∨', '∧')):
                        propositions = []
                        for prop_ in new_proposition.propositions:
                            if(type(prop_) == Proposition_complex):
                                propositions.append(prop_.str())
                                
                        if(prop.str() not in propositions): # Idempotency law
                            new_proposition.propositions.append(simplify(prop, main = True))


            # invalid values
            else:
                print("failed to simplify")

        # handle if simplification returns only a final simple proposition
        if(len(new_proposition.propositions) == 0):
            # prevents oversimplifying into nothing
            if(proposition_complex.symbol == '∨'):
                return("false")
            elif(proposition_complex.symbol == '∧'):
                return("true")
            return
        
        elif(len(new_proposition.propositions) == 1):
            if(new_proposition.symbol == '¬'):
                return(new_proposition)
            else:
                return(new_proposition.propositions[0])
            
        else:
            return(new_proposition)
    

# replaces propositions by True/False to allow for simplification/calculation
def assign(proposition_complex, values):
    if(type(proposition_complex) == str):
        if(proposition_complex in values):
            return(values[proposition_complex])

    new_proposition = Proposition_complex([], proposition_complex.symbol)

    for prop in proposition_complex.propositions:
        if(type(prop) == str):
            if(prop in values):
                new_proposition.propositions.append(values[prop])
            else:
                new_proposition.propositions.append(prop)
        
        else:
            new_proposition.propositions.append(assign(prop, values))

    return(new_proposition)


# make a truth table out of a complex proposition
def make_table(proposition_complex):

    # get all variables
    if(type(proposition_complex) == str):
        variables = [proposition_complex]
    else:
        variables = proposition_complex.variables()

    # make a list of dictionaries of values assigned to variables in all possible cominations
    combinations = []

    values = {}
    for var in variables:
        values[var] = "false"

    value = False
    while(value == False):
        combinations.append(dict(values))

        value = True
        for key in values:

            if((values[key] == "false") and (value == True)):
                values[key] = "true"
                value = False

            elif((values[key] == "true") and (value == True)):
                values[key] = "false"
        
    # assign values and make results
    results = {}
    for combination in combinations:

        vals = "|"
        var_num = 0
        for key in combination:
            if(combination[key] == "false"):
                vals += center("0", len(variables[var_num])+2) + "|"
                # vals += " 0" + " "*len(variables[var_num]) + "|"
            elif(combination[key] == "true"):
                vals += center("1", len(variables[var_num])+2) + "|"
                # vals += " 1" + " "*len(variables[var_num]) + "|"
            var_num += 1

        res = (simplify(assign(proposition_complex, combination)))
        if(res == "false"):
            results[vals] = "0"
        elif(res == "true"):
            results[vals] = "1"


    return(results)



def intro(sleep_mult = 1, keypress = True, border = True, reverse = False):
    if(keypress):
        os.system('cls')
        print("Please maximize this window and press any key to continue...")
        input()
        
        time.sleep(0.2 * sleep_mult)

        # clear screen and hide cursor
        os.system('cls')
        print("\033[?25l")

    # animated logo
    animation = True
    logo_working = ""
    logo_done = logo_anim.copy()
    logo_str = ""
    first_frame = True
    while(animation):

        # print the logo
        logo_str = "\n"
        for str in logo_done[1:-1]:
            if(reverse):
                logo_str += str.replace('█', ' ').replace('▄', ' ').replace('▀', ' ').replace('░', '█') + '\n'
            else:
                logo_str += str.replace('░', ' ') + '\n'
            
        print("\033[0;0H")
        print(logo_str)

        # first frame
        if(first_frame):
            first_frame = False
            logo_working = logo_anim.copy()
            if(keypress):
                time.sleep(0.5 * sleep_mult)

        # other frames
        else:
            time.sleep(0.08 * sleep_mult)

            # check if animation is complete                   
            if(logo_done == logo_working):
                animation = False

        # update logo frame
        logo_done = logo_working.copy()

        # advance the animation
        logo_working = logo_done.copy()
        for str_num in range(len(logo_done)):
            for char_num in range(len(logo_done[str_num])):

                # unlit character
                if(logo_done[str_num][char_num] == "░"):

                    # # 3x3 vicinity
                    # for str_num_ in range(str_num-1, str_num+2):
                    #     for char_num_ in range(char_num-1, char_num+2):

                    #         # spread light
                    #         if(logo_done[str_num_][char_num_] == "█"):
                    #             logo_working[str_num] = logo_working[str_num][:char_num] + "█" + logo_working[str_num][char_num+1:]

                    # cross vicinity
                    for str_num_ in range(str_num-1, str_num+2):
                        if((str_num_ >= 0) and (str_num_ < len(logo_anim))):

                            # spread light
                            if(logo_done[str_num_][char_num] in ("█", "▄", "▀")):
                                logo_working[str_num] = logo_working[str_num][:char_num] + "█" + logo_working[str_num][char_num+1:]

                    for char_num_ in range(char_num-1, char_num+2):
                        if((char_num_ >= 0) and (char_num_ < len(logo_anim[str_num]))):

                            # spread light
                            if(logo_done[str_num][char_num_] in ("█", "▄", "▀")):
                                logo_working[str_num] = logo_working[str_num][:char_num] + "█" + logo_working[str_num][char_num+1:]



    if(border):

        time.sleep(1 * sleep_mult)

        # animation = True
        char_num = len(logo_done[0])
        while(char_num >= 0):

            # print the logo
            logo_str = ""
            for str_num in range(len(logo_done)):
                if((str_num == 0) or (str_num == len(logo_done)-1)):
                    logo_str += logo_done[str_num][char_num:] + '\n'
                else:
                    logo_str += logo_done[str_num] + '\n'
            
            char_num -= 1

            print("\033[0;0H")
            print(logo_str)

            time.sleep(0.03 * sleep_mult)

        time.sleep(1 * sleep_mult)

    if(keypress):

        y_pos = len(logo_done) + 4
        char_num = 0

        string = "Press any key to continue..."
        space = " "*int((len(logo_done[0]) - len(string)) / 2 + 0.5)

        while(char_num <= len(string)):

            char_num += 1

            print("\033[%d;0H" % y_pos)
            print(space + string[:char_num])

            time.sleep(0.05 * sleep_mult)

        input()

        char_num = len(string)-1
        while(char_num >= 0):

            print("\033[%d;0H" % y_pos)
            print(space + string[:char_num] + " "*(len(string)-char_num))

            char_num -= 1

            time.sleep(0.05 * sleep_mult)

        time.sleep(0.5 * sleep_mult)

# guidebook
def guide_book(): # add scrolling with arrowkeys aswell as pages (themes)
    page = 0
    scroll = 0
    os.system('cls')
    while(True):

        # keypresses
        if (msvcrt.kbhit()):
            keystroke = msvcrt.getch()

            # arrow keys
            if(keystroke == b'\xe0'):
                keystroke = msvcrt.getch()

                # pages
                if(keystroke == b'K'):
                    if(page > 0):
                        page -= 1
                        scroll = 0
                        os.system('cls')
                elif(keystroke == b'M'):
                    if(page < len(guidebook.keys()) -1):
                        page += 1
                        scroll = 0
                        os.system('cls')

                # scrolling
                elif(keystroke == b'H'):
                    if(scroll > 0):
                        scroll -= 1
                elif(keystroke == b'P'):
                    if(scroll < len(guidebook[list(guidebook.keys())[page]]) -30):
                        scroll += 1
            
            #ESC
            elif(keystroke == b'\x1b'):
                return
            
        # render book
        topic = list(guidebook.keys())[page]
        page_arr = guidebook[topic]

        view_arr = []

        # get the page width based on longest content
        page_width = 0
        for string in page_arr:
            if(len(string) > page_width):
                page_width = len(string)

        if(len(topic) > page_width):
            page_width = len(topic)

        # head
        view_arr.append("="*page_width)
        view_arr.append(" "*int((page_width - len(topic))/2) + topic + " "*int((page_width - len(topic))/2))
        view_arr.append("="*page_width)
        view_arr.append(" "*(page_width))

        #body
        for string in page_arr[scroll:scroll+36]:
            view_arr.append(string + " "*(page_width - len(string)))
        
        while(len(view_arr) < 40):
            view_arr.append(" "*(page_width))

        #tail
        string = ("Page: " + str(page+1) + " / " + str(len(list(guidebook.keys()))))
        view_arr.append(" "*(page_width))
        view_arr.append("="*page_width)
        view_arr.append(" "*int((page_width - len(string))/2) + string + " "*int((page_width - len(string))/2))
        view_arr.append("="*page_width)

        # print
        string = ""
        for view_str in view_arr:
            string += view_str + '\n'

        print("\033[0;0H")
        print(string)


# returns the string with surrounding spaces, centered.
def center(string, width):
    string = " " * int((width - len(string))/2) + string + " " * int((width - len(string))/2+0.5)
    return(string)


# guidebook
def CLASS(): # add scrolling with arrowkeys aswell as pages (themes)
    tabs = ["Equation", "K-map", "Diagram", "Menu"]
    tab_buttons = []
    window_width = DEFAULT_WINDOW_WIDTH #120

    # balances width for tabs
    window_width = int(window_width/len(tabs))*len(tabs)

    for tab in tabs:
        tab_buttons.append(Button(tab, int(window_width/len(tabs)-4)))

    tab = 0
    selected = tabs[0]
    inside = False
    cursor_pos = 0
    input_buffer = ""
    prev_table_len = 0
    cur_y = 0
    os.system('cls')
    while(True):

        # keypresses
        if (msvcrt.kbhit()):
            keystroke = msvcrt.getch()

            # navigating tabs
            if(not(inside)):

                # arrow keys
                if(keystroke == b'\xe0'):
                    keystroke = msvcrt.getch()

                    # tabs
                    if(keystroke == b'K'):
                        if(tab > 0):
                            tab -= 1
                            os.system('cls')
                    elif(keystroke == b'M'):
                        if(tab < len(tabs) -1):
                            tab += 1
                            os.system('cls')
                    
                    selected = tabs[tab]

                # enter
                elif(keystroke in (b'\r', b'\n')): 
                    if(selected == "Menu"):
                        return

                    inside = True
            
            # inside a tab
            else:
                #ESC
                if(keystroke == b'\x1b'):
                    inside = False
                    cur_y = 0

                else:
                    match selected:
                        case "Equation":

                            # backspace (deleting characters from buffer)
                            if(keystroke == b'\x08'):
                                if(cursor_pos >= 0):
                                    snap = input_buffer
                                    input_buffer = input_buffer[:cursor_pos] + input_buffer[cursor_pos+1:]
                                    if(not(snap == input_buffer)):
                                        cursor_pos -= 1
                            
                            # arrow keys (moving cursor in buffer)
                            elif(keystroke == b'\xe0'): # \xe0K\xe0M
                                keystroke = msvcrt.getch()

                                if(keystroke == b'K'):
                                    cursor_pos -= 1
                                elif(keystroke == b'M'):
                                    cursor_pos += 1
                                if(keystroke == b'H'):
                                    if(cur_y > 0):
                                        cur_y-=1
                                elif(keystroke == b'P'):
                                    cur_y+=1
                            
                            # all other keystrokes
                            else:
                                try:
                                    char = str(keystroke)[2:-1]
                                    if(char.isalpha):
                                        cursor_pos += 1
                                        input_buffer = input_buffer[:cursor_pos] + char + input_buffer[cursor_pos:]
                                        if(len(input_buffer) > in_buffer_size):
                                            in_buffer_size = len(input_buffer)

                                except:
                                    pass

        if(cursor_pos < 0):
            cursor_pos = -1
        elif(cursor_pos >= len(input_buffer)):
            cursor_pos = len(input_buffer)-1

        # build page
        string = ""

        for y in range(5):
            for btn in tab_buttons:
                string += btn.str((selected == btn.text))[y]
            string += '\n'

        string += "\n"
        if(inside):
            string += center("Press [ESC] to deselect tab...", window_width) + '\n'
        else:
            string += center("Press [enter] to select tab...", window_width) + '\n'
        string += "\n"
        string += "=" * window_width + '\n'
        string += center(selected, window_width) + '\n'
        string += "=" * window_width + '\n'
        string += "\n\n"


        match selected:
            case "Menu":
                string += center("Are you sure you want to return to the menu?", window_width) + "\n\n"
                string += center("Press [enter] to return to menu", window_width) + '\n'

            case "K-map":
                string += center("This feature has not been implemented yet...", window_width)

            case "Diagram":
                string += center("This feature has not been implemented yet...", window_width)

            case "Equation":
                input_buffer_cursorified = input_buffer[:cursor_pos+1] + '|' + input_buffer[cursor_pos+1:]

                # manipulate equation
                invalid = ""
                try:
                    standardized = standardize(input_buffer)
                    standardized_str = standardized.str()
                    simplified = simplify(standardize(input_buffer))
                    if(type(simplified) == Proposition_complex):
                        simplified_str = simplified.str()
                    else:
                        simplified_str = str(simplified)

                    try:
                        table = make_table(simplified)

                        vars_str = "|"
                        for var in simplified.variables():
                            vars_str += " " + str(var) + " |"
                    except:
                        table = "INVALID"
                    
                except:
                    invalid = "... (Invalid)"
                
                # constructing output string
                if(len(input_buffer) == 0):
                    table = None
                    standardized_str = ""
                    simplified_str = ""
                    string += center("__INPUT__", window_width) + '\n'
                    string += center("When [enter]ed into the tab, start typing...", window_width) + "\n\n"

                    string += center("__EQUATION__", window_width) + '\n'
                    string += center("The standardized equation will show here...", window_width) + "\n\n"

                    string += center("__SIMPLIFIED__", window_width) + '\n'
                    string += center("The simplified equation will show here...", window_width) + "\n\n"
                else:
                    string += center("__INPUT__", window_width) + '\n'
                    string += center(input_buffer_cursorified, window_width) + "\n\n"

                    string += center("__EQUATION__", window_width) + '\n'
                    string += center(standardized_str + invalid, window_width) + "\n\n"

                    string += center("__SIMPLIFIED__", window_width) + '\n'
                    string += center(simplified_str + invalid, window_width) + "\n\n"

                # truth table title
                string += "\n\n"
                string += "=" * window_width + '\n'
                string += center("=== TRUTH TABLE ===", window_width) + '\n'
                string += "=" * window_width + '\n'
                string += "\n\n"

                table_arr = []

                # table
                if(table == None):
                    string += "\n"
                    string += center("The table will appear here...", window_width) + '\n'
                    for _ in range(prev_table_len):
                        if(_ < 20):
                            string += center("", window_width) + '\n'
                elif(table == "INVALID"):
                    string += "\n"
                    string += center("INVALID TABLE...", window_width) + '\n'
                    for _ in range(prev_table_len):
                        if(_ < 20):
                            string += center("", window_width) + '\n'
                else:
                    # get widest string in table
                    table_max_len = 0
                    for key in table:
                        if(len(str(key) + " == " + str(table[key])) > table_max_len):
                            table_max_len = len(str(key) + " == " + str(table[key]))

                    # construct table
                    table_arr.append(vars_str + " Result  |")
                    divider_str = ""
                    for char in vars_str:
                        if(char == "|"):
                            divider_str += "|"
                        else:
                            divider_str += "-"
                    table_arr.append(divider_str + "---------|")
                    for key in table:
                        table_arr.append(str(key) + "    " + str(table[key] + "    |"))

                    # center table
                    table_str_arr = []
                    for row in table_arr:
                        table_str_arr.append(center(row, window_width))
                    
                    # clearing after previous, longer tables rendered
                    for _ in range(prev_table_len - len(table_arr)):
                        table_str_arr.append(" "*window_width)
                    prev_table_len = len(table_arr)

                    table_str_arr.append(" "*window_width)

                    if(cur_y > len(table_str_arr)-20):
                        cur_y = len(table_str_arr)-20
                    if(cur_y < 0):
                        cur_y = 0

                    # render table
                    string += "\n"
                    for table_str in table_str_arr[cur_y:cur_y + 20]:
                        string += table_str + '\n'


        print("\033[0;0H")
        print(string)


def simple_anim(string):
    string_anim = ""
    for char in string:
        if(char == '\n'):
            print(string_anim)
            string_anim = ""
            time.sleep(0.01)
        else:
            string_anim += char


def practice():
    window_width = 80

    practice_premade_simplify = [
        "a or (b and false or c and true)",
        "a or b or (c or b)",
        "a implies b"
    ]

    practice_premade_solve = [
        "b and false or true and true",
        "true and (a or true) and false",
        "true implies false",
        "true implies true"
    ]

    practice_premade_table = [
        "a or b",
        "a and b",
        "a or b or c",
        "a and b and c",
        "a implies b",
        "(not a) or a"
    ]

    practice_types = ["simplify", "solve", "table"] # "question"
    os.system('cls')
    while(True):
        practice_type = random.choice(practice_types)

        match practice_type:
            case "simplify":
                practice_eq = random.choice(practice_premade_simplify)
            case "solve":
                practice_eq = random.choice(practice_premade_solve)
            case "table":
                practice_eq = random.choice(practice_premade_table)

        intro(0.1, False, False)

        input_buffer = ""
        assigned_char = ''
        table_user = {}
        cursor_pos = 0
        cur_y = 0

        practicing = True
        input_standardized = ""
        anim = True
        while(practicing):

            # keypresses
            if (msvcrt.kbhit()):
                keystroke = msvcrt.getch()

                # arrow keys
                if(keystroke == b'\xe0'):
                    keystroke = msvcrt.getch()

                    if(keystroke == b'K'):
                        cursor_pos -= 1
                    elif(keystroke == b'M'):
                        cursor_pos += 1
                    elif(keystroke == b'H'):
                        cur_y-=1
                    elif(keystroke == b'P'):
                        cur_y+=1

                # enter
                elif(keystroke in (b'\r', b'\n')): 
                    practicing = False
            
                #ESC
                elif(keystroke == b'\x1b'):
                    return
                
                # backspace (deleting characters from buffer)
                elif(keystroke == b'\x08'):
                    snap = input_buffer
                    input_buffer = input_buffer[:cursor_pos] + input_buffer[cursor_pos+1:]
                    if(not(snap == input_buffer)):
                        cursor_pos -= 1
                
                # others
                else:
                    try:
                        char = str(keystroke)[2:-1]

                        if(practice_type == "table"):
                            if(char in ('0', '1')):
                                assigned_char = char

                        else:
                            if(char.isalpha):
                                cursor_pos += 1
                                input_buffer = input_buffer[:cursor_pos] + char + input_buffer[cursor_pos:]
                                if(len(input_buffer) > in_buffer_size):
                                    in_buffer_size = len(input_buffer)

                    except:
                        pass
                    
                
            if(cursor_pos < 0):
                cursor_pos = -1
            elif(cursor_pos >= len(input_buffer)):
                cursor_pos = len(input_buffer) -1


            standardized = standardize(practice_eq)
            simplified = simplify(standardized)
            table = make_table(simplified)

            if(type(simplified) == Proposition_complex):
                simplified_str = simplified.str()
            else:
                simplified_str = str(simplified)
            
            input_buffer_cursorified = input_buffer[:cursor_pos+1] + '|' + input_buffer[cursor_pos+1:]

            string = ""

            string += window_width*"=" + '\n'
            string += center(practice_type, window_width) + '\n'
            string += window_width*"=" + '\n'

            string += "\n\n\n"

            # table
            if(practice_type == "table"):
                string += center("__ASSIGNMENT__", window_width) + '\n'
                string += center(standardized.str(), window_width) + "\n\n\n"

                string += window_width*"=" + '\n'

                # variables
                vars_str = "|"
                for var in simplified.variables():
                    vars_str += " " + str(var) + " |"

                table_arr = []

                # construct table
                table_arr.append(vars_str + " Result  |")
                divider_str = ""
                for char in vars_str:
                    if(char == "|"):
                        divider_str += "|"
                    else:
                        divider_str += "-"
                table_arr.append(divider_str + "---------|")

                if(cur_y < 0):
                    cur_y = 0
                elif(cur_y >= len(list(table.keys()))):
                    cur_y = len(list(table.keys()))-1

                table_y = 0
                for key in table:
                    if(table_y == cur_y):
                        if(assigned_char in ('0', '1')):
                            table_user[key] = assigned_char
                            assigned_char = ' '
                        try:
                            table_arr.append(str(key) + "  >>" + table_user[key] + "<<  |")
                        except:
                            table_arr.append(str(key) + "  >> <<  |")
                    else:
                        try:
                            table_arr.append(str(key) + "    " + table_user[key] + "    |")
                        except:
                            table_arr.append(str(key) + "         |")
                    table_y += 1

                # center table
                table_str_arr = []
                for row in table_arr:
                    table_str_arr.append(center(row, window_width))

                # render table
                string += "\n"
                for table_str in table_str_arr:
                    string += table_str + '\n'

                # check validity
                solved = True
                for key in table:
                    try:
                        if(not(table[key] == table_user[key])):
                            solved = False
                    except:
                        solved = False

                if(solved):
                    practicing = False
                        

            # solve, simplify
            elif(practice_type in ("solve", "simplify")):

                string += center("__ASSIGNMENT__", window_width) + '\n'
                string += center(standardized.str(), window_width) + "\n\n\n"

                string += window_width*"=" + '\n'

                string += center("__INPUT__", window_width) + '\n'
                string += center(input_buffer_cursorified, window_width) + "\n\n\n"

                string += center("__STANDARDIZED__", window_width) + '\n'
                
                invalid = ""
                try:
                    input_standardized = standardize(input_buffer)
                except:
                    invalid = "... INVALID"

                if(type(input_standardized) == Proposition_complex):
                    input_str = input_standardized.str()
                else:
                    input_str = str(input_standardized)

                string += center(input_str + invalid, window_width) + "\n\n\n"

                try:
                    # print(input_table)
                    if(input_str == simplified_str):
                        practicing = False
                        
                except:
                    pass
            

            print("\033[%d;0H" % (len(logo_anim)+4))
            if(anim):
                anim = False
                simple_anim(string)
            else:
                print(string)

        print("\033[%d;0H" % (len(logo_anim)+4))
        for _ in range(30):
            print(center("", window_width))
            time.sleep(0.02)
                
        intro(0.1, False, False, True)


# main menu
def menu_setup():
    for str in menu_buttons_str:
        menu_buttons.append(Button(str, 20))

def menu_animation(time_mult = 1):
    y_level = len(logo_anim) + 4
    for btn in menu_buttons:

        btn_string_arr = []
        for str in btn.str():
            btn_string_arr.append(str)

        space = 80
        for anim_i in range(space):

            btn_string = ""
            for str in btn_string_arr:
                btn_string += (" "*(space-anim_i) + str)[:space] + " \n"
            btn_string +='\n'

            print("\033[%d;0H" % y_level)
            print(btn_string)
            time.sleep(0.005*time_mult)

        y_level += 6


def menu():

    menu_animation()
    
    cur_y = 0
    selected = menu_buttons[cur_y].text
    in_menu = True
    stroke_speed = 0.2
    while(in_menu):
        if (msvcrt.kbhit()):
            keystroke = msvcrt.getch()

            # arrow keys (moving cursor in buffer)
            if(keystroke == b'\xe0'):
                keystroke = msvcrt.getch()

                if(keystroke == b'H'):
                    cur_y-=1
                elif(keystroke == b'P'):
                    cur_y+=1
                
                # last_stroke = keystroke

            # enter
            elif(keystroke in (b'\r', b'\n')): 
                match selected:
                    case "EXIT":
                        in_menu = False

                    case "DEBUG MODE":
                        main_debug()
                        os.system('cls')
                        intro(0.1, keypress=False)
                        menu_animation(0.2)

                    case "FIDGET":
                        stroke_speed = 0.2
                        intro(stroke_speed, keypress=False, border=False, reverse=True)
                        intro(stroke_speed, keypress=False, border=False)
                        
                        # holding button
                        while(keystroke in (b'\r', b'\n')):
                            if(msvcrt.kbhit()):
                                keystroke = msvcrt.getch()
                                intro(stroke_speed, keypress=False, border=False, reverse=True)
                                intro(stroke_speed, keypress=False, border=False)
                                stroke_speed = 0.8*stroke_speed
                            else:
                                keystroke = "x"
                    
                    case "GUIDE":
                        guide_book()
                        os.system('cls')
                        intro(0.1, keypress=False)
                        menu_animation(0.2)

                    case "CLASS":
                        CLASS()
                        os.system('cls')
                        intro(0.1, keypress=False)
                        menu_animation(0.2)

                    case "PRACTICE":
                        practice()
                        os.system('cls')
                        intro(0.1, keypress=False)
                        menu_animation(0.2)

                    case "GAME MODE":
                        intro(0.4, keypress=False, border=False, reverse=True)
                        game()
                        os.system('cls')
                        intro(0.1, keypress=False)
                        menu_animation(0.2)

            # manage double presses
            while(msvcrt.kbhit()): msvcrt.getch()
        
        if(cur_y < 0):
            cur_y = 0
        elif(cur_y >= len(menu_buttons)):
            cur_y = len(menu_buttons) - 1
        
        selected = menu_buttons[cur_y].text

        string = ""
        y_level = len(logo_anim) + 4
        for btn in menu_buttons:
            if(btn.text == selected):
                lit = True
            else:
                lit = False
            
            for str in btn.str(lit):
                string += " " + str + " \n"
            string +='\n'

        print("\033[%d;0H" % y_level)
        print(string)

        time.sleep(0.005)



def main_debug():
    # clear screen and hide cursor
    os.system('cls')
    print("\033[?25l")

    # default message
    default_in =      "equation/end:  Type your equation here..."
    default_out =   "\nstandardized:  The result will appear here..."
    default_out_2 = "\n  simplified:  The result will appear here..."
    print(default_in + default_out + default_out_2)


    running = True
    input_buffer = ""
    in_buffer_size = len(default_in)
    out_buffer_size = len(default_out)
    out_buffer_2_size = len(default_out_2)
    table_clear_space = ""
    cursor_pos = -1
    cursor_h = 0
    standardized_str = ""
    simplified = ""
    table_str = ""
    screen = False
    while running:
        # handle keystrokes
        if ((msvcrt.kbhit) or (screen)):
            if(screen):
                screen = False
                cursor_h += 5
            else:
                keystroke = msvcrt.getch()

                # backspace (deleting characters from buffer)
                if(keystroke == b'\x08'):
                    snap = input_buffer
                    input_buffer = input_buffer[:cursor_pos] + input_buffer[cursor_pos+1:]
                    if(not(snap == input_buffer)):
                        cursor_pos -= 1
                
                # arrow keys (moving cursor in buffer)
                elif(keystroke == b'\xe0'): # \xe0K\xe0M
                    keystroke = msvcrt.getch()

                    if(keystroke == b'K'):
                        cursor_pos -= 1
                    elif(keystroke == b'M'):
                        cursor_pos += 1
                
                # enter
                elif(keystroke in (b'\r', b'\n')):
                    if(not(standardized_str == ("INVALID")) and len(standardized_str) > 0):
                        # cursor_h += 5
                        screen = True

                # ESC
                elif(keystroke == b'\x1b'):
                    return
                
                # all other keystrokes
                else:
                    try:
                        char = str(keystroke)[2:-1]
                        if(char.isalpha):
                            cursor_pos += 1
                            input_buffer = input_buffer[:cursor_pos] + char + input_buffer[cursor_pos:]
                            if(len(input_buffer) > in_buffer_size):
                                in_buffer_size = len(input_buffer)

                    except:
                        pass

            # cursor position limits
            if(cursor_pos > len(input_buffer)-1):
                cursor_pos = len(input_buffer)-1
            elif(cursor_pos < 0):
                cursor_pos = 0

            input_buffer_cursorified = input_buffer[:cursor_pos+1] + '|' + input_buffer[cursor_pos+1:]
            
            # standardize equation
            invalid = ""
            try:
                standardized = standardize(input_buffer)
                standardized_str = standardized.str()
                simplified = simplify(standardize(input_buffer))

                try:
                    table = make_table(simplified)

                    vars = "|"
                    if(type(simplified) == str):
                        vars += " " + simplified + " |"
                    else:
                        for var in simplified.variables():
                            vars += " " + var + " |"
                    
                    vars += " "*(len("\n\nInvalid table") - len(vars))
                    
                    table_str = "\n\n" + vars + "\n"
                    table_str += ("="*len(vars)) + "\n"

                    for key in table:
                        table_str += (str(key) + " == " + str(table[key])) + "\n"

                    if(len(table_str) < len(table_clear_space)-1):
                        os.system('cls')

                    table_clear_space = ""
                    for char in table_str:
                        if(char == "\n"):
                            table_clear_space += "\n"
                        else:
                            table_clear_space += " "

                except:
                    table_str = "\n\nInvalid table" + table_clear_space[len("\n\nInvalid table"):]

                if(type(simplified) == Proposition_complex):
                    simplified = simplified.str()
                
            except:
                invalid = "... (Invalid)"
                table_str = "\n\nInvalid table" + table_clear_space[len("\n\nInvalid table"):]

            if(screen):
                table_str = "\n\nInvalid table" + table_clear_space[len("\n\nInvalid table"):]
            
            # buffer clear space
            if(len(standardized_str) > out_buffer_size):
                out_buffer_size = len(standardized_str)
            if(len(simplified) > out_buffer_2_size):
                out_buffer_2_size = len(simplified)
                
            # constructing output string
            if(len(input_buffer) == 0):
                standardized_str = ""
                simplified = ""
                string = default_in + " "*(in_buffer_size-len(default_in)+1) + \
                         default_out + " "*(out_buffer_size-len(default_out)+1) + \
                         default_out_2 + " "*(out_buffer_2_size-len(default_out_2)+1)
            else:
                string = \
                  "equation/end:  " + input_buffer_cursorified + " "*(in_buffer_size-len(input_buffer_cursorified)+1) + \
                "\nstandardized:  " + standardized_str + invalid + " "*(out_buffer_size-len(standardized_str)-len(invalid)+1) + \
                "\n  simplified:  " + simplified + invalid + " "*(out_buffer_2_size-len(simplified)-len(invalid)+1) + \
                table_str

            print("\033[%d;0H" % cursor_h)
            print(string)
            


############### Game code blocks ###############

def random_dungeon_tile(exits_arr):

    # gather all tiles with passthrough required exits
    valid_types = []
    for preset in Dungeon_map_presets:
        if(dungeon_tile_possible_exits(preset, exits_arr)):
            valid_types.append(preset)


    # choose a tile from the array
    return(random.choice(valid_types))
            


def dungeon_tile_possible_exits(type, exits_arr):
    tile_arr = []
    row = ""
    for char in Dungeon_map_presets[type]:
        if(char == '\n'):
            if(len(row) > 0):
                tile_arr.append(row)
            row = ""
        else:
            row += char
    
    passthrough = 0
    if("left" in exits_arr):
        for row in tile_arr:
            if row[0] == '?':
                passthrough += 1
                break

    if("right" in exits_arr):
        for row in tile_arr:
            if row[len(row)-1] == '?':
                passthrough += 1
                break

    if("top_center" in exits_arr):
        if('?' in tile_arr[0]              [int(len(tile_arr[0])*0.35)              :int(len(tile_arr[0]              )*0.75)]):
            passthrough += 1

    if("top_left" in exits_arr):
        if('?' in tile_arr[0]              [:int(len(tile_arr[0])*0.35)]):
            passthrough += 1

    if("top_right" in exits_arr):
        if('?' in tile_arr[0]              [int(len(tile_arr[0])*0.75):]):
            passthrough += 1

    if("bottom_center" in exits_arr):
        if('?' in tile_arr[len(tile_arr)-1][int(len(tile_arr[len(tile_arr)-1])*0.35):int(len(tile_arr[len(tile_arr)-1])*0.75)]):
            passthrough += 1

    if("bottom_left" in exits_arr):
        if('?' in tile_arr[len(tile_arr)-1][:int(len(tile_arr[len(tile_arr)-1])*0.35)]):
            passthrough += 1

    if("bottom_right" in exits_arr):
        if('?' in tile_arr[len(tile_arr)-1][int(len(tile_arr[len(tile_arr)-1])*0.75):]):
            passthrough += 1


    return(passthrough == len(exits_arr))



def generate_dungeon(game_map, prinitng = False):
    global dungeon_tiles, dungeon_width, dungeon_height

    ############### Generate base ###############
    #vars
    dungeon_agents = 60 # number of agents spawned to carve random paths (first 5 always start at entrance)
    dungeon_agent_energy = 30 # number of tiles to be spawned by each agent

    #generate dungeon
    dungeon_tiles = []
    for _ in range(dungeon_height):
        dungeon_tiles.append([None]*int(dungeon_width))

    dungeon_tiles[0][int(dungeon_width/2)] = Dungeon_tile(int(dungeon_width/2), 0, "basic") # first room
    dungeon_tiles[0][int(dungeon_width/2)].exits["top_center"] = True
    

    ############### Agent generation ###############
    agent_num = 0

    if(prinitng):
        print("agents: " + str(dungeon_agents) + " (5 starting)")
        print("agent energy: " + str(dungeon_agent_energy))

        last_percentage = -1

    for agent in range(dungeon_agents):
        if(prinitng):
            percentage = int((agent/dungeon_agents)*100)
            
            if(last_percentage != percentage):
                if(percentage%10 == 0):
                    print("generating dungeons... ( " + str(percentage) + "% )")

        if(agent_num < 5):
            x = int(dungeon_width/2)
            y = 0
        else:
            y = random.randint(len(dungeon_tiles))
            x = random.choice(dungeon_tiles[y]).x

        for tile_num in range(dungeon_agent_energy):

            # random movement
            match random.choice(["l","l","l", "r","r","r", "u","ul","ur", "d","dl","dr"]):

                case "l":
                    if(dungeon_tile_possible_exits(dungeon_tiles[y][x].type, ["left"])):
                        if(x > 0):
                            x -= 1

                            if(dungeon_tiles[y][x] == None):
                                dungeon_tiles[y][x] = Dungeon_tile(x, y, random_dungeon_tile(["right"]))

                            if(dungeon_tile_possible_exits(dungeon_tiles[y][x].type, ["right"])):
                                dungeon_tiles[y][x+1].exits["left"] = True
                                dungeon_tiles[y][x].exits["right"] = True


                case "r":
                    if(dungeon_tile_possible_exits(dungeon_tiles[y][x].type, ["right"])):
                        if(x+1 < len(dungeon_tiles[0])):
                            x += 1

                            if(dungeon_tiles[y][x] == None):
                                dungeon_tiles[y][x] = Dungeon_tile(x, y, random_dungeon_tile(["left"]))

                            if(dungeon_tile_possible_exits(dungeon_tiles[y][x].type, ["left"])):
                                dungeon_tiles[y][x-1].exits["right"] = True
                                dungeon_tiles[y][x].exits["left"] = True


                case "u":
                    if(dungeon_tile_possible_exits(dungeon_tiles[y][x].type, ["top_center"])):
                        if(y > 0):
                            y -= 1

                            if(dungeon_tiles[y][x] == None):
                                dungeon_tiles[y][x] = Dungeon_tile(x, y, random_dungeon_tile(["bottom_center"]))

                            if(dungeon_tile_possible_exits(dungeon_tiles[y][x].type, ["bottom_center"])):
                                dungeon_tiles[y+1][x].exits["top_center"] = True
                                dungeon_tiles[y][x].exits["bottom_center"] = True

                case "ul":
                    if(dungeon_tile_possible_exits(dungeon_tiles[y][x].type, ["top_left"])):
                        if(y > 0):
                            y -= 1

                            if(dungeon_tiles[y][x] == None):
                                dungeon_tiles[y][x] = Dungeon_tile(x, y, random_dungeon_tile(["bottom_left"]))

                            if(dungeon_tile_possible_exits(dungeon_tiles[y][x].type, ["bottom_left"])):
                                dungeon_tiles[y+1][x].exits["top_left"] = True
                                dungeon_tiles[y][x].exits["bottom_left"] = True

                case "ur":
                    if(dungeon_tile_possible_exits(dungeon_tiles[y][x].type, ["top_right"])):
                        if(y > 0):
                            y -= 1

                            if(dungeon_tiles[y][x] == None):
                                dungeon_tiles[y][x] = Dungeon_tile(x, y, random_dungeon_tile(["bottom_right"]))

                            if(dungeon_tile_possible_exits(dungeon_tiles[y][x].type, ["bottom_right"])):
                                dungeon_tiles[y+1][x].exits["top_right"] = True
                                dungeon_tiles[y][x].exits["bottom_right"] = True


                case "d":
                    if(dungeon_tile_possible_exits(dungeon_tiles[y][x].type, ["bottom_center"])):
                        if(y+1 < len(dungeon_tiles)):
                            y +=1

                            if(dungeon_tiles[y][x] == None):
                                dungeon_tiles[y][x] = Dungeon_tile(x, y, random_dungeon_tile(["top_center"]))

                            if(dungeon_tile_possible_exits(dungeon_tiles[y][x].type, ["top_center"])):
                                dungeon_tiles[y-1][x].exits["bottom_center"] = True
                                dungeon_tiles[y][x].exits["top_center"] = True

                case "dl":
                    if(dungeon_tile_possible_exits(dungeon_tiles[y][x].type, ["bottom_left"])):
                        if(y+1 < len(dungeon_tiles)):
                            y +=1

                            if(dungeon_tiles[y][x] == None):
                                dungeon_tiles[y][x] = Dungeon_tile(x, y, random_dungeon_tile(["top_left"]))

                            if(dungeon_tile_possible_exits(dungeon_tiles[y][x].type, ["top_left"])):
                                dungeon_tiles[y-1][x].exits["bottom_left"] = True
                                dungeon_tiles[y][x].exits["top_left"] = True

                case "dr":
                    if(dungeon_tile_possible_exits(dungeon_tiles[y][x].type, ["bottom_right"])):
                        if(y+1 < len(dungeon_tiles)):
                            y +=1

                            if(dungeon_tiles[y][x] == None):
                                dungeon_tiles[y][x] = Dungeon_tile(x, y, random_dungeon_tile(["top_right"]))

                            if(dungeon_tile_possible_exits(dungeon_tiles[y][x].type, ["top_right"])):
                                dungeon_tiles[y-1][x].exits["bottom_right"] = True
                                dungeon_tiles[y][x].exits["top_right"] = True

    if(prinitng):
        print("generating dungeons... ( 100% )")

        print("Cleaning up dungeons...")

    # cleanup dungeon, to make sure no arenas spawn next to each other
    for row in dungeon_tiles:
        for tile in row:
            if(type(tile) == Dungeon_tile):
                if "Arena" in tile.type:
                    for y in range(-1, 2):
                        for x in range(-1, 2):
                            if(not((x == 0) and (y == 0))):
                                if((tile.y+y < len(dungeon_tiles)) and (tile.x+x < len(dungeon_tiles[tile.y+y]))):
                                    if(type(dungeon_tiles[tile.y+y][tile.x+x]) == Dungeon_tile):
                                        if "Arena" in dungeon_tiles[tile.y+y][tile.x+x].type:
                                            dungeon_tiles[tile.y+y][tile.x+x].type = "hallway_1"
    


    ############### place it ###############
    global dungeon_tile_width, dungeon_tile_height

    if(prinitng):
        print("aligning, placing dungeon...")

    #locate start point
    dungeon_startpoint = game_map[dungeon_y-1].find("▒▒▒▒▒▒▒▒▒▒▒▒") 

    # move original map to center
    for y in range(dungeon_y):
        game_map[y] = " "*(dungeon_tile_width*int(dungeon_width/2) - dungeon_startpoint) + game_map[y]

    # fill in empty space blow map
    for _ in range(len(game_map), dungeon_height*dungeon_tile_height + dungeon_y):
        game_map.append(dungeon_width*dungeon_tile_width*"▓") #▓    

    # recalculate coordinates
    for row in dungeon_tiles:
        for tile in row:
            if(type(tile) == Dungeon_tile):
                tile.x = (tile.x*dungeon_tile_width - int(dungeon_tile_width/2)) + 6 + (int(dungeon_tile_width/2))
                tile.y = (tile.y*dungeon_tile_height + dungeon_y)

    # replace empty space with tiles
    for row in dungeon_tiles:
        for tile in row:
            if(type(tile) == Dungeon_tile):
                
                tile_arr = []
                row = ""
                for char in Dungeon_map_presets[tile.type]:
                    if(char == '\n'):
                        if(len(row) > 0):
                            tile_arr.append(row)
                        row = ""
                    else:
                        row += char

                # manage exits
                for x in range(dungeon_tile_width):
                    if(x < 0.35*dungeon_tile_width):
                        if(tile_arr[0][x] == '?'):
                            if(tile.exits["top_left"]):
                                tile_arr[0] = tile_arr[0][:x] + ' ' + tile_arr[0][x+1:]
                            else:
                                tile_arr[0] = tile_arr[0][:x] + '▓' + tile_arr[0][x+1:]
                    
                    elif(x < 0.65*dungeon_tile_width):
                        if(tile_arr[0][x] == '?'):
                            if(tile.exits["top_center"]):
                                tile_arr[0] = tile_arr[0][:x] + ' ' + tile_arr[0][x+1:]
                            else:
                                tile_arr[0] = tile_arr[0][:x] + '▓' + tile_arr[0][x+1:]

                    else:
                        if(tile_arr[0][x] == '?'):
                            if(tile.exits["top_right"]):
                                tile_arr[0] = tile_arr[0][:x] + ' ' + tile_arr[0][x+1:]
                            else:
                                tile_arr[0] = tile_arr[0][:x] + '▓' + tile_arr[0][x+1:]

                    
                    if(x < 0.35*dungeon_tile_width):
                        if(tile_arr[len(tile_arr)-1][x] == '?'):
                            if(tile.exits["bottom_left"]):
                                tile_arr[len(tile_arr)-1] = tile_arr[len(tile_arr)-1][:x] + '▒' + tile_arr[len(tile_arr)-1][x+1:]
                            else:
                                tile_arr[len(tile_arr)-1] = tile_arr[len(tile_arr)-1][:x] + '▓' + tile_arr[len(tile_arr)-1][x+1:]
                    
                    elif(x < 0.65*dungeon_tile_width):
                        if(tile_arr[len(tile_arr)-1][x] == '?'):
                            if(tile.exits["bottom_center"]):
                                tile_arr[len(tile_arr)-1] = tile_arr[len(tile_arr)-1][:x] + '▒' + tile_arr[len(tile_arr)-1][x+1:]
                            else:
                                tile_arr[len(tile_arr)-1] = tile_arr[len(tile_arr)-1][:x] + '▓' + tile_arr[len(tile_arr)-1][x+1:]

                    else:
                        if(tile_arr[len(tile_arr)-1][x] == '?'):
                            if(tile.exits["bottom_right"]):
                                tile_arr[len(tile_arr)-1] = tile_arr[len(tile_arr)-1][:x] + '▒' + tile_arr[len(tile_arr)-1][x+1:]
                            else:
                                tile_arr[len(tile_arr)-1] = tile_arr[len(tile_arr)-1][:x] + '▓' + tile_arr[len(tile_arr)-1][x+1:]
                                

                
                for y in range(len(tile_arr)):
                    if(tile_arr[y][0] == '?'):
                        if(tile.exits["left"]):
                            tile_arr[y] = ' ' + tile_arr[y][1:]
                        else:
                            tile_arr[y] = '▓' + tile_arr[y][1:]

                    if(tile_arr[y][len(row)-1] == '?'):
                        if(tile.exits["right"]):
                            tile_arr[y] = tile_arr[y][:len(row)-1] + ' '
                        else:
                            tile_arr[y] = tile_arr[y][:len(row)-1] + '▓'

                # random object spawn chances
                for y in range(len(tile_arr)):
                    for x in range(len(tile_arr[y])):
                        if(tile_arr[y][x] == '['):
                            if(tile_arr[y][x+1] == 'B'):
                                if(random.randint(0, 2) == 0):
                                    tile_arr[y] = tile_arr[y][:x] + "   " + tile_arr[y][x+3:]

                game_map = add_tile(game_map, tile_arr, tile.x, tile.y)

    return(game_map)



def add_tile(game_map, texture, x, y):
    width = len(texture[0])

    x = x - int(width/2)


    for row in texture:
        game_map[y] = game_map[y][:x] + row[:len(row)] + game_map[y][x+width:]
        y += 1
    
    return game_map
            


# generates the game map based on the game_map_preset string
def generate_map(printing = True):
    global breakables

    if(printing):
        print("generating world...")

    # turn the game map string into an array of characters to actually work with...
    game_map = []
    breakables = []
    row = ""
    percentage_chunk_size = int(len(game_map_preset) / 100)
    percentage_chunk = percentage_chunk_size
    percentage = 0
    char_num = 0
    for char in game_map_preset:
        if char == '\n':
            game_map.append(row)
            row = ""
        else:
            row += char

        if(printing):
            char_num += 1
            if(char_num >= percentage_chunk):
                percentage_chunk += percentage_chunk_size
                percentage += 1
                
                if(percentage%10 == 0):
                    print("generating overworld... ( " + str(percentage) + "% )")

    global game_map_width, game_map_height

    if(printing):
        print("\naltering limit values... ")
    game_map_height = len(game_map)
    for row in game_map:
        if(len(row) > game_map_width):
            game_map_width = len(row)
    if(printing):
        print("map width: " + str(game_map_width))
        print("map height: " + str(game_map_height))

    if(printing):
        print("\nGenerating dungeons...")
    game_map = generate_dungeon(game_map, printing)

    if(printing):
        print("\naltering limit values... ")
    game_map_height = len(game_map)
    for row in game_map:
        if(len(row) > game_map_width):
            game_map_width = len(row)
    
    if(printing):
        print("map width: " + str(game_map_width))
        print("map height: " + str(game_map_height))

    if(printing):
        print("\nfilling in empty space")
    cnt = 0
    for y in range(len(game_map)):
        space = game_map_width - len(game_map[y])
        game_map[y] += ' '*space
        cnt += space
    if(printing):
        print("filled in: " + str(cnt))

    if(printing):
        print("\nadding objects...")
    counts = {'B': 0, 'N': 0, 'E':0, 'C':0, '?':0}

    global player, npcs, view_blindness, chests
    for y_pos in range(len(game_map)):
        for x_pos in range(len(game_map[y_pos])):
            if game_map[y_pos][x_pos] == '[': # object present
                
                # make object
                match game_map[y_pos][x_pos+1] :
                    case 'P':
                        player = Player(y= y_pos, x= x_pos+1)
                    
                    case 'B':
                        breakables.append(Breakable(x = x_pos, y = y_pos, items = rand_loot(), texture = random.choice(breakable_textrues)))
                        counts['B'] += 1

                    case '1':
                        npcs.append(NPC(x = x_pos, y = y_pos, texture = npc_textures['1'], texture_walk = npc_textures_walk['1'], dialoges=npc_dialoges['1']))
                        counts['N'] += 1

                    case '2':
                        interactables.append(Interactable(x = x_pos, y = y_pos, texture = interactable_textures['2'],
                                                          price = {"0":2, "1":2},
                                                          reward = "Rune",
                                                          minigame = "table"))
                        counts['N'] += 1
                        
                    case '3':
                        interactables.append(Interactable(x = x_pos, y = y_pos, texture = interactable_textures['3'],
                                                          price = {"Rune":4},
                                                          reward = "Dungeon reset",
                                                          minigame = "table"))
                        counts['N'] += 1
                    
                    case '4':
                        interactables.append(Interactable(x = x_pos, y = y_pos, texture = interactable_textures['4'],
                                                          price = {"True":2, "False":2},
                                                          reward = "Health",
                                                          minigame = "table"))
                        counts['N'] += 1
                        
                    case 'T':
                        triggers.append(Control_object(x = x_pos+1, y = y_pos))
                        counts['?'] += 1
                        
                    case 'G':
                        gates.append(Control_object(x = x_pos+1, y = y_pos))
                        counts['?'] += 1

                    case 'E':
                        enemies.append(Enemy(x = x_pos, y = y_pos, texture = npc_textures["1"], texture_walk = npc_textures_walk["1"], texture_ragdoll = npc_textures_ragdoll["1"], texture_crouch = npc_textures_crouch['1'], hp = 2))
                        counts['E'] += 1

                    case 'C':
                        chests.append(Breakable(x = x_pos, y = y_pos, items = rand_loot_chest(), texture = chest_texture))
                        counts['C'] += 1

                game_map[y_pos] = game_map[y_pos][:x_pos] + "   " + game_map[y_pos][x_pos+3:]

    if(printing):
        print("generated: " + str(counts['B']) + " breakables, " + str(counts['N']) + " NPCs, " + str(counts['E']) + " enemies, " + str(counts['C']) + " chests, " + str(counts['?']) + " game controll objects.")

    if(printing):
        print("\nsetting up player...")
    view_blindness = player.view_x*2


    if(printing):
        print("\nDONE! \n\nPress any key to continue... ")
        input()

    return game_map



def rand_loot():
    return({random.choice(("0", "1")):random.randint(1, 2)})



def rand_loot_chest():
    loot = {}

    loot[random.choice(("True", "False"))] = random.randint(2, 6)

    if random.randint(0, 1) == 0:
        loot["0"] = random.randint(4, 12)
        loot["1"] = random.randint(4, 12)
    else:
        loot[random.choice(("0", "1"))] = random.randint(8, 16)
    
    if random.randint(0, 6) == 0:
        loot["Rune"] = 1

    return(loot)



# the game mode in its entirity
def game():
    os.system('cls')

    global game_map, player, debug_info
    game_map = generate_map()

    os.system('cls')

    while(True):
        # keypresses
        if (msvcrt.kbhit()):
            keystroke = msvcrt.getch()

            # arrow keys
            if(keystroke == b'\xe0'):
                keystroke = msvcrt.getch()

                if(player.roll_steps == 0):

                    # tabs
                    if(keystroke == b'K'):
                        player.crouch = False
                        move_player(-1)
                        player.last_step_ts = time.perf_counter()
                        player.texture_frame -= 1
                        if(player.texture_frame < 0):
                            player.texture_frame = len(player.texture)-1
                        
                    elif(keystroke == b'M'):
                        player.crouch = False
                        move_player(1)
                        player.last_step_ts = time.perf_counter()
                        player.texture_frame += 1
                        if(player.texture_frame >= len(player.texture)):
                            player.texture_frame = 0

                    elif(keystroke == b'H'):
                        player.crouch = False

                        if(player.fly):
                            player.y -= 1

                        else:
                            climbing = False
                            
                            # rope
                            for x in range(int(-len(player.texture[0][-1])/2), int(len(player.texture[0][-1]) /2+0.5)):
                                if(game_map[player.y][player.x + x] == '▒'):
                                    climbing = True

                                    if(time.perf_counter() > player.last_step_ts + 0.06):
                                        player.last_step_ts = time.perf_counter()

                                        player.y -= 1
                                        player.texture_frame += 1
                                        if(player.texture_frame >= len(player.texture_up)):
                                            player.texture_frame = 0
                                        break

                            # the rest
                            if(not(climbing)):
                                for x in range(int(-len(player.texture[0][-1])/2), int(len(player.texture[0][-1]) /2+0.5)):
                                    if(game_map[player.y+1][player.x + x] in "█▓▒"):
                                        if(player.g_vel == 0):
                                            player.g_vel = 2.5
                                            break
                        

                    elif(keystroke == b'P'):
                        if(player.fly):
                            player.y += 1

                        else:
                            passable = True
                            for x in range(int(-len(player.texture[0][-1])/2), int(len(player.texture[0][-1]) /2+0.5)):
                                if(not (game_map[player.y+1][player.x + x] in "▒ ")):
                                    passable = False

                            if(passable):
                                player.y += 1
                                player.falling = True
                                player.texture_frame += 1
                                if(player.texture_frame >= len(player.texture_up)):
                                    player.texture_frame = 0
                            else:
                                player.falling = False
                                player.crouch = True

            # other keys
            elif(keystroke == b'w'):
                if(player.stamina > 0):
                    global last_roll_ts
                    last_roll_ts = time.perf_counter()
                    player.roll_steps = 30
                player.crouch = False

            elif(keystroke == b'e'):
                for npc in npcs:
                    if((abs(npc.x - player.x) < 10) and (abs(npc.y - player.y) < 5)):
                        npc.dialoge_charnum = 0
                        if(npc.dialoge_part == -1):
                            npc.dialog = random.choice(npc.dialoges)

                        if(npc.dialoge_part >= len(npc.dialog)-1):
                            npc.dialoge_part = -1
                        else:
                            npc.dialoge_part += 1

                for chest in chests:
                    if((abs(chest.x - player.x) < 10) and (abs(chest.y - player.y) < 5)):
                        if((chest.present) and (chest.frame == 0)):
                            chest.frame = 1
                            chest.anim_timer = time.perf_counter()

                            for item in chest.items:
                                if(player.inventory[item] == None):
                                    player.inventory[item] = chest.items[item]
                                else:
                                    player.inventory[item] += chest.items[item]
                            
                
                for interactable in interactables:
                    if((abs(interactable.x - player.x) < 25) and (abs(interactable.y - player.y) < 5)):

                        affordable = True
                        for item in interactable.price:
                            if player.inventory[item] < interactable.price[item]:
                                affordable = False
                        
                        if(affordable):
                            if((interactable.minigame == None) or (minigame("table"))):
                                for item in interactable.price:
                                    player.inventory[item] -= interactable.price[item]

                                try:
                                    player.inventory[interactable.reward] += 1
                                except:
                                    player.inventory[interactable.reward] = 1
                                
            
            elif(keystroke == b'f'):
                for npc in npcs:
                    if((abs(npc.x - player.x) < 10) and (abs(npc.y - player.y) < 5)):
                        npc.texture_frame = 0
                        npc.following = not(npc.following)

            elif(keystroke == b'1'):
                debug_info = not(debug_info)

            elif(keystroke == b'2'):
                player.fly = not(player.fly)

            elif(keystroke == b'3'):
                player.nightmare_vision = not(player.nightmare_vision)

            else:
                player.crouch = False
        
        world_backend()

        objects_backend()

        player_backend()

        if(player.hp <= 0):
            break

        player_roll()

        if(not(player.fly)):
            player_gravity()
        npc_gravity()
        
        render_game()



def player_backend():
    global player, player_wiggle_timer

    if((player.falling) or (player.upping)):
        if(time.perf_counter() > player_wiggle_timer):
            player_wiggle_timer = time.perf_counter() + 0.05

            player.texture_frame += 1
            if(player.texture_frame >= len(player.texture_up)):
                player.texture_frame = 0



def world_backend():
    global player, game_map, npcs, effects, rift_anim_timer, dungeon_doors_lock, enemies, chests, triggers, gates, breakables, interactables

    # dungeon regeneration
    if "Dungeon reset" in list(player.inventory.keys()):
        del player.inventory["Dungeon reset"]

        player_x = player.x
        player_y = player.y
        npcs_bk = npcs.copy()
        enemies = []
        chests = []
        triggers = []
        gates = []
        breakables = []
        interactables = []
        dungeon_doors_lock = False

        game_map = generate_map(printing=False)

        player.x = player_x
        player.y = player_y
        npcs = npcs_bk.copy()

    # health regeneration
    if "Health" in list(player.inventory.keys()):
        del player.inventory["Health"]
        player.hp += 5
        if(player.hp > 10):
            player.hp = 10

    for trigger in triggers:
        if trigger.x == player.x:
            if (abs(trigger.y - player.y) <= 6):
                dungeon_doors_lock = True

    # enemies
    in_fight = False
    for enemy in enemies:
        if((abs(player.x - enemy.x) < 60) and (abs(player.y - enemy.y) < 20)):
            if(dungeon_doors_lock):
                enemy.following = True
        
        # unlocking rooms
        if(enemy.following):
            in_fight = True

    # unlocking rooms
    if(not(in_fight)):
        dungeon_doors_lock = False

    # rifts
    if(random.randint(0, 15000) == 0):

        effects.append(Effect(player.x + ((random.randint(0, 1)*2)-1)*random.randint(80, 240), player.y + random.randint(-30, 30), effect_textures["rift"], time.perf_counter() + 60))

    
    # effects
    dead = []
    if(time.perf_counter() > rift_anim_timer):
        rift_anim_timer = time.perf_counter()+0.1

        for effect_num in range(len(effects)):
            # end of effect
            if(time.perf_counter() >= effects[effect_num].death_ts):
                dead.append(effect_num)
            
            # animation
            effects[effect_num].texture_frame += 1
            if(effects[effect_num].texture_frame >= len(effects[effect_num].texture)):
                effects[effect_num].texture_frame = 0

            # movement
            if(effects[effect_num].texture_frame % 4 == 0):
                effects[effect_num].x += effects[effect_num].dir_x
    
    for n in range(len(dead)):
        effects.pop(dead[0]-n)
        dead.pop(0)

    while(len(effects) > 512):
        effects.pop(0)
    


def objects_backend():
    global anim_timer, text_anim_timer, interactable_anim_timer, npcs, enemies, npc_mov_timer, npc_rag_timer
    for breakable in breakables:
        if(breakable.present):
            if(breakable.frame > 0):
                if(breakable.anim_timer + 0.06 < time.perf_counter()):
                    breakable.anim_timer = time.perf_counter()

                    breakable.frame +=1
                    if(breakable.frame >= len(breakable.texture)-1):
                        breakable.present = False

    for chest in chests:
        if(chest.present):
            if(chest.frame > 0):
                if(chest.anim_timer + 0.2 < time.perf_counter()):
                    chest.anim_timer = time.perf_counter()

                    chest.frame +=1
                    if(chest.frame >= len(chest.texture)-1):
                        chest.present = False

    # inteactable objects animations
    if(interactable_anim_timer + 0.5 < time.perf_counter()):
        interactable_anim_timer = time.perf_counter()

        for interactable in interactables:
            interactable.texture_frame += 1
                
            if(interactable.texture_frame >= len(interactable.texture)):
                interactable.texture_frame = 0

    # npc texture animation
    if(anim_timer + 1 < time.perf_counter()):
        anim_timer = time.perf_counter()

        for npc in npcs+enemies:
            if(not(npc.following)):
                npc.texture_frame += 1
                
                if(npc.texture_frame >= len(npc.texture)):
                    npc.texture_frame = 0

    if(npc_rag_timer < time.perf_counter()):
        npc_rag_timer = time.perf_counter() + 0.01
        for enemy in enemies:
            if(enemy.ragdoll_frame > 0):
                enemy.ragdoll_frame -= 1

                passable = True
                for y in range(1, len(enemy.texture_crouch)):
                    if(game_map[enemy.y-y][enemy.x + enemy.ragdoll_dir*int(len(enemy.texture_walk[0][0])/2 +0.5)] in "█▓"):
                        passable = False

                if(passable):
                    enemy.x += enemy.ragdoll_dir

    
    dead = []
    for enemy_num in range(len(enemies)):
        if(enemies[enemy_num].hp <= 0):
            if(enemies[enemy_num].ragdoll_frame == 0):
                if(enemies[enemy_num].knockout_frame == 0):
                    dead.append(enemy_num)

    for death in dead:
        enemies.pop(death)

    if(not(BFS_PATHFINDING)):

        # simple pathfinding
        if(npc_mov_timer < time.perf_counter()):
            npc_mov_timer = time.perf_counter() + 0.05
            for npc in npcs+enemies:
                if(type(npc) == Enemy):
                    if(npc.ragdoll_frame > 0):
                        continue
                    if(npc.knockout_frame > 0):
                        npc.knockout_frame -= 1
                        continue

                if(npc.following):
                    if((abs(player.x - npc.x) > 25) or (abs(player.y - npc.y) > 10)):
                        npc.moving = True
                    elif((abs(player.x - npc.x) < npc.stop_dist) and (abs(player.y - npc.y) < npc.stop_dist)):
                        npc.moving = False
                    
                    if(npc.moving):
                        if(npc.x < player.x):
                            x_dir = 1
                        else:
                            x_dir = -1

                        passable = True
                        for y in range(1, len(npc.texture_walk[0])):
                            if(game_map[npc.y-y][npc.x + x_dir*int(len(npc.texture_walk[0][0])/2 +0.5)] in "█▓"):
                                passable = False

                        jumpable = False
                        for y in range(0, 4):
                            for x in range(-1, 2):
                                if(game_map[npc.y-y][npc.x+x] == '▒'):
                                    jumpable = True

                        floor = False
                        ramp = False
                        fallable = True
                        for x in range(-int((len(npc.texture_walk[0][0]))/2), int((len(npc.texture_walk[0][0]))/2)):
                            if(game_map[npc.y+1][npc.x + x] in "█▓"):
                                floor = True
                                fallable = False
                            elif(game_map[npc.y+1][npc.x + x] == '▒'):
                                ramp = True
                            elif(not(game_map[npc.y+1][npc.x + x] == ' ')):
                                fallable = False
                        ramp = ramp and fallable

                        # jumping down
                        if(not(floor) and ramp and (player.y > npc.y)):
                            npc.y += 2

                        # other
                        else:
                            if(passable):
                                if(game_map[npc.y][npc.x + x_dir*int(len(npc.texture_walk[0][0])/2 +0.5)] in "█▓▒"):
                                    npc.y -= 1
                                    npc.x += x_dir
                                else:
                                    npc.x += x_dir

                                npc.texture_frame += 1
                                if(npc.texture_frame >= len(npc.texture_walk)-1):
                                    npc.texture_frame = 0
                            else:
                                if(player.y < npc.y+5):
                                    if(floor or ramp):
                                        npc.g_vel = 2

                            if(player.y < npc.y):
                                if(floor or ramp):
                                    if(jumpable):
                                        npc.g_vel = 2

    else:
        # BFS pathfinding
        if(npc_mov_timer < time.perf_counter()):
            npc_mov_timer = time.perf_counter() + 0.05

            for npc in npcs+enemies:
                if(type(npc) == Enemy):
                    if(npc.ragdoll_frame > 0):
                        continue
                    if(npc.knockout_frame > 0):
                        npc.knockout_frame -= 1
                        continue

                if(npc.following):
                    if((abs(player.x - npc.x) > 25) or (abs(player.y - npc.y) >= 6)):
                        npc.moving = True
                    elif((abs(player.x - npc.x) < npc.stop_dist) and (abs(player.y - npc.y) <= 2)):
                        npc.moving = False
                    
                    if(npc.moving):
                        # path generation
                        if((time.perf_counter() > npc.bfs_reload_timer)):
                            npc.bfs_reload_timer = time.perf_counter() + 1

                            npc.bfs_path = bfs_algorithm(npc, player)

                        # movement
                        if(len(npc.bfs_path) > 0):
                            point = npc.bfs_path[-1]

                            jumpable = False

                            for x in range(-2, 3):
                                if(game_map[npc.y+1][npc.x + x] in "█▓▒"):
                                    jumpable = True
                            
                            if(point[1] < npc.y):
                                if(abs(point[1] - npc.y) == 1):
                                    npc.y -= 1
                                    npc.x = point[0]
                                else:
                                    if(jumpable):
                                        if(npc.g_vel == 0):
                                            npc.x = point[0]
                                            npc.g_vel = 2
                            else:
                                npc.x = point[0]
                                
                                if(point[1] > npc.y):
                                    npc.y += 1

                            npc.texture_frame += 1
                            if(npc.texture_frame >= len(npc.texture_walk)-1):
                                npc.texture_frame = 0

                            if(npc.y == point[1]):
                                if(npc.g_vel == 0):
                                    npc.bfs_path.pop()

                        

            for enemy in enemies:
                if(enemy.following):
                    if(enemy.knockout_frame == 0):
                        if(player.roll_steps == 0):
                            if((abs(enemy.x - player.x) <= 1) and (abs(enemy.y - player.y) <= 1)):
                                player.hp -= 1
                                player.g_vel = 2
                                enemy.knockout_frame = 20
                    

        
        # npc dialog string animation
        if(text_anim_timer + 0.05 < time.perf_counter()):
            text_anim_timer = time.perf_counter()

            for npc in npcs:
                if(npc.dialoge_part >= 0):
                    if(npc.dialoge_charnum <= len(npc.dialog[npc.dialoge_part])):
                        npc.dialoge_charnum += 1



# base of the bfs pathfinding algorithm
def bfs_algorithm(entity_from, entity_to):

    global bfs_explored, bfs_queue, debug_bfs_considered, bfs_energy, bfs_closest_node, bfs_closest_node_dist
    
    bfs_explored = []
    bfs_queue = []
    debug_bfs_considered = []
    bfs_energy = 800
    bfs_closest_node = None
    bfs_closest_node_dist = 99999999

    path = bfs_rec(BFS_node(entity_from.x, entity_from.y), (entity_to.x, entity_to.y))
    
    if(path == None):
        if(bfs_closest_node == None):
            return([])
        else:
            return(bfs_backtrace(bfs_closest_node))

    return(bfs_backtrace(bfs_closest_node))


# recursive part of the bfs pathfinding algorithm
def bfs_rec(current, end_point):
    global bfs_explored, bfs_queue, debug_bfs_considered, bfs_energy, bfs_closest_node, bfs_closest_node_dist

    bfs_energy -= 1
    if(bfs_energy < 0):
        return None

    if((current.x == end_point[0]) and (current.y == end_point[1])):
        return(current)
    
    distance = abs(current.x - end_point[0]) + abs(current.y - end_point[1])*4
    if(distance < bfs_closest_node_dist):
        bfs_closest_node = current
        bfs_closest_node_dist = distance

    possible = bfs_possible(current)

    for possibility in possible:
        if(not((possibility.x, possibility.y) in bfs_explored)):
            bfs_queue.append(possibility)
            bfs_explored.append((possibility.x, possibility.y))

            debug_bfs_considered.append((possibility.x, possibility.y))

    if(len(bfs_queue) < 1):
        return(None)
    
    priority_node = bfs_queue[0]
    bfs_queue = bfs_queue[1:]
    path = bfs_rec(priority_node, end_point)

    return(path)


# returns a path a node has taken in the bfs pathfinding algorithm
def bfs_backtrace(path):
    trace = []

    while(True):
        trace.append((path.x, path.y))
        if(path.parent == None):
            return(trace)
        path = path.parent


# returns filtered possible positions that the ai can aim for in the bfs pathfinding algorithm
def bfs_possible(node):
    possible = []

    # left/right
    for x in range(-1, 2, 2):

        # check ground
        keep = False
        for x_ in range(-2, 3):
            if(game_map[node.y+1][node.x+x+x_] in "█▓▒"):
                keep = True

        if(keep):
            # check space
            for y_ in range(0, 5):
                for x_ in range(-2, 3):
                    if(not(game_map[node.y - y_][node.x+x+x_] in " ▒")):
                        keep = False

            if(keep):
                possible.append(BFS_node(node.x+x, node.y, parent=node))

    # stairs up
    for x in range(-1, 2, 2):

        # stair present
        if(game_map[node.y][node.x+x*3] in "█▓▒"):
            
            # check space
            keep = True
            for y_ in range(0, 5):
                for x_ in range(-2, 3):
                    if(not(game_map[node.y-1 - y_][node.x+x+x_] in " ▒")):
                        keep = False

            if(keep):
                possible.append(BFS_node(node.x+x, node.y-1, parent=node))

    # jump down
    for x in range(-1, 2, 2):

        for y in range(1, 40):
            keep = True
            for x_ in range(-2, 3):
                if(game_map[node.y+y][node.x+x+x_] in "█▓"):
                    keep = False
                    break
            if(not(keep)):
                break

            # check ground
            keep = False
            for x_ in range(-2, 3):
                if(game_map[node.y+y+1][node.x+x+x_] in "█▓▒"):
                    keep = True

            if(keep):
                # check space
                for y_ in range(0, 5):
                    for x_ in range(-2, 3):
                        if(not(game_map[node.y+y-y_][node.x+x+x_] in " ▒")):
                            keep = False

                if(keep):
                    if(game_map[node.y+y][node.x+x] == " "):
                        possible.append(BFS_node(node.x+x, node.y+y, parent=node))
                        break
    
    # jump up
    for x in range(-1, 2, 2):

        for y in range(4, 1, -1):

            # check ground
            keep = False
            for x_ in range(-2, 3):
                if(game_map[node.y-y+1][node.x+x+x_] in "█▓▒"):
                    keep = True

            if(keep):
                # check space
                for y_ in range(0, 5):
                    for x_ in range(-2, 3):
                        if(not(game_map[node.y-y-y_][node.x+x+x_] in " ▒")):
                            keep = False

                if(keep):

                    # check celings
                    for y_ in range(0, y):
                        for x_ in range(-1, 2):
                            if(not(game_map[node.y-y-y_][node.x+x+x_] in " ▒")):
                                keep = False

                    if(keep):
                        if(game_map[node.y-y][node.x+x] == " "):
                            possible.append(BFS_node(node.x+x, node.y-y, parent=node))
                            break

    return(possible)



def move_player(x):
    global player

    if(not(player.fly)):
        # check collisions
        passable = True
        for y in range(1, len(player.texture[0])):
            if(game_map[player.y-y][player.x + x*int(len(player.texture[0][0])/2 +0.5)] in "█▓"):
                passable = False

        if(passable):
            if(game_map[player.y][player.x + x*int(len(player.texture[0][0])/2 +0.5)] in "█▓▒"):
                player.y -= 1
                player.x += x
            else:
                player.x += x

        player.last_x_dir = x


    else:
        player.x += x
        


def player_gravity():
    global player, g_timer

    #timer
    if(time.perf_counter() > g_timer):

        solid = False
        for x in range(int(-len(player.texture[0][-1])/2), int(len(player.texture[0][-1]) /2+0.5)):
            if(game_map[player.y+1][player.x + x] in "█▓▒"):
                solid = True

        if((not(solid)) or (not(player.g_vel == 0))):
            player.g_vel -= 0.5
            g_timer = time.perf_counter() + 0.05

        player.upping = False
        player.falling = False

        # movement
        for _ in range(abs(int(player.g_vel))):

            # check floor collision
            if(player.g_vel < 0):
                solid_floor = False
                for x in range(int(-len(player.texture[0][-1])/2), int(len(player.texture[0][-1]) /2+0.5)):
                    if(game_map[player.y+1][player.x + x] in "█▓▒"):
                        solid_floor = True
                        break

                if(solid_floor):
                    player.g_vel = 0
                    break


            # check for ceiling collision
            if(player.g_vel > 0):
                solid_roof = False
                for x in range(int(-len(player.texture[0][-1])/2), int(len(player.texture[0][-1]) /2+0.5)):
                    if(game_map[(player.y -1)-len(player.texture[0]) +1][player.x + x] in "█▓"):
                        solid_roof = True
                        break
            
                if(solid_roof):
                    player.g_vel = 0
                    break

            if(player.g_vel > 0):
                player.y -= 1
                player.upping = True
                player.falling = False
            elif(player.g_vel < 0):
                player.y += 1
                player.falling = True
                player.upping = False
                            


def npc_gravity():
    global npcs

    for npc in npcs + enemies:
        if(npc.following):

            # check inground collision
            burried = True
            while(burried):
                burried = False
                for x in range(int(-len(npc.texture[0][-1])/2), int(len(npc.texture[0][-1]) /2+0.5)):
                    if(game_map[npc.y][npc.x + x] in "█▓"):
                        burried = True
                        npc.y -= 1

            # check floor collision
            solid = False
            for x in range(int(-len(npc.texture[0][-1])/2), int(len(npc.texture[0][-1]) /2+0.5)):
                if(game_map[npc.y+1][npc.x + x] in "█▓▒"):
                    solid = True
            
            if(solid):
                if(npc.g_vel <= 0.5):
                    npc.g_vel = 0


            # check for ceiling collision
            if(npc.g_vel > 0):

                solid_roof = True
                while(solid_roof):
                    solid_roof = False
                    for x in range(int(-len(npc.texture[0][-1])/2), int(len(npc.texture[0][-1]) /2+0.5)):
                        if(game_map[(npc.y - int(npc.g_vel))-len(npc.texture[0])][npc.x + x] in "█▓"):
                            solid_roof = True
                
                    if(solid_roof):
                        npc.g_vel -= 0.5

            
            #timer
            if(time.perf_counter() > npc.g_timer):

                if(not solid):
                    npc.g_vel -= 0.5
                    npc.g_timer = time.perf_counter() + 0.1


                # move npc
                npc.y -= int(npc.g_vel)



def player_roll():
    global player, roll_timer, stamina_timer, last_roll_ts

    # stamina
    if(time.perf_counter() > stamina_timer):
        stamina_timer = time.perf_counter() + 0.02

        if(player.roll_steps > 0):
            player.stamina -= 1
        if(player.stamina < player.max_stamina):
            if(time.perf_counter() > last_roll_ts + 1):
                player.stamina += 1
        
    if(player.stamina <= 0):
        player.roll_steps = 0

    # rolling
    if(player.roll_steps > 0):
        if(time.perf_counter() > roll_timer):

            roll_timer = time.perf_counter() + 0.01
            player.roll_steps -= 1
            move_player(player.last_x_dir)

            for breakable in breakables:
                if((player.x == breakable.x) and (player.y == breakable.y)):

                    if((breakable.present) and (breakable.frame == 0)):
                        breakable.frame = 1
                        breakable.anim_timer = time.perf_counter()

                        # # adding items to player inventory
                        for item in breakable.items:
                            if(player.inventory[item] == None):
                                player.inventory[item] = breakable.items[item]
                            else:
                                player.inventory[item] += breakable.items[item]

            for enemy in enemies:
                if((abs(player.x - enemy.x) < 2) and (abs(player.y - enemy.y) < 2) and (enemy.ragdoll_frame == 0)):
                    enemy.ragdoll_frame = 20
                    enemy.knockout_frame = 20
                    enemy.ragdoll_dir = player.last_x_dir
                    enemy.g_vel = 1
                    enemy.hp -= 1

                    player.last_x_dir = -player.last_x_dir



def interaction_table(interactable):

    price_str = "Price: "
    for item in interactable.price:
        price_str += str(interactable.price[item]) + "x(" + item + ")  "

    if(interactable.minigame == None):
        table_inside = [
            "Price: " + price_str,
            "Reward: " + interactable.reward
        ]
    else:
        table_inside = [
            "Price: " + price_str,
            "Reward: " + interactable.reward,
            "Minigame: " + str(interactable.minigame)
        ]

    width = 0
    for row in table_inside:
        if(len(row) > width):
            width = len(row)

    table = ["#" + "="*width + "#"]
    for row in table_inside:
        table.append("|" + row + " "*(width - len(row)) + "|")
    table.append("#" + "="*width + "#")

    return(table)



def minigame(minigame):
    global view, minigame_graphics

    if(minigame == "table"):
        practice_premade_table = [
            "a or b",
            "a and b",
            "a or b or c",
            "a and b and c",
            "a implies b",
            "(not a) or a"
        ]
        
        practice_eq = random.choice(practice_premade_table)

        assigned_char = ''
        table_user = {}
        cur_y = 0

        practicing = True
        while(practicing):

            # keypresses
            if (msvcrt.kbhit()):
                keystroke = msvcrt.getch()

                # arrow keys
                if(keystroke == b'\xe0'):
                    keystroke = msvcrt.getch()

                    if(keystroke == b'H'):
                        cur_y-=1
                    elif(keystroke == b'P'):
                        cur_y+=1
            
                #ESC
                elif(keystroke == b'\x1b'):
                    minigame_graphics = None
                    return False
                
                # others
                else:
                    try:
                        char = str(keystroke)[2:-1]

                        if(char in ('0', '1')):
                            assigned_char = char

                    except:
                        pass
                    


            standardized = standardize(practice_eq)
            simplified = simplify(standardized)
            table = make_table(simplified)

            window_width = 40

            table_inside = []

            table_inside.append(window_width*"=")
            table_inside.append(center("Truth table", window_width))
            table_inside.append(window_width*"=")

            table_inside.append("")

            table_inside.append(center("__ASSIGNMENT__", window_width))
            table_inside.append(center(standardized.str(), window_width))
            table_inside.append("")

            table_inside.append(window_width*"=")

            # variables
            vars_str = "|"
            if(type(simplified) == Proposition_complex):
                for var in simplified.variables():
                    vars_str += " " + str(var) + " |"
            else:
                vars_str += " " + str(simplified) + " |"

            table_arr = []

            # construct table
            table_arr.append(vars_str + " Result  |")
            divider_str = ""
            for char in vars_str:
                if(char == "|"):
                    divider_str += "|"
                else:
                    divider_str += "-"
            table_arr.append(divider_str + "---------|")

            if(cur_y < 0):
                cur_y = 0
            elif(cur_y >= len(list(table.keys()))):
                cur_y = len(list(table.keys()))-1

            table_y = 0
            for key in table:
                if(table_y == cur_y):
                    if(assigned_char in ('0', '1')):
                        table_user[key] = assigned_char
                        assigned_char = ' '
                    try:
                        table_arr.append(str(key) + "  >>" + table_user[key] + "<<  |")
                    except:
                        table_arr.append(str(key) + "  >> <<  |")
                else:
                    try:
                        table_arr.append(str(key) + "    " + table_user[key] + "    |")
                    except:
                        table_arr.append(str(key) + "         |")
                table_y += 1

            # center table
            table_str_arr = []
            for row in table_arr:
                table_str_arr.append(center(row, window_width))

            # render table
            table_inside.append("")
            for table_str in table_str_arr:
                table_inside.append(table_str)

            width = 0
            for row in table_inside:
                if(len(row) > width):
                    width = len(row)

            table_final = ["#" + "="*width + "#"]
            for row in table_inside:
                table_final.append("|" + row + " "*(width - len(row)) + "|")
            table_final.append("#" + "="*width + "#")

            minigame_graphics = table_final
            render_game()

            # check validity
            solved = True
            for key in table:
                try:
                    if(not(table[key] == table_user[key])):
                        solved = False
                except:
                    solved = False

            if(solved):
                minigame_graphics = None
                return(True)
            
    else:
        print("Not implemented !!!")
        input()

    

def render_game():

    global game_map, player, view

    # make the visible screen array
    view = []

    limit_y_l = player.y-player.view_y
    limit_y_r = player.y+player.view_y
    limit_x_l = player.x-player.view_x
    limit_x_r = player.x+player.view_x

    offscreen_x_l = 0
    offscreen_x_r = 0

    if(limit_y_l < 0):
        limit_y_l = 0
    elif(limit_y_r > game_map_height):
        limit_y_r = game_map_height
    if(limit_x_l < 0):
        offscreen_x_l = abs(limit_x_l)
        limit_x_l = 0
    elif(limit_x_r > game_map_width):
        offscreen_x_r = limit_x_r-game_map_width
        limit_x_r = game_map_width

    for row in game_map[limit_y_l:limit_y_r]:
        view.append(row[limit_x_l:limit_x_r])

    if(not((player.falling) or (player.upping))):
        if(time.perf_counter() > player.last_step_ts + 0.25):
            player.texture_frame = 0

    if(time.perf_counter() > player.last_blink_ts + 2):
        player.blink = True
        if(time.perf_counter() > player.last_blink_ts + 2.2):
            player.blink = False
            player.last_blink_ts = time.perf_counter()


    # gates
    for gate in gates:
        if(dungeon_doors_lock):
            y = 0
            while(y < 20):
                if(game_map[gate.y-y][gate.x] == " "):
                    game_map[gate.y-y] = game_map[gate.y-y][:gate.x] + "█" + game_map[gate.y-y][gate.x+1:]
                    y += 1
                else:
                    break

        else:
            y = 0
            while(y < 20):
                if(game_map[gate.y-y][gate.x] == "█"):
                    game_map[gate.y-y] = game_map[gate.y-y][:gate.x] + " " + game_map[gate.y-y][gate.x+1:]
                    y += 1
                else:
                    break

    # add interactables
    for interactable in interactables:
        view = add_graphics(view, interactable.texture[interactable.texture_frame], interactable.x-limit_x_l, interactable.y-limit_y_l)
        if((abs(player.x - interactable.x) < 25) and abs(player.y - interactable.y) < 10):
            view = add_graphics(view, interaction_table(interactable), interactable.x-limit_x_l, interactable.y-limit_y_l-10, False)

    # add npcs
    for npc in npcs:

        if(npc.following):
            view = add_graphics(view, npc.texture_walk[npc.texture_frame], npc.x-limit_x_l, npc.y-limit_y_l)
        else:
            view = add_graphics(view, npc.texture[npc.texture_frame], npc.x-limit_x_l, npc.y-limit_y_l)


        if(npc.dialoge_part == -1):
            if((abs(npc.x - player.x) < 10) and (abs(npc.y - player.y) < 5)):
                view = add_graphics(view, ["╔═══╗", "║ E ║", "╚═══╝"], npc.x-limit_x_l, npc.y-limit_y_l-5, False)
        else:
            view = add_graphics(view, [npc.dialog[npc.dialoge_part][:npc.dialoge_charnum]], npc.x-limit_x_l, npc.y-limit_y_l-5, False)
        
    # add enemies
    for enemy in enemies:
        if(enemy.ragdoll_frame > 0):
            view = add_graphics(view, enemy.texture_ragdoll[int(enemy.ragdoll_frame%2+0.5)], enemy.x-limit_x_l, enemy.y-limit_y_l)
        elif(enemy.knockout_frame > 0):
            view = add_graphics(view, enemy.texture_crouch, enemy.x-limit_x_l, enemy.y-limit_y_l)
            view = add_graphics(view, [" ... "], enemy.x-limit_x_l, enemy.y-limit_y_l-len(enemy.texture_crouch))

        elif(enemy.following):
            view = add_graphics(view, enemy.texture_walk[enemy.texture_frame], enemy.x-limit_x_l, enemy.y-limit_y_l)
            view = add_graphics(view, [str(enemy.hp)], enemy.x-limit_x_l, enemy.y-limit_y_l-len(enemy.texture_walk[enemy.texture_frame]))
        else:
            view = add_graphics(view, enemy.texture[enemy.texture_frame], enemy.x-limit_x_l, enemy.y-limit_y_l)
            view = add_graphics(view, [str(enemy.hp)], enemy.x-limit_x_l, enemy.y-limit_y_l-len(enemy.texture[enemy.texture_frame]))


    if(player.roll_steps > 0):
        if(player.last_x_dir == 1):
            view = add_graphics(view, player.texture_shadows[3], player.x-4-limit_x_l, player.y-limit_y_l)
            view = add_graphics(view, player.texture_shadows[2], player.x-2-limit_x_l, player.y-limit_y_l)
        elif(player.last_x_dir == -1):
            view = add_graphics(view, player.texture_shadows[3], player.x+4-limit_x_l, player.y-limit_y_l)
            view = add_graphics(view, player.texture_shadows[2], player.x+2-limit_x_l, player.y-limit_y_l)

        view = add_graphics(view, player.texture_roll[int(player.roll_steps/4) % len(player.texture_roll)], player.x-limit_x_l, player.y-limit_y_l)
    
    else:
        if(player.crouch):
            texture = player.texture_crouch.copy()
        elif(player.falling):
            texture = player.texture_down[player.texture_frame].copy()
        elif(player.upping):
            texture = player.texture_up[player.texture_frame].copy()
        else:
            texture = player.texture[player.texture_frame].copy()
            if(player.blink):
                texture[1] = "█████"
            
        view = add_graphics(view, texture, player.x-limit_x_l, player.y-limit_y_l)


    for breakable in breakables:

        view = add_graphics(view, breakable.texture[breakable.frame], breakable.x-limit_x_l, breakable.y-limit_y_l)

        if((breakable.frame > 0) and (breakable.anim_timer + 2 > time.perf_counter())):

            str_arr = []
            length = 0
            for item in breakable.items:
                str_arr.append("(" + str(item) + ") x " + str(breakable.items[item]))
                if len(str_arr[-1]) > length:
                    length = len(str_arr[-1])
            for arr_num in range(len(str_arr)):
                str_arr[arr_num] = str_arr[arr_num] + " "*(length-len(str_arr[arr_num]))
                
            view = add_graphics(view, str_arr, breakable.x-limit_x_l, breakable.y-limit_y_l - breakable.frame, False)

    for chest in chests:
        view = add_graphics(view, chest.texture[chest.frame], chest.x-limit_x_l, chest.y-limit_y_l)

        if((chest.frame > 0) and (chest.anim_timer + 2 > time.perf_counter())):
            str_arr = []
            length = 0
            for item in chest.items:
                str_arr.append("(" + str(item) + ") x " + str(chest.items[item]))
                if len(str_arr[-1]) > length:
                    length = len(str_arr[-1])
            for arr_num in range(len(str_arr)):
                str_arr[arr_num] = str_arr[arr_num] + " "*(length-len(str_arr[arr_num]))

            view = add_graphics(view, str_arr, chest.x-limit_x_l, chest.y-limit_y_l - chest.frame - 4, False)
        
        elif(chest.present and (abs(player.x - chest.x) < 10) and (abs(player.y - chest.y) < 5)):
            view = add_graphics(view, ["╔═══╗", "║ E ║", "╚═══╝"], chest.x-limit_x_l, chest.y-limit_y_l-5, False)

    if(minigame_graphics):
        view = add_graphics(view, minigame_graphics, player.x-limit_x_l, player.y-limit_y_l +int(len(minigame_graphics)/2), False)

    
    # dungeon minimap
    if(player.y > dungeon_y):

        for y in range(-1, 2):
            for x in range(-1, 2):
                if(type(dungeon_tiles[x + int((player.y-dungeon_y)/dungeon_tile_height)][y + int((player.x + int(dungeon_tile_width/2))/dungeon_tile_width)]) == Dungeon_tile):
                    dungeon_tiles[x + int((player.y-dungeon_y)/dungeon_tile_height)][y + int((player.x + int(dungeon_tile_width/2))/dungeon_tile_width)].revealed = True

        minimap = ["█████████████████"]
        for y in range(-3, 4):
            row = "█"

            for x in range(-7, 8):
                try:
                    tile = dungeon_tiles[y + int((player.y-dungeon_y)/dungeon_tile_height)][x + int((player.x + int(dungeon_tile_width/2))/dungeon_tile_width)]
                    
                    if((tile == None) or (not(tile.revealed))):
                        row += ' '
                    else:
                        if(tile.exits["left"]):
                            if(tile.exits["right"]):
                                if(tile.exits["top_left"] or tile.exits["top_center"] or tile.exits["top_right"]):
                                    if(tile.exits["bottom_left"] or tile.exits["bottom_center"] or tile.exits["bottom_right"]):
                                        row += '╬'
                                    else:
                                        row += '╩'
                                else:
                                    if(tile.exits["bottom_left"] or tile.exits["bottom_center"] or tile.exits["bottom_right"]):
                                        row += '╦'
                                    else:
                                        row += '═'
                            else:
                                if(tile.exits["top_left"] or tile.exits["top_center"] or tile.exits["top_right"]):
                                    if(tile.exits["bottom_left"] or tile.exits["bottom_center"] or tile.exits["bottom_right"]):
                                        row += '╣'
                                    else:
                                        row += '╝'
                                else:
                                    if(tile.exits["bottom_left"] or tile.exits["bottom_center"] or tile.exits["bottom_right"]):
                                        row += '╗'
                                    else:
                                        row += '╡'
                        else:
                            if(tile.exits["right"]):
                                if(tile.exits["top_left"] or tile.exits["top_center"] or tile.exits["top_right"]):
                                    if(tile.exits["bottom_left"] or tile.exits["bottom_center"] or tile.exits["bottom_right"]):
                                        row += '╠'
                                    else:
                                        row += '╚'
                                else:
                                    if(tile.exits["bottom_left"] or tile.exits["bottom_center"] or tile.exits["bottom_right"]):
                                        row += '╔'
                                    else:
                                        row += '╞'
                            else:
                                if(tile.exits["top_left"] or tile.exits["top_center"] or tile.exits["top_right"]):
                                    if(tile.exits["bottom_left"] or tile.exits["bottom_center"] or tile.exits["bottom_right"]):
                                        row += '║'
                                    else:
                                        row += '╨'
                                else:
                                    if(tile.exits["bottom_left"] or tile.exits["bottom_center"] or tile.exits["bottom_right"]):
                                        row += '╥'
                                    else:
                                        row += ' '
                except:
                    row += ' '


            minimap.append(row + "█")
        minimap.append("█████████████████")

        if(int(time.perf_counter()*2)%2 == 0):
            minimap[int(len(minimap)/2)] = minimap[int(len(minimap)/2)][:int(len(minimap[0])/2)] + '+' + minimap[int(len(minimap)/2)][int(len(minimap[0])/2)+1:]

        view = add_graphics(view, minimap, (player.view_x*2 - 11), 9, False)


    # UI
    if((player.hp != player.max_hp) or (player.stamina != player.max_stamina)):
        bar_size = int(player.view_x/2)

        healthbar_arr = []
        healthbar_arr.append("░"*(bar_size+4))
        healthbar_arr.append("░░" + "█"*int((player.hp/player.max_hp)*bar_size) + " "*(bar_size-int((player.hp/player.max_hp)*bar_size)) + "░░")
        healthbar_arr.append("░░" + "█"*int((player.hp/player.max_hp)*bar_size) + " "*(bar_size-int((player.hp/player.max_hp)*bar_size)) + "░░")
        healthbar_arr.append("░"*(bar_size+4))

        staminabar_arr = []
        staminabar_arr.append("░"*(bar_size+4))
        staminabar_arr.append("░░" + "█"*int((player.stamina/player.max_stamina)*bar_size) + " "*(bar_size-int((player.stamina/player.max_stamina)*bar_size)) + "░░")
        staminabar_arr.append("░░" + "█"*int((player.stamina/player.max_stamina)*bar_size) + " "*(bar_size-int((player.stamina/player.max_stamina)*bar_size)) + "░░")
        staminabar_arr.append("░"*(bar_size+4))

        view = add_graphics(view, healthbar_arr, int(player.view_x*2/3 +0.5), player.view_y*2-2, False)
        view = add_graphics(view, staminabar_arr, int(player.view_x*2/3*2 +0.5), player.view_y*2-2, False)

    # inventory
    inventory_arr = [" "]
    max_len = 0

    for key in player.inventory:
        inventory_arr.append(str(player.inventory[key]) + "x (" + key + ")")
        if(len(inventory_arr[-1]) > max_len):
            max_len = len(inventory_arr[-1])
        inventory_arr.append(" ")
            
    for row_num in range(len(inventory_arr)):
        inventory_arr[row_num] = "  " + inventory_arr[row_num] + " "*(max_len - len(inventory_arr[row_num])) + " ░"

    inventory_arr.append("░"*(max_len+4))

    view = add_graphics(view, inventory_arr, int(len(inventory_arr[0])/2+0.5), len(inventory_arr)-1, False)


    # effeccts
    for effect in effects:
        view = add_graphics(view, effect.texture[effect.texture_frame], effect.x-limit_x_l, effect.y-limit_y_l)

            
    # view animation
    global view_blindness, view_blindness_timer
    if(view_blindness > 0):
        if(time.perf_counter() > view_blindness_timer):
            view_blindness_timer = time.perf_counter() + 0.02

            view_blindness -= 1

        for row_num in range(len(view)):

            if(row_num < len(view)/2):
                covered = view_blindness - row_num
            else:
                covered = view_blindness - len(view) + row_num

            if(covered > int(player.view_x)):
                covered = int(player.view_x)
            elif(covered < 0):
                covered = 0
            
            new_row = view[row_num][covered:(len(view[row_num])-covered)]
            view[row_num] = " "*(covered) + new_row + " "*(covered)

    


    # debug info panel
    if(debug_info):

        debug_inventory_arr = [""]
        debug_inventory_arr.append("HP: " + str(player.hp))
        debug_inventory_arr.append("STAMINA: " + str(player.stamina))
        debug_inventory_arr.append("X: " + str(player.x))
        debug_inventory_arr.append("Y: " + str(player.y))

        for key in player.inventory:
            debug_inventory_arr.append(str(player.inventory[key]) + "x (" + key + ")")

        debug_inventory_arr.append("g_vel: " + str(player.g_vel))

        max_len = 14
        for row in debug_inventory_arr:
            if(len(row) > max_len):
                max_len = len(row)

        debug_inventory_arr[0] = "░"*max_len + "░░"
        for row_num in range(1, len(debug_inventory_arr)):
            debug_inventory_arr[row_num] = debug_inventory_arr[row_num] + " "*(max_len - len(debug_inventory_arr[row_num])) + " ░"

        view = add_graphics(view, debug_inventory_arr, int(len(debug_inventory_arr[0])/2), player.view_y*2-1, False)

        # BFS paths rendering
        if(int(time.perf_counter())%2 == 0):
            for point in debug_bfs_considered:
                view = add_graphics(view, ["_"], point[0] - limit_x_l, point[1] - limit_y_l, False)
            
        for npc in npcs+enemies:
            for point in npc.bfs_path:
                view = add_graphics(view, ["#"], point[0] - limit_x_l, point[1] - limit_y_l, False)

        

    # rendering
    view_str = "\033[0;0H"
    view_str += (player.view_x*2 + 4)*"░" + '\n'
    view_str += (player.view_x*2 + 4)*"░" + '\n'
    for row in view:
        view_str += "░░" + offscreen_x_l*" " + row + offscreen_x_r*" " + "░░ \n"
    view_str += (player.view_x*2 + 4)*"░" + '\n'
    view_str += (player.view_x*2 + 4)*"░"
    

    print(view_str)
    


def add_graphics(screen, texture, x, y, transparent = True):
    height = len(texture)
    width = len(texture[0])

    y = y - height +1
    x = x - int(width/2)

    offscr_xl = 0
    offscr_xr = 0

    if(x < 0):
        offscr_xl = abs(x)
        if(x <= -width):
            return screen
    if(x+width >= len(screen[0])):
        offscr_xr = (x+width - len(screen[0]))
        if(x >= len(screen[0])):
            return screen
        
    for row in texture:
        
        if((y >= 0) and (y < len(screen))):
            if(player.nightmare_vision):
                row_trans = ""
                for char_num in range(len(row)):
                    if row[char_num] == ' ':
                        row_trans += screen[y][:x+offscr_xl+char_num]
                    else:
                        row_trans += row[char_num]
            
                screen[y] = screen[y][:x+offscr_xl] + row_trans[offscr_xl:len(row)-offscr_xr] + screen[y][x+width-offscr_xr:]

            else:
                row_cis = row[offscr_xl:len(row)-offscr_xr]

                if(transparent):
                    row_trans = ""
                    for char_num in range(len(row_cis)):
                        if row_cis[char_num] == ' ':
                            row_trans += screen[y][x+offscr_xl+char_num]
                        else:
                            row_trans += row_cis[char_num]
                else:
                    row_trans = row_cis
            
                screen[y] = screen[y][:x+offscr_xl] + row_trans + screen[y][x+width-offscr_xr:]
        y += 1
    
    return screen



############### Main ###############

def main(): 

    intro(0.4) # default = 0.4

    menu_setup()

    menu()



main()
    


############### MISC ###############


# Proposition_complex explanations:

'''
A or B and C
============
██████████████████████████
█                        █
█         █████████████  █
█  A  or  █  B and C  █  █
█         █████████████  █
█                        █
██████████████████████████

A or (B and C) or (D and E)
===========================
██████████████████████████████████████████████
█                                            █
█         █████████████       █████████████  █
█  A  or  █  B and C  █   or  █  D and E  █  █
█         █████████████       █████████████  █
█                                            █
██████████████████████████████████████████████

A and (B or C or not(Q))
========================
███████████████████████████████████████████████
█                                             █
█            ███████████████████████████████  █
█            █                             █  █
█            █                ███████████  █  █
█    A  and  █  B  or  C  or  █  not Q  █  █  █
█            █                ███████████  █  █
█            █                             █  █
█            ███████████████████████████████  █
█                                             █
███████████████████████████████████████████████


- Every square is an object.
- This object represents a propositional equation, with all same operators (and; or; ..).

'''    






# LOGO variants

# ██████████    ██            ████████████    ██████████    ██████████
# ██            ██            ██        ██    ██            ██
# ██            ██            ██        ██    ██            ██
# ██            ██            ████████████    ██████████    ██████████
# ██            ██            ██        ██            ██            ██
# ██CIRCUIT     LEARNING      AND       ██    SIMULATION    SOFTWARE██
# ██████████    ██████████    ██        ██    ██████████    ██████████



# ██████████    ██            ████████████    ████████████████████████
# ██            ██            ██        ██    ██            ██
# ██            ██            ██        ██    ██            ██
# ██            ██            ████████████    ██████████    ██████████
# ██            ██            ██        ██            ██            ██
# ██CIRCUIT     ██LEARNING    ██AND     ██  SIMULATION██    SOFTWARE██
# ██████████████████████████████        ████████████████    ██████████



# ██████████▀▀▀▀██            ████████████    ██████████▀▀▀▀██████████
# ██            ██            ██        ██    ██            ██
# ██            ██            ██        ██    ██            ██
# ██            ██            ████████████    ██████████    ██████████
# ██            ██            ██        ██            ██            ██
# ██CIRCUIT     ██LEARNING    ██AND     ██  SIMULATION██    SOFTWARE██
# ██████████    ██████████▄▄▄▄██▀▀▀     ██▄▄▄▄██████████    ██████████



#                                                                 ▄▄▄▄
# ████████████████            ████████████    █████████████████████  █
# ██            ██            ██        ██    ██            ██    ▀▀▀▀
# ██            ██            ██        ██    ██            ██
# ██            ██            ████████████    ██████████    ██████████
# ██            ██            ██        ██            ██            ██
# ██    ▄▄▄▄    ██            ██        ██            ██    ▄▄▄▄    ██
# ███████  █    ████████████████        ████████████████    █  ███████
#       ▀▀▀▀                                                ▀▀▀▀



#                                                                 ▄▄▄▄
# ████████████████            ████████████    █████████████████████  █
# ██            ██            ██        ██    ██            ██    ▀▀▀▀
# ██            ██            ██        ██    ██            ██
# ██            ██            ██████████████████████████    ██████████
# ██            ██            ██        ██            ██            ██
# ██    ▄▄▄▄    ██            ██       ▄██▄   ▄▄▄▄    ██    ▄▄▄▄    ██
# ███████  █    ████████████████       █  █   █  ███████    █  ███████
#       ▀▀▀▀                           ▀▀▀▀   ▀▀▀▀          ▀▀▀▀



# ////////////////////////////////////////////////////////////////////////
# ███████▀▀█   █▀▀█           ████████████    █████████████████████▀▀█
# ██    █▄▄█   █▄▄█           ██        ██    ██            ██    █▄▄█
# ██            ██            ██        ██    ██            ██
# ██            ██            ████████████    ██████████    ██████████
# ██            ██            ██        ██            ██            ██
# ██            ██            ██        ██            ██    █▀▀█    ██
# ██████████████████████████████        ████████████████    █▄▄███████
# CIRCUIT ///// LEARNING /// AND //////////// SIMULATION //// SOFTWARE ///



# ////////////////////////////////////////////////////////////////////////
# ██████████    ██            ████████████    ████████████████████████
# ██            ██            ██        ██    ██            ██
# ██            ██            ██        ██    ██            ██
# ██            ██            ████████████    ██████████    ██████████
# ██            ██            ██        ██            ██            ██
# ██            ██            ██        ██            ██            ██
# ██████████████████████████████        ████████████████    ██████████
# CIRCUIT ///// LEARNING /// AND //////////// SIMULATION //// SOFTWARE ///



# "////////////////////////////////////////////////////////////////////////",
# "░░░░░░█▀▀█   █▀▀█           ░░░░░░░░░░░░    ░░░░░░░░░░░░░░░░░░░░█▀▀█    ",
# "░░    █▄▄█   █▄▄█           ░░        ░░    ░░            ░░    █▄▄█    ",
# "░░            ░░            ░░        ░░    ░░            ░░            ",
# "░░            ░░            ░░░░░░░░░░░░    ░░░░░░░░░░    ░░░░░░░░░░    ",
# "░░            ░░            ░░        ░░            ░░            ░░    ",
# "░░            ░░            ░░        ░░            ░░    █▀▀█    ░░    ",
# "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░        ░░░░░░░░░░░░░░░░    █▄▄█░░░░░░    ",
# "CIRCUIT ///// LEARNING //////// AND /////// SIMULATION //// SOFTWARE ///"









# Game mechanics ideas:
# Solve simple equations to collect True and False flowers.
# Mine for 1s and 0s
# Insert 1s and 0s into puzzles that are just truth table filling.
# Maybe like craft runes with different symbols propositions and such hou have to colllect, farm, solve puzzles for? (Craftable with an npc)
# (Also refining true/false and such into equations with other npcs)

# Maybe proceduraly generated dungeons accessible with runes and involving fighting enemies while math obelisks in the background do some cool animated math or whatever and sometimes it has an effect on the area of the dungeon.

# Maybe add a bar where you can buy energy drinks and such? (Instead of hunger you refill energy)
# Maybe currency in bits?




# SIMULATION IDEA

# ////////////////////////////////////////////////////////////////////////
# ░░░░░░█▀▀█   █▀▀█           ░░░░░░░░░░░░    ░░░░░░░░░░░░░░░░░░░░█▀▀█
# ░░    █▄▄█   █▄▄█           ░░        ░░    ░░            ░░    █▄▄█
# ░░            ░░            ░░        ░░    ░░            ░░
# ░░            ░░            ░░░░░░░░░░░░    ░░░░░░░░░░    ░░░░░░░░░░
# ░░            ░░            ░░        ░░            ░░            ░░
# ░░            ░░            ░░        ░░            ░░    █▀▀█    ░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░        ░░░░░░░░░░░░░░░░    █▄▄█░░░░░░
# CIRCUIT ///// LEARNING /// AND //////////// SIMULATION //// SOFTWARE ///

# this as string, print only full blocks, in a loop change dotted into full if they are adjecent to an already lit up character.
