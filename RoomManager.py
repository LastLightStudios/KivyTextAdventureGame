from __future__ import annotations
from dataclasses import dataclass, field
import jsonpickle
import GameState

from Commands import InteractCommand, TravelCommand


@dataclass
class RoomMap(object):
    name: str = ""
    current_room: Room = None
    starting_room: Room = None

    def __init__(self):
        self.rooms = {}

    def enter_current_room(self, client_call_back):
        client_call_back ({"Commands": self.current_room.get_room_command_dict(),
                            "Log": self.current_room.get_room_desc()})

    def travel(self, direction, client_call_back):
        print("Traveling from: " + self.current_room.name)
        if direction in self.current_room.connected_rooms:
            self.current_room = self.current_room.connected_rooms[direction]
            print("Entering: " + self.current_room.name)
            client_call_back({"Commands": self.current_room.get_room_command_dict(),
                             "Log": self.current_room.get_room_desc()})
            return True
        else:
            print("cannot travel in this direction")
            return False


# RoomManager singleton definition
@dataclass()
class RoomManager:
    room_map: RoomMap = RoomMap()


    # Read/Write Map Methods
    def create_new_map(self):
        self.room_map = RoomMap()
        generate_default_map()


    def load(self, file_path):
        with open(file_path, "r") as load_file:
            frozen = load_file.read()
            map_obj = jsonpickle.decode(frozen)
            self.room_map = map_obj


    def save(self, file_path):
        temp_string = jsonpickle.encode(room_map, indent=4, keys=True)
        with open(file_path, "w") as save_file:
            self.save_file.write(temp_string)


    def print_map(self):
        print(jsonpickle.encode(self.room_map, indent=4, keys=True))


    # Modifying Map Data Methods
    def add_room(self, new_room):
        if new_room.name in self.room_map.rooms:
            print(new_room.name + "already exists")
            return False
        else:
            room_map.rooms[new_room.name] = new_room
            print(new_room.name + " added to rooms")
            if self.room_map.current_room is None:
                self.room_map.current_room = new_room
                print(new_room.name + " set as current_room")
            new_room.room_map = self.room_map
            return True


    def set_starting_room(self, room):
        self.room_map.starting_room = room


    def change_name(self, room, name):
        log = ""
        old_name = room.name
        # does the room exist in this manager
        if old_name in self.room_map.rooms:
            # is there already an existing room with the new name
            if name in self.room_map.rooms:
                log += "The room: " + name + "has been overwritten"
            # change the name of the room
            room.name = name
            # add the room to the dictionary of rooms with a matching name as the key
            self.room_map.rooms[name] = room
            # remove the old key:value
            del self.room_map.rooms[old_name]


    def does_room_exist(self, new_name):
        if new_name in self.room_map.rooms:
            return True
        else:
            return False


    def travel(self, direction):
        return self.room_map.travel(direction)


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
        kitchen.create_new_edge("Left", "Living Room")


@dataclass()
class Room(object):
    name: str
    owner: RoomMap = None
    description: str = ""
    connected_rooms: dict = field(default_factory=dict)
    inventory: list = field(default_factory=list)
    characters: list = field(default_factory=list)

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
            # log += old_direction + " does not exist in this room's connected_rooms dict"
            log = "something fucked up, somehow we are trying to edit a direction that doesnt exist \n"
        return log

    def set_destination_room(self, direction, new_destination_name):
        log = ""
        if new_destination_name in self.owner.rooms:
            if direction in self.connected_rooms:
                log += direction + ": " + self.connected_rooms[direction].name + " changed to " + \
                       direction + ": " + new_destination_name + "\n"
                self.connected_rooms[direction] = self.owner.rooms[new_destination_name]
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
            self.connected_rooms[direction] = self.owner.rooms[destination_name]
        else:
            if destination_name in self.owner.rooms:
                self.connected_rooms[direction] = self.owner.rooms[destination_name]
                log += "'" + direction + ": " + destination_name + "' has been added as a connected room"
            else:
                log += "The destination room: '" + destination_name + "' does not exist in this room manager\n"
        print("called: " + log)
        return log

    def get_room_desc(self):
        return self.description

    def get_room_command_dict(self):
        command_dict = {}
        for key in self.connected_rooms:
            command_dict[key] = TravelCommand(self.owner, key)
        for name in self.characters:
            command_dict[name] = InteractCommand(GameState, GameState.character_manager.character_dict[name])
        return command_dict
