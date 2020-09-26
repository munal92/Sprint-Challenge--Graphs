from room import Room
from player import Player
from world import World
from collections import deque
import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


reverse = {"n": "s", "s": "n", "e": "w", "w": "e"}

graph = {}


def traverse_map(starting_rm=None):
    to_visit = deque()

    if player.current_room.id not in graph:
        graph[player.current_room.id] = {}

    if starting_rm is not None:
        graph[player.current_room.id][reverse[
            starting_rm]] = player.current_room.get_room_in_direction(reverse[starting_rm]).id

    for direction in player.current_room.get_exits():
        if direction not in graph[player.current_room.id]:
            graph[player.current_room.id][direction] = '?'

    for direction in player.current_room.get_exits():
        adj_room = player.current_room.get_room_in_direction(direction).id

        if adj_room not in graph or graph[player.current_room.id][direction] == '?':
            to_visit.append(direction)

    while len(to_visit) > 0:

        map_ = to_visit.pop()

        if player.current_room.get_room_in_direction(map_).id not in graph:
            traversal_path.append(map_)
            graph[player.current_room.id][map_] = player.current_room.get_room_in_direction(
                map_).id
            player.travel(map_)
            traverse_map(map_)

            if len(graph) == len(world.rooms):
                return

            traversal_path.append(reverse[map_])
            player.travel(reverse[map_])


print(traverse_map())


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
