import unittest
from app.classes.amity import Amity
from app.classes.room import Office, LivingSpace
from app.classes.person import Staff, Fellow

class AmityTest(unittest.TestCase):
    """ AMITY TESTS"""
    def setUp(self):
        self.amity = Amity()

        self.lspace1 = self.amity.create_room("lspace1", "lspace")
        self.office1 = self.amity.create_room("office1", "office")

        self.staff1 = self.amity.add_person("staff1","Staff")
        self.fellow1 = self.amity.add_person("fellow1","Fellow", "Y")

    def tearDown(self):
        """ Clear all variables created"""
        del self.amity
        del self.lspace1
        del self.office1
        del self.staff1
        del self.fellow1

    def test_add_staff(self):
        """ TESTS FOR NEW STAFF"""
        self.assertIsInstance(self.amity.add_person("Ian KS","Staff", "N"), Staff)
        self.assertIsInstance(self.amity.add_person("Ian KS2","Staff", "Y"), Staff)

    def test_add_fellow(self):

        """ TESTS FOR NEW FELLOW"""
        self.assertIsInstance(self.amity.add_person("Ian K3","Fellow"),
                                Fellow)
        self.assertEqual(self.amity.add_person("Ian K1","Fellow","N").living_space_allocated,
                                None)
        self.assertIsInstance(self.amity.add_person("Ian K2","Fellow","Y").
                                living_space_allocated, LivingSpace)

    def test_add_person_invalid_input(self):
        """ TEST INVALID ROLE"""
        self.assertEqual(self.amity.add_person("Ian KI", "Intern", "Y" ),
                                "Invalid role")

        """ TEST ATTEMPT TO RECREATE PERSON"""
        self.assertEqual(self.amity.add_person("fellow1","Fellow","N"),\
                None, msg = "Error, Person already exists")

    def test_create_living_space(self):
        """ CREATE NEW LSPACE"""
        self.assertIsInstance(self.amity.create_room("lspace12","lspace"),
                                    LivingSpace )

    def test_create_office(self):
        """ CREATE NEW OFFICE"""
        self.assertIsInstance(self.office1, Office )
        self.assertEqual(self.office1.name, "OFFICE1")

    def test_create_room_invalid_input(self):

        """ INVALID INPUT"""
        self.assertEqual(self.amity.create_room("testinvalid", "live-in"), None)

        """ ROOM NAME ALREADY EXISTS"""
        self.assertEqual(self.amity.create_room("office1", "office"),  None)

    def test_search_room(self):
        """ TEST ROOM SEARCH"""
        self.assertIsInstance(self.amity.search_room("lspace1"), LivingSpace)

        """ TEST NON EXISTENT ROOM"""
        self.assertFalse(self.amity.search_room("notthere"))

    def test_search_person(self):
        """ STAFF SEARCH TEST"""
        self.assertIsInstance(self.amity.search_person("STAFF1"), Staff)

        """ TEST FELLOW SEARCH"""
        self.assertIsInstance(self.amity.search_person("FELLOW1"), Fellow)


        """ TEST NON EXISTENT PERSON"""
        self.assertFalse(self.amity.search_person("NOONE"))

    def test_on_room_update(self):
        """ TEST WAITING LIST AUTO ALLOCATIONS"""
        self.amity.add_person("Ian 1", "FELLOW", "Y")
        self.amity.add_person("Ian 2", "FELLOW", "Y")
        self.amity.add_person("Ian 3", "FELLOW", "Y")
        self.amity.add_person("Ian 4", "FELLOW", "Y")
        self.amity.add_person("Ian 5", "FELLOW", "Y")
        self.amity.add_person("Ian 6", "FELLOW", "Y")

        """" ASSERT WAITING LIST IS NOT EMPTY"""
        self.assertGreater(len(self.amity.living_space_unallocated), 0)
        self.assertGreater(len(self.amity.office_unallocated), 0)

        """ CREATE NEW ROOMS(VACANCIES)"""
        self.amity.create_room("lspace2", "lspace")
        self.amity.create_room("office2", "office")

        """ ASSERT WAITING LIST IS  EMPTY"""
        self.assertEqual(len(self.amity.living_space_unallocated), 0)
        self.assertEqual(len(self.amity.office_unallocated), 0)

    def test_reallocate_person(self):
        """ REALLOCATION TEST"""
        lspace2 = self.amity.create_room("lspace2", "lspace")
        office2 = self.amity.create_room("office2", "office")


        """ FELLOW LSPACE REALLOCATION"""
        self.assertIn("FELLOW1", self.lspace1.occupants)
        self.assertEqual(self.fellow1.living_space_allocated.name, "LSPACE1")

        self.amity.reallocate_person("fellow1", "lspace2")

        self.assertIn("FELLOW1", lspace2.occupants)
        self.assertEqual(self.fellow1.living_space_allocated.name, "LSPACE2")


        """ TEST STAFF OFFICE REALLOCATION"""
        self.assertTrue("STAFF1" in self.office1.occupants)
        self.assertEqual(self.staff1.office_allocated.name, "OFFICE1")

        self.amity.reallocate_person("staff1", "OFFICE2")

        self.assertTrue("STAFF1" in office2.occupants)
        self.assertEqual(self.staff1.office_allocated.name, "OFFICE2")

        """ TEST STAFF LSPACE REALLOCATION"""
        self.assertEqual(self.amity.reallocate_person("staff1", "lspace1"),\
                None, msg="Staff Cannot be allocated a living space")

    def test_reallocate_person_no_room(self):
        """ TEST NON EXISTENT ROOM REALLOCATION"""
        self.assertEqual(self.amity.reallocate_person("staff1", "OFFICE7"),\
                None, msg = "You cannot be reallocated to a non existent room")
        self.assertEqual(self.amity.reallocate_person("fellow1", "lspace7"), \
                None, msg = "You cannot be reallocated to a non existent room")

    def test_save_state(self):
        """ SAVE STATE TEST"""
        """ CAPTURE ALL INSTANCE VARIABLES"""
        rooms = [room.name for room in self.amity.rooms]
        people = [person.name for person in self.amity.people]
        living_space_unallocated = [person.name for person in self.amity.living_space_unallocated]
        office_unallocated = [person.name for person in self.amity.office_unallocated]
        old_sate = [rooms, people, living_space_unallocated, office_unallocated]
        """ SAVE STATE TO TEST DB"""
        self.amity.save_state("test")

        """ LOAD STATE FROM TEST DB INTO NEW AMITY INSTANCE"""
        amity2 = Amity()
        amity2.load_state("test")
        rooms2 = [room.name for room in amity2.rooms]
        people2 = [person.name for person in amity2.people]
        living_space_unallocated2 = [person.name for person in amity2.living_space_unallocated]
        office_unallocated2 = [person.name for person in amity2.office_unallocated]
        new_state = [rooms2, people2, living_space_unallocated2, office_unallocated2]

        """ COMPARE NEW AND OLD INSTANCE"""
        self.assertCountEqual(old_sate, new_state)

    def test_load_people(self):
        """ LOAD PEOPLE TEST"""
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

        """ ASSERT PERSON DOESN'T EXIST BEFORE LOAD"""
        self.assertFalse(self.amity.search_person("OLUWAFEMI SULE"))
        self.assertFalse(self.amity.search_person("DOMINIC WALTERS"))
        self.assertFalse(self.amity.search_person("SIMON PATTERSON"))

        """ LOAD PEOPLE FROM TEXT FILE"""
        self.amity.load_people("test")

        """ ASSERT PERSON EXISTS AFTER LOAD"""
        self.assertTrue(self.amity.search_person("OLUWAFEMI SULE"))
        self.assertTrue(self.amity.search_person("DOMINIC WALTERS"))
        self.assertTrue(self.amity.search_person("SIMON PATTERSON"))




if __name__ == '__main__':
    unittest.main()
