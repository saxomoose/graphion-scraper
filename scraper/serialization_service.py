import dataclasses
import json
from scraper import utils

logger = utils.get_logger(__name__)

# Target enterprise number is not encapsulated in serialized object.
def to_json(officers_obj):
    wrapper = dict()
    officers_list = list()
    for value in officers_obj.values():
        officers_list.append(dataclasses.asdict(value))
    wrapper['officers'] = officers_list
    return json.dumps(wrapper, default=str)
