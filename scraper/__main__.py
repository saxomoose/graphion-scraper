from scraper import db_service
from scraper import scraper_service


def main():
    # officers_table = scraper_service.retrieve_target(enterprise_number=502465839)
    with open("./dummy/target.html", encoding="utf-8") as f:
        officers_dict = scraper_service.parse_target(f)
    # officers_dict = scraper_service.parse_target(officers_table)
    if officers_dict is not None:
        parents, children = scraper_service.parse_dictionary(officers_dict)
    db_service.insert_parents(parents)


if __name__ == "__main__":
    main()
