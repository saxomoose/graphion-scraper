import dataclasses
import json
from scraper import utils

logger = utils.get_logger(__name__)


def to_json(enterprise_number, officers_obj):
    wrapper = dict()
    officers_list = list()
    for value in officers_obj.values():
        officers_list.append(dataclasses.asdict(value))
    wrapper[enterprise_number] = officers_list
    return json.dumps(wrapper, default=str)
