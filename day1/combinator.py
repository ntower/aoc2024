from draftsman.blueprintable import Blueprint
from draftsman.entity import ConstantCombinator
from draftsman.data import items
from itertools import islice

# Process the input file into two lists of numbers

f = open('./day1/input.txt', 'r')
lines = f.read().splitlines()

left = []
right = []

for line in lines:
    words = line.split('   ')
    left.append(int(words[0]))
    right.append(int(words[1]))

left.sort()
right.sort()

# Create a factorio blueprint with constant combinators that
# output the numbers in the two lists

blueprint = Blueprint()

left_combinator = None
right_combinator = None

combinator_slots = 20
signals_added = 0

for item in items.raw:
    if (signals_added >= 21):
        break
    if ("flags" in items.raw[item] and "hidden" in items.raw[item]["flags"]):
        continue

    print(item)

    row_index = signals_added // combinator_slots
    signal_index = signals_added % combinator_slots

    if (signal_index == 0):
        #starting a new row of combinators
        if (left_combinator != None):
            blueprint.entities.append(left_combinator)
        if (right_combinator != None):
            blueprint.entities.append(right_combinator)
        left_combinator = ConstantCombinator()
        left_combinator.tile_position = (0, row_index)
        right_combinator = ConstantCombinator()
        right_combinator.tile_position = (2, row_index)

    left_combinator.set_signal(signal_index, item, left[signals_added])
    right_combinator.set_signal(signal_index, item, right[signals_added])
    signals_added += 1

# if there's a partial combinator add it to the blueprint
if (left_combinator != None and len(left_combinator.signals) > 0):
    blueprint.entities.append(left_combinator)
if (right_combinator != None and len(right_combinator.signals) > 0):
    blueprint.entities.append(right_combinator)
   

print(blueprint.to_string())

