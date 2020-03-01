import pandas as pd
import math
import json
import bs4
import dateparser
from bs4 import BeautifulSoup
from dataclasses import dataclass, field
from typing import Any, List, Dict, ClassVar, Union, Iterable
from urllib.parse import urlparse
from .files import FileClient

Url = str


@dataclass
class CollectiveAction:
    """ The class for an action we want to track.

    This class is used to manage the data of an individual CollectiveAction.
    It is used to perform the following:
        - set mandatory/optional fields
        - set meta fields
        - cast an validate data so that it knows how to read datafields from
          markdown and dataframes
        - output actions as for dataframes and markdown
        - create and populate action instances from markdown and dataframes
    """

    # mandatory fields
    date: str
    sources: List[Url]
    actions: List[str]
    struggles: List[str]
    employment_types: List[str]
    description: str

    # optional fields
    locations: List[str] = None
    companies: List[str] = None
    workers: int = None
    tags: List[str] = None
    author: str = None

    _meta_fields: ClassVar = ["author"]

    _valid_struggles: ClassVar = [
        "ethics",
        "pay_and_benefits",
        "working_conditions",
        "discrimination",
        "unfair_labor_practices",
        "job_security",
    ]

    _valid_actions: ClassVar = [
        "strike",
        "protest",
        "open_letter",
        "legal_action",
        "union_drive",
        "union_representation",
    ]

    _valid_employement_types: ClassVar = [
        "blue_collar_workers",
        "white_collar_workers",
        "in_house_workers",
        "contract_workers",
        "gig_workers",
        "na"
    ]

    @staticmethod
    def is_none(field: Any) -> bool:
        if field is None:
            return True
        elif isinstance(field, float) and math.isnan(field):
            return True
        elif isinstance(field, str) and field.lower() == "none":
            return True
        elif isinstance(field, (list,)) and len(field) == 0:
            return True
        else:
            return False

    def listify(self, field: Union[List[Any], Any]) -> List[Any]:
        if self.is_none(field):
            return None
        else:
            if isinstance(field, (list,)):
                return field
            else:
                field = field.strip('\"')
                return [s.strip().lower() for s in field.split(",")]

    def __post_init__(self):
        """ Used to validate fields. """
        self.date = dateparser.parse(self.date).date()
        self.sources = self.listify(self.sources)
        self.struggles = self.listify(self.struggles)
        self.actions = self.listify(self.actions)
        self.employment_types = self.listify(self.employment_types)

        self.companies = self.listify(self.companies)
        self.tags = self.listify(self.tags)
        self.locations = self.listify(self.locations)

        self.workers = (
            None if self.is_none(self.workers) else int(self.workers)
        )

        # make sure action is a valid action
        for action in self.actions:
            assert (
                action in self._valid_actions
            ), f"'{action}' is not a valid input. Valid inputs are: {self._valid_actions}"

        # make sure all struggles are valid struggles
        for struggle in self.struggles:
            assert (
                struggle in self._valid_struggles
            ), f"'{struggle}' is not a valid input. Valid inputs are: {self._valid_struggles}"

        # make sure all struggles are valid struggles
        for employment_type in self.employment_types:
            assert (
                employment_type in self._valid_employement_types
            ), f"'{employment_type}' is not a valid input. Valid inputs are: {self._valid_employement_types}"

        # make sure source is either a url or a html link tag <a>
        for source in self.sources:
            assert (
                BeautifulSoup(source, "html.parser").a is not None
                or urlparse(source).netloc is not ""
            ), f"'{source}' is invalid. source must be a valid url or an html link tag element"

        # if html, extract only href from sources
        self.sources = [
            BeautifulSoup(source, "html.parser").a["href"]
            if "href" in source
            else source
            for source in self.sources
        ]

    def __lt__(self, other):
        """ Used to make CollectiveActions sortable.

        This will sort actions first based on the date, then based on the
        length of the description if the date is equal.
        """
        if self.date == other.date:
            return len(self.description) < len(other.description)
        else:
            return self.date < other.date

    def __eq__(self, other):
        """ Overrides the default implementation for equality. """
        if isinstance(other, CollectiveAction):
            return self.__dict__.items() == other.__dict__.items()
        return False

    def to_dict(self) -> Dict[str, Any]:
        """ Return dict of all fields serialized to string """
        return {
            key: self.stringify(key) for key, value in self.__dict__.items()
        }

    def stringify(self, field: str) -> str:
        """ Returns the value of the field in str. """
        assert (
            field in self.__dataclass_fields__
        ), f"Cannot serialize {field}. Not a valid field in CollectivenAction."

        value = self.__getattribute__(field)
        ret = None
        if field in ["date"]:
            ret = value.strftime("%Y/%m/%d")
        elif field in ["workers"]:
            ret = str(value)
        elif field in [
            "locations",
            "actions",
            "struggles",
            "employment_types",
            "companies",
            "tags",
            "sources",
        ]:
            ret = (
                str(value)
                .strip("[")
                .strip("]")
                .replace("'", "")
                .replace('"', "")
            )
        else:
            ret = value
        return ret

    @classmethod
    def create_from_row(cls, row: pd.Series) -> "CollectiveAction":
        """ Create an CollectiveAction instance from a dataframe row. """
        fields = [
            key
            for key, value in cls.__dataclass_fields__.items()
            if value.type != ClassVar
        ]
        d = {
            key: value for key, value in row.to_dict().items() if key in fields
        }
        return cls(**d)

    @classmethod
    def create_from_dict(cls, d: dict) -> "CollectiveAction":
        """ Create an action instance from a dictionary. """
        return cls(**d)


