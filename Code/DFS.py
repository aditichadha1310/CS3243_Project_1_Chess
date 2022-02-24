# Helper functions to aid in your implementation. Can edit/remove
import sys

from collections import deque


queue = deque()

dr = [1, 1, -1, 0, 1, -1, -1, 0]
dc = [1, -1, 0, 1, 0, -1, 1, -1]
rows = 0
cols = 0
board_dictionary = {}
parent_child_mapping = {}
nodes_in_next_layer = 0
node_left_in_layer = 1
visited = {}
final_path = []
num_obstacles = 0
start_position = ''
num_enemy_pieces = 0
nodes_explored = 0
position_of_enemies = []
type_of_character = {"King": "K", "Queen": "Q", "Bishop": "B", "Rook": "R", "Knight": "N", "Empty Spot": "E",
                     "Obstacle": "X", "Start Position": "S", "Goal-Position": "G"}


class Piece:
    pass


class Board:
    pass


class State:
    pass


def input_parser():
    global rows
    global cols
    global board_dictionary
    global num_enemy_pieces
    global position_of_enemies
    global type_of_character
    global start_position
    prevline = ""
    num_ene_character = [0, 0, 0, 0, 0]
    with open(sys.argv[1]) as f:
        line = f.readline()
        while line:
            if line.startswith("Rows:"):
                rows = int(line.strip("Rows:"))
            elif line.startswith("Cols:"):
                cols = int(line.strip("Cols:"))
                if cols > 26:
                    break
                else:
                    design_board(rows, cols)
            elif line.startswith("Number of Obstacles:"):
                num_obstacles = int(line.strip("Number of Obstacles:"))
            elif line.startswith("Position of Obstacles (space between):"):
                position_of_obstacle = (line[38:]).strip("\n")
                positions = position_of_obstacle.split(" ")
                for i in range(0, num_obstacles):
                    designate_position(positions[i], type_of_character.get("Obstacle"))
            elif line.startswith("Step cost to move to selected grids (Default cost is 1) [Pos, Cost]:"):
                line = f.readline().strip("\n")
                prevline = line
                while line.startswith("["):
                    in1 = (line.strip("[")).strip("\n")  # a5 2
                    in2 = in1.strip("]")
                    pos_cost = in2.split(",")
                    path_cost_pos = int(pos_cost[1])
                    designate_path_cost(pos_cost[0], path_cost_pos)
                    line = f.readline()
                prevline = line
            elif (prevline.startswith(
                "Number of Enemy King, Queen, Bishop, Rook, Knight (space between):")):
                num_ene = prevline[66:].strip("\n")
                num_piece = num_ene.split(" ")
                for i in range(0, 5):
                    if (int(num_piece[i])) > 0:
                        num_ene_character[i] = int(num_piece[i])
                        num_enemy_pieces = int(num_piece[i]) + num_enemy_pieces
                for i in range(0, num_enemy_pieces):
                    line = f.readline()
                    in3 = line.strip("[").strip("\n")
                    in4 = in3.strip("]")
                    char_pos = in4.split(",")
                    enemy_char = char_pos[0]
                    enemy_pos = char_pos[1]
                    position_of_enemies.append(enemy_pos)
                    designate_position(enemy_pos, type_of_character.get(enemy_char))
                prevline = ""
                if num_enemy_pieces==0:
                    line = f.readline()
            elif line.startswith("Starting Position of Pieces [Piece, Pos]:"):
                line = f.readline()
                len_st = len(line)
                pos_king2 = line[1:len_st - 2]
                pos_king3 = pos_king2.split(",")
                start_pos = pos_king3[1]
                start_position = pos_king3[1]
                designate_position(start_pos, type_of_character.get("Start Position"))
            elif line.startswith("Goal Positions (space between):"):
                goal_positions = line[31:].strip("\n")
                goal_position_list = goal_positions.split(" ")
                for k in goal_position_list:
                    designate_position(k, type_of_character.get("Goal-Position"))
            line = f.readline()


def design_board(rows, cols):
    global board_dictionary
    global visited
    default_action_cost = 1
    for i in range(0, cols):
        for j in range(0, rows):
            board_dictionary[(chr(i + 97), j)] = ["E", int(default_action_cost)]
            visited[(chr(i + 97), j)] = False


