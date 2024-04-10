from models.systems.basesystem import BaseSystem


class HorrorSystem(BaseSystem):
    _genre = "Horror"

    _currency = {
        "dollars": "$",
        "cents": "p",
    }

    _titles = {
        "city": "Building",
        "creature": "Creature",
        "faction": "Faction",
        "region": "Town",
        "world": "Area",
        "location": "Room",
        "poi": "POI",
        "item": "Item",
        "encounter": "Encounter",
        "character": "Character",
    }

