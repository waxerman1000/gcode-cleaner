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


def make_new_file(final_list):
    '''writes a new .gcode file using the given list'''
    new_file_name = input('What would you like to name the new file? (add .gcode at the end please) :')
    new_file = open(new_file_name,'a')
    seperator = ' '
    for line in final_list:
        str_line = seperator.join(line)
        str_line += '\n'
        new_file.write(str_line)

def do_shell_stuff(shell,distance_of_edge):
    '''Runs through the given commands and removes any movements that don't
        form a straight line from one corner of the object to the next.'''
    global extrusion_removed
    global prev_extrusion
    shell_to_return = []
    move_float = []
    corner = []
    has_passed_first_coord = False
    is_first_from_corner = True
    moving_x = False
    moving_y = False
    keep_line = True
    prev_removed = False
    if distance_of_edge == 0:
        return shell
    for move in shell:
        if move == ['G92', 'E0']:
            extrusion_removed = 0.0
            previous_extrusion = []
        try:
            if 'X' in move[1] and 'Y' in move[2]:
                #if has x and y values
                move_float = []
                move_float.append(float(move[1][1:]))
                move_float.append(float(move[2][1:]))
                if has_passed_first_coord == False:
                    if move_float[0] == move_float[1]:
                        corner.append(float(move_float[0]))
                        corner.append(float(move_float[1]))
                        has_passed_first_coord = True
                elif is_first_from_corner:
                    if move_float != corner:
                        if move_float[0] != corner[0]:
                            moving_x = True
                            is_first_from_corner = False
                        elif move_float[1] != corner[1]:
                            moving_y = True
                            is_first_from_corner = False

                if moving_x == True:
                    if move_float[1] != corner[1]:
                        keep_line = False
                    corner_to_move = abs(corner[0]) + abs(move_float[0])
                    if (distance_of_edge - 0.5) <= corner_to_move and\
                        corner_to_move <= (distance_of_edge + 0.5):
                            corner = move_float.copy()
                            is_first_from_corner = True
                            moving_x = False

                elif moving_y == True:
                    if move_float[0] != corner[0]:
                        keep_line = False
                    corner_to_move = abs(corner[1]) + abs(move_float[1])
                    if (distance_of_edge - 0.5) <= corner_to_move and\
                        corner_to_move <= (distance_of_edge + 0.5):
                            corner = move_float.copy()
                            is_first_from_corner = True
                            moving_x = False

                
        except IndexError:
            pass
        if keep_line:

            true_prev = 0.0
            edited_prev = 0.0
            true_current = 0.0
            edited_current = 0.0
            command_to_append = []
            move_to_append = []
            retract = ['G1', 'E', 'F1800']
            post_move = ['G1', 'E', 'F1800']
            if prev_removed:
                #moves the print head to the next point after the pore.
                #retracts 1.3mm before move and pushes 1.3mm back out after move.
                for command in move:
                    if "E" in command:
                        prev_extrusion[1] = float(command[1:])
                    elif "F" in command:
                        command_to_append.append('F4200')
                    else:
                        move_to_append.append(command)
                retract[1] += str(round(prev_extrusion[0] - 1.3,4))
                post_move[1] += str(round(prev_extrusion[0],4))
                shell_to_return.append(retract)
                shell_to_return.append(move_to_append)
                shell_to_return.append(post_move)
                shell_to_return.append(move_to_append)
                prev_removed = False
            else:
                try:
                    for command in move:
                        if 'E' in command:
                            true_current = float(command[1:])
                            edited_current = round(true_current - extrusion_removed, 4)
                            command_to_append = 'E' + str(edited_current)
                            move_to_append.append(command_to_append)
                            prev_extrusion[0] = edited_current
                        else:
                            move_to_append.append(command)
                    shell_to_return.append(move_to_append)
                except IndexError:
                    shell_to_return.append(move)
        else:
            keep_line = True
            prev_removed = True
            try:
                for command in move:
                    if 'E' in command:
                        extrusion_removed = round(extrusion_removed + (float(command[1:]) - prev_extrusion[0]),4)
                        prev_extrusion[1] = float(command[1:])
            except IndexError:
                pass
    return shell_to_return