def designate_position(position, character_type):
    global board_dictionary
    col_pos = position[0]
    row_pos = int(position[1:])
    p=[]
    p.append(col_pos)
    p.append(row_pos)
    if check_valid_coordinate(p):
        board_dictionary[(col_pos, row_pos)][0] = character_type
        p.clear()


def designate_path_cost(position, path_costs):
    col_pos = position[0]
    row_pos = int(position[1:])
    board_dictionary[(col_pos, row_pos)][1] = path_costs



def mark_threatened(pos_threat):
    global board_dictionary
    if len(pos_threat) == 0:
        return
    else:
        col_threat = pos_threat[0]
        row_threat = pos_threat[1]
        char_present = board_dictionary.get((col_threat, int(row_threat)))[0]
        if char_present == 'E' or char_present == 'G':
            board_dictionary[(col_threat, row_threat)][0] = 'X'
        else:
            return


def generate_eight_positions(col_pos, row_pos):
    position = []
    temp_col_pos = chr(ord(col_pos) + 1)
    temp_row_pos = row_pos + 2
    position.append([temp_col_pos, temp_row_pos])
    temp_row_pos = row_pos - 2
    position.append([temp_col_pos, temp_row_pos])
    temp_col_pos = chr(ord(col_pos) + 2)
    temp_row_pos = row_pos + 1
    position.append([temp_col_pos, temp_row_pos])
    temp_row_pos = row_pos - 1
    position.append([temp_col_pos, temp_row_pos])

    temp_col_pos = chr(ord(col_pos) - 1)
    temp_row_pos = row_pos + 2
    position.append([temp_col_pos, temp_row_pos])
    temp_row_pos = row_pos - 2
    position.append([temp_col_pos, temp_row_pos])
    temp_col_pos = chr(ord(col_pos) - 2)
    temp_row_pos = row_pos + 1
    position.append([temp_col_pos, temp_row_pos])
    temp_row_pos = row_pos - 1
    position.append([temp_col_pos, temp_row_pos])
    return position


