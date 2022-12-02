import dataclasses
import json
import pprint

from scraper import models, utils

logger = utils.get_logger(__name__)


def to_json(enterprise_number, parents, children):
    json_dict = dict()
    json_list = list()
    permanent_representative_keys = list()

    for parent_key, parent_value in parents.items():
        if isinstance(parent_value, models.Entity):
            parent_dataclass_asdict = dataclasses.asdict(parent_value)
            child_dataclass_asdict = dataclasses.asdict(children[parent_key])
            parent_dataclass_asdict.update(child_dataclass_asdict)
            for child_key, child_value in children.items():
                child_d_a = dataclasses.asdict(child_value)
                parent_d_a = dataclasses.asdict(parents[child_key])
                child_d_a.update(parent_d_a)
                if isinstance(child_value, models.EntityEntity):
                    if child_value.representative_entity == parent_key:
                        del child_d_a["representative_entity"]
                        parent_dataclass_asdict["permanent_representative"] = child_d_a
                        json_list.append(parent_dataclass_asdict)
                        permanent_representative_keys.append(child_key)
        elif parent_key not in permanent_representative_keys:
            parent_dataclass_asdict = dataclasses.asdict(parent_value)
            child_dataclass_asdict = dataclasses.asdict(children[parent_key])
            parent_dataclass_asdict.update(child_dataclass_asdict)
            json_list.append(parent_dataclass_asdict)

    json_dict[enterprise_number] = json_list
    return json.dumps(json_dict, default=str)
