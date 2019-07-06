import pandas as pd
import math
import json
import html
import bs4
import re
import dateparser
from bs4 import BeautifulSoup
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, List, Dict, ClassVar, Union
from urllib.parse import urlparse
from .markdown import MarkdownData, MarkdownDocument
from .files import FileClient

Url = str


@dataclass
class Action:
    """ The class for an action we want to track.

    This class is used to manage the data of an individual Action. It is used
    to perform the following:
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
    action: str
    struggles: List[str]
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
                return [s.strip().lower() for s in field.split(",")]

    def __post_init__(self):
        """ Used to validate fields. """
        # self.date = datetime.strptime(self.date, "%Y-%m-%d").date()
        self.date = dateparser.parse(self.date).date()
        self.sources = self.listify(self.sources)
        self.struggles = self.listify(self.struggles)
        self.action = self.action.strip().lower()

        self.companies = self.listify(self.companies)
        self.tags = self.listify(self.tags)
        self.locations = self.listify(self.locations)

        self.workers = None if self.is_none(self.workers) else int(self.workers)

        # make sure action is a valid action
        assert (
            self.action in self._valid_actions
        ), f"'{self.action}' is not a valid input. Valid inputs are: {self._valid_actions}"

        # make sure all struggles are valid struggles
        for struggle in self.struggles:
            assert (
                struggle in self._valid_struggles
            ), f"'{struggle}' is not a valid input. Valid inputs are: {self._valid_struggles}"

        # make sure source is either a url or a html link tag <a>
        for source in self.sources:
            assert (
                BeautifulSoup(source, "html.parser").a is not None
                or urlparse(source).netloc is not ""
            ), f"'{source}' is in valid. source must be a valid url or an html link tag element"

        # if html, extract only href from sources
        self.sources = [
            BeautifulSoup(source, "html.parser").a["href"]
            if "href" in source
            else source
            for source in self.sources
        ]

    def __lt__(self, other):
        """ Used to make Actions sortable. """
        return self.date < other.date

    def __eq__(self, other):
        """ Overrides the default implementation for equality. """
        if isinstance(other, Action):
            return self.__dict__.items() == other.__dict__.items()
        return False

    def to_dict(self) -> Dict[str, Any]:
        """ Return dict of all fields serialized to string """
        return {key: self.render_df(key) for key, value in self.__dict__.items()}

    def render_df(self, field: str) -> str:
        """ Return the value of the field rendered for df. """
        value = self.__getattribute__(field)
        if field in ["date", "workers"]:
            return str(value)
        elif field in ["locations", "struggles", "companies", "tags", "sources"]:
            return str(value).strip("[").strip("]").replace("'", "").replace('"', "")
        else:
            return value

    def to_md(self, field: str, td: bs4.element.Tag) -> str:
        """ Convert field for markdown

        Takes a td BeautifulSoup object and updates it according to the field
        type so that it renders correctly in markdown.
        """
        assert (
            field in self.__dataclass_fields__
        ), f"Cannot serialize {field}. Not a valid field in Action."

        value = self.__getattribute__(field)

        if field in ["date", "workers"]:
            td.string = str(value)
        elif field in ["locations", "struggles", "companies", "tags"]:
            td.string = (
                str(value).strip("[").strip("]").replace("'", "").replace('"', "")
            )
        elif field == "sources":
            ret = []
            for source in value:
                tag = (
                    f"<a href='{source}' target='_blank'>{urlparse(source).netloc}</a>"
                )
                ret.append(tag)
            td.append(BeautifulSoup(html.unescape(", ".join(ret)), "html.parser"))
        else:
            td.string = value

        return td

    @classmethod
    def create_from_md(cls, table: bs4.element.Tag) -> "Action":
        """ Create an Action instance from a md table. """
        a = {}
        trs = table.find_all("tr")
        for key, val in table.attrs.items():
            if key != "class":
                a[key] = val
        for i, tr in enumerate(trs):
            td_key = tr.find("td", class_="field-key")
            td_val = tr.find("td", class_="field-value")
            val = "".join(str(e) for e in td_val.contents).strip()
            key = "".join(str(e) for e in td_key.contents).strip()
            a[key] = val
        return cls(**a)

    @classmethod
    def create_from_row(cls, row: pd.Series) -> "Action":
        """ Create an Action instance from a dataframe row. """
        fields = [
            key
            for key, value in cls.__dataclass_fields__.items()
            if value.type != ClassVar
        ]
        d = {key: value for key, value in row.to_dict().items() if key in fields}
        return cls(**d)


@dataclass
class Actions:
    """ The class for a set of actions.

    This class is a collection of actions. It is used to for the four primary
    usecases:
        - to serialize the list of actions into a dataframe
        - to serialize the list of actions into a markdown/html table
        - to create and populate an Actions instance from a dataframe
        - to create and populate an Actions instance from a markdown document
    """

    action_id: ClassVar = "actions"
    actions: List[Action] = field(default_factory=lambda: [])
    fields: List[str] = field(
        default_factory=lambda: [
            key
            for key, value in Action.__dataclass_fields__.items()
            if value.type != ClassVar
        ]
    )

    def __len__(self) -> int:
        """ Get the number of actions. """
        return len(self.actions)

    def __eq__(self, other):
        """ Overrides the default implementation for equality. """
        if isinstance(other, Actions):
            return self.actions == other.actions
        return False

    def sort(self, *args, **kwargs) -> "Actions":
        """ Sorts the list of actions. """
        self.actions.sort(*args, **kwargs)
        return self

    def append(self, action: Action) -> None:
        """ Append an action onto this instance of Actions. """
        self.actions.append(action)

    def to_df(self) -> pd.DataFrame:
        """ Converts this instance of Actions to a df. """
        data = []
        for action in self.actions:
            data.append(action.to_dict())
        df = pd.read_json(json.dumps(data), orient="list")
        return df[self.fields]

    def to_md(self) -> None:
        """ Convert this instance of Actions to markdown/HTML. """
        soup = BeautifulSoup(f"<div id={self.action_id}></div>", "html.parser")
        for action in self.actions:
            table = soup.new_tag("table")
            soup.div.append(table)
            for meta_field in Action._meta_fields:
                table[meta_field] = action.__getattribute__(meta_field)
            for field in self.fields:
                if action.__getattribute__(field) is None:
                    continue
                if field in Action._meta_fields:
                    continue
                tr = soup.new_tag("tr")
                td_key = soup.new_tag("td", attrs={"class": "field-key"})
                td_val = soup.new_tag("td", attrs={"class": "field-value"})
                td_key.string = field
                td_val = action.to_md(field, td_val)
                tr.append(td_key)
                tr.append(td_val)
                table.append(tr)
        return soup.prettify()

    def to_files(self) -> None:
        """ Convert this instance of Actions to files. """
        fc = FileClient()
        fc.remove_actions()
        for i, action in enumerate(self.actions):
            struggles = ""
            for s in action.struggles:
                struggles += f"{s},"
            fn = f"[{i+1}]{action.date}.txt"
            fc.save_to_file(filename=fn, action=action.to_dict())

    @classmethod
    def read_from_md(cls, md_doc: MarkdownDocument) -> "Actions":
        """ Create and populate an Actions instance from a Markdown Document. """
        md_data = re.findall(fr'<div id="{cls.action_id}">+[\s\S]+<\/div>', md_doc)
        assert len(md_data) == 1, f"multiple divs with id={cls.action_id} were found"
        md_data = md_data[0]
        soup = BeautifulSoup(md_data, "html.parser")
        tables = soup.div.find_all("table")
        actions = Actions()
        for table in tables:
            action = Action.create_from_md(table)
            actions.append(action)
        return actions

    @staticmethod
    def read_from_df(df: pd.DataFrame) -> "Actions":
        """ Create and populate an Actions instance from a dataframe. """
        actions = Actions()
        for i, row in df.iterrows():
            action = Action.create_from_row(row)
            actions.append(action)
        return actions