def mark_threatened_positions(col_pos, row_pos, enemy_type):
    pos_threat = []
    temp_row_pos = row_pos
    temp_col_pos = col_pos
    global board_dictionary
    if enemy_type == "K":
        pos_threat = move_left(col_pos, row_pos)
        mark_threatened(pos_threat)
        pos_threat = move_right(col_pos, row_pos)
        mark_threatened(pos_threat)
        pos_threat = move_up(col_pos, row_pos)
        mark_threatened(pos_threat)
        pos_threat = move_down(col_pos, row_pos)
        mark_threatened(pos_threat)
        pos_threat = move_north_east(col_pos, row_pos)
        mark_threatened(pos_threat)
        pos_threat = move_north_west(col_pos, row_pos)
        mark_threatened(pos_threat)
        pos_threat = move_south_east(col_pos, row_pos)
        mark_threatened(pos_threat)
        pos_threat = move_south_west(col_pos, row_pos)
        mark_threatened(pos_threat)
        board_dictionary[(col_pos, row_pos)][0] = 'X'

    if enemy_type == "B" or enemy_type == 'Q':
        # north-east
        threat = []
        tp = []
        tp_c = ' '
        tp_r = 0
        flag = False
        threat.append(col_pos)
        threat.append(row_pos)
        temp_row_pos = row_pos
        temp_col_pos = col_pos
        while check_valid_coordinate(threat) == True and flag == False:
            tp = move_north_east(temp_col_pos, temp_row_pos)
            if len(tp) != 0:
                tp_c = tp[0]
                tp_r = tp[1]
                cpresent = board_dictionary[(tp_c, tp_r)][0]
                if cpresent == 'K' or cpresent == 'N' or cpresent == 'Q' or cpresent == 'B' or cpresent == 'X' or cpresent == 'R':
                    flag = True
                else:
                    temp_row_pos = tp_r
                    temp_col_pos = tp_c
                    mark_threatened(tp)
                    threat.clear()
                    threat.append(tp_c)
                    threat.append(tp_r)
            else:
                flag = True
        #         north west
        threat.clear()
        flag = False
        temp_col_pos = col_pos
        temp_row_pos = row_pos
        threat.append(temp_col_pos)
        threat.append(temp_row_pos)
        tp.clear()
        while check_valid_coordinate(threat) == True and flag == False:
            tp = move_north_west(temp_col_pos, temp_row_pos)
            if len(tp) != 0:
                tp_c = tp[0]
                tp_r = tp[1]
                cpresent = board_dictionary[(tp_c, tp_r)][0]
                if cpresent == 'K' or cpresent == 'N' or cpresent == 'Q' or cpresent == 'B' or cpresent == 'X' or cpresent == 'R':
                    flag = True
                else:
                    temp_row_pos = tp_r
                    temp_col_pos = tp_c
                    mark_threatened(tp)
                    threat.clear()
                    threat.append(tp_c)
                    threat.append(tp_r)
            else:
                flag = True

        # south-east
        threat.clear()
        flag = False
        temp_col_pos = col_pos
        temp_row_pos = row_pos
        threat.append(col_pos)
        threat.append(row_pos)
        while check_valid_coordinate(threat) == True and flag == False:
            tp = move_south_east(temp_col_pos, temp_row_pos)
            if len(tp) != 0:
                tp_c = tp[0]
                tp_r = tp[1]
                cpresent = board_dictionary[(tp_c, tp_r)][0]
                if cpresent == 'K' or cpresent == 'N' or cpresent == 'Q' or cpresent == 'B' or cpresent == 'X' or cpresent == 'R':
                    flag = True
                    break
                else:
                    temp_row_pos = tp_r
                    temp_col_pos = tp_c
                    mark_threatened(tp)
                    threat.clear()
                    threat.append(tp_c)
                    threat.append(tp_r)
            else:
                flag = True
        # south-west
        threat.clear()
        flag = False
        temp_col_pos = col_pos
        temp_row_pos = row_pos
        threat.append(col_pos)
        threat.append(row_pos)
        while check_valid_coordinate(threat) == True and flag == False:
            tp = move_south_west(temp_col_pos, temp_row_pos)
            if len(tp) != 0:
                tp_c = tp[0]
                tp_r = tp[1]
                cpresent = board_dictionary[(tp_c, tp_r)][0]
                if cpresent == 'K' or cpresent == 'N' or cpresent == 'Q' or cpresent == 'B' or cpresent == 'X' or cpresent == 'R':
                    flag = True
                    break
                else:
                    temp_row_pos = tp_r
                    temp_col_pos = tp_c
                    mark_threatened(tp)
                    threat.clear()
                    threat.append(tp_c)
                    threat.append(tp_r)
            else:
                flag = True
        threat.clear()
        flag = False
        temp_col_pos = col_pos
        temp_row_pos = row_pos
        threat.append(col_pos)
        threat.append(row_pos)
    if enemy_type == 'B':
        board_dictionary[(col_pos, row_pos)][0] = 'X'

    if enemy_type == 'R' or enemy_type == 'Q':
        # left
        threat = []
        tp = []
        tp_c = ' '
        tp_r = 0
        flag = False
        threat.append(col_pos)
        threat.append(row_pos)
        temp_row_pos = row_pos
        temp_col_pos = col_pos
        while check_valid_coordinate(threat) == True and flag == False:
            tp = move_left(temp_col_pos, temp_row_pos)
            if len(tp) != 0:
                tp_c = tp[0]
                tp_r = tp[1]
                cpresent = board_dictionary[(tp_c, tp_r)][0]
                if cpresent == 'K' or cpresent == 'N' or cpresent == 'Q' or cpresent == 'B' or cpresent == 'X' or cpresent == 'R':
                    flag = True
                else:
                    temp_row_pos = tp_r
                    temp_col_pos = tp_c
                    mark_threatened(tp)
                    threat.clear()
                    threat.append(tp_c)
                    threat.append(tp_r)
            else:
                flag = True
        #         right
        threat.clear()
        flag = False
        temp_col_pos = col_pos
        temp_row_pos = row_pos
        threat.append(temp_col_pos)
        threat.append(temp_row_pos)
        tp.clear()
        while check_valid_coordinate(threat) == True and flag == False:
            tp = move_right(temp_col_pos, temp_row_pos)
            if len(tp) != 0:
                tp_c = tp[0]
                tp_r = tp[1]
                cpresent = board_dictionary[(tp_c, tp_r)][0]
                if cpresent == 'K' or cpresent == 'N' or cpresent == 'Q' or cpresent == 'B' or cpresent == 'X' or cpresent == 'R':
                    flag = True
                else:
                    temp_row_pos = tp_r
                    temp_col_pos = tp_c
                    mark_threatened(tp)
                    threat.clear()
                    threat.append(tp_c)
                    threat.append(tp_r)
            else:
                flag = True

        # up
        threat.clear()
        flag = False
        temp_col_pos = col_pos
        temp_row_pos = row_pos
        threat.append(col_pos)
        threat.append(row_pos)
        while check_valid_coordinate(threat) == True and flag == False:
            tp = move_up(temp_col_pos, temp_row_pos)
            if len(tp) != 0:
                tp_c = tp[0]
                tp_r = tp[1]
                cpresent = board_dictionary[(tp_c, tp_r)][0]
                if cpresent == 'K' or cpresent == 'N' or cpresent == 'Q' or cpresent == 'B' or cpresent == 'X' or cpresent == 'R':
                    flag = True
                    break
                else:
                    temp_row_pos = tp_r
                    temp_col_pos = tp_c
                    mark_threatened(tp)
                    threat.clear()
                    threat.append(tp_c)
                    threat.append(tp_r)
            else:
                flag = True
        # down
        threat.clear()
        flag = False
        temp_col_pos = col_pos
        temp_row_pos = row_pos
        threat.append(col_pos)
        threat.append(row_pos)
        while check_valid_coordinate(threat) == True and flag == False:
            tp = move_down(temp_col_pos, temp_row_pos)
            if len(tp) != 0:
                tp_c = tp[0]
                tp_r = tp[1]
                cpresent = board_dictionary[(tp_c, tp_r)][0]
                if cpresent == 'K' or cpresent == 'N' or cpresent == 'Q' or cpresent == 'B' or cpresent == 'X' or cpresent == 'R':
                    flag = True
                    break
                else:
                    temp_row_pos = tp_r
                    temp_col_pos = tp_c
                    mark_threatened(tp)
                    threat.clear()
                    threat.append(tp_c)
                    threat.append(tp_r)
            else:
                flag = True
    board_dictionary[(col_pos, row_pos)][0] = 'X'

    if enemy_type == "N":
        prospective_pos = generate_eight_positions(col_pos, row_pos)
        for poss in prospective_pos:
            if check_valid_coordinate(poss):
                mark_threatened(poss)
        board_dictionary[(col_pos, row_pos)][0] = 'X'


