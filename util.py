import asyncio
from playwright.async_api import (
    async_playwright,
    TimeoutError as PlaywrightTimeoutError
)

MAX_RETRIES = 5
TIMEOUT_MS = 10000  # 10秒


async def fetch_page(playwright, url,
                     max_retries=MAX_RETRIES, wait_css_selector=None):
    for attempt in range(1, max_retries + 1):
        try:
            browser = await playwright.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(url,
                            timeout=TIMEOUT_MS,
                            wait_until='domcontentloaded')

            if wait_css_selector:
                await page.wait_for_selector(wait_css_selector)
            html_content = await page.content()

            await browser.close()
            break  # 成功したらループ終了

        except PlaywrightTimeoutError:
            print(f"[タイムアウト] ({url}) リトライ {attempt}/{max_retries}")
            if attempt == max_retries:
                print(f"[失敗] ({url}) 最大リトライ回数に到達")
        except Exception as e:
            print(f"[エラー] ({url}) {type(e).__name__}: {e}")
            break  # その他のエラーはリトライしない

        finally:
            try:
                # タイムアウトエラーのときはブラウザが開いたままになることがあるので、必ず閉じる
                await browser.close()
            except:
                pass  # 閉じる処理でエラーが起きても無視

    if attempt >= max_retries:
        raise PlaywrightTimeoutError("最大リトライ回数に到達")

    print("HTMLの取得が完了しました")
    return html_content


async def fetch_pages(urls, max_retries=MAX_RETRIES, wait_css_selector=None):
    async with async_playwright() as playwright:
        tasks = [fetch_page(
            playwright,
            url,
            max_retries=max_retries,
            wait_css_selector=wait_css_selector
        ) for url in urls]
        html_contents = await asyncio.gather(*tasks)
        print(f"{len(html_contents)}個のHTMLの取得が完了しました")
    return html_contents


def fetch_multi_pages(urls, max_retries=MAX_RETRIES, wait_css_selector=None):
    html_contents = asyncio.run(
        fetch_pages(urls,
                    max_retries=max_retries,
                    wait_css_selector=wait_css_selector)
    )
    return html_contents


def fetch_single_page(url, max_retries=MAX_RETRIES, wait_css_selector=None):
    html_contents = asyncio.run(
        fetch_pages([url],
                    max_retries=max_retries,
                    wait_css_selector=wait_css_selector)
    )
    return html_contents[0]


def sublist(lst, n):
    """リストからn個ずつのサブリストを返すジェネレーター"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
