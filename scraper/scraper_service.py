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


# TODO: error handling.
def parse_target(content):
    try:
        parse_tree = bs4.BeautifulSoup(content, "lxml")
        table = parse_tree.find(id="toonfctie")
        rows = table.find_all("tr")
    except (AttributeError):
        return None

    officers = dict()
    for row_index, row in enumerate(rows):
        officer = []
        for string in row.stripped_strings:
            officer.append(string)

        officers[row_index] = officer

    return officers


def parse_dictionary(officers):
    parents = dict()
    for key, value in officers.items():
        for string in value:
            if ",\xa0" in string:
                # Only adds model to dict if not already present.
                model = models.Person(string)
                try:
                    model_key = list(parents.keys())[
                        list(parents.values()).index(model)
                    ]
                    parents[key] = parents[model_key]
                except (ValueError):
                    parents[key] = model
            if re.match(r"\d{4}\.\d{3}\.\d{3}", string):
                model = models.Entity(string)
                try:
                    model_key = list(parents.keys())[
                        list(parents.values()).index(model)
                    ]
                    parents[key] = parents[model_key]
                except (ValueError):
                    parents[key] = model

    children = dict()
    for key, value in officers.items():
        if len(value) == 3:
            children[key] = models.Pivot(function_str=value[0], start_date_str=value[2])
        if len(value) == 4:
            children[key] = models.Pivot(
                function_str=value[0],
                start_date_str=value[3],
                representative_entity_str=value[2],
            )

    return parents, children
