import pandas as pd
import json
import bs4
import datetime
import dateparser
import math
import ast
from pathlib import Path
from bs4 import BeautifulSoup
from dataclasses import dataclass, field, asdict
from typing import Any, List, Dict, ClassVar, Iterable, Tuple
from urllib.parse import urlparse
from geopy.geocoders import Nominatim
from geopy.exc import GeopyError
from .files import save_to_file, parse_file, remove_all_files
from .misc import Url, literal_eval, NoneType, ACTION_FOLDER


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
    id: int
    date: str
    sources: List[Url]
    actions: List[str]
    struggles: List[str]
    employment_types: List[str]
    description: str

    # optional fields
    online: bool = None
    locations: List[List[str]] = None
    companies: List[str] = None
    workers: int = None
    tags: List[str] = None
    author: str = None
    latlngs: List[Tuple[float, float]] = None
    addresses: List[str] = None

    _meta_fields: ClassVar = ["author"]

    def __post_init__(self):
        """ Used to validate fields. """
        # check all the types
        assert isinstance(self.date, (str, pd.Timestamp, datetime.date))
        assert isinstance(self.sources, (str, list))
        assert isinstance(self.struggles, list)
        assert isinstance(self.actions, list)
        assert isinstance(self.employment_types, list)
        assert isinstance(self.companies, (list, NoneType))
        assert isinstance(self.tags, (list, NoneType))
        assert isinstance(self.workers, (int, float, NoneType))
        assert isinstance(self.locations, (list, NoneType))

        assert isinstance(self.latlngs, (list, float, NoneType))
        if isinstance(self.latlngs, list):
            assert all(isinstance(el, list) for el in self.latlngs)

        assert isinstance(self.addresses, (list, float, NoneType))

        # cast source to comma separate list
        if isinstance(self.sources, str):
            self.sources = [x.strip() for x in self.sources.split(',')]

        # cast workers to int
        if isinstance(self.workers, float):
            if math.isnan(self.workers):
                self.workers = None
            else:
                self.workers = int(self.workers)

        # change date to datetime
        if isinstance(self.date, str):
            self.date = dateparser.parse(self.date).date()
        if isinstance(self.date, pd.Timestamp):
            self.date = pd.Timestamp.to_pydatetime(self.date)

        # if latlng is not set, set it
        if not self.latlngs and not self.addresses:
            self.latlngs, self.addresses = self.get_locs()

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
        """ Return dict of all fields. """
        return asdict(self)

    def get_locs(self) -> Tuple[List[str], List[Tuple[float, float]]]:
        """ Generate lat/lngs by passing in location + company string to Geopy. """
        geolocator = Nominatim(user_agent="collective_action")
        latlngs = []
        addresses = []

        def add_address_latlng(loc):
            """ mini helper func to append lat/loc and address """
            latlngs.append((loc.latitude, loc.longitude))
            addresses.append(loc.address)

        if self.locations:
            for location in self.locations:
                location = ", ".join(location.split("-"))

                # skip is location is online or worldwide
                if location in ["worldwide"]:
                    continue

                # attach company name to each city/state/country location
                if self.companies:
                    for company in self.companies:
                        try:
                            loc = geolocator.geocode(f"{company}, {location}")
                            if loc:
                                add_address_latlng(loc)
                        except GeopyError:
                            print(f"Geocoder error, skipping entry: '{company}, {location}'...")

                # if no company listed, just use location
                else:
                    try:
                        loc = geolocator.geocode(f"{location}")
                        if loc:
                            add_address_latlng(loc)
                    except GeopyError:
                        print(f"Geocoder error, skipping entry: '{location}'...")

        if len(latlngs) == 0:
            latlngs = None
        if len(addresses) == 0:
            addresses = None

        return latlngs, addresses

    def stringify(self) -> Dict[str, str]:
        """ Return a dict of all fields serialized to a string. """
        return {key: str(value) for key, value in self.__dict__.items()}

    @classmethod
    def create_from_row(cls, row: pd.Series) -> "CollectiveAction":
        """ Create an CollectiveAction instance from a dataframe row. """
        fields = [
            key
            for key, value in cls.__dataclass_fields__.items()
            if value.type != ClassVar
        ]
        d = {
            key: literal_eval(value)
            for key, value in row.to_dict().items()
            if key in fields
        }
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
    cas: List[CollectiveAction] = field(default_factory=lambda: [])
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
        """ Converts this instance of CollectiveActions to a df (for CSV)

        This function will assert a least-recent to most-recent ordering of
        events.
        """
        self.sort()
        data = []
        for ca in self.cas:
            data.append(ca.stringify())
        df = pd.read_json(json.dumps(data), orient="list", convert_dates=False)
        return df[self.fields]

    def to_readme(self) -> None:
        """ Convert this instance of CollectiveActions to markdown/HTML for the README.md.

        This function will assert a most-recent to least-recent ordering of
        events.
        """
        soup = BeautifulSoup(f"<div id={self.ca_id}></div>", "html.parser")
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
            td_date.string = str(ca.date)
            tr.append(td_date)

            td_action = soup.new_tag("td")
            td_action.string = ca.description
            tr.append(td_action)

            td_action = soup.new_tag("td")
            a = soup.new_tag("a")
            a["href"] = f"/actions/{len(self.cas) - 1 - i:04}.json"
            emoji = create_emoji_tag()
            a.append(emoji)
            td_action.append(a)
            tr.append(td_action)

            table.append(tr)
        return soup.prettify()

    def to_files(self, folder: Path = ACTION_FOLDER) -> None:
        """ Convert this instance of Actions to files.

        This function will assert a least-recent to most-recent ordering of
        events.
        """
        self.sort()
        remove_all_files(folder)
        for i, ca in enumerate(self.cas):
            struggles = ""
            for s in ca.struggles:
                struggles += f"{s},"
            fn = f"{i:04}.json"
            save_to_file(filepath=Path(folder) / fn, ca=ca.to_dict())

    def to_dict(self) -> str:
        """ Convert this instance of Actions to JSON. """
        self.sort()
        return [ca.to_dict() for ca in self.cas]

    @classmethod
    def read_from_df(cls, df: pd.DataFrame) -> "CollectiveActions":
        """ Create and populate a CollectiveActions instance from a dataframe. (CSV/JSON) """
        cas = CollectiveActions()
        for _, row in df.iterrows():
            ca = CollectiveAction.create_from_row(row)
            cas.append(ca)
        return cas

    @classmethod
    def read_from_files(
        cls, files: List[str], folder: Path = ACTION_FOLDER
    ) -> "CollectiveActions":
        """ Create and populate a CollectiveActions instance from the actions folder. """
        cas = CollectiveActions()
        for file in files:
            contents = parse_file(folder / file)
            ca = CollectiveAction(**contents)
            cas.append(ca)
        return cas