def check_valid_coordinate(pos_threat):
    global rows
    global cols
    col_threat = ord(pos_threat[0]) - 97
    row_threat = int(pos_threat[1])
    if 0 <= col_threat < cols and 0 <= row_threat < rows:
        return True
    else:
        return False


def find_char_present(col_pos, row_pos):
    return board_dictionary.get((col_pos, row_pos))[0]


def move_left(col_pos, row_pos):
    if col_pos == 'a':
        return []
    else:
        col_pos = chr(ord(col_pos) - 1)
        return [col_pos, row_pos]


def move_up(col_pos, row_pos):
    if row_pos == 0:
        return []
    else:
        row_pos = row_pos - 1
        return [col_pos, row_pos]


def move_right(col_pos, row_pos):
    global cols
    if ord(col_pos) - 96 >= cols:
        return []
    else:
        col_pos = chr((ord(col_pos)) + 1)
        return [col_pos, row_pos]


def move_down(col_pos, row_pos):
    global rows
    if row_pos == rows - 1:
        return []
    else:
        row_pos = row_pos + 1
        return [col_pos, row_pos]


def move_north_east(col_pos, row_pos):
    global cols
    if ord(col_pos) - 96 >= cols or row_pos == 0:
        return []
    else:
        row_pos = row_pos - 1
        col_pos = chr((ord(col_pos)) + 1)
        return [col_pos, row_pos]


