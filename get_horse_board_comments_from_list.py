import pandas as pd
from argparse import ArgumentParser
from pathlib import Path
from lib.horse_board_comments import UserComment, HorseBoardComments


DATA_DIR = "cache"


def write_to_text(file_path: Path,
                  horse_name: str, user_comments: list[UserComment]) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, mode='w', newline='') as f:
        f.write(f"＜{horse_name}＞\n\n")
        for user_comment in user_comments:
            f.write(f"{user_comment.time}\n{user_comment.text}\n\n")


def output_filename(horse_id: str) -> Path:
    return Path(DATA_DIR) / "horse_board" / f"{horse_id}.txt"


def main():
    parser = ArgumentParser(description="Fetch horse board comments.")
    parser.add_argument("ranking_list", type=str, help="Bookmark ranking list csv filename")
    parser.add_argument("--minimum_count", type=int, default=100)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--pages_per_fetch", type=int, default=5,
                        help="Page numbers to fetch once")
    args = parser.parse_args()

    th_count = args.minimum_count
    csvfile = args.ranking_list
    overwrite = args.overwrite

    df = pd.read_csv(csvfile)
    for _i, row in df.iterrows():
        horse_name = row['name']
        horse_id = row['id']
        bookmark_count = row['count']

        if bookmark_count < th_count:
            continue

        print(f"{bookmark_count}: {horse_name} ({horse_id})")
        if Path(output_filename(horse_id)).exists() and not overwrite:
            print("Already fetched.")
            continue

        horse_board = HorseBoardComments(horse_id,
                                         pages_per_fetch=args.pages_per_fetch)
        user_comments = horse_board.fetch_comments()

        # ファイルに出力
        write_to_text(output_filename(horse_id), horse_name, user_comments)


if __name__ == "__main__":
    main()
