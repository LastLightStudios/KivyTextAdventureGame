class RoomManager:
    rooms = {}
    current_room = None

    def add_room(self, new_room):
        if new_room.name in self.rooms:
            print(new_room.name + "already exists")
            return False
        else:
            self.rooms[new_room.name] = new_room
            print(new_room.name + " added to rooms")
            if self.current_room is None:
                self.current_room = new_room
                print(new_room.name + " set as current_room")
            return True

    @staticmethod
    # this method stores first_direction:other_room in the dictionary this_room.connected_rooms and vice versa
    # first_direction and second_direction are both expected to be strings.
    def add_connection(this_room, first_direction, other_room, second_direction):
        if not isinstance(first_direction, str):
            print("first_direction is not a string as expected")
        if not isinstance(second_direction, str):
            print("second_direction is not a string as expected")
        if first_direction in this_room.connected_rooms:
            print(this_room.name + "'s " + str(first_direction) + " is occupied")
            return False
        if second_direction in other_room.connected_rooms:
            print(other_room.name + "'s " + str(second_direction) + " is occupied")
            return False
        this_room.connected_rooms[first_direction] = other_room
        other_room.connected_rooms[second_direction] = this_room
        return True

    def travel(self, direction):
        print("Traveling from: " + self.current_room.name)
        if direction in self.current_room.connected_rooms:
            self.current_room = self.current_room.connected_rooms[direction]
            print("Entering: " + self.current_room.name)
            return self.current_room.description
        else:
            print("cannot travel in this direction")
            return "Cannot travel in this direction."


class Room:
    def __init__(self, name):
        self.description = None
        self.name = name
        self.connected_rooms = {}
        self.inventory = []

    def set_desc(self, desc):
        self.description = desc
