from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime
from sqlalchemy import create_engine, update, delete
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


class Database():
    def __init__(self, db_name="default"):
        self.db_name = "sqlite:///" +db_name + ".db"
        self.engine = create_engine(self.db_name)
        self.Base = declarative_base()
        self.Base.metadata.bind = self.engine
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()
        self.Room, self.Person = self.create_database()

    def create_database(self):
        class Person(self.Base):
            __tablename__ = 'people'
            __table_args__ = {'extend_existing':True}
            id = Column(Integer, primary_key=True)
            name = Column(String(100))
            role = Column(String(10))
            office = Column(String(20))
            living_space = Column(String(20))
            date_created = Column(DateTime(timezone=True), server_default = func.now())
            last_updated = Column(DateTime(timezone=True), onupdate = func.now())


        class Room(self.Base):
            __tablename__ = 'rooms'
            __table_args__ = {'extend_existing':True}
            id = Column(Integer, primary_key=True)
            name = Column(String(40))
            max_occupants = Column(Integer)
            no_of_occupants = Column(Integer)
            room_type = Column(String(10))
            occupants = Column(String)
            date_created = Column(Date, server_default = func.now())
            last_updated = Column(Date, onupdate = func.now())

        engine = create_engine(self.db_name)
        self.Base.metadata.create_all(engine)
        return [Room, Person]

    def get_people(self):
        people = self.session.query(self.Person).all()
        return people

    def get_rooms(self):
        rooms = self.session.query(self.Room).all()
        return rooms

    def check_exists(self, name, table):
        person = self.session.query(table).\
                    filter(table.name == name).all()
        return len(person) > 0

    def save_person(self, name, role, office = None, living_space = None):
        if self.check_exists(name, self.Person):
            mod = update(self.Person).where(self.Person.name == name).values(
                                            name = name,
                                            role = role,
                                            office = office,
                                            living_space = living_space
                                        )
            self.session.execute(mod)
            self.session.commit()
        else:
            new_person = self.Person(
                                name = name ,
                                role = role,
                                office = office,
                                living_space = living_space
                                )
            self.session.add(new_person)
            self.session.commit()


    def save_room(self, name, max_occupants = 0, no_of_occupants = 0, room_type = None, occupants = None):
        if self.check_exists(name, self.Room):
            mod = update(self.Room).where(self.Room.name == name).values(
                                            name = name,
                                            max_occupants = max_occupants,
                                            no_of_occupants = no_of_occupants,
                                            room_type = room_type,
                                            occupants = occupants

                                        )
            self.session.execute(mod)
            self.session.commit()
        else:
            new_room = self.Room(
                                name = name,
                                max_occupants = max_occupants,
                                no_of_occupants = no_of_occupants,
                                room_type = room_type,
                                occupants = occupants
                                )
            self.session.add(new_room)
            self.session.commit()

    def delete_person(self, name):
        delete(self.Person).where(self.Person.name == name)

    def delete_room(self, name):
        delete(self.Room).where(self.Room.name == name)
