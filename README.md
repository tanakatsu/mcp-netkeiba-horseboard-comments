## mcp-netkeiba-horseboard-comments

A Model Context Protocol (MCP) server that provides horse board comments from [netkeiba.com](https://www.netkeiba.com/).

### Features

- Bookmarked horse rankings
- Conversion between horse names and IDs
- Horse board comments

### Get started

1. Install uv
    ```
    $ curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
1. Clone this repository
    ```
    $ git clone https://github.com/tanakatsu/mcp-netkeiba-horseboard-comments.git
    ```
1. Create virtual environment and activate it
    ```
    $ uv venv
    $ . .venv/bin/activate
    ```
1. Install packages
    ```
    $ uv sync
    ```
1. Install browsers
    ```
    $ playwright install
    ```
1. Run scripts to fetch data and save it
    ```
    $ uv run get_bookmark_ranking_list.py
    $ uv run get_horse_board_comments_from_list.py cache/bookmark_ranking.csv
    ```
1. Configure mcp server settings for Claude Desktop

    Open `~/Library/Application\ Support/Claude/claude_desktop_config.json` and add following settings:
    ```json
    {
      "mcpServers": {
        "netkeiba_horseboard_comments": {
          "command": "uv",
          "args": [
            "run",
            "--with",
            "mcp[cli]",
            "--with",
            "pandas",
            "mcp",
            "run",
            "/path/to/netkeiba-horseboard-comments/server.py"
          ]
        }
      }
    }
    ```

Now, you can use this tool in Claude Desktop.
