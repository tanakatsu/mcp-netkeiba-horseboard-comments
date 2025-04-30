import csv
from argparse import ArgumentParser
from lib.bookmark_ranking import Age, Bookmark, BookmarkRanking

DATA_DIR = "cache"


def write_to_csv(file_path: str, data_instances: list[Bookmark]) -> None:
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write header
        writer.writerow(data_instances[0].__annotations__.keys())

        # Write data
        for instance in data_instances:
            writer.writerow(instance.__dict__.values())


def main():
    parser = ArgumentParser(description="Get bookmark ranking list")
    parser.add_argument("--age", type=Age, choices=list(Age), default=Age.TWO, help="Age")
    parser.add_argument("--pages_per_fetch", type=int, default=5)
    args = parser.parse_args()

    bookmark_ranking = BookmarkRanking(args.age,
                                       pages_per_fetch=args.pages_per_fetch)
    bookmarks = bookmark_ranking.fetch()

    # csvに出力
    write_to_csv(f"{DATA_DIR}/bookmark_ranking.csv", bookmarks)


if __name__ == "__main__":
    main()
