# keep these three import statements
import game_API
import fileinput
import json

# your import statements here
import random

first_line = True # DO NOT REMOVE

# global variables or other functions can go here
stances = ["Rock", "Paper", "Scissors"]

AUTO_RETREAT_HEALTH = 50
MONSTER_HEALTH_WEIGHT = .7
MONSTER_ATTACK_WEIGHT = 1
PLAYER_ROCK_REWARD_WEIGHT = 20
PLAYER_PAPER_REWARD_WEIGHT = 20
PLAYER_SCISSORS_REWARD_WEIGHT = 20
PLAYER_SPEED_REWARD_WEIGHT = 20
PLAYER_HEALTH_REWARD_WEIGHT = 30
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
        if game.has_monster(node):
            monster = game.get_monster(node)
            score = monster_score(monster)
            if score > max_score:
                max_score = score
                max_monster = monster

    return max_monster

# Healing monster spawns at turn 40
def attack_decision(node):
    if len(nodes) == 0:
        return
    chosen_stance = stances[random.randint(0,2)]
    destination_node = game.get_self().location
    max_score = -1000000
    max_location = 0
    if game.get_self().health < AUTO_RETREAT_HEALTH:
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
    elif game.has_monster(game.get_self().location):
        chosen_stance = get_winning_stance(game.get_monster(game.get_self().location).stance)
    else:
        nodes = game.get_adjacent_nodes(game.get_self().location)
        monst = max_score_monster(nodes)
        if monst != None:
            destination_node = monst.location
            chosen_stance = get_winning_stance(monst.stance)
        else:
            destination_node = nodes[random.randint(0, len(nodes) - 1)]

    return (chosen_stance, destination_node)

    # me = game.get_self()
    #
    # if me.location == me.destination: # check if we have moved this turn
    #     # get all living monsters closest to me
    #     monsters = game.nearest_monsters(me.location, 1)
    #
    #     # choose a monster to move to at random
    #     monster_to_move_to = monsters[random.randint(0, len(monsters)-1)]
    #
    #     # get the set of shortest paths to that monster
    #     paths = game.shortest_paths(me.location, monster_to_move_to.location)
    #     destination_node = paths[random.randint(0, len(paths)-1)][0]
    # else:
    #     destination_node = me.destination
    #
    # if game.has_monster(me.location):
    #     # if there's a monster at my location, choose the stance that damages that monster
    #     chosen_stance = get_winning_stance(game.get_monster(me.location).stance)
    # else:
    #     # otherwise, pick a random stance
    #     chosen_stance = stances[random.randint(0, 2)]
    #
    # # submit your decision for the turn (This function should be called exactly once per turn)
    decision = attack_decision(game.get_self().location)
    game.submit_decision(decision[0], decision[1])
