from draftsman.blueprintable import Blueprint
from draftsman.entity import ConstantCombinator
from typing import Literal
import pyperclip as pc 
from draftsman.utils import string_to_JSON, JSON_to_string

# pc.copy(string_to_JSON('0eNqdkvFqgzAQxt/l/o6lWi1T2JOMUqLetoC5uHjaifjuu+jm6GArK4Lol/t+912SCcqmx9YbYigmMJWjDoqnCTrzQroJGmmLUEBYYU0cVc6WhjQ7D7MCQzW+QxHPJwVIbNjgClh+xjP1tkQvBeovkILWdeJ1FDoKL8kPu0zBKMZ4l0kfcbF3zbnEVz0YsUhdh1WwdNff0vsrlIJn0zD6nyqPbUgyGM+9DLlFq92FIu29u4j2JksygcjkvF3KJHGr/ZK4gMdF6MPGxbPa8Mnv+HVPo9rx/fjDTbzH+n58ehO/vx+ebaxQalFO5v+4kzxzuG0bYz3dz9gmDC+v6x6h3jBakb/vu4JBzMudy45JnuZ5lubJwzHdz/MH780GTQ=='))

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
    

# Returns a list of possible signals. It's not a full list of everything
# in the game, but it's a good starting point.
def list_signals():
    # type: () -> list[dict]
    raw = open('./day4/items.txt', 'r').read().splitlines()
    items= [(tuple(item.rsplit(" ", 1)) if " " in item else (item, "item")) for item in raw]
    signals = []
    for item in items:
    #     for quality in ('normal', 'uncommon', 'rare', 'epic', 'legendary'):        
        signals.append({ "name": item[0], "type": item[1], "quality": 'normal' })
    return signals

# Create a factorio blueprint with a series of constant combinators. 
# Combinator 1 contains the first value for all 1000 reports, then #2 contains
# the second value, etc. The number of values is variable, but never more than 8

blueprint = Blueprint()
blueprint.setup(version = 562949954928640) #2.0.23

combinator = MyConstantCombinator()

signals = list_signals()
signals_per_section = 1000

signals_added = 0
def section_index():
    return signals_added // signals_per_section
def item_index():
    return signals_added % signals_per_section

for signal in signals:
    for quality in ('normal', 'uncommon', 'rare', 'epic', 'legendary'):
        combinator.set_signal(item_index(), signal["name"], 1, quality, section_index(), signal["type"])
        signals_added += 1

blueprint.entities.append(combinator)

pc.copy(blueprint.to_string()) 