def move_north_west(col_pos, row_pos):
    if col_pos == 'a' or row_pos == 0:
        return []
    else:
        row_pos = row_pos - 1
        col_pos = chr(ord(col_pos) - 1)
        return [col_pos, row_pos]


def move_south_east(col_pos, row_pos):
    global rows
    global cols
    if row_pos == rows - 1 or ord(col_pos) - 96 >= cols:
        return []
    else:
        row_pos = row_pos + 1
        col_pos = chr((ord(col_pos)) + 1)
        return [col_pos, row_pos]


def move_south_west(col_pos, row_pos):
    global rows
    if row_pos == rows - 1 or col_pos == 'a':
        return []
    else:
        row_pos = row_pos + 1
        col_pos = chr(ord(col_pos) - 1)
        return [col_pos, row_pos]


def build_board():
    global type_of_character
    global board_dictionary
    global num_enemy_pieces
    global position_of_enemies
    global num_enemy_pieces
    for i in range(0, num_enemy_pieces):
        pos = position_of_enemies[i]
        col_pos = pos[0]
        row_pos = int(pos[1:])
        enemy_type = board_dictionary.get((col_pos, row_pos))[0]
        mark_threatened_positions(col_pos, row_pos, enemy_type)


def explore_neighbours(r, c):
    global rows
    global cols
    global dr
    global dc
    global board_dictionary
    global nodes_explored
    global nodes_in_next_layer
    global visited

    for i in range(0, 8):
        rr = r + dr[i]
        cc = ord(c) + dc[i]
        ccc = chr(cc)
        if 0 <= (ord(ccc) - 97) < cols and 0 <= rr < rows:
            if visited.get((ccc, rr)) is False and (board_dictionary.get((ccc, rr)))[0] != 'X':
                visited[(ccc, rr)] = True
                nodes_explored = nodes_explored + 1
                queue.append((ccc, rr))
                parent_child_mapping[(ccc, rr)] = (c, r)
                nodes_in_next_layer = nodes_in_next_layer + 1


def solve():
    global queue
    global board_dictionary
    global nodes_in_next_layer
    global node_left_in_layer
    global nodes_explored
    global start_position
    goal_pos_reached = []
    reached_end = False
    start_c = start_position[0]
    start_r = int((start_position[1:]))
    start_pos = (start_c, start_r)
    queue.append(start_pos)
    visited[start_pos] = True
    nodes_explored = nodes_explored + 1

    while queue:
        pos_tuple = queue.pop()
        if board_dictionary.get((pos_tuple[0], pos_tuple[1]))[0] == 'G':
            goal_pos_reached.append(pos_tuple[0])
            goal_pos_reached.append(pos_tuple[1])
            return goal_pos_reached
            # reached_end = True
        explore_neighbours(pos_tuple[1], pos_tuple[0])
        node_left_in_layer = node_left_in_layer - 1
        if node_left_in_layer == 0:
            node_left_in_layer = nodes_in_next_layer
            nodes_in_next_layer = 0
    if reached_end:
        return goal_pos_reached
    return 0


def search():
    pass


def retrace_path(goal_position_reached):
    path = []
    global parent_child_mapping
    global start_position
    global final_path
    start_c = start_position[0]
    start_r = int(start_position[1:])
    goal_c = goal_position_reached[0]
    goal_r = goal_position_reached[1]
    goal_tuple = (goal_c, goal_r)
    current_tuple = goal_tuple
    while current_tuple[0] != start_c or current_tuple[1] != start_r:
        path.append([parent_child_mapping.get(current_tuple), current_tuple])
        current_tuple = parent_child_mapping.get(current_tuple)
    return path


def run_DFS():
    global rows
    global cols
    global board_dictionary
    input_parser()

    # Builds the board with threatened positions
    if num_enemy_pieces > 0:
        build_board()
    goal_attained = solve()
    if goal_attained:
        path = retrace_path(goal_attained)
        if len(path) != 0:
            path.reverse()
            return (path, nodes_explored)
    else:
        return ([], 0)
