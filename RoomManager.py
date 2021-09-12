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
            new_room.manager = self
            return True

        # this method stores first_direction:other_room in the dictionary this_room.connected_rooms and vice versa
    # first_direction and second_direction are both expected to be strings.
    def add_connection(self, this_room, first_direction, other_room, second_direction):
        if not isinstance(first_direction, str):
            print(first_direction + " is not a string as expected: ")
        if not isinstance(second_direction, str):
            print(second_direction + " is not a string as expected")
        if this_room.name not in self.rooms:
            print(this_room.name + " is not in the rooms list: ")
        if other_room.name not in self.rooms:
            print(other_room.name +  " is not in the rooms list")
        if first_direction in this_room.connected_rooms:
            print(this_room.name + "'s " + str(first_direction) + " is occupied")
            return False
        if second_direction in other_room.connected_rooms:
            print(other_room.name + "'s " + str(second_direction) + " is occupied")
            return False
        this_room.connected_rooms[first_direction] = other_room
        other_room.connected_rooms[second_direction] = this_room
        return True

    def change_name(self, room, name):
        log = ""
        old_name = room.name
        # does the room exist in this manager
        if room.name in self.rooms:
            #is there already an existing room with the new name
            if name in self.rooms:
                log += "The room: " + name + "has been overwritten"
            # change the name of the room
            room.name = name
            # add the room to the dictionary of rooms with a matching name as the key
            self.rooms[name] = room
            # remove the old key:value
            del self.rooms[old_name]

    def travel(self, direction) -> str:
        print("Traveling from: " + self.current_room.name)
        if direction in self.current_room.connected_rooms:
            self.current_room = self.current_room.connected_rooms[direction]
            print("Entering: " + self.current_room.name)
            return self.current_room.description
        else:
            print("cannot travel in this direction")
            return "Cannot travel in this direction."

    def generate_default_map(self):
        home = Room("Home")
        home.set_desc("This is the starting room.")
        self.add_room(home)
        left_room = Room("Left Room")
        left_room.set_desc("Welcome to the Left Room.")
        self.add_room(left_room)
        right_room = Room("Right Room")
        right_room.set_desc("Welcome to the dining room.")
        self.add_room(right_room)
        porch = Room("Porch")
        porch.set_desc("This is the porch. There is a new nice view of the street.")
        self.add_room(porch)
        living_room = Room("Living Room")
        living_room.set_desc("This is living room. You can see a nice couch. To the right you can see the kitchen.")
        self.add_room(living_room)
        kitchen = Room("Kitchen")
        kitchen.set_desc("This is the kitchen. There is a dirty pot on the stove and two more in the sink.")
        self.add_room(kitchen)
        self.add_connection(home, "Left", left_room, "Right")
        self.add_connection(home, "Right", right_room, "Left")
        self.add_connection(home, "Forward", living_room, "Backwards")
        self.add_connection(right_room, "Forward", kitchen, "Backwards")
        self.add_connection(living_room, "Right", kitchen, "Left")

class Room:
    def __init__(self, name):
        self.manager = None
        self.description = None
        self.name = name
        self.connected_rooms = {}
        self.inventory = []

    def set_desc(self, desc):
        self.description = desc

    def set_direction(self, old_direction, new_direction):
        log = ""
        if new_direction in self.connected_rooms:
            log += "The edge '" + new_direction + ": " + self.connected_rooms[new_direction].name + \
                   "' has also been removed" + "\n"
        if old_direction in self.connected_rooms:
            self.connected_rooms[new_direction] = self.connected_rooms[old_direction]
            del self.connected_rooms[old_direction]
            log += "'" + old_direction + ": " + self.connected_rooms[new_direction].name + "' changed to '" + \
                   new_direction + ": " + self.connected_rooms[new_direction].name + "'\n"
        else:
            #log += old_direction + " does not exist in this room's connected_rooms dict"
            log = "something fucked up, somehow we are trying to edit a direction that doesnt exist \n"
        return log

    def set_destination_room(self, direction, new_destination_name):
        log = ""
        if new_destination_name in self.manager.rooms:
            if direction in self.connected_rooms:
                log += direction + ": " + self.connected_rooms[direction].name + " changed to " + \
                       direction + ": " + new_destination_name + "\n"
                self.connected_rooms[direction] = self.manager.rooms[new_destination_name]
            else:
                log += "The Direction: '" + direction + "' does not exist in this room's connected_rooms dict\n" + \
                       "I am pretty sure this msg should never pop up tho."
        else:
            log += "The destination room: '" + new_destination_name + "' does not exist in this room manager\n"
        return log

    def create_new_edge(self, direction, destination_name):
        log = ""
        if direction in self.connected_rooms:
            log += "'" + direction + "' already exists. Check the edge list if you wish to modify it.\n"
        else:
            if destination_name in self.manager.rooms:
                self.connected_rooms[direction] = self.manager.rooms[destination_name]
                log += "'" + direction + ": " + destination_name + "' has been added as a connected room"
            else:
                log += "The destination room: '" + destination_name + "' does not exist in this room manager\n"
        return log

