##extrusion check

def open_file():
    '''opens the file and returns it'''
    while True:
        user_input = input ('Enter the name of the file you would like to insert pores in: ')
        if user_input == 'q':
            return False
        try:
            gcode_file = open(user_input,'r')
            gcode_list = convert_file (gcode_file)
            return gcode_list
        except FileNotFoundError:
            print('File not Found! Please try again.')
    


def convert_file(file):
    '''reads the file and returns it as a list where each increment is a line'''
    gcode_list = []
    line_num = 0
    for line in file:
        gcode_list.append(line)
        line_num += 1
    return gcode_list


def make_new_file(final_list):
    '''writes a new .gcode file using the given list'''
    new_file_name = input('What would you like to name the new file? (add .gcode at the end please) :')
    new_file = open(new_file_name,'a')
    seperator = ' '
    for line in final_list:
        str_line = seperator.join(line)
        str_line += '\n'
        new_file.write(str_line)

def extr_check(gcode_list):
    new_list = []
    previous_extr: 0.0
    current_extr: 0.0
    extr_change: 0.0
    for item in gcode_list:
        new_list.append(item.strip().split())
    try:
        for item in new_list:
            for command in item:
                if 'E' in command:
                    current_extr = float(command[1:])
                    if prev_extrusion == 0.0:
                        prev_extrusion = current_extr
                    if prev_extrusion > current_extr:
                        extr_change = prev_extrusion - current_extr
                    elif current_extr > prev_extrusion:
                        extr_change = current_extr - prev_extrusion
                    else:
                        print ('hold up...')
                    if extr_change >= 5:
                        print ('hold up...')
    except IndexError:
        print ('index')

def main():
    '''the main, lol'''
    print('bruh')
    in_prompt = True  
    done = False
    while True:
        gcode_list = open_file()
        if gcode_list == False:
            done = True
            completed = True
        else:
            global extrusion_removed
            global prev_extrusion
            global extr_rat
            extr_rat = 0
            extrusion_removed = 0.0
            prev_extrusion = [0,0]
            extr_check(gcode_list)
            completed = True
            in_prompt = True
        while in_prompt == True:
            user_input2 = input ('Would you like to remove from another file? (y/n) ')
            if user_input2 == 'n':
                done = True
                break
            elif user_input2 == 'y':
                in_prompt = False
            else:
                print('Invalid Input!')
        if completed == True and done == True:
            print ('Thank you for using this program.')
            input('Hit enter to close this window.')
            break
        
    

main()



