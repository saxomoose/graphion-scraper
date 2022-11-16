from .service import retrieve_target, parse_target


def main():
    # officers_table = retrieve_target(enterprise_number=502465839)
    with open("./dummy/target.html", encoding="utf-8") as f:
        officers_dict = parse_target(f)
    # officers_dict = parse_target(officers_table)
    print(officers_dict)


if __name__ == "__main__":
    main()
