import dataclasses
import datetime
import enum
import typing


class FunctionEnum(enum.StrEnum):
    DIRECTOR = "DIRECTOR"
    PERMANENT_REPRESENTATIVE = "PERMANENT_REPRESENTATIVE"
    PERSON_IN_CHARGE_OF_DAILY_MANAGEMENT = "PERSON_IN_CHARGE_OF_DAILY_MANAGEMENT"


@dataclasses.dataclass
class Pivot:
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
class DirectFunction(Pivot):
    def __init__(self, function: str, start_date: str):
        super().__init__(function, start_date)


@dataclasses.dataclass
class NaturalPersonOfficer:
    last_name: str
    first_name: str
    functions: typing.List[DirectFunction]

    def __init__(self, names: str):
        names = tuple(names.split(","))
        self.last_name = names[0]
        self.first_name = names[1]
        self.functions = list()

@dataclasses.dataclass
class IndirectFunction(Pivot):
    permanent_representative: NaturalPersonOfficer

    def __init__(
        self,
        function: str,
        start_date: str,
        permanent_representative: NaturalPersonOfficer,
    ):
        super().__init__(function, start_date)
        self.permanent_representative = permanent_representative


@dataclasses.dataclass
class LegalPersonOfficer:
    enterprise_number: int
    functions: typing.List[IndirectFunction]

    def __init__(self, enterprise_number: str):
        enterprise_number_parsed = int(
            str.join("", (c for c in enterprise_number if c.isdigit()))
        )
        self.enterprise_number = enterprise_number_parsed
        self.functions = list()
