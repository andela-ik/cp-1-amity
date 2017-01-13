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
        return


    def create_room(self, name, room_type):
        """ Create and Office or Lspace and return Room instance

        Keyword arguments:
        name -- name of the room to be created
        room_type -- OFFICE|LSPACE
        """
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

    def search_person(self, person_name):
        """ Check if person exists in the system, return Person instance or False"""
        return




    def search_room(self, room_name):
        """ Check if room exists in the system, return Room instance or False"""
        return

    def save_state(self, db_name = "default"):
        """ Store all data in memory to database

        Keyword arguments:
        db_name -- if specified, save to specified database, else use default
        """
        return



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