def do_infill_stuff(infill):
    '''runs through the given commands, and removes extrusion from any movement
        that only changes one axis to prevent the infill from making walls.'''

    return infill

    global extrusion_removed
    global prev_extrusion
    global extr_rat
    infill_to_return = []
    first_loc = True
    prev_loc = []
    not_adding = False
    current_true_extrusion = 0
    prev_removed = False
    for move in infill:
        spare_G1 = ['G1']
        for item in move:
            if 'E' in item:
                current_true_extrusion = round(float(item[1:]),4)
        move_to_append = move.copy()
        if move == ['G92', 'E0']:
            extrusion_removed = 0.0
            previous_extrusion = [0,0]
        try:
#            print('prev',prev_loc)
#            print('current',move)
            if 'X' in move[1] and 'Y' in move[2]:
                if not first_loc:
                    prev_loc_floats = [float(prev_loc[1][1:]),float(prev_loc[2][1:])]  
                move_floats = [float(move[1][1:]),float(move[2][1:])]
                is_move = True
                if first_loc:
                    prev_loc = move.copy()
                    infill_to_return.append(move)
                    prev_loc_floats = [float(prev_loc[1][1:]),float(prev_loc[2][1:])]
                    first_loc = False
                elif (prev_loc_floats[0] - 2) <= move_floats[0] <= (prev_loc_floats[0] + 2) and move[2] != prev_loc[2]:
                    for item in move:
                        if "E" in item:
                            prev_removed = True
                            not_adding = True
                            extrusion_removed = round(extrusion_removed + (float(item[1:]) - prev_extrusion[1]),4)
                    if not_adding == False:
                        #going to append to final
                        true_current = 0.0
                        edited_current = 0.0
                        command_to_append = []
                        move_to_append = []
                        if prev_removed == True:
                            retract = ['G1', 'E', 'F1800']
                            post_move = ['G1', 'E', 'F1800']
                            for command in move:
                                if "E" in command:
                                    prev_extrusion[1] = float(command[1:])
                                elif "F" in command:
                                    command_to_append.append('F4200')
                                else:
                                    move_to_append.append(command)
                            retract[1] += str(round(prev_extrusion[0] - 1.3,4))
                            post_move[1] += str(round(prev_extrusion[0],4))
                            infill_to_return.append(retract)
                            infill_to_return.append(move_to_append)
                            infill_to_return.append(post_move)
                            infill_to_return.append(move_to_append)
                            prev_removed = False
                        else:
                            for command in move:
                                if 'E' in command:
                                    true_current = float(command[1:])
                                    edited_current = round(true_current - extrusion_removed, 4)
                                    command_to_append = 'E' + str(edited_current)
                                    move_to_append.append(command_to_append)
                                    prev_extrusion[0] = edited_current
                                else:
                                    move_to_append.append(command)
                        infill_to_return.append(move_to_append)
                    else:
                        for command in move:
                            if 'F' in command:
                                spare_G1.append(command)
                                infill_to_return.append(spare_G1)
                        not_adding = False
                elif (prev_loc_floats[2] - 2) <= move_floats[2] <= (prev_loc_floats[2] - 2) and move[1] != prev_loc[1]:
                    for item in move:
                        if "E" in item:
                            prev_removed = True
                            not_adding = True
                            extrusion_removed = round(extrusion_removed + (float(item[1:]) - prev_extrusion[1]),4)
                    if not_adding == False:
                        #going to append to final list
                        true_current = 0.0
                        edited_current = 0.0
                        command_to_append = []
                        move_to_append = []
                        if prev_removed == True:
                            retract = ['G1', 'E', 'F1800']
                            post_move = ['G1', 'E', 'F1800']
                            for command in move:
                                if "E" in command:
                                    prev_extrusion[1] = float(command[1:])
                                elif "F" in command:
                                    command_to_append.append('F4200')
                                else:
                                    move_to_append.append(command)
                            retract[1] += str(round(prev_extrusion[0] - 1.3,4))
                            post_move[1] += str(round(prev_extrusion[0],4))
                            infill_to_return.append(retract)
                            infill_to_return.append(move_to_append)
                            infill_to_return.append(post_move)
                            infill_to_return.append(move_to_append)
                            prev_removed = False
                        else:
                            for command in move:
                                if 'E' in command:
                                    true_current = float(command[1:])
                                    edited_current = round(true_current - extrusion_removed, 4)
                                    command_to_append = 'E' + str(edited_current)
                                    move_to_append.append(command_to_append)
                                    prev_extrusion[0] = edited_current
                                else:
                                    move_to_append.append(command)
                        infill_to_return.append(move_to_append)

                    else:
                        for command in move:
                            if 'F' in command:
                                spare_G1.append(command)
                                infill_to_return.append(spare_G1)
                        not_adding = False

                    
                            

                else:
                    #going to append to final list
                    true_current = 0.0
                    edited_current = 0.0
                    command_to_append = []
                    move_to_append = []
                    if prev_removed == True:
                        retract = ['G1', 'E', 'F1800']
                        post_move = ['G1', 'E', 'F1800']
                        for command in move:
                            if "E" in command:
                                prev_extrusion[1] = float(command[1:])
                            elif "F" in command:
                                command_to_append.append('F4200')
                            else:
                                move_to_append.append(command)
                        retract[1] += str(round(prev_extrusion[0] - 1.3,4))
                        post_move[1] += str(round(prev_extrusion[0],4))
                        infill_to_return.append(retract)
                        infill_to_return.append(move_to_append)
                        infill_to_return.append(post_move)
                        infill_to_return.append(move_to_append)
                        prev_removed = False
                    else:
                        for command in move:
                            if 'E' in command:
                                true_current = float(command[1:])
                                edited_current = round(true_current - extrusion_removed, 4)
                                command_to_append = 'E' + str(edited_current)
                                move_to_append.append(command_to_append)
                                prev_extrusion[0] = edited_current
                            else:
                                move_to_append.append(command)
                    infill_to_return.append(move_to_append)
            else:
                #going to append to final list
                for command in move:
                    if 'E' in command:
                        true_current = float(command[1:])
                        edited_current = round(true_current - extrusion_removed, 4)
                        command_to_append = 'E' + str(edited_current)
                        move_to_append.append(command_to_append)
                        prev_extrusion[0] = edited_current
                    else:
                        move_to_append.append(command)
                infill_to_return.append(move_to_append)
        except IndexError:
            #going to append to final list
            infill_to_return.append(move_to_append)
        prev_extrusion[1] = current_true_extrusion
    return infill_to_return




