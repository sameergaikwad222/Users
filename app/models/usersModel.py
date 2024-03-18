from pydantic import BaseModel
from typing import Optional


class Contacts(BaseModel):
    email: str
    phoneNumber: str


class Location(BaseModel):
    countryName: str
    countryCode: str
    phoneCode: str
    area: str


class Users(BaseModel):
    firstName: str
    lastName: str
    age: int
    contact: Contacts
    location: Location
    password: str
    statusId: int = 1
