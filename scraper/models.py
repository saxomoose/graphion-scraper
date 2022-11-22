import datetime
import enum
from dataclasses import dataclass


class FunctionEnum(enum.Enum):
    DIRECTOR = 1
    PERMANENT_REPRESENTATIVE = 2
    PERSON_IN_CHARGE_OF_DAILY_MANAGEMENT = 3


@dataclass
class Entity:
    enterprise_number: int

    def __init__(self, enterprise_number_str: str):
        enterprise_number = int(
            "".join(c for c in enterprise_number_str if c.isdigit())
        )
        self.enterprise_number = enterprise_number


@dataclass
class Person:
    last_name: str
    first_name: str

    def __init__(self, names_str: str):
        names = tuple(names_str.split(" ,\xa0 "))
        self.last_name = names[0]
        self.first_name = names[1]


@dataclass
class EntityPerson:
    function: FunctionEnum
    start_date: datetime.date

    def __init__(self, function_str: str, start_date_str: str):
        if function_str == "Director":
            self.function = FunctionEnum.DIRECTOR
        if (
            function_str == "Person in charge of daily management"
            or function_str == "Managing Director"
        ):
            self.function = FunctionEnum.PERSON_IN_CHARGE_OF_DAILY_MANAGEMENT
        substring = start_date_str[6:]
        self.start_date = datetime.datetime.strptime(substring, "%B %d, %Y")


@dataclass
class EntityEntity:
    representative_entity: int
    function: FunctionEnum
    start_date: datetime.date

    def __init__(
        self, representative_entity_str: str, function_str: str, start_date_str: str
    ):
        self.representative_entity = int(
            "".join(c for c in representative_entity_str if c.isdigit())
        )
        if function_str == "Permanent representative":
            self.function = FunctionEnum.PERMANENT_REPRESENTATIVE
        substring = start_date_str[6:]
        self.start_date = datetime.datetime.strptime(substring, "%B %d, %Y").date()
