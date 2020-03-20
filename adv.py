from room import Room
from player import Player
from world import World
from util import Queue

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
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)
traversal_path = []
# Fill this out with directions to walk
opposites_dict = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}
traversal_graph = {player.current_room.id: {}}
exits = player.current_room.get_exits()
for element in exits:
    if element not in traversal_graph[player.current_room.id].keys():
        traversal_graph[player.current_room.id][element] = '?'
room_coords = {}
for i in range(500):
    room_coords[i] = None
room_coords[0] = [0, 0]
true_path = []

while len(traversal_graph) < 500:
    while True:
        exits = player.current_room.get_exits()
        new_exits = [element for element in exits if traversal_graph[player.current_room.id][element] == '?']
        if len(new_exits) == 0:
            break
        direction_of_travel = random.choice(new_exits)
        last_room = player.current_room.id
        player.travel(direction_of_travel)
        room_coords[player.current_room.id] = player.location
        traversal_path.append(direction_of_travel)
        traversal_graph[last_room][direction_of_travel] = player.current_room.id
        if traversal_graph.get(player.current_room.id) == None:
            traversal_graph[player.current_room.id] = {}
        else:
            pass
        exits = player.current_room.get_exits()
        for element in exits:
            if element not in traversal_graph[player.current_room.id].keys():
                traversal_graph[player.current_room.id][element] = '?'
        traversal_graph[player.current_room.id][opposites_dict[direction_of_travel]] = last_room
    q = Queue()
    q.enqueue([player.current_room.id])
    visited = set()
    while q.size() > 0:
        path = q.dequeue()
        v = path[-1]
        if v not in visited:
            visited.add(v)
            if '?' in traversal_graph[v].values():
                candidates = []
                for key, value in traversal_graph[v].items():
                    if value == '?':
                        candidates.append(key)
                test_coords = room_coords[v]
                n_neighbor = [test_coords[0], test_coords[1] + 1]
                e_neighbor = [test_coords[0] + 1, test_coords[1]]
                s_neighbor = [test_coords[0], test_coords[1] - 1]
                w_neighbor = [test_coords[0] - 1, test_coords[1]]
                for key in candidates:
                    if key == 'n':
                        if n_neighbor not in room_coords.values():
                            true_path = path
                    if key == 'e':
                        if e_neighbor not in room_coords.values():
                            true_path = path
                    if key == 's':
                        if s_neighbor not in room_coords.values():
                            true_path = path
                    if key == 'w':
                        if w_neighbor not in room_coords.values():
                            true_path = path
                if len(true_path) > 0:
                    break
            for neighbor in traversal_graph[v].values():
                path_copy = path.copy()
                path_copy.append(neighbor)
                q.enqueue(path_copy)
    for element in true_path[1:]:
        for key, value in traversal_graph[player.current_room.id].items():
            if element == value:
                direction_to_go = key
                break
        player.travel(direction_to_go)
        traversal_path.append(direction_to_go)
        true_path.clear()

        # key_list = list(traversal_graph[player.current_room.id].keys())
        # value_list = list(traversal_graph[player.current_room.id].values())
        # traversal_path.append(key_list[value_list.index(element)])
        # player.travel(key_list[value_list.index(element)])


    #
    # backtrack = traversal_path[::-1]
    # for path in backtrack:
    #     player.travel(opposites_dict[path])
    #     traversal_path.append(opposites_dict[path])
    #     if '?' in traversal_graph[player.current_room.id].values():
    #         print('yup')
    #         break
    #     else:
    #         print('nope')
    #         pass





# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
