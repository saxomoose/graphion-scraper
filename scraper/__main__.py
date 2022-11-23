from scraper import db_service, scraper_service


def main():
    enterprise_number = 502465839
    officers_table = scraper_service.retrieve_target(enterprise_number)
    # with open("./dummy/target.html", encoding="utf-8") as f:
    #     officers_dict = scraper_service.parse_target(f)
    officers_dict = scraper_service.parse_target(officers_table)
    if officers_dict is not None:
        parents, children = scraper_service.parse_dictionary(officers_dict)
    target_pk = db_service.insert_parents(enterprise_number, parents)
    db_service.insert_children(target_pk, parents, children)


if __name__ == "__main__":
    main()
