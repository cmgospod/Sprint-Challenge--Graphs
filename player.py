class Player:
    def __init__(self, starting_room):
        self.current_room = starting_room
        self.location = [0, 0]
    def travel(self, direction, show_rooms = False):
        if direction == 'n':
            self.location[1] += 1
        if direction == 's':
            self.location[1] -= 1
        if direction == 'e':
            self.location[0] += 1
        if direction == 'w':
            self.location[0] -= 1
        next_room = self.current_room.get_room_in_direction(direction)
        if next_room is not None:
            self.current_room = next_room
            if (show_rooms):
                next_room.print_room_description(self)
        else:
            print("You cannot move in that direction.")
