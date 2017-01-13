import unittest
from app.classes.amity import Amity
from app.classes.room import Room, Office, Lspace
from app.classes.person import Person, Staff, Fellow

class AmityTest(unittest.TestCase):
    """ AMITY TESTS"""
    def setUp(self):
        self.amity = Amity()
        #Staff
        self.staff1 = self.amity.add_person("staff1","Staff")
        self.staff2 = self.amity.add_person("staff2","Staff", "N")
        #Fellows
        self.fellow1 = self.amity.add_person("fellow1","Fellow","N")
        self.fellow2 = self.amity.add_person("fellow2","Fellow","Y")
        self.fellow3 = self.amity.add_person("fellow1","Fellow","Y")
        #Living spaces
        self.lspace1 = self.amity.create_room("lspace1", "lspace")
        self.lspace2 = self.amity.create_room("lspace2", "lspace")
        self.lspace3 = self.amity.create_room("lspace3", "lspace")
        #Offices
        self.office1 = self.amity.create_room("office1", "office")
        self.office2 = self.amity.create_room("office2", "office")
        self.office3 = self.amity.create_room("office3", "office")
        #Load People File Prep
        output = "{}\n{}\n{}\n{}\n{}\n{}\n{}".format(
                    "OLUWAFEMI SULE FELLOW Y",
                    "DOMINIC WALTERS STAFF",
                    "SIMON PATTERSON FELLOW Y",
                    "MARI LAWRENCE FELLOW Y",
                    "LEIGH RILEY STAFF",
                    "TANA LOPEZ FELLOW Y",
                    "KELLY McGUIRE STAFF"
                    )
        f = open("test.txt", "w")
        f.write(output)
        f.close()


    def test_add_person(self):
        "ADD PERSON"
        self.assertIsInstance(self.staff1, Staff)
        self.assertIsInstance(self.amity.add_person("Ian KS","Staff", "N"), Staff)


        "TESTS FOR NEW FELLOW"
        self.assertIsInstance(self.amity.add_person("Ian K1","Fellow","N"), Fellow)
        self.assertIsInstance(self.amity.add_person("Ian K2","Fellow","Y"), Fellow)
        self.assertIsInstance(self.amity.add_person("Ian K3","Fellow"), Fellow)

        "TEST INVALID INPUT"
        self.assertEqual(self.amity.add_person("Ian KI", "Intern", "Y" ), "Invalid role")
        self.assertEqual(self.amity.add_person("Ian KS1","Staff","Y"), \
                "Error, Staff cannot be allocated a living space")

    def test_create_room(self):
        "CREATE NEW ROOM"

        "CREATE NEW LSPACE"
        self.assertIsInstance(self.lspace1, Lspace )
        self.assertEqual(self.lspace1.name, "LSPACE1")

        "CREATE NEW OFFICE"
        self.assertIsInstance(self.office1, Office )
        self.assertEqual(self.office1.name, "OFFICE1")

        "INVALID INPUT"
        self.assertEqual(self.amity.create_room("test_invalid", "live-in"),  None)

    def test_search_room(self):
        "TEST ROOM SEARCH"
        self.assertIsInstance(self.amity.search_room("lspace1"), Lspace)

        "TEST NON EXISTENT ROOM"
        self.assertFalse(self.amity.search_room("notthere"))

    def test_search_room(self):
        "STAFF SEARCH TEST"
        self.assertIsInstance(self.amity.search_person("STAFF1"), Staff)

        "TEST FELLOW SEARCH"
        self.assertIsInstance(self.amity.search_person("FELLOW1"), Fellow)


        "TEST NON EXISTENT PERSON"
        self.assertFalse(self.amity.search_person("NOONE"))

    def test_reallocate_person(self):
        "REALLOCATION TEST"

        "FELLOW LSPACE REALLOCATION"
        self.amity.reallocate_person("fellow1", "lspace3")
        self.assertEqual(self.fellow1.lspace_allocated.name, "LSPACE3")
        self.assertTrue("FELLOW1" in self.lspace3.occupants)

        self.amity.reallocate_person("fellow1", "lspace2")
        self.assertEqual(self.fellow1.lspace_allocated.name, "LSPACE2")
        self.assertTrue("FELLOW1" in self.lspace2.occupants)
        self.assertFalse("FELLOW1" in self.lspace3.occupants)

        "TEST STAFF OFFICE REALLOCATION"
        self.amity.reallocate_person("staff1", "office1")
        self.assertEqual(self.staff1.office_allocated.name, "OFFICE1")
        self.assertTrue("STAFF1" in self.office1.occupants)

        self.amity.reallocate_person("staff1", "office2")
        self.assertEqual(self.staff1.office_allocated.name, "OFFICE2")
        self.assertTrue("STAFF1" in self.office2.occupants)
        self.assertFalse("STAFF1" in self.office1.occupants)

        "TEST STAFF LSPACE REALLOCATION"
        self.assertEqual(self.amity.reallocate_person("staff1", "lspace1"),\
                None, msg="Staff Cannot be allocated a living space")

        "TEST NONE EXISTENT ROOM REALLOCATION"
        self.assertEqual(self.amity.reallocate_person("staff1", ""),\
                None, msg = "You cannot be reallocated to a non existent room")
        self.assertEqual(self.amity.reallocate_person("fellow1", "lspace7"), \
                None, msg = "You cannot be reallocated to a non existent room")

    def test_save_state(self):
        "SAVE STATE TEST"
        "CAPTURE ALL INSTANCE VARIABLES"
        rooms = self.amity.rooms
        people = self.amity.people
        lspace_unallocated = self.amity.lspace_unallocated
        office_unallocated = self.amity.office_unallocated

        "SAVE STATE TO TEST DB"
        self.amity.save_state("test")

        "LOAD STATE FROM TEST DB INTO NEW AMITY INSTANCE"
        amity2 = Amity()
        amity2.load_state("test")

        old_state = [rooms, people, lspace_unallocated, office_unallocated]
        new_state = [amity2.rooms, amity2.people, amity2.lspace_unallocated, amity2.office_unallocated]

        "COMPARE NEW AND OLD INSTANCE"
        self.assertEqual(old_state, new_state)

    def test_load_people(self):
        "LOAD PEOPLE TEST"

        "ASSERT PERSON DOESN'T EXIST BEFORE LAOD"
        self.assertFalse(self.amity.search_person("OLUWAFEMI SULE"))
        self.assertFalse(self.amity.search_person("DOMINIC WALTERS"))
        self.assertFalse(self.amity.search_person("SIMON PATTERSON"))

        "LOAD PEOPLE FROM TEXT FILE"
        self.amity.load_people("test.txt")

        "ASSERT PERSON EXISTS AFTER LOAD"
        self.assertTrue(self.amity.search_person("OLUWAFEMI SULE"))
        self.assertTrue(self.amity.search_person("DOMINIC WALTERS"))
        self.assertTrue(self.amity.search_person("SIMON PATTERSON"))




    def test_print_allocations(self):
        "PRINT ALLOCATIONS"
        pass

    def test_print_unallocated(self):
        "PRINT UNALLOCATED"
        pass

    def test_print_room(self):
        "PRINT ROOM"
        pass



if __name__ == '__main__':
    unittest.main()
