#The file that I will be making the program with
#yay

import math

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


def get_int(line_to_read):
    '''gets an integer from a commented line of gcode'''
    int_to_return = 0
    past_words = False
    for char in line_to_read:
        if past_words == True:
            try:
                char = int(char)

                int_to_return = int_to_return * 10
                int_to_return += int(char)
            except ValueError:
                pass
        if char == ':':
            past_words = True
    return int_to_return


def get_float(line_to_read):
    '''gets an integer from a commented line of gcode'''
    float_to_return = 0.0
    past_words = False
    past_decimal = False
    i = 0.0
    for char in line_to_read:
        if past_words == True:
            try:
                char = float(char)
                if past_decimal == False:
                    float_to_return = float_to_return * 10
                    float_to_return += char
                else:
                    if i == 1:
                        if i >= 10:
                            i += 10
                        else:
                            i += 9
                    else:
                        i += 1.0
                    char = char / (10.0*i)
                    float_to_return += char
            except ValueError:
                if char == '.':
                    past_decimal = True
        if char == ':':
            past_words = True
    float_to_return = round(float_to_return,3)
    return float_to_return

def edit_hole_count_info(hole_count_info):
    editing_info = True
    while editing_info:
        print ('What feature would you like to change?')
        user_input2 = input('hamt1, hamt2, vamt, or depth: ')
        if user_input2 == 'hamt1':
            print ('The first horizontal amount is currently',hole_count_info[0])
            amt = input('What would you like to change it to? ')
            if amt.isdigit() == True:
                hole_count_info[0] = int(amt)
            else:
                print ('That needs to be an integer!')
        elif user_input2 == 'hamt2':
            print ('The second horizontal amount is currently',hole_count_info[1])
            amt = input('What would you like to change it to? ')
            if amt.isdigit() == True:
                hole_count_info[1] = int(amt)
            else:
                print ('That needs to be an integer!')
        elif user_input2 == 'vamt':
            print ('The vertical amount is currently',hole_count_info[2])
            amt = input('What would you like to change the vertical amount to? ')
            if amt.isdigit() == True:
                hole_count_info[2] = int(amt)
            else:
                print ('That needs to be an integer!')
        elif user_input2 == 'depth':
            print ('The depth is currently',hole_count_info[3])
            amt = input('What would you like to change the depth to? ')
            if amt.isdecimal() == True:
                hole_count_info[3] = float(amt)
            else:
                print ('That needs to be a float!')
        else:
            print ('Invalid input!')
        in_second_prompt = True
        while in_second_prompt == True:
            user_input2 = input ('Would you like to change something else? (y/n) ')
            if user_input2 == 'n':
                editing_info = False
                in_second_prompt = False
            elif user_input2 == 'y':
                in_second_prompt = False
            else:
                print('Invalid Input!')
    return hole_count_info
            

def determine_hole_sizing(height_of_layers, num_of_layers, layer1_perimeter,\
    hole_count_info):
    '''determines where to put the holes in the object. starts by
    finding out the size of the holes, then lays out a rule set to follow.'''
    output = []
    height_of_object = height_of_layers * num_of_layers
    print ('The object is',height_of_object,'millimeters tall')
    output.append(height_of_object)

    height_of_holes = math.floor((height_of_object/(hole_count_info[2]+((hole_count_info[2] - 1)/2)+2)*10))
    height_of_holes = height_of_holes/10
    print ('The holes will be',height_of_holes,'millimeters tall')
    output.append(height_of_holes)

    length_of_holes = math.floor((layer1_perimeter/(hole_count_info[1]+(hole_count_info[1]+4))*10))
    length_of_holes = length_of_holes/10
    print ('The holes will be',length_of_holes,'millimeters long')
    output.append(length_of_holes)

    depth_of_holes = hole_count_info[3]
    print ('The holes will be',depth_of_holes,'millimeters deep')
    output.append(depth_of_holes)
    return(output)

