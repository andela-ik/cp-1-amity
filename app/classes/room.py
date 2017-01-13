class Room():
    def __init__(self, name, max_occupants):
        self.name = name.upper()
        self.max_occupants = max_occupants
        self.occupants = []
        self.number_of_occupants = 0

    def check_availability(self):
        """ Checks whether there are vacancies in the room"""
        if self.number_of_occupants == self.max_occupants:
            return False
        else:
            return True


class Office(Room):
    def __init__(self, name):
        super().__init__(name, 6)


class Lspace(Room):
    def __init__(self, name):
        super().__init__(name, 4)
