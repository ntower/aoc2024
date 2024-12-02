from draftsman.blueprintable import Blueprint
from draftsman.entity import ConstantCombinator
from typing import Literal

# Draftsman has not yet been updated for factorio 2.0. I need to add additional
# capabilities to combinators
class MyConstantCombinator(ConstantCombinator):
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
    

# Returns a list of possible signals. It's not a full list of everything
# in the game, but it's a good starting point.
def list_signals():
    # type: () -> list[dict]
    items = open('./items.txt', 'r').read().splitlines()
    signals = []
    for item in items:
        for quality in ('normal', 'uncommon', 'rare', 'epic', 'legendary'):        
            signals.append({ "name": item, "quality": quality })
    return signals


# Process the input file into a list of lists

reports: list[list[int]] = []

for line in open('./day2/input.txt', 'r').read().splitlines():
    reports.append([int(item) for item in line.strip().split(' ')])

# Create a factorio blueprint with a series of constant combinators. 
# Combinator 1 contains the first value for all 1000 reports, then #2 contains
# the second value, etc. The number of values is variable, but never more than 8

blueprint = Blueprint()
blueprint.setup(version = 562949954928640) #2.0.23


combinators: list[MyConstantCombinator] = []
for i in range(8):
    combinator = MyConstantCombinator()
    combinator.id = "combinator_{}".format(i)
    combinator.tile_position = (i * 2, 0)
    combinators.append(combinator)

signals = list_signals()

for (report_index, report) in enumerate(reports):
    for (value_index, value) in enumerate(report):
        combinator = combinators[value_index]
        signal = signals[report_index]
        combinator.set_signal(report_index, signal["name"], value, signal["quality"])

for i in range(8):
    blueprint.entities.append(combinators[i])


        
print(blueprint.to_string())



# COMBINATOR_SLOTS = 200000 # There is no longer a limit on the number of signals. Used to have to split into multiple combinators.
# TOTAL_SIGNALS = len(left)
# signals_added = 0
# row_index = 0

# def get_position(side: str, row: int):
#     x = 0 if side=='left' else 2
#     return (x, row)

# def get_id(side: str, row: int):
#     return "{}_{}".format(*get_position(side, row))
    

# def place_combinator(combinator: MyCombinator, side:str):
#     combinator.id = get_id(side, row_index)
#     combinator.tile_position = get_position(side, row_index)
#     blueprint.entities.append(combinator)


# for item in open('./day1/items.txt', 'r').read().splitlines():
#     if (signals_added >= TOTAL_SIGNALS):
#         break

#     for quality in ('normal', 'uncommon', 'rare', 'epic', 'legendary'):
#         if (signals_added >= TOTAL_SIGNALS):
#             break

#         row_index = signals_added // COMBINATOR_SLOTS
#         signal_index = signals_added % COMBINATOR_SLOTS
#         if (signal_index == 0):
#             #starting a new row of combinators
#             if (left_combinator != None):
#                 place_combinator(left_combinator, 'left')
#                 place_combinator(right_combinator, 'right')

#             left_combinator = MyCombinator()
#             right_combinator = MyCombinator()

#         left_combinator.set_signal(signal_index, item, left[signals_added], quality)
#         right_combinator.set_signal(signal_index, item, right[signals_added], quality)

#         signals_added += 1

# if (signals_added < TOTAL_SIGNALS):
#     # time to add more stuff to the items.txt file
#     print(signals_added, TOTAL_SIGNALS)
#     raise Exception("Not enough signals")

# # if there's a partial combinator add it to the blueprint
# if (left_combinator != None and len(left_combinator.sections) > 0):
#     try:
#         place_combinator(left_combinator, 'left')
#         place_combinator(right_combinator, 'right')
#     except DuplicateIDError:
#         pass

# # connect combinators with wires
# for i in range(row_index):
#     for color in ('red', 'green'):
#         for side in ('left', 'right'):
#             id = get_id(side, i)
#             next_id = get_id(side, i+1)
#             try:
#                 blueprint.add_circuit_connection(color, id, next_id)
#             except KeyError:
#                 pass
   

# print(blueprint.to_string())

