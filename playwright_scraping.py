from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError, expect
import re
import time


def get_attribute(link):
    if link.get_attribute('src'):
        return link.get_attribute('src')


def element_click(page, xpath):
    clicked = False
    try:
        elem = page.locator(xpath)
        elem.click(timeout=2000)
        clicked = True
    except Exception as e:
        print(e)
    finally:
        return clicked


def goto_url(page, url_navigate):
    try:
        page.goto(url_navigate)
        return True
    except Exception as e:
        print(e)
        return False


def xpath_locator_exists(page, xpath):
    try:
        expect(page.locator(xpath))
        return True
    except Exception as e:
        print(e)
        return False


def get_total_pages(url):
    total_pages = None
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page_reached = goto_url(page, url)
        if page_reached:
            # time.sleep(2)
            element_click(page, '//*[contains(@class,"flip_button_last")]')
            # time.sleep(2)
            total_pages = int(re.search(r'=(.*)', page.url).group(1))
    # browser.close()
    return total_pages


def get_xpath_field_locator(page, xpath, action):
    result = None
    try:
        locator = page.locator(xpath)
        if action == 'click':
            locator.click(timeout=1000)
        elif action == 'text':
            result = locator.text_content(timeout=1000)
    except PlaywrightTimeoutError:
        print("Timeout Error, or  Unable to find xpath")
    finally:
        return result


def playwright_scraping_url_image(edition):
    img_lst = []
    total_pages = get_total_pages(url=f"https://online.fliphtml5.com/{edition}/#p=1")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        if total_pages:
            for page_number in range(1, total_pages):
                # time.sleep(2)
                url = f"https://online.fliphtml5.com/{edition}/#p={page_number}"
                page_reached = goto_url(page, url)
                time.sleep(1)
                if page_reached:
                    url_images = page.query_selector_all('img[src*="files/large/"]')
                    [img_lst.append(imagen.get_attribute('src')) for imagen in url_images
                     if imagen.get_attribute('src') not in img_lst]
        browser.close()
    result_lst = [f'"https://online.fliphtml5.com/{edition}/{img_partial_url}' for img_partial_url in img_lst]
    result_lst = [x.replace('"', "") for x in result_lst]
    return result_lst
