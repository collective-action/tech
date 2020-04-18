import datetime
from typing import Any


Url = str


def ca_json_converter(o: Any) -> str:
    """ converts datetime to str if type is datetime """
    if isinstance(o, datetime.date):
        return o.strftime("%Y/%m/%d")


