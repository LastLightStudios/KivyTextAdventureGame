from __future__ import annotations
from dataclasses import dataclass, field
import jsonpickle


@dataclass
class Map(object):
    name: str = ""
    current_room: Room = None
    starting_room: Room = None

    def __init__(self):
        self.rooms = {}

    def travel(self, direction):
        print("Traveling from: " + self.current_room.name)
        if direction in self.current_room.connected_rooms:
            self.current_room = self.current_room.connected_rooms[direction]
            print("Entering: " + self.current_room.name)
            return self.current_room.description
        else:
            print("cannot travel in this direction")
            return "Cannot travel in this direction."


@dataclass
class RoomManager(object):
    map: Map = Map()

    # Read/Write Map Methods
    def create_new_map(self):
        self.map = Map()
        self.generate_default_map()

    def load(self, file_path):
        with open(file_path, "r") as load_file:
            frozen = load_file.read()
            map_obj = jsonpickle.decode(frozen)
            self.map = map_obj

    def save(self, file_path):
        temp_string = jsonpickle.encode(self.map, indent=4, keys=True)
        with open(file_path, "w") as save_file:
            save_file.write(temp_string)

    def print(self):
        print(jsonpickle.encode(self.map, indent=4, keys=True))

    # Modifying Map Data Methods
    def add_room(self, new_room):
        if new_room.name in self.map.rooms:
            print(new_room.name + "already exists")
            return False
        else:
            self.map.rooms[new_room.name] = new_room
            print(new_room.name + " added to rooms")
            if self.map.current_room is None:
                self.map.current_room = new_room
                print(new_room.name + " set as current_room")
            new_room.map = self.map
            return True

    def set_starting_room(self, room):
        self.map.starting_room = room

    def change_name(self, room, name):
        log = ""
        old_name = room.name
        # does the room exist in this manager
        if old_name in self.map.rooms:
            #is there already an existing room with the new name
            if name in self.map.rooms:
                log += "The room: " + name + "has been overwritten"
            # change the name of the room
            room.name = name
            # add the room to the dictionary of rooms with a matching name as the key
            self.map.rooms[name] = room
            # remove the old key:value
            del self.map.rooms[old_name]

    def does_room_exist(self, new_name):
        if new_name in self.map.rooms:
            return True
        else:
            return False

    def travel(self, direction):
        return self.map.travel(direction)

    def generate_new_default_map(self):
        home = Room(name="Home")
        home.set_desc("This is the starting room.")
        self.add_room(home)
        self.set_starting_room(home)

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
        home.create_new_edge("Left", "Left Room")
        left_room.create_new_edge("Right", "Home")
        home.create_new_edge("Right", "Right Room")
        right_room.create_new_edge("Left", "Home")
        home.create_new_edge("Backward", "Living Room")
        living_room.create_new_edge("Forward", "Home")
        right_room.create_new_edge("Backward", "Kitchen")
        kitchen.create_new_edge("Forward", "Right Room")
        living_room.create_new_edge("Right", "Kitchen")
        kitchen.create_new_edge("Left", "Living room")


@dataclass()
class Room(object):
    name: str
    map: Map = None
    description: str = ""
    connected_rooms: dict = field(default_factory=dict)
    inventory: list = field(default_factory=list)

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
        if new_destination_name in self.map.rooms:
            if direction in self.connected_rooms:
                log += direction + ": " + self.connected_rooms[direction].name + " changed to " + \
                       direction + ": " + new_destination_name + "\n"
                self.connected_rooms[direction] = self.map.rooms[new_destination_name]
            else:
                log += "The Direction: '" + direction + "' does not exist in this room's connected_rooms dict\n" + \
                       "I am pretty sure this msg should never pop up tho."
        else:
            log += "The destination room: '" + new_destination_name + "' does not exist in this room manager\n"
        return log

    def create_new_edge(self, direction, destination_name):
        log = ""
        # In this case, it's basically just changing the destination
        if direction in self.connected_rooms:
            log += "'" + direction + ": " + self.connected_rooms[direction].name + "' changed to '" + direction + \
                   ": " + destination_name + "'\n"
            # change the value of this direction to the destination room
            self.connected_rooms[direction] = self.map.rooms[destination_name]
        else:
            if destination_name in self.map.rooms:
                self.connected_rooms[direction] = self.map.rooms[destination_name]
                log += "'" + direction + ": " + destination_name + "' has been added as a connected room"
            else:
                log += "The destination room: '" + destination_name + "' does not exist in this room manager\n"
        print("called: " + log)
        return log

