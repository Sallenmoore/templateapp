from models.systems.basesystem import BaseSystem


class HardboiledSystem(BaseSystem):
    _genre = "Hardboiled Detective"

    _currency = {
        "dollars": "$",
        "cents": "p",
    }

    _titles = {
        "city": "Street",
        "creature": "Criminal",
        "faction": "Gang",
        "region": "District",
        "world": "City",
        "location": "Location",
        "poi": "POI",
        "item": "Item",
        "encounter": "Encounter",
        "character": "Character",
    }
