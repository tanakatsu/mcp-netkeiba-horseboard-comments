from enum import StrEnum
from dataclasses import dataclass
from bs4 import BeautifulSoup
from util import fetch_multi_pages, fetch_single_page, sublist

PAGES_PER_FETCH = 5


class Age(StrEnum):
    ALL = "all"
    TWO = "2"
    THREE = "3"
    FOUR_AND_OVER = "4+"


@dataclass
class Bookmark:
    name: str
    id: str
    count: int


class BookmarkRanking:
    ENTRY_URLS = {
        "all": "https://db.netkeiba.com/?pid=ranking_list&hr=bookmark&sort=1-1",
        "2": "https://db.netkeiba.com/?pid=ranking_list&hr=bookmark&sort=2-1",
        "3": "https://db.netkeiba.com/?pid=ranking_list&hr=bookmark&sort=3-1",
        "4+": "https://db.netkeiba.com/?pid=ranking_list&hr=bookmark&sort=4-1",
    }
    WAIT_CSS_SELECTOR = "div.db_data_list"

    def __init__(self, age: Age, pages_per_fetch: int = PAGES_PER_FETCH):
        self.pages_per_fetch = pages_per_fetch
        self.entry_url = self.ENTRY_URLS[age]

    def fetch(self):
        # 最初のページを取得
        html_content = fetch_single_page(self.entry_url,
                                         wait_css_selector=self.WAIT_CSS_SELECTOR)
        last_page_no = self.__get_last_page(html_content)

        # 2ページ目以降を取得
        html_contents = [html_content]
        urls = self.__make_urls(last_page_no)

        for url_list in sublist(urls, self.pages_per_fetch):
            htmls = fetch_multi_pages(url_list,
                                      wait_css_selector=self.WAIT_CSS_SELECTOR)
            html_contents.extend(htmls)

        bookmarks = []
        for html_content in html_contents:
            bookmarks += self.__parse_html(html_content)

        # ブックマーク数でソート
        bookmarks.sort(key=lambda x: x.count, reverse=True)

        return bookmarks

    def __make_urls(self, last_page_no: int) -> list[str]:
        urls = []
        for i in range(2, last_page_no + 1):
            urls.append(f"{self.entry_url}&page={i}")
        return urls

    def __get_last_page(self, html_content: str) -> int:
        soup = BeautifulSoup(html_content, 'html.parser')
        elms = soup.select('a[title="last page"]')
        lastpage_no = int(elms[0]['href'].split("=")[-1])

        return lastpage_no

    def __parse_html(self, html_content: str) -> list[Bookmark]:
        bookmarks = []
        soup = BeautifulSoup(html_content, 'html.parser')
        elms = soup.select('div.db_data_list table tr')
        for elm in elms:
            horse_name = elm.select('p.rank_horse')[0].text.strip()
            horse_url = elm.select('p.rank_horse a')[0].get('href')
            horse_id = horse_url.split("/")[-2]
            bookmark_cnt = int(elm.select('div.access strong')[0].text.replace('人', '').replace(',', ''))

            bookmarks.append(Bookmark(horse_name, horse_id, bookmark_cnt))
        return bookmarks
