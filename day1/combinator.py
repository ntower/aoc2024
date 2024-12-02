from draftsman.blueprintable import Blueprint
from draftsman.entity import ConstantCombinator
from draftsman.data import items
from draftsman.error import DuplicateIDError
from draftsman.utils import string_to_JSON, JSON_to_string
from typing import Literal

print(string_to_JSON('0eNqlkN0KgkAQhd9lrjcpU9N9lQhZbagBnZXdVRLZd2+si4igi7qbv3O+wyzQdCMOjjiAXoBayx70cQFPFzbdOmPTI2hYN8Fw2LS2b4hNsA6iAuIz3kDv4kkBcqBA+DR4NHPNY9+gkwP1zUjBYL1oLa9E8UvLfZIrmEEfklwwIgrOdnWDVzORKOTMY7sq/Hst6FemGKP6iJL+GqX4M4q8iAL2An49XcGEzj9oeZFWWVXlWZWWRbaN8Q4+0I2C'))

# Draftsman has not yet been updated for factorio 2.0. I need to add additional
# capabilities to combinators
class MyCombinator(ConstantCombinator):
    def set_signal(self, index, signal, count=0, quality: Literal["normal", "uncommon", "rare", "epic", "legendary"] = "normal", section_index=0):
        # type: (int, str, int, str, int) -> None
        if "sections" not in self.control_behavior:
            self.control_behavior["sections"] = { "sections": [] }

        # check to see if the section already exists
        found_section = None
        for (i, section) in enumerate(self.control_behavior["sections"]["sections"]):
            if section_index + 1 == section["index"]:
                if signal is None:
                    del self.control_behavior["sections"]["sections"][i]
                    return
                else:
                    found_section = section
                break

        # If there's no section, create it
        if found_section is None:
            found_section = {
                "index": section_index + 1,
                "filters": []
            }
            self.control_behavior["sections"]["sections"].append(found_section)
        
        # check to see if the filter already exists
        for (i, filter) in enumerate(found_section["filters"]):
            if index + 1 == filter["index"]:
                if signal is None:
                    del found_section["filters"][i]
                else:
                    found_section["filters"][i] = {
                        "index": index + 1,
                        "name": signal,
                        "quality": quality,
                        "comparator": "=",
                        "count": count,
                    }
                return
            
        # if no filter was found, create a new one
        found_section["filters"].append({
            "index": index + 1,
            "name": signal,
            "quality": quality,
            "comparator": "=",
            "count": count,
        })
    
    @property
    def sections(self):
        # type: () -> list
        return self.control_behavior.get("sections", [])

# Process the input file into two lists of numbers

left = []
right = []

for line in open('./day1/input.txt', 'r').read().splitlines():
    words = line.split('   ')
    left.append(int(words[0]))
    right.append(int(words[1]))

# Create a factorio blueprint with constant combinators that
# output the numbers in the two lists

blueprint = Blueprint()
blueprint.setup(version = 562949954928640) #2.0.23

left_combinator = None
right_combinator = None

COMBINATOR_SLOTS = 200000 # There is no longer a limit on the number of signals. Used to have to split into multiple combinators.
TOTAL_SIGNALS = len(left)
COMBINATOR_HEIGHT = 5
signals_added = 0
row_index = 0

def get_position(side: str, row: int):
    x = 0 if side=='left' else 2
    return (x, row)

def get_id(side: str, row: int):
    return "{}_{}".format(*get_position(side, row))
    

def place_combinator(combinator: MyCombinator, side:str):
    combinator.id = get_id(side, row_index)
    combinator.tile_position = get_position(side, row_index)
    blueprint.entities.append(combinator)


for item in open('./day1/items.txt', 'r').read().splitlines():
    if (signals_added >= TOTAL_SIGNALS):
        break

    for quality in ('normal', 'uncommon', 'rare', 'epic', 'legendary'):
        if (signals_added >= TOTAL_SIGNALS):
            break

        row_index = signals_added // COMBINATOR_SLOTS
        signal_index = signals_added % COMBINATOR_SLOTS
        if (signal_index == 0):
            #starting a new row of combinators
            if (left_combinator != None):
                place_combinator(left_combinator, 'left')
                place_combinator(right_combinator, 'right')

            left_combinator = MyCombinator()
            right_combinator = MyCombinator()

        left_combinator.set_signal(signal_index, item, left[signals_added], quality)
        right_combinator.set_signal(signal_index, item, right[signals_added], quality)

        signals_added += 1

if (signals_added < TOTAL_SIGNALS):
    # time to add more stuff to the items.txt file
    print(signals_added, TOTAL_SIGNALS)
    raise Exception("Not enough signals")

# if there's a partial combinator add it to the blueprint
if (left_combinator != None and len(left_combinator.sections) > 0):
    try:
        place_combinator(left_combinator, 'left')
        place_combinator(right_combinator, 'right')
    except DuplicateIDError:
        pass

# connect combinators with wires
for i in range(row_index):
    for color in ('red', 'green'):
        for side in ('left', 'right'):
            id = get_id(side, i)
            next_id = get_id(side, i+1)
            try:
                blueprint.add_circuit_connection(color, id, next_id)
            except KeyError:
                pass
   

print(blueprint.to_string())

