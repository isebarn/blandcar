from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy import (
    ForeignKey,
    desc,
    create_engine,
    func,
    Column,
    BigInteger,
    JSON,
    Integer,
    Float,
    String,
    Boolean,
    DateTime,
    Text,
)

from datetime import datetime
from sqlalchemy import desc

import os
import json

connectionString = os.environ.get('CAR_DATABASE')

engine = create_engine(connectionString, echo=False)

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text


class Car(Base):
    __tablename__ = 'cars'

    Id = Column(Integer, primary_key=True)
    Price = Column(Float)
    Driven = Column(Integer)
    Fuel = Column(String)
    Doors = Column(Integer)
    Valves = Column(Integer)
    Seats = Column(Integer)
    Maker = Column(String)
    Drivetrain = Column(String)
    Transmission = Column(String)
    Color = Column(String)
    Inspected = Column(Boolean)
    Model = Column(String)
    Year = Column(Integer)

    def __init__(self, data):
        self.Id = data.get('_id')

        self.Price = data.get('price', 0)
        self.Driven = int(data.get('Akstur', '0').replace(".", ''))
        self.Fuel = data.get('Eldsneyti', '')
        self.Doors = (
            int(data.get('Fjöldi dyra', '0'))
            if data.get('Fjöldi dyra').isnumeric()
            else 0
        )
        self.Valves = int(data.get('Fjöldi strokka', '0'))
        self.Seats = (
            int(data.get('Fjöldi sæta', '0'))
            if data.get('Fjöldi sæta').isnumeric()
            else 0
        )
        self.Maker = data.get('Framleiðandi', '')
        self.Drivetrain = data.get('Hjóladrifin', '')
        self.Color = data.get('Litur', '')
        self.Transmission = data.get('Skipting', '')
        self.Inspected = data.get('Skoðaður', '') == 'Já'
        self.Model = data.get('Undirtegund', '')
        self.Year = int(data.get('Ár', '0'))


class Operations:
    def SaveCar(car):
        session.add(car)
        session.commit()

    def SavedIds():
        return [x[0] for x in session.query(Car.Id).all()]


Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
