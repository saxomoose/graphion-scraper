import dotenv
from scraper import redis_service, scraper_service, serialization_service


def main():
    # 404616494
    dotenv.load_dotenv()
    enterprise_number = 502465839
    officers_table = scraper_service.retrieve_target(enterprise_number)
    # with open("./dummy/target.html", encoding="utf-8") as f:
    #     officers_obj = scraper_service.parse_target(f)
    officers_obj = scraper_service.parse_target(officers_table)
    json = serialization_service.to_json(officers_obj)
    redis_service.store(enterprise_number, json)


if __name__ == "__main__":
    main()