def start_removal(gcode_list):
    '''gets the length of the first outer side of the object of the second
        layer, continues the removal process by going to the functions that
        work on the infill and the shell when it finishes processing each
        command for the related movements. Returns the final product as a
        list.'''
    list_to_return = []
    is_in_shell = True
    is_in_infill = False
    is_in_object = False
    current_layer_num = 0
    wall_length = 0
    edge_distance = 0
    current_layer_shell = []
    current_layer_infill = []
    fixed_shell = []
    fixed_infill = []
    for line in gcode_list:
        line = line.strip().split()
        if 'M106' in line:
            is_in_object = True
        elif 'M107' in line:
            is_in_object = False
        if is_in_object == True:
            if ';shell' in line:
                if is_in_shell == True:
                    if current_layer_num == 2:
                        edge_distance = round(abs(float(current_layer_shell[6][1][1:]))\
                            +abs(float(current_layer_shell[7][1][1:])),2)
                    fixed_shell = do_shell_stuff(current_layer_shell,edge_distance)
                    current_layer_shell = []
                    for item in fixed_shell:
                        list_to_return.append(item)
                else:
                    is_in_shell = True
                    is_in_infill = False
                    fixed_infill = do_infill_stuff(current_layer_infill)
                    current_layer_infill = []
                    for item in fixed_infill:
                        list_to_return.append(item)
            elif ';infill' in line:
                is_in_shell = False
                is_in_infill = True
                if current_layer_num == 2:
                    edge_distance = round(abs(float(current_layer_shell[6][1][1:]))\
                        +abs(float(current_layer_shell[7][1][1:])),2)
                if current_layer_num == 25:
                    print ('lunch break')
                fixed_shell = do_shell_stuff(current_layer_shell, edge_distance)
                current_layer_shell = []
                for item in fixed_shell:
                    list_to_return.append(item)
            try:
                if 'Z' in line[1]:
                    current_layer_num += 1
                    print (current_layer_num)
            except IndexError:
                pass
            if is_in_shell:
                current_layer_shell.append(line)
            elif is_in_infill:
                current_layer_infill.append(line)
        else:
            list_to_return.append(line)
    return (list_to_return)




def main():
    '''the main, lol'''
    print('Welcome to the wall remover!')
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
            no_wall_file = start_removal(gcode_list)
            make_new_file(no_wall_file)
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



