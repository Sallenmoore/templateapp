from models.systems.basesystem import BaseSystem


class FantasySystem(BaseSystem):
    _genre = "Fantasy"

    _currency = {
        "copper": "CP",
        "silver": "SP",
        "gold": "GP",
        "platinum": "PP",
    }

    _titles = {
        "city": "City",
        "creature": "Creature",
        "faction": "Faction",
        "region": "Region",
        "world": "World",
        "location": "Location",
        "poi": "POI",
        "item": "Item",
        "encounter": "Encounter",
        "character": "Character",
    }