@dataclass
class CollectiveActions:
    """ The class for a set of actions.

    This class is a collection of actions. It is used to for the four primary
    usecases:
        - to serialize the list of actions into a dataframe
        - to serialize the list of actions into a markdown/html table
        - to create and populate an CollectiveActions instance from a dataframe
        - to create and populate an CollectiveActions instance from a markdown document
    """

    cas_iterator: Iterable = None
    ca_id: ClassVar = "actions"
    cas: List[CollectiveAction] = field(
        default_factory=lambda: []
    )
    fields: List[str] = field(
        default_factory=lambda: [
            key
            for key, value in CollectiveAction.__dataclass_fields__.items()
            if value.type != ClassVar
        ]
    )

    def __iter__(self):
        """ Make this class iterable. """
        return self

    def __next__(self):
        """ Override dunder method. """
        if self.cas_iterator is None:
            raise Exception(
                "This instance of CollectiveActions is empty and not iterable."
            )
        return next(self.cas_iterator)

    def __len__(self) -> int:
        """ Get the number of actions. """
        return len(self.cas)

    def __eq__(self, other):
        """ Overrides the default implementation for equality. """
        if isinstance(other, CollectiveActions):
            return self.cas == other.cas
        return False

    def sort(self, *args, **kwargs) -> "CollectiveActions":
        """ Sorts the list of actions. """
        self.cas.sort(*args, **kwargs)
        return self

    def append(self, ca: CollectiveAction) -> None:
        """
        Append an CollectiveAction onto this instance of CollectiveActions and
        make the actions iterable.
        """
        self.cas.append(ca)
        self.cas_iterator = iter(self.cas)

    def to_df(self) -> pd.DataFrame:
        """ Converts this instance of CollectiveActions to a df.

        This function will assert a least-recent to most-recent ordering of
        events.
        """
        self.sort()
        data = []
        for ca in self.cas:
            data.append(ca.to_dict())
        df = pd.read_json(json.dumps(data), orient="list", convert_dates=False)
        return df[self.fields]

    def to_readme(self) -> None:
        """ Convert this instance of CollectiveActions to markdown/HTML for the README.md.

        This function will assert a most-recent to least-recent ordering of
        events.
        """
        soup = BeautifulSoup(
            f"<div id={self.ca_id}></div>", "html.parser"
        )
        table = soup.new_tag("table")
        soup.div.append(table)

        def create_td_tag(tag) -> bs4.element.Tag:
            td = soup.new_tag("td")
            td.string = tag
            return td

        def create_emoji_tag() -> bs4.element.Tag:
            emoji = soup.new_tag("g-emoji")
            emoji["class"] = "g-emoji"
            emoji["alias"] = "link"
            emoji[
                "fallback-src"
            ] = "https://github.githubassets.com/images/icons/emoji/unicode/1f517.png"
            emoji.string = ":link:"
            return emoji

        # table header
        tr = soup.new_tag("tr")
        tr.append(create_td_tag("YYYYMMDD"))
        tr.append(create_td_tag("description"))
        tr.append(create_td_tag("link"))
        table.append(tr)

        # table body
        self.sort(reverse=True)
        for i, ca in enumerate(self.cas):
            tr = soup.new_tag("tr")

            for meta_field in CollectiveAction._meta_fields:
                tr[meta_field] = ca.__getattribute__(meta_field)

            td_date = soup.new_tag("td")
            td_date.string = ca.stringify("date")
            tr.append(td_date)

            td_action = soup.new_tag("td")
            td_action.string = ca.stringify("description")
            tr.append(td_action)

            td_action = soup.new_tag("td")
            a = soup.new_tag("a")
            a["href"] = f"/actions/{len(self.cas) - 1 - i:04}.md"
            emoji = create_emoji_tag()
            a.append(emoji)
            td_action.append(a)
            tr.append(td_action)

            table.append(tr)
        return soup.prettify()

    def to_files(self) -> None:
        """ Convert this instance of Actions to files.

        This function will assert a least-recent to most-recent ordering of
        events.
        """
        self.sort()
        fc = FileClient()
        fc.remove_all_files()
        for i, ca in enumerate(self.cas):
            struggles = ""
            for s in ca.struggles:
                struggles += f"{s},"
            fn = f"{i:04}.md"
            fc.save_to_file(
                filepath=fc.cas_folder / fn,
                ca=ca.to_dict(),
            )

    @staticmethod
    def read_from_df(df: pd.DataFrame) -> "CollectiveActions":
        """ Create and populate an CollectiveActions instance from a dataframe. """
        cas = CollectiveActions()
        for i, row in df.iterrows():
            ca = CollectiveAction.create_from_row(row)
            cas.append(ca)
        return cas

    @classmethod
    def read_from_files(cls, files: List[str]) -> "CollectiveActions":
        """ Create and populate an CollectiveActions instance from the actions folder. """
        fc = FileClient()
        cas = CollectiveActions()
        for file in files:
            contents = fc.parse_file(fc.cas_folder / file)
            ca = CollectiveAction.create_from_dict(contents)
            cas.append(ca)
        return cas
