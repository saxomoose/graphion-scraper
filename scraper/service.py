from bs4 import BeautifulSoup, NavigableString
from playwright.sync_api import (
    Error as PlaywrightError,
    TimeoutError as PlaywrightTimeoutError,
    sync_playwright,
)
from .utils import get_logger


logger = get_logger(__name__)


def retrieve_target(enterprise_number):
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(
                f"https://kbopub.economie.fgov.be/kbopub/toonondernemingps.html?ondernemingsnummer={enterprise_number}"
            )
            page.get_by_text("Toon de functiehouders").click()
            content = page.content()
            browser.close()
        except (PlaywrightError, PlaywrightTimeoutError) as e:
            # TODO: implement logging.
            logger.error("Error while retrieving target: %s", e.message)
    return content


# TODO: error handling.
def parse_target(content):
    parse_tree = BeautifulSoup(content, "lxml")
    table = parse_tree.find(id="toonfctie")
    # print(table.prettify())
    text = []
    row_gen = (
        row for row in table.tr.next_siblings if not isinstance(row, NavigableString)
    )
    for row in row_gen:
        for data_cell in row.find_all("td"):
            for string in data_cell.stripped_strings:
                # text.append(unicodedata.normalize("NFKD", string))
                text.append(string)

    logger.info("test")
    return text
