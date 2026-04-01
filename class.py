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

DEFAULT_WINDOW_WIDTH = 120

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

# operation_order = ('¬', ('∧', '⊻'), '∨', '→', '↔') # operation symbol priority from left ot right
operation_order = ('¬', '∧', '⊻', '∨', '→', '↔') # operation symbol priority from left ot right
operands = ('¬', '∧', '⊻', '∨', '→', '↔')

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
menu_buttons_str = ["FIDGET", "GUIDE", "CLASS", "PRACTICE", "DEBUG MODE", "EXIT"]
menu_buttons = []

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



def main(): 

    intro(0.4) # default = 0.4

    menu_setup()

    menu()




def main_debug():
    # clear screen and hide cursor
    os.system('cls')
    print("\033[?25l")

    
    # btn = Button("hello :3")
    # for srt in btn.str():
    #     print(srt)
    
    # btn = Button("I am a buttton")
    # for srt in btn.str(True):
    #     print(srt)

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


main()



# MISC


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