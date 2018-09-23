# keep these three import statements
import game_API
import fileinput
import json

# your import statements here
import random

first_line = True # DO NOT REMOVE

# global variables or other functions can go here
stances = ["Rock", "Paper", "Scissors"]
loop_number = 0
loop_index = 0;
loop_list = [[0,1,3,1],[0,1,0,6],[0,1,3,1],[0,1,3,1,0,6],[0,1,3,1,0,10,16,15,16,10]]
temp_path = []
beelining_for_health = False
is_joey = False

def get_winning_stance(stance):
    if stance == "Rock":
        return "Paper"
    elif stance == "Paper":
        return "Scissors"
    elif stance == "Scissors":
        return "Rock"

# main player script logic
# DO NOT CHANGE BELOW ----------------------------
for line in fileinput.input():
    if first_line:
        game = game_API.Game(json.loads(line))
        first_line = False
        continue
    game.update(json.loads(line))
# DO NOT CHANGE ABOVE ---------------------------

    # code in this block will be executed each turn of the game

    me = game.get_self()
    '''
    if (len(beeline_path)*(7-me.speed))-(me.movement_counter-me.speed))>=game.get_monster(0).repsawn_counter or game.get_monster(0).health>0:
        beeline_path=game.shortest_paths(me.location,0)
        destination_node=beeline_path[0][0]
    '''
    if False:
        pass

    else:
        if game.has_monster(me.location) and game.get_monster(me.location).health > 0:
            # if there's a living monster at my location, choose the stance that damages that monster, don't change location
            destination_node = me.location
            chosen_stance = get_winning_stance(game.get_monster(me.location).stance)
        else:
            # otherwise, go to the next location in the loop
            if (me.location == 0 and game.get_monster(0).respawn_counter <= 17):
                pass
            else:
                if (loop_list[loop_number][loop_index] == me.location):    #only change my target if I moved to the previous target
                    loop_index = loop_index + 1
                if (loop_index > len(loop_list[loop_number]) - 1):
                    loop_index = 0
                    loop_number = loop_number + 1
            chosen_stance = stances[random.randint(0, 2)]
        if (loop_number > len(loop_list) - 1):
            loop_number = len(loop_list) - 1
        destination_node = loop_list[loop_number][loop_index];

    game.log("Turn: {0},\tMyNode: {1},\tloopNumber: {2},\tMonsterHealth: {3},\tDestinationNode: {4},\tloopIndex: {5}".format(game.turn_number, me.location, loop_number, game.get_monster(me.location).health, destination_node, loop_index))


    # submit your decision for the turn (This function should be called exactly once per turn)
    game.submit_decision(destination_node, chosen_stance) #destination_node
