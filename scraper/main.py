from bs4 import BeautifulSoup, NavigableString
from playwright.sync_api import (
    Error as PlaywrightError,
    TimeoutError as PlaywrightTimeoutError,
    sync_playwright,
)


# browser.close()
def retrieve_target(enterprise_number):
    with open("./dummy/target.html", encoding="utf-8") as f:
        parse_tree = BeautifulSoup(f, "lxml")
    return parse_tree.find(id="toonfctie")
    # with sync_playwright() as p:
    #     try:
    #         browser = p.chromium.launch()
    #         page = browser.new_page()
    #         page.goto(
    #             f"https://kbopub.economie.fgov.be/kbopub/toonondernemingps.html?ondernemingsnummer={enterprise_number}"
    #         )
    #         page.get_by_text("Toon de functiehouders").click()
    #         content = page.content()
    #         browser.close()
    #     except (PlaywrightError, PlaywrightTimeoutError) as e:
    #         # TODO: implement logging.
    #         print(f"Error while retrieving target: {e.message}")
    # parse_tree = BeautifulSoup(content, "lxml")
    # return parse_tree.find(id="toonfctie")


# TODO: error handling.
def parse_target(table):
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
    return text


def main():
    officers_table = retrieve_target(enterprise_number=502465839)
    officers_dict = parse_target(officers_table)
    print(officers_dict)


if __name__ == "__main__":
    main()
