from models.location import Location


class POI(Location):
    attributes = Location.attributes | {
        "district": "",
    }

    @property
    def state_data(self):
        obj_data = super().state_data
        obj_data["attributes"]["district"] = self.district
        return obj_data
