from argparse import ArgumentParser
from pathlib import Path
from lib.horse_board_comments import UserComment, HorseBoardComments


DATA_DIR = "cache"


def write_to_text(file_path: Path, user_comments: list[UserComment]) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, mode='w', newline='') as f:
        if len(user_comments) == 0:
            f.write("まだコメントの投稿がありません。\n")
            return

        for user_comment in user_comments:
            f.write(f"{user_comment.time}\n{user_comment.text}\n\n")


def main():
    parser = ArgumentParser(description="Fetch horse board comments.")
    parser.add_argument("horse_id", type=str, help="netkeiba horse ID")
    parser.add_argument("--pages_per_fetch", type=int, default=5,
                        help="Page numbers to fetch once")
    args = parser.parse_args()

    horse_id = args.horse_id

    horse_board = HorseBoardComments(horse_id)
    user_comments = horse_board.fetch_comments()

    # ファイルに出力
    output_filename = Path(DATA_DIR) / "horse_board" / f"{horse_id}.txt"
    write_to_text(output_filename, user_comments)


if __name__ == "__main__":
    main()
