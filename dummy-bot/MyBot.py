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
loop_list = [[0, 10, 9, 8, 14],[19]]

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

    if game.has_monster and game.get_monster(me.location).health > 0:
        # if there's a living monster at my location, choose the stance that damages that monster, don't change location
        chosen_stance = get_winning_stance(game.get_monster(me.location).stance)
    else:
        # otherwise, go to the next location in the loop
        if (loop_list[loop_number][loop_index] == me.location):    #only change my target if I moved to the previous target
            loop_index = loop_index + 1
        if (loop_index > len(loop_list[loop_number]) - 1):
            loop_index = 0
            loop_number = loop_number + 1
        chosen_stance = stances[random.randint(0, 2)]
    if (loop_number > len(loop_list) - 1):
        loop_number = len(loop_list) - 1

    destination_node = loop_list[loop_number][loop_index];

    #game.log("Turn: {0},\tMyNode: {1},\tloopNumber: {2},\tMonsterHealth: {3},\tDestinationNode: {4},\tloopIndex: {5}".format(game.turn_number, me.location, loop_number, game.get_monster(9).health, destination_node, loop_index))


    # submit your decision for the turn (This function should be called exactly once per turn)
    game.submit_decision(destination_node, chosen_stance) #destination_node
