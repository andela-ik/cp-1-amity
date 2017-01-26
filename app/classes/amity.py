import random
from .room import Office, LivingSpace
from .person import Staff, Fellow
from app.models.database import Database
import os.path


class Amity():
    def __init__(self):
        self.rooms = []
        self.people = []
        self.living_space_unallocated = []
        self.office_unallocated = []
        self.db = None

    def add_person(self, name, role, wants_accomodation = 'N'):
        """ Create a Fellow or Staff and return Person instance

        Keyword arguments:
        name -- Name of person to be created
        role -- STAFF|FELLOW
        wants_accomodation -- Y|N Does the person require a living space(Fellow)
        """

        for person in self.people:
            if name.upper() == person.name:
                print(person.name + " ALREADY EXISTS")
                return
        if role.upper() == 'STAFF':
            if wants_accomodation == 'Y':
                print("Error, Staff cannot be allocated a living space")
            office = self.select_random_room(Office)
            person = Staff(name, office )
            self.people.append(person)
            if office:
                self.allocate_room(person, office)
            else:
                self.office_unallocated.append(person)

            print(person.name + " added successfully")

        elif role.upper() == 'FELLOW':
            living_space = None
            office = None
            if wants_accomodation == 'Y':
                living_space = self.select_random_room(LivingSpace)
            office = self.select_random_room(Office)
            person = Fellow(name, office, living_space)
            self.people.append(person)
            if office:
                self.allocate_room(person, office)
            else:
                self.office_unallocated.append(person)

            if living_space:
                self.allocate_room(person, living_space)
            elif wants_accomodation == 'Y' and not living_space:
                self.living_space_unallocated.append(person)

            print(person.name + " added successfully")

        else:
            print("Invalid Role")
            person = "Invalid role"

        return person


    def allocate_room(self, person, room):
        """ Allocates a person to a specific room"""
        if room and room.check_availability():
            room.occupants.append(person.name.upper())
            room.number_of_occupants += 1
            print('{name} has been allocated to {room}'.format(
                                    name = person.name.upper(),
                                    room = room.name.upper()))



    def create_room(self, name, room_type):
        """ Create an Office or LivingSpace and return Room instance

        Keyword arguments:
        name -- name of the room to be created
        room_type -- OFFICE|LSPACE
        """
        if room_type.upper() not in ['LSPACE','OFFICE']:
                print("Invalid room type")
                return

        for room in self.rooms:
            if room.name == name.upper():
                print(room.name + " ALREADY EXISTS")
                return
        room = None
        if room_type.upper() == 'OFFICE':
            room = Office(name)
            self.rooms.append(room)
            message = room.name+" office created successfully"

        elif room_type.upper() == 'LSPACE':
            room = LivingSpace(name)
            self.rooms.append(room)
            message = room.name+" living space created successfully"


        print(message)
        if room:
            self.on_room_update(room)
        return room


    def deallocate_room(self, person, room):
        """ Removes a person from a specific room"""
        if room:
            room.occupants.remove(person.name.upper())
            room.number_of_occupants -= 1

    def on_room_update(self, room):
        """ Track vacancies and auto allocate unallocated people"""
        allocated = []
        if type(room) == LivingSpace:
            for i,person in enumerate(self.living_space_unallocated):
                if room.check_availability():
                    self.allocate_room(person, room)
                    person.living_space_allocated = room
                    allocated.append(person)
                else:
                    break
            for person in allocated:
                if person in self.living_space_unallocated:
                    self.living_space_unallocated.remove(person)



        elif type(room) == Office:
            for i,person in enumerate(self.office_unallocated):
                if room.check_availability():
                    self.allocate_room(person, room)
                    person.office_allocated = room
                    allocated.append(person)

                else:
                    break
            for person in allocated:
                if person in self.office_unallocated:
                    self.office_unallocated.remove(person)
                    

    def print_allocations(self, file_name = False):
        """ Loop through rooms and print out persons allocated to each

        Keyword arguments:
        file_name -- if specified, write to file
        """

        if not file_name:
            for room in self.rooms:
                print("\n")
                print(room.name)
                print ("-------------------------------------")
                print(', '.join(str(name) for name in room.occupants))
                print("\n")
        else:
            file_name = file_name + " allocations.txt"
            file = open(file_name, 'w')
            for room in self.rooms:
                file.write(room.name + "\n")
                file.write("-------------------------------------\n")
                file.write(', '.join(str(name) for name in room.occupants))
                file.write("\n\n")
            file.closed
            print("Data has been saved to {0}".format(file_name))


    def print_unallocated(self, file_name = False):
        """ Loop through *_unallocated lists and print out persons in each

        Keyword arguments:
        file_name -- if specified, write to file
        """

        if not file_name:
            print("\nOFFICE UNALLOCATED")
            print ("-------------------------------------")
            print(', '.join(str(person.name) for person in self.office_unallocated))
            print("\n")

            print("\nLIVING SPACE UNALLOCATED")
            print ("-------------------------------------")
            print(', '.join(str(person.name) for person in self.living_space_unallocated))
            print("\n")

        else:
            file_name = file_name + " unallocated.txt"
            file = open(file_name, 'w')
            file.write("OFFICE UNALLOCATED\n")
            file.write ("-------------------------------------\n")
            file.write(', '.join(str(person.name) for person in self.office_unallocated))
            file.write("\n")

            file.write("\nLIVING SPACE UNALLOCATED\n")
            file.write ("-------------------------------------\n")
            file.write(', '.join(str(person.name) for person in self.living_space_unallocated))
            file.write("\n")
            print("Data has been saved to {0}".format(file_name))


    def print_room(self, name):
        """ Print out specific room and persons allocated

        Keyword arguments:
        name -- name of the room to be printed
        """
        room = self.search_room(name)
        if room:
            print("\n")
            print(room.name)
            print ("-------------------------------------")
            print(', '.join(str(name) for name in room.occupants))
            print("\n")

        else:
            print("\n" + name.upper() + " not found")

    def reallocate_person(self, name, room_name):
        """ Move person from current room to another

        Keyword arguments:
        name -- name of the peron to be moved
        room_name -- name of the destination room
        """
        new_room = self.search_room(room_name)
        if not new_room:
            print("Room Does Not Exist")
        elif new_room.check_availability() == False:
            print("The room is full")
        else:
            person = self.search_person(name)
            if (person):
                if type(new_room) == Office:
                    self.deallocate_room(person, person.office_allocated)
                    person.office_allocated = new_room
                    self.allocate_room(person, new_room)
                elif type(new_room) == LivingSpace:
                    if type(person) == Fellow:
                        self.deallocate_room(person, person.living_space_allocated)
                        person.living_space_allocated = new_room
                        self.allocate_room(person, new_room)
                    else:
                        print("Staff Cannot be alocated an LSPACE")


    def save_state(self, db_name = "default"):
        """ Store all data in memory to database

        Keyword arguments:
        db_name -- if specified, save to specified database, else use default
        """
        print("PLEASE WAIT")
        self.db = Database(db_name)
        self.save_rooms()
        self.save_people()
        print("\nSESSION SAVED")


    def save_people(self):
        for person in self.people:
            living_space = None
            office = None
            if type(person) == Staff:
                role = "STAFF"
            else:
                role = "FELLOW"
                if person.living_space_allocated:
                    living_space = person.living_space_allocated.name
                elif person in self.living_space_unallocated:
                    living_space = "PENDING"
            if person.office_allocated:
                office = person.office_allocated.name
            else:
                office = "PENDING"
            self.db.save_person(person.name, role, office, living_space)
            print(".", end = "")


    def save_rooms(self):
        for room in self.rooms:
            if type(room) == Office:
                room_type = "OFFICE"
            else:
                room_type = "LSPACE"
            self.db.save_room(room.name,
                            room.max_occupants,
                            room.number_of_occupants,
                            room_type,
                            ','.join(str(name) for name in room.occupants)
                            )
            print(".", end = "")


    def search_person(self, person_name):
        """ Check if person exists in the system, return Person instance or False"""
        for person in self.people:
            if person.name == person_name.upper():
                return person
        return False


    def search_room(self, room_name):
        """ Check if room exists in the system, return Room instance or False"""
        if not room_name:
            return None
        elif room_name == "PENDING":
            return "PENDING"
        else:
            for room in self.rooms:
                if (room.name).upper() == room_name.upper():
                        return room
            return False



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
            if room_type == Office:
                room = "Offices"
            elif room_type == LivingSpace:
                room = "Lspaces"
            print("There are no vacant "+ room + " at the moment")
        return selected_room



    def load_state(self, db_name = "default"):
        """ Retreive data from database and load into memory

        Keyword arguments:
        db_name -- if specified, load from specified database, else use default
        """
        self.__init__()
        if (os.path.isfile(db_name+".db")):
            self.db = Database(db_name)
            self.load_rooms()
            self.load_persons()
            print ("LOADED SUCCESSFULLY")
        else:
            print("DATABASE NOT FOUND")

    def load_persons(self):
        for person in self.db.get_people():
            office = self.search_room(person.office)
            if person.role == "STAFF":
                staff = Staff(person.name, office)
                if office == "PENDING":
                    staff.office_allocated = None
                    self.office_unallocated.append(staff)
                self.people.append(staff)
            elif person.role == "FELLOW":
                living_space = self.search_room(person.living_space)
                fellow = Fellow(person.name, office, living_space)
                if living_space == "PENDING":
                    fellow.living_space_allocated = None
                    self.living_space_unallocated.append(fellow)
                if office == "PENDING":
                    fellow.office = None
                    self.office_unallocated.append(fellow)
                self.people.append(fellow)
            else:
                print("Error: Check Database")

    def load_rooms(self):
        for room in self.db.get_rooms():
            if room.room_type == "OFFICE":
                office = Office(room.name)
                office.occupants = room.occupants.split(',')
                office.number_of_occupants = int(room.no_of_occupants)
                self.rooms.append(office)
            elif room.room_type == "LSPACE":
                living_space = LivingSpace(room.name)
                living_space.occupants = room.occupants.split(',')
                living_space.number_of_occupants = int(room.no_of_occupants)
                self.rooms.append(living_space)
            else:
                print("Error: Check Database")



    def load_people(self, file_name):
        """ Read data from file and create people

        Keyword arguments:
        file_name -- file containing desired data
        """
        file_name = file_name + ".txt"
        if (not os.path.isfile(file_name)):
            print("FILE DOES NOT EXIST")

        else:
            f = open(file_name, 'r')
            index = None
            for line in f:
                line = line.replace('\n', '')
                data = line.split(" ")
                for item in data:
                    if item ==  "STAFF" or item == "FELLOW":
                        index = data.index(item)
                        name = " ".join(data[:index])
                        role = data[index]
                        wants_accomodation = data[-1]
                        self.add_person(name, role, wants_accomodation)
                        break
                if index is None:
                    print("INCORRECT INPUT FORMAT")
