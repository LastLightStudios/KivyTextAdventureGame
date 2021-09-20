from dataclasses import dataclass, field
import json
from Commands import DirectDialogueCommand, EnterCurrentRoomCommand


@dataclass
class Story(object):
    full_dict: dict = field(default_factory=dict)
    # this is a dict of all the stitches
    stitches: dict = field(default_factory=dict)
    # a stitch is a dictionary that contains "content":list of dicts
    current_stitch_name: str = ""
    # this is the log that gets added to when there is a direct story divert
    current_story_log: str = ""
    # this will be the command list
    # the key will be the button text (which is option in the content list/dict)
    # debating on if teh command will not show if something isnt available
    # or make a greyed out command
    # or what...probably gonna make a dummy command for now, that just says cond
    # b/c i think i want an opt to show even if its blocked
    # eventually will have tooltips and what not, so it can be a "empty" command
    # that just has a tooltip display
    current_story_options: dict = field(default_factory=dict)

    def get_story_log(self):
        return self.current_story_log

    def get_story_commands(self):
        return self.current_story_options

    def find_chain(self, stitch):
        for list_ele in stitch["content"]:
            if type(list_ele) is str:
                self.current_story_log += list_ele

    def find_next_stitch(self, stitch):
        for list_ele in stitch["content"]:
            if type(list_ele) is dict:
                if "divert" in list_ele:
                    return self.stitches[list_ele["divert"]]

    def find_options(self, stitch) -> dict:
        for list_ele in stitch["content"]:
            if type(list_ele) is dict:
                if "option" in list_ele:
                    # set the key:value pair as the option string:linkPath string
                    self.current_story_options[list_ele["option"]] = DirectDialogueCommand(self, list_ele["linkPath"])

    # this accepts the actual stitch
    def building_node(self, stitch):
        self.find_chain(stitch)
        self.current_story_options = self.find_options(stitch)
        if self.find_next_stitch(stitch):
            self.building_node(self.find_next_stitch(stitch))

    # link_path is just a string that corresponds to the stitch
    def build_node(self, link_path, client_call_back):
        self.current_story_options["Back"] = DirectDialogueCommand(self, self.current_stitch_name)
        self.building_node(self.stitches[link_path])
        client_call_back(self)

    def initialize_story(self):
        self.stitches = self.full_dict["data"]["stitches"]
        self.current_stitch_name = self.full_dict["data"]["initial"]
        self.current_story_options = {"Back": EnterCurrentRoomCommand()}
        self.building_node(self.stitches[self.current_stitch_name])

# DialogueManager singleton definition


# total story info
story = Story()  # the full dictionary


# 4 methods
# find chain -> just the dialogue info
# find option -> this will create my commands, it looks for option
# find next stitch -> finds divert and returns the found stitch
# build node -> this will call the first two
# it will recursively call itself if the 3rd method returns a stitch

def load_story(file_path):
    global story
    with open(file_path, "r") as load_file:
        frozen = load_file.read()
        story.full_dict = json.loads(frozen)
    story.initialize_story()
