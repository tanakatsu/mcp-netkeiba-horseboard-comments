import pandas as pd
import re
from bs4 import BeautifulSoup
from dataclasses import dataclass
from datetime import datetime, timedelta
from util import fetch_multi_pages, fetch_single_page, sublist

PAGES_PER_FETCH = 5


@dataclass
class UserComment:
    time: datetime
    text: str


class HorseBoardComments:
    BASE_URL = "https://db.netkeiba.com/?pid=horse_board"
    # WAIT_CSS_SELECTOR = "ul.user_report_list"
    WAIT_CSS_SELECTOR = "#Comment_List"

    def __init__(self, horse_id: int, pages_per_fetch: int = PAGES_PER_FETCH):
        self.horse_id = horse_id
        self.pages_per_fetch = pages_per_fetch

    def fetch_comments(self) -> list[UserComment]:
        entry_url = f"{self.BASE_URL}&id={self.horse_id}&page=1"

        # 最初のページを取得
        html_content = fetch_single_page(entry_url,
                                         wait_css_selector=self.WAIT_CSS_SELECTOR)
        last_page_no = self.__get_last_page(html_content)

        # 2ページ目以降を取得
        html_contents = [html_content]
        urls = self.__make_urls(last_page_no, self.horse_id)

        for url_list in sublist(urls, self.pages_per_fetch):
            htmls = fetch_multi_pages(url_list, wait_css_selector=self.WAIT_CSS_SELECTOR)
            html_contents.extend(htmls)

        user_comments = []
        for html_content in html_contents:
            user_comments += self.__parse_html(html_content)

        # 時刻でソート
        user_comments.sort(key=lambda x: x.time, reverse=True)

        return user_comments

    def __make_urls(self, last_page_no: int, horse_id: int) -> list[str]:
        urls = []
        for i in range(2, last_page_no + 1):
            url = f"{self.BASE_URL}&id={horse_id}&page={i}"
            urls.append(url)
        return urls

    def __get_last_page(self, html_content: str) -> int:
        soup = BeautifulSoup(html_content, 'html.parser')
        elms = soup.select('a[title="最後"]')
        if len(elms) == 0:
            return 1

        url = elms[0].get('href')
        lastpage_no = int(url.split("&page=")[-1])

        return lastpage_no

    def __parse_html(self, html_content: str) -> list[UserComment]:
        user_comments = []
        soup = BeautifulSoup(html_content, 'html.parser')

        elms = soup.select('ul.user_report_list div.CommentWrap')
        for elm in elms:
            text = elm.select('p.comment')[0].text
            time_str = elm.select('span.time_data_01')[0].text
            time = self.__convert_time_str_to_datetime(time_str)

            user_comments.append(UserComment(time, text))
        return user_comments

    def __convert_time_str_to_datetime(self, time_str: str) -> datetime:
        if m := re.match(r'(\d+)秒前', time_str):
            seconds = int(m.group(1))
            dt = datetime.now() + timedelta(seconds=-seconds)
        elif m := re.match(r'(\d+)分前', time_str):
            minutes = int(m.group(1))
            dt = datetime.now() + timedelta(minutes=-minutes)
        elif m := re.match(r'(\d+)時間前', time_str):
            hours = int(m.group(1))
            dt = datetime.now() + timedelta(hours=-hours)
        else:  # YYYY/MM/DD HH:MM
            dt = pd.to_datetime(time_str).to_pydatetime()
        return dt
