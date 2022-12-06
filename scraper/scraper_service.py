import re

import bs4
from playwright.sync_api import (
    Error as PlaywrightError,
    TimeoutError as PlaywrightTimeoutError,
)

from playwright import sync_api
from scraper import models, utils

logger = utils.get_logger(__name__)


def retrieve_target(enterprise_number):
    with sync_api.sync_playwright() as p:
        try:
            browser = p.chromium.launch()
            # context = browser.new_context()
            page = browser.new_page()
            page.goto(
                f"https://kbopub.economie.fgov.be/kbopub/toonondernemingps.html?lang=en&ondernemingsnummer={enterprise_number}"
            )
            page.get_by_text("Show the legal functions").click()
            content = page.content()
            browser.close()
        except (PlaywrightError, PlaywrightTimeoutError) as e:
            logger.error("Error while retrieving target: %s", e.message)
    return content


def parse_target(content):
    try:
        parse_tree = bs4.BeautifulSoup(content, "lxml")
        table = parse_tree.find(id="toonfctie")
        rows = table.find_all("tr")
    except (AttributeError) as e:
        logger.error(e)

    officers_raw = dict()
    for row_index, row in enumerate(rows):
        officer = []
        for string in row.stripped_strings:
            officer.append(string)

        officers_raw[row_index] = officer

    return _parse_dictionary_to_objects(officers_raw)


def _parse_dictionary_to_objects(officers_raw):
    officers = dict()
    duplicated_keys = list()
    entities = list()
    for key, value in officers_raw.items():
        for string in value:
            if ",\xa0" in string:
                # If model already in dict, assign same reference to key.
                model = models.Person(string)
                try:
                    model_key = list(officers.keys())[
                        list(officers.values()).index(model)
                    ]
                    officers[key] = officers[model_key]
                    duplicated_keys.append(key)
                except (ValueError):
                    officers[key] = model
            if re.match(r"\d{4}\.\d{3}\.\d{3}", string):
                entities.append(key)
                model = models.Entity(string)
                try:
                    model_key = list(officers.keys())[
                        list(officers.values()).index(model)
                    ]
                    officers[key] = officers[model_key]
                except (ValueError):
                    officers[key] = model

    permanent_representatives = dict()
    for key, value in officers_raw.items():
        if isinstance(officers[key], models.Person):
            if len(value) == 3:
                officers[key].functions.append(
                    models.EntityPerson(function=value[0], start_date=value[2])
                )
            elif len(value) == 4:
                officers[key].functions.append(
                    models.EntityPerson(function=value[0], start_date=value[3])
                )
                stripped = value[2].strip("()")
                enterprise_number = int(
                    str.join("", (c for c in stripped if c.isdigit()))
                )
                permanent_representatives[enterprise_number] = key

    if duplicated_keys:
        for key in duplicated_keys:
            del officers[key]

    if permanent_representatives:
        for (
            enterprise_number,
            permanent_representative_index,
        ) in permanent_representatives.items():
            for key in entities:
                if officers[key].enterprise_number == enterprise_number:
                    officers[key].functions.append(
                        models.EntityEntity(
                            function=officers_raw[key][0],
                            start_date=officers_raw[key][2],
                            permanent_representative=officers[
                                permanent_representative_index
                            ],
                        )
                    )
            del officers[permanent_representative_index]

    return officers
