from draftsman.blueprintable import Blueprint
from draftsman.entity import ConstantCombinator
from draftsman.data import items
from draftsman.error import DuplicateIDError
from draftsman.utils import string_to_JSON
from typing import Literal

print(string_to_JSON('0eNrlUMtqwzAQ/Jc9K8VWEzsV9EtKCbKzJQvWriPJaYPxv3flhlB6a69FB4lhXpoZumHCMRJncDNQxgDuG2bggjGRMDi7r7ftk233W301lQHkTJkwgXuZgX1AVfbCKXvOm15CR+yzRPUYJSmzmMzwAa562Bm4rvdiiiRHGQ4dnvyFlK+khH3hf1kTH1FVtYE3GrLW+YHeot9Fjsib/oSp9D5PfqCsKcASgx+gJIXRx7WTg+cVmMq/m8o+Nou5e9q7J0X5k6Ntd1W7vOq5zXQ98BQ6VFpdgn6zlv3Pa1kFl09TBOAT'))
# print(string_to_JSON('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'))

# Draftsman has not yet been updated for factorio 2.0. I need to add additional
# capabilities to combinators, and omit items that don't exist any more
class MyCombinator(ConstantCombinator):
    def set_signal(self, index, signal, count=0, quality: Literal["normal", "uncommon", "rare", "epic", "legendary"] = "normal", section_index=0):
        # type: (int, str, int, str, int) -> None
        if "sections" not in self.control_behavior:
            print("creating sections")
            self.control_behavior["sections"] = []

        # check to see if the section already exists
        found_section = None
        for (i, section) in enumerate(self.control_behavior["sections"]):
            print('considering section', section)   
            if section_index + 1 == section["index"]:
                if signal is None:
                    del self.control_behavior["sections"][i]
                    return
                else:
                    found_section = section
                break

        # If there's no section, create it
        if found_section is None:
            print("creating section")
            found_section = {
                "index": section_index + 1,
                "filters": []
            }
            self.control_behavior["sections"].append(found_section)
        
        # check to see if the filter already exists
        for (i, filter) in enumerate(found_section["filters"]):
            if index + 1 == filter["index"]:
                if signal is None:
                    del found_section["filters"][i]
                else:
                    print('filter already exists, updating')
                    found_section["filters"][i] = {
                        "index": index + 1,
                        "name": signal,
                        "quality": quality,
                        "comparator": "=",
                        "count": count,
                    }
                    print(found_section["filters"][i])
                return
            
        # if no filter was found, create a new one
        print('creating filter') 
        found_section["filters"].append({
            "index": index + 1,
            "name": signal,
            "quality": quality,
            "comparator": "=",
            "count": count,
        })
        print(found_section)
    
    @property
    def sections(self):
        # type: () -> list
        return self.control_behavior.get("sections", [])
        
deprecated_items = set(('filter-inserter', 'stack-filter-inserter', 'satellite', 'rocket-control-unit'))

# Process the input file into two lists of numbers

f = open('./day1/input.txt', 'r')
lines = f.read().splitlines()

left = []
right = []

for line in lines:
    words = line.split('   ')
    left.append(int(words[0]))
    right.append(int(words[1]))

# Create a factorio blueprint with constant combinators that
# output the numbers in the two lists

blueprint = Blueprint()

left_combinator = None
right_combinator = None

combinator_slots = 20
signals_to_add = 2 # len(left)
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

for quality in ('normal', 'uncommon', 'rare', 'epic', 'legendary'):
    if (signals_added >= signals_to_add):
        break
    for item in items.raw:
        if (signals_added >= signals_to_add):
            break
        if (item in deprecated_items or ("flags" in items.raw[item] and "hidden" in items.raw[item]["flags"])):
            continue

        row_index = signals_added // combinator_slots
        signal_index = signals_added % combinator_slots
        if (signal_index == 0):
            #starting a new row of combinators
            if (left_combinator != None):
                print('placing combinators and starting a row')
                place_combinator(left_combinator, 'left')
                place_combinator(right_combinator, 'right')

            left_combinator = MyCombinator()
            right_combinator = MyCombinator()

        left_combinator.set_signal(signal_index, item, left[signals_added])
        right_combinator.set_signal(signal_index, item, right[signals_added])

        signals_added += 1

# if there's a partial combinator add it to the blueprint
if (left_combinator != None and len(left_combinator.sections) > 0):
    try:
        print('placing last combinators')
        place_combinator(left_combinator, 'left')
        place_combinator(left_combinator, 'right')
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