def make_hole_location(hole_count_info, hole_size_info, prev_pos, current_pos, current_total_difference, current_horizontal, line_info):
    points_to_return = []
    distance_worked = 0.0
    pretend_ex = prev_pos.copy()
    hole_points = []
    if line_info == ['x','pos']:
        if current_horizontal == 1:
            pretend_ex[0] = round(pretend_ex[0] + 2*hole_size_info[2],1)
            distance_worked = 2*hole_size_info[2]
            while distance_worked <= current_total_difference[0]-(2*hole_size_info[2]):
                hole_points = []
                pretend_ex2 = pretend_ex.copy()
                pretend_ex2[0] = round(pretend_ex2[0] + 0.01,2)
                pretend_ex2[1] = round(pretend_ex[1] + 2/2,2)
                while pretend_ex2[1] >= (pretend_ex[1] - hole_size_info[3]/2):
                    while pretend_ex2[0] <= (pretend_ex[0] + hole_size_info[2]/2):
                        hole_points.append(pretend_ex2.copy())
                        pretend_ex2[0] = round(pretend_ex2[0] + 0.01,2)
                    pretend_ex2[1] = round(pretend_ex2[1] - 0.01,2)
                points_to_return.append(hole_points)
                pretend_ex[0] = round(pretend_ex[0] + 2*hole_size_info[2],1)
                distance_worked += 2*hole_size_info[2]
            return points_to_return
        elif current_horizontal == 2:
            pretend_ex[0] = round(pretend_ex[0] + hole_size_info[2],1)
            distance_worked = 2*hole_size_info[2]
            while distance_worked <= current_total_difference[0]-(hole_size_info[2]):
                points_to_return.append([pretend_ex[0],pretend_ex[1]])
                pretend_ex[0] = round(pretend_ex[0] + 2*hole_size_info[2],1)
                distance_worked += 2*hole_size_info[2]
            return points_to_return
    if line_info == ['y','pos']:
        if current_horizontal == 1:
            pretend_ex[1] = round(pretend_ex[1] + 2*hole_size_info[2],1)
            distance_worked = 2*hole_size_info[2]
            while distance_worked <= current_total_difference[1]-(2*hole_size_info[2]):
                points_to_return.append([pretend_ex[0],pretend_ex[1]])
                pretend_ex[1] = round(pretend_ex[1] + 2*hole_size_info[2],1)
                distance_worked += 2*hole_size_info[2]
            return points_to_return
        elif current_horizontal == 2:
            pretend_ex[1] = round(pretend_ex[1] + hole_size_info[2],1)
            distance_worked = 2*hole_size_info[2]
            while distance_worked <= current_total_difference[1]-(hole_size_info[2]):
                points_to_return.append([pretend_ex[0],pretend_ex[1]])
                pretend_ex[1] = round(pretend_ex[1] + 2*hole_size_info[2],1)
                distance_worked += 2*hole_size_info[2]
            return points_to_return
    elif line_info == ['x','neg']:
        if current_horizontal == 1:
            pretend_ex[0] = round(pretend_ex[0] - 2*hole_size_info[2],1)
            distance_worked = 2*hole_size_info[2]
            while distance_worked <= current_total_difference[0]-(2*hole_size_info[2]):
                points_to_return.append([pretend_ex[0],pretend_ex[1]])
                pretend_ex[0] = round(pretend_ex[0] - 2*hole_size_info[2],1)
                distance_worked += 2*hole_size_info[2]
            return points_to_return
        elif current_horizontal == 2:
            pretend_ex[0] = round(pretend_ex[0] - hole_size_info[2],1)
            distance_worked = 2*hole_size_info[2]
            while distance_worked <= current_total_difference[0]-(hole_size_info[2]):
                points_to_return.append([pretend_ex[0],pretend_ex[1]])
                pretend_ex[0] = round(pretend_ex[0] - 2*hole_size_info[2],1)
                distance_worked += 2*hole_size_info[2]
            return points_to_return
    elif line_info == ['y','neg']:
        if current_horizontal == 1:
            pretend_ex[1] = round(pretend_ex[1] - 2*hole_size_info[2],1)
            distance_worked = 2*hole_size_info[2]
            while distance_worked <= current_total_difference[1]-(2*hole_size_info[2]):
                points_to_return.append([pretend_ex[0],pretend_ex[1]])
                pretend_ex[1] = round(pretend_ex[1] + 2*hole_size_info[2],1)
                distance_worked += 2*hole_size_info[2]
            return points_to_return
        elif current_horizontal == 2:
            pretend_ex[1] = round(pretend_ex[1] - hole_size_info[2],1)
            distance_worked = 2*hole_size_info[2]
            while distance_worked <= current_total_difference[1]-(hole_size_info[2]):
                points_to_return.append([pretend_ex[0],pretend_ex[1]])
                pretend_ex[1] = round(pretend_ex[1] + 2*hole_size_info[2],1)
                distance_worked += 2*hole_size_info[2]
            return points_to_return



