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
    raw = open('./day2/items.txt', 'r').read().splitlines()
    items= [(tuple(item.rsplit(" ", 1)) if " " in item else (item, None)) for item in raw]
    signals = []
    for item in items:
        for quality in ('normal', 'uncommon', 'rare', 'epic', 'legendary'):        
            signals.append({ "name": item[0], "type": item[1], "quality": quality })
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