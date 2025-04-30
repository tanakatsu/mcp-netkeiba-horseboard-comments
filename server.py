import pandas as pd
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("netkeiba_user_comments")

# Constants
WORK_DIR = Path(__file__).parent
CACHE_DIR = "cache"
BOOKMARK_RANKING_CSV = WORK_DIR / CACHE_DIR / "bookmark_ranking.csv"


@mcp.tool()
def get_horse_id(horse_name: str) -> str:
    """Get Netkeiba's horse id by horse name

    Args:
        horse_name: horse name
    """
    df = pd.read_csv(BOOKMARK_RANKING_CSV, dtype={"id": str})
    df_target = df[df["name"] == horse_name]
    if df_target.empty:
        return "Horse not found."
    return df_target["id"].values[0]


@mcp.tool()
def get_horse_name(horse_id: str) -> str:
    """Get horse name by Netkeiba's horse id

    Args:
        horse_id: Netkeiba's horse id
    """
    df = pd.read_csv(BOOKMARK_RANKING_CSV, dtype={"id": str})
    df_target = df[df["id"] == horse_id]
    if df_target.empty:
        return "Horse not found."
    return df_target["name"].values[0]


@mcp.tool()
def get_bookmark_ranking(top_n: int) -> str:
    """Get bookmarked horse ranking

    Args:
        top_n: Top N horses
    """
    df = pd.read_csv(BOOKMARK_RANKING_CSV)
    df_top_n = df.head(top_n)
    rankings = []
    for i, row in df_top_n.iterrows():
        rankings.append(f"{i+1}位: {row['name']} ({row['count']} bookmarks)")
    return "\n---\n".join(rankings)


@mcp.tool()
def get_user_comments_of_horse(horse_id: str) -> str:
    """Get user's comments of horse

    Args:
        horse_id: Netkeiba's horse id
    """
    filename = WORK_DIR / CACHE_DIR / "horse_board" / f"{horse_id}.txt"
    if not filename.exists():
        return "No comments found."
    with open(filename, "r") as f:
        comments = f.read()
    return comments


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
