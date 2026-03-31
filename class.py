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
    equation = equation.replace("if", '(') # DEBUG (untested brackets)
    equation = equation.replace("then", ')→') # DEBUG (untested brackets)
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

        # DEBUG DEBUG DEBUG   - ensure that standardization only passes with two propositions in these:

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

                            # DEBUG DEBUG DEBUG   (Clean this up u lazy fu*k)
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
                            new_proposition.propositions.append(simplify(prop, main = True)) # DEBUG DEBUG DEBUG ( was False )
                            
                    # new_proposition.propositions.append(simplify(prop, main = False))   <<<<<<<<<<<   DEBUG DEBUG DEBUG (deleted for complex idempotency)


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
        for key in combination:
            if(combination[key] == "false"):
                vals += " F |"
            elif(combination[key] == "true"):
                vals += " T |"

        results[vals] = (simplify(assign(proposition_complex, combination)))


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



menu_buttons_str = ["NYA :3", "GUIDE", "CLASS", "PRACTICE", "DEBUG MODE", "EXIT"]
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

        space = 60
        for anim_i in range(space):

            btn_string = ""
            for str in btn_string_arr:
                btn_string += (" "*(space-anim_i) + str)[:60] + " \n"
            btn_string +='\n'

            print("\033[%d;0H" % y_level)
            print(btn_string)
            time.sleep(0.005*time_mult)

        y_level += 6


def menu():

    menu_animation()
    
    cur_y = 0
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
                        intro(0.2, keypress=False)
                        menu_animation(0.2)
                    case "NYA :3":
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

                
    




    # print(string)


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

# main_debug()

main()







##############################################################
#################     DEBUG DEBUG DEBUG     ##################
##############################################################



# equation = "a or b and c or d or false or d"
# values = {
#     "b":"false"
# }

# equation = "not (not not a or not b)"
# equation = "not not a"
# equation = "((not a) and a)"
# equation = "if (not (a and b)) then (a or (b and c or g) if and only if (a or b and (g or l)))" # if and only if (not g implies (l xor (not a and (b or c))))"
# equation = "not(a or not not(b))"
# equation = "not not not not not a or not (not (not b)) and not c"
# equation = "a or b and c if and only if g or (l and o or p and q)"
# equation = "a or b and c"
# equation = "a or (a and b)"
# equation = "(not a) and a or b"
equation = "a or (a and b) implies c"


values = {
    # "a":"false",
    # "b":"true",
    # "c":"true",
    # "g":"true"
}

os.system('cls')

print("equation: " + equation)
print("values: " + str(values))
print("=============")

standardized = standardize(equation)
print("\nstandardized: " + standardized.str())

simplified = simplify(standardized)
if(type(simplified) == str):
    print("\nsimplified: " + simplified)
else:
    print("\nsimplified: " + simplified.str())

assigned = assign(standardized, values)
print("\nassigned: " + assigned.str())

assigned_simplified = simplify(assigned)
if(type(assigned_simplified) == str):
    print("\nassigned + simplified: " + assigned_simplified)

    print("\nvariables: " + simplified) 

    print("\ntable: " + simplified)
else:
    print("\nassigned + simplified: " + assigned_simplified.str())

    print("\nvariables: " + str(simplified.variables())) 

    print("\ntable: " + simplified.str())


table = make_table(simplified)
vars = "|"
if(type(assigned_simplified) == str):
    vars += " " + assigned_simplified + " |"
else:
    for var in simplified.variables():
        vars += " " + var + " |"
print(vars)
print("="*len(vars))
for key in table:
    print(str(key) + " == " + str(table[key]))

print("\n")




# TO DO LIST

# - UI
#    - ASCII study material
#    - Practice mode (randomly from selected: questions, equation solving, interactive(set values for diagram, solve truth table, ...)))
#    - Diagram generation and simulation (interactive)
#    - K-maps   (if theres time)

# - The rest of simplification (through K-maps adj.)



# IDEAS

# for UI, make arrow keys select buttons in menu, [enter] them to get into modes
#    then have a screen with the equations, truth table etc...,    on top of screen different tabs, move into buttons space, move with arrows, automatically changes (equations / truth table / diagram), 





# ISSUES:
# (a ∨ b) ∧ (a ∨ c)  =  a ∧ (b ∨ c)




# MISC

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