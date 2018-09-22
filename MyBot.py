# keep these three import statements
import game_API
import fileinput
import json

# your import statements here
import random

first_line = True # DO NOT REMOVE
# Global variables
RETREAT_HEALTH = 50
MONSTER_DEATH_REWARD_PRIORITY = DeathEffects.health
MONSTER_HEALTH_WEIGHT = .7
MONSTER_ATTACK_WEIGHT = 1
MONSTER_REWARD_WEIGHT = 20

#Function return errors

# global variables or other functions can go here
stances = ["Rock", "Paper", "Scissors"]

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
# Function that calculates a monster's desireablitiy score for attacking
def monster_score (monster):
    score = 100
    score -= monster.health * MONSTER_HEALTH_WEIGHT
    score -= monster.attack * MONSTER_ATTACK_WEIGHT
    if monster.death_effects == MONSTER_DEATH_REWARD_PRIORITY:
        score += MONSTER_REWARD_WEIGHT
    return score
# From a list of monsters return the most ideal one to attacks
def ideal_monster_location(node):
    monsters = game.nearest_monsters(node, 1)
    if len(monsters) == 0:
        return game.shortest_paths(game.get_self().location, 0)[0]
    max_priority = monster_score(monsters[0])
    max_priority_location = monsters[0].location
    for monster in monsters:
        priority = monster_score(monster)
        if priority > max_priority:
            max_priority = priority
            max_priority_location = monster.location
    return max_priority_location
def should_retreat():
    if game.get_self().health < RETREAT_HEALTH:
        monsters = game.get_all_monsters()
        nodes = game.get_adjacent_nodes()
        if len(monsters) == 0:
            game.get_self().destination = game.get_self().shortest_paths(game.get_self().location, 0)
            return True
        min_monster_health = monsters[0]
        min_monster_health_node = -1
        priority_monsters = []
        for monster in monsters:
            for node in nodes:
                if monster.location != node:
                    game.get_self().destination = node
                    break
                if monster.health < min_monster_health:
                    min_monster_health = monster.health
                    min_monster_health_node = node
        if min_monster_health_node != -1:
            game.get_self().destination = min_monster_health_node
        else game.get_self().destination = nodes[0];
        return True
    return False
    # code in this block will be executed each turn of the game

    me = game.get_self()

    if me.location == me.destination: # check if we have moved this turn
        # get all living monsters closest to me
        monsters = game.nearest_monsters(me.location, 1)

        # choose a monster to move to at random
        monster_to_move_to = monsters[random.randint(0, len(monsters)-1)]

        # get the set of shortest paths to that monster
        paths = game.shortest_paths(me.location, monster_to_move_to.location)
        destination_node = paths[random.randint(0, len(paths)-1)][0]
    else:
        destination_node = me.destination

    if game.has_monster(me.location):
        # if there's a monster at my location, choose the stance that damages that monster
        chosen_stance = get_winning_stance(game.get_monster(me.location).stance)
    else:
        # otherwise, pick a random stance
        chosen_stance = stances[random.randint(0, 2)]

    # submit your decision for the turn (This function should be called exactly once per turn)
    game.submit_decision(destination_node, chosen_stance)
