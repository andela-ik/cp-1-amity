class Person():
    def __init__(self, name, office):
        self.name = name.upper()
        self.office_allocated = office

class Staff(Person):
    def __init__(self, name, office):
        super().__init__(name, office)

class Fellow(Person):
    def __init__(self, name, office, lspace):
        super().__init__(name, office)
        self.lspace_allocated = lspace
