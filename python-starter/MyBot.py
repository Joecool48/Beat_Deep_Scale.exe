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
AUTO_RETREAT_HEALTH = 70
MONSTER_HEALTH_WEIGHT = .7
MONSTER_ATTACK_WEIGHT = 1
PLAYER_ROCK_REWARD_WEIGHT = 20
PLAYER_PAPER_REWARD_WEIGHT = 20
PLAYER_SCISSORS_REWARD_WEIGHT = 20
PLAYER_SPEED_REWARD_WEIGHT = 20
PLAYER_HEALTH_REWARD_WEIGHT = 50
isJ = False
isEarly = True

def monster_score (monster):
    score = 0
    score -= monster.health * MONSTER_HEALTH_WEIGHT
    score -= monster.attack * MONSTER_ATTACK_WEIGHT
    score += monster.death_effects.rock * PLAYER_ROCK_REWARD_WEIGHT
    score += monster.death_effects.paper * PLAYER_PAPER_REWARD_WEIGHT
    score += monster.death_effects.scissors * PLAYER_SCISSORS_REWARD_WEIGHT
    score += monster.death_effects.health * PLAYER_HEALTH_REWARD_WEIGHT
    score += monster.death_effects.speed * PLAYER_SPEED_REWARD_WEIGHT
    return score

def max_score_monster(nodes):
    if len(nodes) == 0:
        return None
    max_score = -10000000
    max_monster = None
    for node in nodes:
        if game.has_monster(node) and game.get_self().location != node and game.get_monster(node).health > 0 and node != 0:
            monster = game.get_monster(node)
            score = monster_score(monster)
            if score > max_score and node != 0:
                max_score = score
                max_monster = monster

    return max_monster

def attack_decision(node):
    chosen_stance = stances[random.randint(0,2)]
    destination_node = game.get_self().location
    max_score = -1000000
    max_location = 0
    if game.get_self().location == 0 and game.get_monster(0).respawn_counter < 7:
        destination_node = 0
    elif game.get_self().health < AUTO_RETREAT_HEALTH and game.get_monster(0).respawn_counter < 25:
        game.log("Retreat")
        shortest = game.shortest_paths(game.get_self().location, 0)
        max_location = shortest[0][0]
        for path in shortest:
            score = monster_score(game.get_monster(path[0]))
            if not game.has_monster(path[0]):
                destination_node = path[0]
            elif score > max_score:
                max_score = score
                max_location = path[0]
        destination_node = max_location
        game.log("Dest node = " + str(destination_node))
    elif game.has_monster(game.get_self().location) and game.get_monster(game.get_self().location).health > 0:
        game.log("Current node has monster")
        chosen_stance = get_winning_stance(game.get_monster(game.get_self().location).stance)
    else:
        game.log("No retreat or monster on space")
        nodes = game.get_adjacent_nodes(game.get_self().location)
        all_nodes = game.get_all_monsters()

        monst = max_score_monster(nodes)
        if monst != None:
            destination_node = monst.location
            game.log("Dest node = " + str(destination_node))
            chosen_stance = get_winning_stance(monst.stance)
        else:
            game.log("choose a node")
            if len(all_nodes) == 0:
                destination_node = 0
            destination_node = all_nodes[0].location
            game.log("Dest node = " + str(destination_node))
    return (chosen_stance, destination_node)

def fighting():
    rockWeight = me.rock
    paperWeight = me.paper
    scissorsWeight = me.scissors
    num = randint(0, rockWeight+paperWeight+scissorsWeight)
    if num > 0 and num < rockWeight:
        return "Rock"
    elif num <paperWeight+rockWeight:
        return "Paper"
    else:
        return "scissors"

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
    if (game.turn_number >= 300):
        game.submit_decision(me.location, fighting())
    else:
        if (((loop_number == len(loop_list) - 1) and (loop_index == len(loop_list[loop_number]) - 1)) and (isJ == False)):
            isJ = True
        if (isJ == False):
            if (game.turn_number < 7):
                game.submit_decision(1,"Paper")
                isEarly = True
            elif game.has_monster(me.location) and game.get_monster(me.location).health > 0:
                # if there's a living monster at my location, choose the stance that damages that monster, don't change location
                isEarly = False
                chosen_stance = get_winning_stance(game.get_monster(me.location).stance)
                destination_node = me.location
            else:
                # otherwise, go to the next location in the loop
                isEarly = False
                if (me.location == 0 and game.get_monster(0).respawn_counter <=16):
                    destination_node = me.location
                elif (me.location == 3 and game.get_monster(3).respawn_counter <= 8 and loop_number < 2):
                    destination_node = me.location
                else:
                    if (loop_list[loop_number][loop_index] == me.location):    #only change my target if I moved to the previous target
                        loop_index = loop_index + 1
                    if (loop_index > len(loop_list[loop_number]) - 1):
                        loop_index = 0
                        loop_number = loop_number + 1
                chosen_stance = stances[random.randint(0, 2)]
            if (loop_number > len(loop_list) - 1):
                loop_number = len(loop_list) - 1
            if isEarly == False:
                destination_node = loop_list[loop_number][loop_index];
                game.submit_decision(destination_node, chosen_stance)
        if (isJ == True):
            decision = attack_decision(game.get_self().location)
            game.submit_decision(decision[1], decision[0])
    #game.log("Turn: {0},\tMyNode: {1},\tloopNumber: {2},\tMonsterHealth: {3},\tDestinationNode: {4},\tloopIndex: {5}".format(game.turn_number, me.location, loop_number, game.get_monster(9).health, destination_node, loop_index))


    # submit your decision for the turn (This function should be called exactly once per turn)
 #destination_node
