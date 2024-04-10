from models.systems.basesystem import BaseSystem


class HistoricalSystem(BaseSystem):
    _genre = "Historical"

    _currency = {
        "dollars": "$",
        "cents": "p",
    }

    _titles = {
        "city": "City",
        "creature": "Rival",
        "faction": "Faction",
        "region": "Region",
        "world": "Country",
        "location": "Location",
        "poi": "POI",
        "item": "Item",
        "encounter": "Encounter",
        "character": "Character",
    }
