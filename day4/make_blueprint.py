from draftsman.blueprintable import Blueprint
from draftsman.entity import ConstantCombinator
from typing import Literal

# Draftsman has not yet been updated for factorio 2.0. I need to add additional
# capabilities to combinators
class MyConstantCombinator(ConstantCombinator):
    def set_signal(self, index, signal, count=0, quality: Literal["normal", "uncommon", "rare", "epic", "legendary"] = "normal", section_index=0, type="item"):
        # type: (int, str, int, str, int, str) -> None
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
                        "type": type
                    }
                return
            
        # if no filter was found, create a new one
        found_section["filters"].append({
            "index": index + 1,
            "name": signal,
            "quality": quality,
            "comparator": "=",
            "count": count,
            "type": type
        })
    
    @property
    def sections(self):
        # type: () -> list
        return self.control_behavior.get("sections", [])

# Dont use these signals in the combinator, because they are used eleswhere and
# might conflict
banned_signals = ["signal-dot", "signal-N", "signal-info"]

blueprint = Blueprint()
blueprint.setup(version = 562949954928640) #2.0.23

# describes the order of the signals
orderCombinator = MyConstantCombinator()
# contains the data from the problem
dataCombinator = MyConstantCombinator()

signals_per_section = 1000

signals_added = 0
def section_index():
    return signals_added // signals_per_section
def item_index():
    return signals_added % signals_per_section

characters = open('./day4/input.txt', 'r').read().replace("\n", "")


def pairwise(iterable):
    it = iter(iterable)
    return zip(it, it)

def signal_generator():
    items = open('./day4/items.txt', 'r').read().splitlines()
    for item in items:
        for quality in ('normal', 'uncommon', 'rare', 'epic', 'legendary'):
            if (" " in item):
                (name, type) = item.rsplit(" ", 1)
            else:
                name = item
                type = None
            if (quality == 'normal' and name in banned_signals):
                continue

            yield (name, type, quality)

generator = signal_generator()

def char_to_value(char):
    # turning the characters XMAS into small numbers, so i can then put two
    # of them in a single integer to represent multiple input values. This is
    # needed because i don't have enough signals to fit all the caracters as
    # individual signals.
    if char == 'X':
        return 1
    elif char == 'M':
        return 2
    elif char == 'A':
        return 3
    elif char == 'S':
        return 4
    else:
        raise ValueError("Invalid character")

for (data_index, pair) in enumerate(pairwise(characters)):
    try:
        (name, type, quality) = next(generator)
    except StopIteration:
        print ("Ran out of signals")
        raise StopIteration
    
    (first, second) = pair
    value = char_to_value(first) + char_to_value(second) * 5
    
    orderCombinator.set_signal(item_index(), name, data_index, quality, section_index(), type)
    dataCombinator.set_signal(item_index(), name, 1, quality, section_index(), type)
    signals_added += 1

orderCombinator.tile_position = (0, 0)
dataCombinator.tile_position = (2, 0)

blueprint.entities.append(orderCombinator)
blueprint.entities.append(dataCombinator)

print(blueprint.to_string())