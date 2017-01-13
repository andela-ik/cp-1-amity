import random
from .room import Office, Lspace
from .person import Staff, Fellow

class Amity():
    def __init__(self):
        self.rooms = []
        self.people = []
        self.lspace_unallocated = []
        self.office_unallocated = []

    def add_person(self, name, role, wants_accomodation = 'N'):
        """ Create a Fellow or Staff and return Person instance

        Keyword arguments:
        name -- Name of person to be created
        role -- STAFF|FELLOW
        wants_accomodation -- Y|N Does the person require a living space(Fellows Only)
        """

        for person in self.people:
            if name.upper() == person.name:
                print(person.name + " ALREADY EXISTS")
                return
        if role.upper() == 'STAFF':
            if wants_accomodation == 'Y':
                print("Error, Staff cannot be allocated a living space")
                return "Error, Staff cannot be allocated a living space"
            office = self.select_random_room(Office)
            person = Staff(name, office )
            self.people.append(person)
            if office is not None:
                self.allocate_room(person, office)
            else:
                self.office_unallocated.append(person)

            print(person.name + " added successfully")

        elif role.upper() == 'FELLOW':
            lspace = None
            office = None
            if wants_accomodation == 'Y':
                lspace = self.select_random_room(Lspace)
            office = self.select_random_room(Office)
            person = Fellow(name, office, lspace)
            self.people.append(person)
            if office is not None:
                self.allocate_room(person, office)
            else:
                self.office_unallocated.append(person)

            if lspace is not None:
                self.allocate_room(person, lspace)
            elif wants_accomodation == 'Y' and lspace is None:
                self.lspace_unallocated.append(person)
            else:
                pass

            print(person.name + " added successfully")

        else:
            person = "Invalid role"

        return person


    def allocate_room(self, person, room):
        """ Allocates a person to a specific room"""
        if room is not None and room.check_availability():
            room.occupants.append(person.name.upper())
            room.number_of_occupants += 1



    def create_room(self, name, room_type):
        """ Create and Office or Lspace and return Room instance

        Keyword arguments:
        name -- name of the room to be created
        room_type -- OFFICE|LSPACE
        """
        for room in self.rooms:
            if room.name == name.upper():
                print(room.name + " ALREADY EXISTS")
                return
        room = None
        if room_type.upper() == 'OFFICE':
            room = Office(name)
            self.rooms.append(room)
            message = room.name+" office created successfully"
            self.on_room_update()

        elif room_type.upper() == 'LSPACE':
            room = Lspace(name)
            self.rooms.append(room)
            message = room.name+" lspace created successfully"
            self.on_room_update()

        else:
            message = "Invalid room type"
        print(message)
        return room

        
    #TODO: Implement Automated Waiting List
    def on_room_update(self):
        """ Track vacancies and auto allocate unallocated people"""
        return

    def print_allocations(self, file_name = False):
        """ Loop through rooms and print out persons allocated to each

        Keyword arguments:
        file_name -- if specified, write to file
        """
        return

    def print_unallocated(self, file_name = False):
        """ Loop through *_unallocated lists and print out persons in each

        Keyword arguments:
        file_name -- if specified, write to file
        """
        return

    def print_room(self, name):
        """ Print out specific room and persons allocated

        Keyword arguments:
        name -- name of the room to be printed
        """
        return

    def reallocate_person(self, name, room_name):
        """ Move person from current room to another

        Keyword arguments:
        name -- name of the peron to be moved
        room_name -- name of the destination room
        """
        return

    def save_state(self, db_name = "default"):
        """ Store all data in memory to database

        Keyword arguments:
        db_name -- if specified, save to specified database, else use default
        """
        return


    def search_person(self, person_name):
        """ Check if person exists in the system, return Person instance or False"""
        return




    def search_room(self, room_name):
        """ Check if room exists in the system, return Room instance or False"""
        return



    def select_random_room(self, room_type):
        """ Given a room type, selects a vacant room at random"""
        available_rooms = []
        selected_room = None
        for room in self.rooms:
            if type(room) == room_type:
                if(room.check_availability()):
                    available_rooms.append(room)
        number_available = len(available_rooms)
        if number_available > 0:
            selected_room = random.sample(available_rooms, 1)[0]
        else:
            #TODO:Implement waiting list
            print("There are no vacancies")
        return selected_room



    def load_state(self, db_name = "default"):
        """ Retreive data from database and load into memory

        Keyword arguments:
        db_name -- if specified, load from specified database, else use default
        """
        return



    def load_people(self, file_name):
        """ Read data from file and create people

        Keyword arguments:
        file_name -- file containing desired data
        """
        return
