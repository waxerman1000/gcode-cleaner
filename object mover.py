import math

def open_file():
    '''opens the file and returns it'''
    running = True
    while running == True:
        user_input = input ('Enter the name of the file you would like to reposition: ')
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

def the_thing(file):
    new_file_name = input('What would you like to name the new file? (add .gcode at the end please) :')
    new_file = open(new_file_name,'a')
    for line in file:
        temp_line = []
        temp_line = line.strip().split()
        try:
            if 'X' in temp_line[1]:
                temp_float = 0.0
                try:
                    temp_float = float(temp_line[1][1:])
                    temp_float += 112
                    temp_float = round(temp_float,3)
                    temp_str = 'X' + str(temp_float)
                    temp_line [1] = temp_str
                except ValueError:
                    pass
            if 'Y' in temp_line [2]:
                temp_float = 0.0
                try:
                    temp_float = float(temp_line[2][1:])
                    temp_float += 112
                    temp_float = round(temp_float,3)
                    temp_str = 'Y' + str(temp_float)
                    temp_line [2] = temp_str
                except ValueError:
                    pass
        except IndexError:
            pass
        seperator = ' '
        temp_line = seperator.join(temp_line)
        temp_line = temp_line + '\n'
        new_file.write(temp_line)





def main():
    file = open_file()
    the_thing(file)

main()