# keep these three import statements
import game_API
import fileinput
import json

# your import statements here
import random

first_line = True # DO NOT REMOVE

# global variables or other functions can go here
stances = ["Rock", "Paper", "Scissors"]

AUTO_RETREAT_HEALTH = 70
MONSTER_HEALTH_WEIGHT = .7
MONSTER_ATTACK_WEIGHT = 1
PLAYER_ROCK_REWARD_WEIGHT = 20
PLAYER_PAPER_REWARD_WEIGHT = 20
PLAYER_SCISSORS_REWARD_WEIGHT = 20
PLAYER_SPEED_REWARD_WEIGHT = 20
PLAYER_HEALTH_REWARD_WEIGHT = 30

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

# Healing monster spawns at turn 40
def attack_decision(node):
    chosen_stance = stances[random.randint(0,2)]
    destination_node = game.get_self().location
    max_score = -1000000
    max_location = 0
    if game.get_self().location == 0 and game.get_monster(0).respawn_counter < 7:
        destination_node = 0
    elif game.get_self().health < AUTO_RETREAT_HEALTH and game.get_monster(0).respawn_counter < 10:
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

    decision = attack_decision(game.get_self().location)
    game.submit_decision(decision[1], decision[0])