def get_hole_locations(current_layer, hole_count_info, hole_size_info, layer_perimeters,current_layer_num,current_horizontal):
    line_info = []
    layer_hole_locations = []
    last_location = []
    has_passed_infill = False
    for line in current_layer:
        if line [0] == ';infill':
            has_passed_infill = True
        if len(line) != 1 and line[1][0] == 'X' and has_passed_infill == False:
            if last_location == []:
                last_location = line
            else:
                current_x = round(float(line[1][1:]),3)
                current_y = round(float(line[2][1:]),3)
                current_pos = [current_x, current_y]
                last_x = round(float(last_location[1][1:]),3)
                last_y = round(float(last_location[2][1:]),3)
                last_pos = [last_x, last_y]
                current_total_difference = []
                current_total_difference.append(current_x - last_x)
                current_total_difference.append(current_y - last_y)
                if current_total_difference[0] >= hole_size_info[2]:
                    line_info = ['x','pos']
                    layer_hole_locations.append(make_hole_location(hole_count_info,hole_size_info,last_pos,current_pos,current_total_difference,current_horizontal,line_info))
                elif current_total_difference[0] <= (-1*hole_size_info[2]):
                    line_info = ['x','neg']
                    layer_hole_locations.append(make_hole_location(hole_count_info,hole_size_info,last_pos,current_pos,current_total_difference,current_horizontal,line_info))
                elif current_total_difference[1] >= (hole_size_info[2]):
                    line_info = ['y','pos']
                    layer_hole_locations.append(make_hole_location(hole_count_info,hole_size_info,last_pos,current_pos,current_total_difference,current_horizontal,line_info))
                elif current_total_difference[1] <= (-1*hole_size_info[2]):
                    line_info = ['y','neg']
                    layer_hole_locations.append(make_hole_location(hole_count_info,hole_size_info,last_pos,current_pos,current_total_difference,current_horizontal,line_info))
    return layer_hole_locations

def make_holes(current_layer,hole_count_info,hole_size_info,hole_locations):
    return_list = []
    prev_move = []
    should_append = True
    for move in current_layer:
        if ';' in move[0]:
            if prev_move != []:
                return_list.append(prev_move)
            return_list.append(move)
            prev_move = []
        elif move[1][0]=='Z' or move[1][0]=='E':
            if prev_move != []:
                return_list.append(prev_move)
            return_list.append(move)
            prev_move = []
        elif prev_move == []:
            prev_move = move.copy()
            prev_move_floats = [round(float(prev_move[1][1:]),3),round(float(prev_move[2][1:]),3)]
        else:
            move_floats = [round(float(move[1][1:]),3),round(float(move[2][1:]),3)]
            while prev_move_floats[0] < move_floats[0] or prev_move_floats[1] < move_floats[1]:
#                print (prev_move_floats,move_floats)
                for side in hole_locations:
                    for hole in side:
                        if prev_move_floats in hole:
                            should_append = False
                if prev_move_floats[0] < move_floats[0]:
                    prev_move_floats[0] = round(prev_move_floats[0] + 0.01,1)
                    for side in hole_locations:
                        for hole in side:
                            if prev_move_floats in hole:
                                should_append = False
                if prev_move_floats[1] < move_floats[1]:
                    prev_move_floats[1] = round(prev_move_floats[1] + 0.01,1)
                    for side in hole_locations:
                        for hole in side:
                            if prev_move_floats in hole:
                                should_append = False
            if should_append == True:
                return_list.append(prev_move)
            else:
                should_append == True
            prev_move = move.copy()
            prev_move_floats = [round(float(prev_move[1][1:]),3),round(float(prev_move[2][1:]),3)]
    print ('returning...')
    return return_list
                
            



def work_on_layer(current_layer, hole_count_info, hole_size_info, layer_perimeters, current_layer_num, current_horizontal):

    previous_movement = []
    hole_locations = []
    holed_list = []
    for movement in current_layer:
        if len(movement) >= 3:
            if previous_movement == []:
                previous_movement = movement
            else:
                hole_locations = get_hole_locations(current_layer,hole_count_info,hole_size_info,layer_perimeters,current_layer_num,current_horizontal)
                holed_list = make_holes(current_layer, hole_count_info, hole_size_info, hole_locations)
        else:
            if previous_movement != []:
                pass
    if holed_list == []:
        return current_layer
    return holed_list



def make_final_list(pored_list,hole_count_info,hole_size_info,\
    layer_perimeters,layer_count,layer_height):
    i = 0

    layers_to_skip = []
    while i < layer_count:
        i += 1
        if i*layer_height <= hole_size_info[1]:
            layers_to_skip.append(i)
        elif i*layer_height >= ((layer_height*layer_count)-hole_size_info[1]):
            layers_to_skip.append(i)
    current_layer_num = 0
    current_horizontal = 1
    is_printing_object = False
    actual_pored_list = []
    current_loc = []
    current_layer = []
    worked_layer = []
    had_z = False
    work_counter = 0
    work_counter2 = 0
    for line in pored_list:
        work_counter += 1
        if work_counter % 100 == 0:
            work_counter2 += 1
            if work_counter2 == 1:
                print('working.')
            elif work_counter2 == 2:
                print('working..')
            else:
                print('working...')
                print(work_counter)
                work_counter2 = 0
        if ';shell' in line:
            is_printing_object = True
        if 'M107' in line:
            is_printing_object = False
            worked_layer = work_on_layer(current_layer,hole_count_info,hole_size_info,layer_perimeters,current_layer_num,current_horizontal)
            for command in worked_layer:
                seperator = ' '
                command_str = seperator.join(command)
                command_str += '\n'
                actual_pored_list.append(command_str)
            current_layer = []
        if is_printing_object == False:
            actual_pored_list.append(line)
        else:
            current_loc = line.strip().split()
            for item in current_loc:
                if 'Z' in item:
                    had_z = True
            if had_z:
                worked_layer = work_on_layer(current_layer,hole_count_info,hole_size_info,layer_perimeters,current_layer_num,current_horizontal)
                for command in worked_layer:
                    seperator = ' '
                    command_str = seperator.join(command)
                    command_str += '\n'
                    actual_pored_list.append(command_str)
                current_layer = []
                current_layer.append(current_loc)
                had_z = False
                current_layer_num += 1
            else:
                current_layer.append(current_loc)
    return actual_pored_list




