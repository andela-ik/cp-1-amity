"""Amity
Usage:
  create_room <room_name>
  add_person <person_name> <role> [wants_accommodation]

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

from docopt import docopt, DocoptExit
import cmd
from app.classes.amity import Amity

amity = Amity()

def docopt_cmd(func):
    """Amity
    Usage:
      create_room <room_name>
      add_person <person_name> <role> [wants_accommodation]

    Options:
      -h --help     Show this screen.
      --version     Show version.
    """
    def fn(self, arg):
        try:
            ARGS = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.
            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            return

        return func(self, ARGS)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn

class AmityInterface(cmd.Cmd):
    intro = "AMITY DEMO INTRO"
    prompt = 'amity> '


    @docopt_cmd
    def do_add_person(self, arg):
        """ Usage: add_person <first_name> <last_name> (fellow|staff) [<wants_accommodation>]"""
        if arg['fellow']:
            role = "FELLOW"
        if arg['staff']:
            role = "STAFF"
        name = " ".join([arg['<first_name>'], arg['<last_name>']])
        amity.add_person(name, role, arg['<wants_accommodation>'])

    @docopt_cmd
    def do_create_room(self, arg):
        """ Usage: create_room <room_type> <room_name>..."""
        for name in arg['<room_name>']:
            amity.create_room(name, arg['<room_type>'])

    @docopt_cmd
    def do_exit(self, arg):
        """ Usage: exit"""
        print("Goodbye!!")
        exit()

    @docopt_cmd
    def do_print_allocations(self, arg):
        """ Usage: print_allocations [--o=filename]"""
        if arg["--o"]:
            amity.print_allocations(arg["--o"])
        else:
            amity.print_allocations()


    @docopt_cmd
    def do_print_unallocated(self, arg):
        """ Usage: print_unallocated [--o=filename]"""
        if arg["--o"]:
            amity.print_unallocated(arg["--o"])
        else:
            amity.print_unallocated()

    @docopt_cmd
    def do_load_people(self, arg):
        """ Usage: load_people <filename>"""
        amity.load_people(arg["<filename>"])

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """ Usage: reallocate_person <first_name> <last_name> <new_room_name>"""
        name = " ".join([arg['<first_name>'], arg['<last_name>']])
        amity.reallocate_person(name, arg['<new_room_name>'])

    @docopt_cmd
    def do_print_room(self, arg):
        """ Usage: print_room <room_name> """
        amity.print_room(arg["<room_name>"])

    @docopt_cmd
    def do_save_state(self, arg):
        """ Usage: save_state [--db=sqlite_database]"""
        if arg:
            amity.save_state(arg["--db"])
        else:
            amity.save_state()

    @docopt_cmd
    def do_load_state(self,arg):
        """ Usage: load_state <sqlite_database>"""
        amity.load_state(arg['<sqlite_database>'])



if __name__ == '__main__':

    AmityInterface().cmdloop()
