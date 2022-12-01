from scraper import serialization_service, scraper_service


def main():
    enterprise_number = 404616494
    # officers_table = scraper_service.retrieve_target(enterprise_number)
    with open("./dummy/target.html", encoding="utf-8") as f:
        officers_dict = scraper_service.parse_target(f)
    # officers_dict = scraper_service.parse_target(officers_table)
    parents, children = scraper_service.parse_dictionary(officers_dict)
    json = serialization_service.to_json(enterprise_number, parents, children)
    print(json)
    # Send serialized json to queue


if __name__ == "__main__":
    main()