def get_layer_stuff(pored_list,hole_count_info):
    layer_count = 0
    i = 0
    layer_height = 0.0
    layer_perimeter = 0
    layer_perimeters = []
    current_layer = 0
    finding_perimeter = False
    for line in pored_list:
        #finds details about the gcode
        if ';layer:' in line:
            current_layer += 1
        if ';end gcode' in line:
            break
        if ';layer_count:' in line:
            #sends to the get_int function to get the layer count
            layer_count = get_int(line)
            print ('Number of layers: ', layer_count)
        if ';layer_height:' in line:
            #sends to the get_float function to get the height of the layers
            layer_height = get_float(line)
            print ('Layer height:', layer_height)
        if ';infill' in line and finding_perimeter == True:
            layer_perimeter = round((X_moved + Y_moved), 3)
            format (layer_perimeter, '.3f')
            layer_perimeters.append(layer_perimeter)
            finding_perimeter = False
            if current_layer == 1:
                print ('The perimeter of layer 1 is:',layer_perimeter)
                hole_size_info = determine_hole_sizing(layer_count,\
                    layer_height,layer_perimeter,hole_count_info)
        if finding_perimeter == True:
            temp_line = line.strip().split()
            for item in temp_line:
                if 'X' in item:
                    item = item[1:]
                    current_X = round(float(item),3)
                elif 'Y' in item:
                    item = item[1:]
                    current_Y = round(float(item),3)
            if (previous_X != 0.0) & (previous_Y != 0.0):
                X_moved += round(math.fabs(previous_X - current_X),3)
                Y_moved += round(math.fabs(previous_Y - current_Y),3)
            previous_X = current_X
            previous_Y = current_Y        
        if ';shell' in line:
            previous_X = 0.0
            current_X = 0.0
            X_moved = 0.0
            previous_Y = 0.0
            current_Y = 0.0
            Y_moved = 0.0
            finding_perimeter = True
    in_prompt = True
    while in_prompt == True:
        user_input2 = input ('Does everything seem ok? (y/n) ')
        if user_input2 == 'n':
            print ('Sorry! If the program was in error, please contact someone!')
            return True
        elif user_input2 == 'y':
            in_prompt = False
        else:
            print('Invalid Input!')
    final_list = []
    final_list = make_final_list(pored_list,hole_count_info,\
        hole_size_info,layer_perimeters,layer_count,layer_height)
    make_new_file(final_list)
    



def make_new_file(final_list):
    '''writes a new .gcode file using the given list'''
    new_file_name = input('What would you like to name the new file? (add .gcode at the end please) :')
    new_file = open(new_file_name,'a')
    for line in final_list:
        new_file.write(line)

def main():
    '''the main, lol'''
    print('Welcome to the pore inserter!')
    done = False
    while True:
        gcode_list = open_file()
        if gcode_list == False:
            done = True
            completed = True
        else:
            while True:
                user_input1 = input('Would you like to use the defaults? (y/n): ')
                hole_count_info = [12,16,4,2]
                if user_input1 == 'n':
                    hole_count_info = edit_hole_count_info(hole_count_info)
                            
                if user_input1 == 'n' or 'y':
                    print ('\n')
                    list_to_pore = gcode_list
                    completed = get_layer_stuff(list_to_pore,hole_count_info)
                    break
                else:
                    print ('Command unrecognized!')
        if completed == True and done == False:
            in_prompt = True
            while in_prompt == True:
                user_input2 = input ('Would you like to pore something else? (y/n) ')
                if user_input2 == 'n':
                    done = True
                    break
                elif user_input2 == 'y':
                    in_prompt = False
                else:
                    print('Invalid Input!')
        elif completed == True and done == True:
            print ('Thank you for using this program.')
            closing = input('Hit enter to close this window.')
            break
        
    

main()



