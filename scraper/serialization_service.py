import dataclasses
import json

from scraper import utils

logger = utils.get_logger(__name__)


def to_json(enterprise_number, parents, children):
    json_dict = dict()
    json_list = list()
    for parent_key, parent_value in parents.items():
        parent_dataclass_asdict = dataclasses.asdict(parent_value)
        child_dataclass_asdict = dataclasses.asdict(children[parent_key])
        parent_dataclass_asdict.update(child_dataclass_asdict)
        json_list.append(parent_dataclass_asdict)
    json_dict[enterprise_number] = json_list
    return json.dumps(json_dict, default=str)
