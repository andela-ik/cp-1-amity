class Room():
    def __init__(self, name, max_occupants):
        self.name = name.upper()
        self.max_occupants = max_occupants
        self.occupants = []
        self.number_of_occupants = 0

    def check_availability(self):
        """ Checks whether there are vacancies in the room"""
        return self.number_of_occupants != self.max_occupants


class Office(Room):
    def __init__(self, name):
        super().__init__(name, 6)


class LivingSpace(Room):
    def __init__(self, name):
        super().__init__(name, 4)
