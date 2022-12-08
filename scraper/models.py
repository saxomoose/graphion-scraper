import dataclasses
import datetime
import enum
import typing


class FunctionEnum(enum.IntEnum):
    DIRECTOR = 1
    PERMANENT_REPRESENTATIVE = 2
    PERSON_IN_CHARGE_OF_DAILY_MANAGEMENT = 3


@dataclasses.dataclass
class _Pivot:
    function: FunctionEnum
    start_date: datetime.date

    def __init__(
        self,
        function: str,
        start_date: str,
    ):
        if function == "Director":
            self.function = FunctionEnum.DIRECTOR
        if (
            function == "Person in charge of daily management"
            or function == "Managing Director"
        ):
            self.function = FunctionEnum.PERSON_IN_CHARGE_OF_DAILY_MANAGEMENT
        if function == "Permanent representative":
            self.function = FunctionEnum.PERMANENT_REPRESENTATIVE
        substring = start_date[6:]
        self.start_date = datetime.datetime.strptime(substring, "%B %d, %Y").date()


@dataclasses.dataclass
class EntityPerson(_Pivot):
    def __init__(self, function: str, start_date: str):
        super().__init__(function, start_date)


@dataclasses.dataclass
class Person:
    last_name: str
    first_name: str
    functions: typing.List[EntityPerson]

    def __init__(self, names: str):
        names = tuple(names.split(" ,\xa0 "))
        self.last_name = names[0]
        self.first_name = names[1]
        self.functions = list()


@dataclasses.dataclass
class EntityEntity(_Pivot):
    permanent_representative: Person

    def __init__(
        self,
        function: str,
        start_date: str,
        permanent_representative: Person,
    ):
        super().__init__(function, start_date)
        self.permanent_representative = permanent_representative


@dataclasses.dataclass
class Entity:
    enterprise_number: int
    functions: typing.List[EntityEntity]

    def __init__(self, enterprise_number: str):
        enterprise_number_parsed = int(
            str.join("", (c for c in enterprise_number if c.isdigit()))
        )
        self.enterprise_number = enterprise_number_parsed
        self.functions = list()
