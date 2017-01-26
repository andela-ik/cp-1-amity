# Amity

A simple command line room allocation system

## Installation

Clone the repo: `git clone https://github.com/andela-ik/cp-1-amity.git`

### Install dependencies
-Activate/Create a **python 3.6** virtual environment
```
cd cp-1-amity
pip install -r requirements.txt
```
## Running The App
Execute `python run.py`
you should be presented with the below once the app starts up:
![image](https://cloud.githubusercontent.com/assets/25026203/22325629/fb6ac14c-e3bf-11e6-8b11-6c197ade8e50.png)

### Usage:
```
  create_room <room_name>
  add_person <person_name> <role> [wants_accommodation]
  print_allocations [--o=filename]
  print_unallocated [--o=filename]
  load_people <filename>
  reallocate_person <first_name> <last_name> <new_room_name>
  print_room <room_name>
  save_state [--db=sqlite_database]
  load_state <sqlite_database>

Options:
  help     Show help.
```
