from bs4 import BeautifulSoup, NavigableString
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(
        "https://kbopub.economie.fgov.be/kbopub/toonondernemingps.html?ondernemingsnummer=502465839"
    )
    page.get_by_text("Toon de functiehouders").click()
    parse_tree = BeautifulSoup(page.content(), "lxml")
    browser.close()

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

    print(text)
